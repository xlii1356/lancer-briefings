<template>
	<div class="pilot-view-modal">
		<div class="pilot-header-container">
			<div class="section-header clipped-medium-backward-bio">
				<img src="/icons/pilot.svg" />
				<h1>PILOT ROSTER</h1>
			</div>
			<div class="rhombus-back">&nbsp;</div>
		</div>
		<div class="pilot-detail-wrapper">
			<Pilot :pilot="pilot" :animate="animate" :nhps="nhps" />
		</div>
	</div>
</template>

<script>
import Pilot from '@/components/Pilot.vue';

export default {
	name: "PilotViewModal",
	components: {
		Pilot,
	},
	props: {
		pilot: {
			type: Object,
			required: true,
		},
		nhps: {
			type: Array,
			default: () => []
		},
		animate: {
			type: Boolean,
			default: false
		}
	}
}
</script>

<style scoped>
/* Ensure the modal content wraps correctly on mobile */
.pilot-view-modal {
    max-width: 100%;
    z-index: 2147483647 !important; /* Max z-index */
    position: relative;
    overflow: visible;
}

.pilot-header-container {
    display: flex;
    margin-bottom: 10px;
}

.pilot-header-container .section-header {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
    height: 52px;
    display: inline-flex;
    gap: 15px;
    padding-left: 16px;
    margin-top: -38px !important;
}

.pilot-header-container .section-header h1 {
    font-size: 26px;
    margin: 0%;
    align-self: center;
    font-family: "Big Shoulders Display", cursive;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.pilot-header-container .rhombus-back {
    transform: skew(0.785398rad) !important;
    background-color: var(--primary-color);
    border-color: var(--primary-color);
    width: 40px;
    height: 52px;
    display: inline-block;
    position: relative;
    left: -10px;
    top: -38px;
}

/* Ensure the modal stays within bounds */
.pilot-view-modal {
    width: 100%;
    max-width: 85vw; /* Explicitly constrain width relative to viewport */
    max-height: 85vh; /* Limit height to allow scrolling within view */
    overflow-y: auto;
    overflow-x: hidden;
    box-sizing: border-box;
    margin: 0 auto; /* Center it */
}

.pilot-detail-wrapper {
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
    overflow-x: hidden;
    overflow-y: auto;
    padding: 0;
    margin: 0;
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 0;
}

/* Custom scrollbar */
.pilot-view-modal::-webkit-scrollbar {
    width: 8px;
}

.pilot-view-modal::-webkit-scrollbar-track {
    background: rgba(0,0,0,0.3);
}

.pilot-view-modal::-webkit-scrollbar-thumb {
    background: var(--primary-color);
    border-radius: 4px;
}

.pilot-view-modal::-webkit-scrollbar-thumb:hover {
    background: var(--primary-color);
    opacity: 0.8;
}
</style>
