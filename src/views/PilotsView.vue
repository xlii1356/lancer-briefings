<template>
	<div class="section-content-container" :class="{ animate: animateView }" :style="{ 'animation-delay': animationDelay }" id="pilots">
		<div class="pilot-list-container">
			<!-- Added draggable property and dragStart handler to make pilots available for assignment -->
			<Pilot 
				v-for="item in pilots" 
				:key="item.callsign" 
				:pilot="item" 
				:animate="animate" 
				draggable="true" 
				@dragstart="dragStart($event, item.callsign)"
			/>
		</div>
	</div>
</template>

<script>
import { VueMarkdownIt } from '@f3ve/vue-markdown-it';
import Pilot from "@/components/Pilot.vue";


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
			clockAnimationDelay: "2500",
		};
	},
	methods: {
		setAnimate() {
			if (this.animate) {
				this.animateView = true;
			}
			let statusAnimated = window.sessionStorage.getItem("statusAnimated");
			if (statusAnimated) {
				this.animationDelay = "0s";
			}
			if (statusAnimated === null) {
				window.sessionStorage.setItem("statusAnimated", true);
				this.animationDelay = "1500ms";
			}
		},
		
		// Method to make pilots draggable (moved from PilotAssignment.vue)
		dragStart(event, callsign) {
			event.dataTransfer.setData("pilotCallsign", callsign);
			event.dataTransfer.effectAllowed = "move";
		},
	},
	watch: {
		animate() {
			this.setAnimate();
		},
	},
	created() {
		this.setAnimate();
	},
};
</script>

<style scoped>
/* Existing styles */
.pilot-list-container {
	display: flex;
	flex-wrap: wrap;
	gap: 15px;
	justify-content: space-evenly;
	padding: 10px;
}
</style>