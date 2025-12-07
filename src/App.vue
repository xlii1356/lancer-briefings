<template>
	<div class="page-wrapper">
		<Header :planet-path="planetPath" :class="{ animate: animate }" :header="header" />
		<Sidebar :animate="animate" :class="{ animate: animate }" />
	</div>
	<div class="header-countdown-box">
		<span class="label">NEXT DEPLOYMENT:</span>
		<span class="value">{{ countdownDisplay }}</span>
	</div>
	<div id="router-view-container">
		<router-view :animate="animate" :initial-slug="initialSlug" :missions="missions" :events="events"
			:pilots="pilots" :clocks="clocks" :reserves="reserves" />
	</div>
	<svg style="visibility: hidden; position: absolute" width="0" height="0" xmlns="http://www.w3.org/2000/svg"
		version="1.1">
		<defs>
			<filter id="round">
				<feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur" />
				<feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 19 -5"
					result="goo" />
				<feComposite in="SourceGraphic" in2="goo" operator="atop" />
			</filter>
		</defs>
	</svg>
	<audio autoplay>
		<source src="/startup.ogg" type="audio/ogg" />
	</audio>
</template>

// App.vue <script>
import Header from "./components/layout/Header.vue";
import Sidebar from "./components/layout/Sidebar.vue";
import Config from "@/assets/info/general-config.json";

export default {
	components: {
		Header,
		Sidebar,
	},

	data() {
		return {
			animate: Config.animate,
			initialSlug: Config.initialSlug,
			planetPath: Config.planetPath,
			header: Config.header,
			pilotSpecialInfo: Config.pilotSpecialInfo,
			clocks: [],
			events: [],
			missions: [],
			pilots: [],
			reserves: [],
			bonds: [],
            // NEW: Countdown Data
            countdownDisplay: 'CALCULATING...',
            countdownInterval: null,
		};
	},
	created() {
		this.setTitleFavicon(Config.defaultTitle + " MISSION BRIEFING", Config.icon);
		this.importMissions(import.meta.glob("@/assets/missions/*.md", { query: '?raw', import: 'default' }));
		this.importEvents(import.meta.glob("@/assets/events/*.md", { query: '?raw', import: 'default' }));
		this.importClocks(import.meta.glob("@/assets/clocks/*.json"));
		this.importReserves(import.meta.glob("@/assets/reserves/*.json"));
		this.importPilots(import.meta.glob("@/assets/pilots/*.json"));
	},
	mounted() {
		this.$router.push("/status");
        
        // NEW: Start the countdown timer
        this.updateCountdown();
        this.countdownInterval = setInterval(this.updateCountdown, 1000);
	},
    beforeUnmount() {
        // Clean up the timer when the app is destroyed
        if (this.countdownInterval) clearInterval(this.countdownInterval);
    },
	methods: {
        // NEW: Countdown Logic
        updateCountdown() {
            const now = new Date();
            
            // 1. Find the next Tuesday (Day 2)
            const currentDay = now.getDay();
            let daysUntilTuesday = 2 - currentDay;

            // If it's already past Tuesday (e.g. Wednesday), cycle to the next week
            if (daysUntilTuesday < 0) {
                daysUntilTuesday += 7;
            }
            
            // 2. Set the target time to 7:00 PM (19:00:00)
            const targetTime = new Date(now.getFullYear(), now.getMonth(), now.getDate() + daysUntilTuesday, 19, 0, 0);

            // 3. Special check: If it IS Tuesday but AFTER 7 PM, target next week
            if (targetTime < now) {
                targetTime.setDate(targetTime.getDate() + 7);
            }

            // 4. Calculate difference in milliseconds
            const distance = targetTime - now;

            // 5. Format the text
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            // Helper to add leading zero (e.g., "05" instead of "5")
            const pad = (n) => String(n).padStart(2, '0');

            this.countdownDisplay = `${days}D ${pad(hours)}H ${pad(minutes)}M ${pad(seconds)}S`;
        },
		setTitleFavicon(title, favicon) {
			// ... existing method content ...
		},
		async importMissions(files) {
			// ... existing method content ...
		},
		async importEvents(files) {
			// ... existing method content ...
		},
		async importClocks(files) {
			// ... existing method content ...
		},
		async importReserves(files) {
			// ... existing method content ...
		},
		async importPilots(files) {
			// ... existing method content ...
		},
	},
};
</script>

<style>
#app {
	min-height: 100vh;
	overflow: hidden !important;
	/* border-right: 1px solid #ff0;
	border-bottom: 1px solid #ff0; */
}
.header-countdown-box {
  /* Positioning for Centering */
  position: absolute; 
  top: 10px; /* Adjust vertical position */
  left: 50%; /* Start positioning 50% from the left edge */
  transform: translateX(-50%); /* Shift left by 50% of the box's own width (true center) */
  z-index: 999; /* Ensure it is rendered on top of other header elements */

  /* Compact Size and Layout */
  display: inline-flex;
  align-items: center;
  gap: 8px; /* Space between label and numbers */
  height: 30px; 
  padding: 0 12px;
  
  /* Visual Style */
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid #333;
  border-left: 2px solid #39ff14; /* Neon green accent bar */
}

.header-countdown-box .label {
  font-family: 'Rubik', sans-serif;
  color: #888;
  font-size: 0.7rem;
  font-weight: bold;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.header-countdown-box .value {
  font-family: 'Fragment Mono', monospace;
  color: #39ff14;
  font-size: 0.9rem;
  font-weight: bold;
  letter-spacing: 1px;
  min-width: 130px; 
  text-align: right;
  text-shadow: 0 0 5px rgba(57, 255, 20, 0.5);
}

</style>
