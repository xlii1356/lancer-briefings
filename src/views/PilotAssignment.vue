<script>
import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } from 'https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js';
import { initializeApp } from 'https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js';
import { getFirestore, doc, setDoc, onSnapshot } from 'https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js';

// --- Global Constants (Provided by Canvas Environment) ---
const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';
const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : {};
const initialAuthToken = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : undefined;
const ASSIGNMENTS_DOC_ID = 'pilot_assignments';
const PUBLIC_COLLECTION_PATH = `artifacts/${appId}/public/data/mission_status`;

export default {
    props: {
        missions: { type: Array, required: true },
        pilots: { type: Array, required: true },
    },
    data() {
        return {
            // Firestore State
            db: null,
            auth: null,
            assignmentsDocRef: null,
            dbReady: false,
            userId: null,
            loading: true,
            error: null,
            
            // Assignment State: { [missionSlug]: [{ callsign, name, portrait }] }
            missionAssignments: {}, 
            
            // Drag State
            draggingPilotCallsign: null,
        };
    },
    computed: {
        // This computed property generates the list of all pilots, prepared for dragging
        allPilots() {
            return this.pilots.map(p => ({
                callsign: p.callsign.toUpperCase(),
                name: p.name,
                // Assuming pilot portrait is available in the pilot object, maybe p.portrait or p.image_url
                portraitUrl: p.portrait_url || p.image_url || 'https://placehold.co/80x80/2C3E50/FFFFFF?text=P',
                // Add the pilot's current assignment status if needed, but for the drag list, they are always 'available'
            }));
        },
        // Missions extended with their assigned pilots
        missionsWithPilots() {
            return this.missions.map(mission => ({
                ...mission,
                assignedPilots: this.missionAssignments[mission.slug] || [],
            }));
        }
    },
    created() {
        this.initializeFirebase();
    },
    methods: {
        initializeFirebase() {
            try {
                const app = initializeApp(firebaseConfig);
                this.db = getFirestore(app);
                this.auth = getAuth(app);
                this.assignmentsDocRef = doc(this.db, PUBLIC_COLLECTION_PATH, ASSIGNMENTS_DOC_ID);
                
                onAuthStateChanged(this.auth, async (user) => {
                    if (user) {
                        this.userId = user.uid;
                        this.dbReady = true;
                        this.loading = false;
                        this.setupFirestoreListener();
                    } else {
                        if (initialAuthToken) {
                            await signInWithCustomToken(this.auth, initialAuthToken);
                        } else {
                            await signInAnonymously(this.auth);
                        }
                    }
                });
            } catch (e) {
                console.error("Firebase Initialization Failed:", e);
                this.error = 'System error: Failed to initialize Firebase.';
                this.loading = false;
            }
        },
        
        setupFirestoreListener() {
            if (!this.dbReady) return;
            
            onSnapshot(this.assignmentsDocRef, (docSnapshot) => {
                if (docSnapshot.exists()) {
                    const data = docSnapshot.data();
                    // Load assignments, default to empty object if data is missing
                    this.missionAssignments = data.assignments || {}; 
                    console.log("Assignments updated in real-time.");
                } else {
                    console.log("Assignments not found, initializing with empty data.");
                    this.saveAssignments({}); // Initial save
                }
            }, (e) => {
                console.error("Firestore listen error:", e);
                this.error = "Real-time sync failed.";
            });
        },
        
        // --- Drag and Drop Handlers ---
        
        dragStart(event, callsign) {
            this.draggingPilotCallsign = callsign;
            if (event.dataTransfer) {
                event.dataTransfer.setData('text/plain', callsign);
                // Set the pilot data for easier drop handling
                const pilot = this.allPilots.find(p => p.callsign === callsign);
                event.dataTransfer.setData('application/json', JSON.stringify(pilot));
                event.dataTransfer.effectAllowed = 'move';
            }
        },
        
        allowDrop(event) {
            event.preventDefault(); // Required to allow drop
        },
        
        /**
         * Assigns a pilot to a mission (drop target).
         * @param {DragEvent} event 
         * @param {string} missionSlug 
         */
        drop(event, missionSlug) {
            event.preventDefault();
            if (!this.dbReady) return;
            
            let pilotData;
            try {
                pilotData = JSON.parse(event.dataTransfer?.getData('application/json'));
            } catch (e) {
                console.error("Failed to parse pilot data during drop:", e);
                return;
            }

            if (!pilotData || !pilotData.callsign) return;
            
            const callsign = pilotData.callsign;

            // 1. Create a copy of the current assignments
            let newAssignments = { ...this.missionAssignments };
            
            // 2. Remove pilot from ALL missions first (to ensure only one assignment)
            for (const slug in newAssignments) {
                newAssignments[slug] = newAssignments[slug].filter(p => p.callsign !== callsign);
            }

            // 3. Add pilot to the target mission (if it's not the removal zone)
            if (missionSlug !== 'unassign') {
                const pilotDetails = {
                    callsign: pilotData.callsign,
                    name: pilotData.name,
                    portraitUrl: pilotData.portraitUrl 
                };
                
                // Initialize array if null
                if (!newAssignments[missionSlug]) {
                    newAssignments[missionSlug] = [];
                }
                
                // Add pilot if not already present in the list (though step 2 should handle this)
                if (!newAssignments[missionSlug].some(p => p.callsign === callsign)) {
                    newAssignments[missionSlug].push(pilotDetails);
                }
            }

            // 4. Update and Save
            this.saveAssignments(newAssignments);
            this.draggingPilotCallsign = null;
        },

        /**
         * Saves the new assignments map to Firestore.
         * @param {Object} assignmentsMap - The new state of missionAssignments.
         */
        async saveAssignments(assignmentsMap) {
            if (!this.dbReady) return;

            // Check if there are any assignments left. If not, save an empty object.
            const hasAssignments = Object.values(assignmentsMap).some(arr => arr.length > 0);
            const dataToSave = { 
                assignments: hasAssignments ? assignmentsMap : {},
                timestamp: Date.now()
            };
            
            try {
                await setDoc(this.assignmentsDocRef, dataToSave);
                this.error = 'Assignment Saved.';
                setTimeout(() => this.error = null, 3000);
            } catch (e) {
                console.error("Failed to save assignments:", e);
                this.error = 'Failed to save assignment.';
            }
        }
    },
    template: `
        <div id="pilot-drag-source" class="section-container" :style="{ 'animation-delay': '1.75s' }">
            <div class="section-header clipped-medium-backward">
                <img src="/icons/pilot.svg" />
                <h1>Available Pilots</h1>
            </div>
            <div class="section-content-container">
                <div v-if="loading" class="text-center p-4 text-gray-400">Loading pilot data...</div>
                <div v-else-if="!dbReady" class="text-center p-4 text-red-400">Authentication Required to Drag.</div>
                <div v-else class="available-pilots-list" @dragover="allowDrop" @drop="drop($event, 'unassign')">
                    <div 
                        v-for="pilot in allPilots" 
                        :key="pilot.callsign"
                        :draggable="dbReady"
                        @dragstart="dragStart($event, pilot.callsign)"
                        class="pilot-card"
                        :class="{'dragging': draggingPilotCallsign === pilot.callsign}"
                        :title="'Drag ' + pilot.name + ' to a mission to assign.'"
                    >
                        <img :src="pilot.portraitUrl" :alt="pilot.name" class="pilot-portrait" onerror="this.src='https://placehold.co/80x80/2C3E50/FFFFFF?text=P'"/>
                        <div class="pilot-info">
                            <div class="callsign">{{ pilot.callsign }}</div>
                            <div class="name">{{ pilot.name }}</div>
                        </div>
                    </div>
                    <div class="unassign-zone">
                        Drop here to unassign pilot
                    </div>
                </div>
            </div>
        </div>
        
        <div v-if="error" :class="error.includes('Saved') ? 'status-message-success' : 'status-message-error'">
            {{ error }}
        </div>
    
        <style>
            .pilot-card {
                cursor: grab;
                display: flex;
                align-items: center;
                background-color: rgba(0, 0, 0, 0.4);
                border: 1px solid #00ffc1;
                padding: 5px;
                border-radius: 4px;
                transition: transform 0.1s, box-shadow 0.1s;
                user-select: none;
                width: 200px;
            }
            .pilot-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 0 8px rgba(0, 255, 193, 0.5);
            }
            .pilot-card.dragging {
                opacity: 0.5;
                border-style: dashed;
            }
            .pilot-portrait {
                width: 40px;
                height: 40px;
                object-fit: cover;
                border-radius: 50%;
                border: 2px solid #00ffc1;
                margin-right: 10px;
            }
            .pilot-info {
                line-height: 1.1;
            }
            .pilot-info .callsign {
                font-weight: bold;
                color: #00ffc1;
                font-size: 0.9em;
            }
            .pilot-info .name {
                color: white;
                font-size: 0.75em;
            }
            .available-pilots-list {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                padding: 10px;
            }

            .unassign-zone {
                border: 2px dashed #ff4444;
                color: #ff4444;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 10px;
                width: 200px;
                height: 52px;
                font-size: 0.8em;
                background-color: rgba(255, 68, 68, 0.1);
            }

            /* Generic Status Message Styles */
            .status-message-success, .status-message-error {
                position: fixed;
                bottom: 20px;
                right: 20px;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                z-index: 1000;
                transition: opacity 0.5s;
            }
            .status-message-success {
                background-color: #00ffc1;
                color: #1a1a1a;
                border: 2px solid #00e0b3;
            }
            .status-message-error {
                background-color: #ff4444;
                color: white;
                border: 2px solid #cc3333;
            }
        </style>
    `
};
</script>