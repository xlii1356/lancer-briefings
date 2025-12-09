<template>
	<div id="pilots" :class="{ animate: animateView }" :style="{ 'animation-delay': animationDelay }" class="section-container full-height">
        <!-- Layout Split -->
        <div class="pilots-layout">
            <!-- Left: Pilot Roster -->
            <div class="roster-panel custom-scroll">
                <div class="section-header clipped-medium-backward">
                    <img src="/icons/pilot.svg" />
                    <h1>ROSTER</h1>
                </div>
                
                <div class="roster-list">
                    <div 
                        v-for="pilot in pilots" 
                        :key="pilot.callsign"
                        class="roster-item"
                        :class="{ active: selectedPilot && selectedPilot.callsign === pilot.callsign }"
                        @click="selectPilot(pilot)"
                    >
                        <div class="roster-portrait">
                            <img :src="`/pilots/${pilot.callsign.toUpperCase()}.webp`" />
                            <div class="status-dot"></div>
                        </div>
                        <div class="roster-info">
                            <div class="roster-callsign">{{ pilot.callsign }}</div>
                            <div class="roster-name">{{ pilot.name }}</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right: Details Panel -->
            <div class="details-panel custom-scroll">
                <div v-if="selectedPilot" class="pilot-detail-view">
                    <!-- Tactical Profile Card -->
                    <div class="section-header clipped-info-backward">
                        <img src="/icons/license.svg" />
                        <h1>TACTICAL PROFILE</h1>
                    </div>
                    
                    <div class="profile-card-wrapper">
                        <Pilot :pilot="selectedPilot" :animate="animate" />
                    </div>

                    <!-- Mech & NHP Info -->
                    <div class="mech-intel-section">
                        <div class="mech-visual">
                            <div class="section-header clipped-medium-backward">
                                <img src="/icons/mech.svg" />
                                <h1>ACTIVE FRAME</h1>
                            </div>
                            <div class="mech-image-container">
                                <img :src="`/mechs/${selectedPilot.callsign.toUpperCase()}.webp`" class="mech-portrait-lg" />
                            </div>
                        </div>

                        <div class="nhp-visual">
                             <div class="section-header clipped-medium-backward">
                                <img src="/icons/clockwork.svg" />
                                <h1>NHP COFFIN</h1>
                            </div>
                            <div class="nhp-box">
                                <div v-if="currentNhps.length === 0" class="no-nhp">
                                    NO NHP DETECTED
                                </div>
                                <div v-else class="nhp-list">
                                    <div v-for="(nhp, idx) in currentNhps" :key="idx" class="nhp-item">
                                        <div class="nhp-icon">
                                            <img src="/icons/clockwork.svg" />
                                        </div>
                                        <div class="nhp-details">
                                            <div class="nhp-name">{{ nhp.name }}</div>
                                            <div class="nhp-type">NON-HUMAN PERSON</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
                <div v-else class="empty-state">
                    SELECT A PILOT TO VIEW TACTICAL PROFILE
                </div>
            </div>
        </div>
	</div>
</template>

<script>
import { VueMarkdownIt } from '@f3ve/vue-markdown-it';
import Pilot from "@/components/Pilot.vue";
import lancerData from '@massif/lancer-data';
import ktbData from 'lancer-ktb-data';
import nrfawData from 'lancer-nrfaw-data';
import longrimData from 'lancer-longrim-data';

export default {
	components: {
		VueMarkdownIt,
		Pilot,
	},
	props: {
		animate: {
			type: Boolean,
			required: true,
		},
		pilots: {
			type: Array,
			required: true,
		},
	},
	data() {
		return {
			animateView: this.animate,
			animationDelay: "0s",
            selectedPilot: null,
		};
	},
    computed: {
        allSystems() {
             return [...lancerData.systems, ...ktbData.systems, ...nrfawData.systems, ...longrimData.systems];
        },
        currentNhps() {
            if (!this.selectedPilot) return [];
            
            // Find active mech
            const activeMechId = this.selectedPilot.state.active_mech_id;
            const activeMech = this.selectedPilot.mechs.find(m => m.id === activeMechId) || this.selectedPilot.mechs[0];
            
            if (!activeMech) return [];

            // Get active loadout
            const loadout = activeMech.loadouts[activeMech.active_loadout_index];
            if (!loadout) return [];

            // Collect all systems from mounts and generic systems
            let systems = [...loadout.systems];
            
            // Add mounted systems if they are technically separate items (usually just weapons or mods, but checking)
            // Typically NHPs are "systems".
            
            const nhps = [];

            systems.forEach(sys => {
                const sysData = this.allSystems.find(s => s.id === sys.id);
                if (sysData && (sysData.tags.includes('AI') || sysData.tags.includes('NHP') || sysData.name.includes('NHP'))) {
                    nhps.push({
                        name: sysData.name,
                        id: sysData.id
                    });
                }
            });

            return nhps;
        }
    },
    mounted() {
        if (this.pilots.length > 0) {
            this.selectedPilot = this.pilots[0];
        }
    },
	methods: {
		selectPilot(pilot) {
            this.selectedPilot = pilot;
        },
		setAnimate() {
			if (this.animate) {
				this.animateView = true;
			}
        }
	}
};
</script>

<style scoped>
.full-height {
    width: 1755px; /* Maintain existing width from global layout but better context */
    height: 100%;
    margin: 30px;
    display: flex;
    flex-direction: column;
}

.pilots-layout {
    display: flex;
    flex: 1;
    min-height: 0;
    gap: 20px;
}

/* --- Roster Panel --- */
.roster-panel {
    width: 300px;
    background: rgba(0,0,0,0.3);
    border: 1px solid var(--primary-color);
    display: flex;
    flex-direction: column;
}

.roster-list {
    overflow-y: auto;
    flex: 1;
}

.roster-item {
    display: flex;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    cursor: pointer;
    transition: background 0.2s;
}

.roster-item:hover {
    background: rgba(255,255,255,0.05);
}

.roster-item.active {
    background: var(--primary-color);
    color: var(--secondary-color);
}

.roster-item.active .roster-callsign {
    color: var(--secondary-color);
}

.roster-portrait {
    position: relative;
    width: 50px;
    height: 50px;
    margin-right: 15px;
}

.roster-portrait img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border: 1px solid white;
}

.status-dot {
    position: absolute;
    bottom: -2px;
    right: -2px;
    width: 10px;
    height: 10px;
    background: #00ff00;
    border-radius: 50%;
    border: 1px solid #000;
}

.roster-callsign {
    font-family: "Big Shoulders Display", cursive;
    font-weight: 800;
    font-size: 1.2rem;
    letter-spacing: 1px;
    color: var(--primary-color);
}

.roster-name {
    font-family: "Roboto", sans-serif;
    font-size: 0.8rem;
    opacity: 0.8;
}

/* --- Details Panel --- */
.details-panel {
    flex: 1;
    overflow-y: auto;
    padding-right: 10px;
}

.empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    font-family: "Big Shoulders Display", cursive;
    font-size: 2rem;
    color: rgba(255,255,255,0.3);
}

.profile-card-wrapper {
    margin-bottom: 20px;
}

/* --- Mech & NHP Section --- */
.mech-intel-section {
    display: flex;
    gap: 20px;
    height: 400px; /* Fixed height for visuals */
}

.mech-visual {
    flex: 2;
    display: flex;
    flex-direction: column;
}

.mech-image-container {
    flex: 1;
    border: 1px solid var(--primary-color);
    background: rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
}

.mech-portrait-lg {
    width: 100%;
    height: 100%;
    object-fit: contain;
    object-position: center;
}

.nhp-visual {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.nhp-box {
    flex: 1;
    border: 1px solid var(--primary-color);
    background: rgba(0,0,0,0.2);
    padding: 10px;
    overflow-y: auto;
}

.no-nhp {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: "Big Shoulders Display", cursive;
    font-size: 1.5rem;
    color: rgba(255,50,50,0.5);
    letter-spacing: 2px;
}

.nhp-item {
    display: flex;
    align-items: center;
    background: rgba(255, 0, 0, 0.1);
    border: 1px solid rgba(255, 0, 0, 0.3);
    padding: 10px;
    margin-bottom: 10px;
}

.nhp-icon img {
    width: 40px;
    height: 40px;
    filter: invert(15%) sepia(96%) saturate(6327%) hue-rotate(356deg) brightness(96%) contrast(116%); /* Red-ish filter */
    margin-right: 15px;
}

.nhp-name {
    color: #ff5555;
    font-family: "Big Shoulders Display", cursive;
    font-size: 1.2rem;
    font-weight: bold;
}

.nhp-type {
    font-size: 0.7rem;
    color: rgba(255,255,255,0.5);
}

/* Mobile Adjustments */
@media (max-width: 768px) {
    .full-height {
        width: 100% !important;
        margin: 0 !important;
        padding: 10px;
    }
    
    .pilots-layout {
        flex-direction: column;
    }

    .roster-panel {
        width: 100%;
        height: 200px; /* Reduced height list */
    }

    .mech-intel-section {
        flex-direction: column;
        height: auto;
    }

    .mech-visual, .nhp-visual {
        height: 300px;
    }
}
</style>