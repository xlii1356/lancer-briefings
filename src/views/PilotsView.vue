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
                    <div class="profile-card-wrapper">
                        <Pilot :pilot="selectedPilot" :key="selectedPilot.callsign" :animate="animate" :nhps="currentNhps" />
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
import MechModal from '@/components/modals/MechModal.vue';
import lancerData from '@massif/lancer-data';
import ktbData from 'lancer-ktb-data';
import nrfawData from 'lancer-nrfaw-data';
import longrimData from 'lancer-longrim-data';

import nhpData from '@/assets/pilots/nhps.json';

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
            nhpAssociations: nhpData
		};
	},
    computed: {
        allSystems() {
             return [...lancerData.systems, ...ktbData.systems, ...nrfawData.systems, ...longrimData.systems];
        },
        mechWeapons() {
             return [...lancerData.weapons, ...ktbData.weapons, ...nrfawData.weapons, ...longrimData.weapons];
        },
        mechSystems() {
             return [...lancerData.systems, ...ktbData.systems, ...nrfawData.systems, ...longrimData.systems];
        },
        activeMech() {
            if (!this.selectedPilot) return null;
            const activeMechId = this.selectedPilot?.state?.active_mech_id;
            let mech = null;
            if (this.selectedPilot.mechs && this.selectedPilot.mechs.length > 0) {
                 mech = this.selectedPilot.mechs.find(m => m.id === activeMechId);
                 if (!mech) mech = this.selectedPilot.mechs[0];
            }
            return mech;
        },
        currentNhps() {
            if (!this.selectedPilot) return [];
            
            const pilotEntry = this.nhpAssociations.find(p => p.callsign.toUpperCase() === this.selectedPilot.callsign.toUpperCase());
            if (pilotEntry) {
                return pilotEntry.nhps;
            }
            return [];
        },
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
        },
	}
};
</script>

<style scoped>
/* scoped styles */
.full-height {
    width: 100%;
    /* height: 100%; Removing fixed height to rely on page scroll if needed */
    min-height: 100vh; 
    padding: 30px;
    display: flex;
    flex-direction: column;
    /* overflow: hidden; Removing clip to see if it reveals content */
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
    min-width: 300px; /* Prevent shrinking */
    background: rgba(0,0,0,0.3);
    border: 1px solid var(--primary-color);
    display: flex;
    flex-direction: column;
    height: 80vh; /* Fixed height for roster so it remains scrollable specifically */
    position: sticky;
    top: 20px;
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
    /* overflow-y: auto;  Disable nested scroll for details, let the page flow */
    padding-right: 10px;
    min-width: 0; /* Prevent flex child from overflowing */
}

/* --- Mech & NHP Section --- */
.mech-intel-section {
    display: flex;
    gap: 20px;
    /* height: 400px; Remove fixed height */
    min-height: 400px;
    margin-bottom: 50px; /* Add bottom margin for scroll clearing */
    flex-shrink: 0; /* Don't squash me */
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
        height: auto !important; /* Allow growing */
        overflow: visible !important;
    }
    
    .pilots-layout {
        flex-direction: column;
        height: auto; /* Allow growing */
    }

    .roster-panel {
        width: 100%;
        height: 200px;
        flex: none; /* Don't expand, just be 200px */
    }
    
    .details-panel {
        overflow: visible; /* Let body scroll it */
        flex: none; /* Just stack */
        height: auto;
    }

    .mech-intel-section {
        flex-direction: column;
        height: auto;
        margin-bottom: 20px;
    }

    .mech-visual, .nhp-visual {
        min-height: 300px;
    }
}
</style>

<style>
/* Global override for section headers in this view */
/* Removing specific overrides to match Mission Log style */
#pilots .mech-image-container {
    background: rgba(255, 255, 255, 0.05);
    background-image: linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
    background-size: 20px 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 300px; /* Ensure visibility */
}

#pilots .mech-portrait-lg {
    max-width: 90%;
    max-height: 90%;
    object-fit: contain;
}
</style>