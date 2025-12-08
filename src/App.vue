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
        <router-view :animate="animate" :initial-slug="initialSlug" :missions="missions" :factions="factions"
            :pilots="pilots" :clocks="clocks" :reserves="reserves" :messages="messages" />
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

<script>
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
            factions: [],
            missions: [],
            pilots: [],
            reserves: [],
            bonds: [],
            messages: [],
            // NEW: Countdown Data
            countdownDisplay: 'CALCULATING...',
            countdownInterval: null,
        };
    },
    created() {
        this.setTitleFavicon(Config.defaultTitle + " MISSION BRIEFING", Config.icon);
        this.importMissions(import.meta.glob("@/assets/missions/*.md", { query: '?raw', import: 'default' }));
        this.importFactions(import.meta.glob("@/assets/factions/*.md", { query: '?raw', import: 'default' }));
        this.importClocks(import.meta.glob("@/assets/clocks/*.json"));
        this.importReserves(import.meta.glob("@/assets/reserves/*.json"));

        this.importPilots(import.meta.glob("@/assets/pilots/*.json"));
        this.importMessages(import.meta.glob("@/assets/messages/*.md", { query: '?raw', import: 'default' }));
    },
    mounted() {
        this.$router.push("/status");
        // NEW: Start the countdown timer
        this.updateCountdown();
        this.countdownInterval = setInterval(this.updateCountdown, 1000);
    },
    // NEW: Clean up the timer when the app is destroyed
    beforeUnmount() {
        if (this.countdownInterval) clearInterval(this.countdownInterval);
    },
    methods: {
        // NEW: Countdown Logic (using local time)
        updateCountdown() {
            const now = new Date();
            const currentDay = now.getDay();
            let daysUntilTuesday = 2 - currentDay;

            // If it's already past Tuesday (e.g. Wednesday), cycle to the next week
            if (daysUntilTuesday < 0) {
                daysUntilTuesday += 7;
            }
            
            // Set the target time to 7:00 PM (19:00:00) in local time
            const targetTime = new Date(now.getFullYear(), now.getMonth(), now.getDate() + daysUntilTuesday, 19, 0, 0);

            // Special check: If it IS Tuesday but AFTER 7 PM, target next week
            if (targetTime < now) {
                targetTime.setDate(targetTime.getDate() + 7);
            }

            const distance = targetTime - now;
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            const pad = (n) => String(n).padStart(2, '0');

            this.countdownDisplay = `${days}D ${pad(hours)}H ${pad(minutes)}M ${pad(seconds)}S`;
        },
        setTitleFavicon(title, favicon) {
            document.title = title;
            let headEl = document.querySelector('head');
            let faviconEl = document.createElement('link');
            faviconEl.setAttribute('rel', 'shortcut icon');
            faviconEl.setAttribute('href', favicon);
            headEl.appendChild(faviconEl);
        },
        async importMissions(files) {
            let filePromises = Object.keys(files).map(path => files[path]());
            let fileContents = await Promise.all(filePromises);
            fileContents.forEach(content => {
                let mission = {};
                mission["slug"] = content.split("\n")[0].trim();
                mission["name"] = content.split("\n")[1].trim();
                mission["status"] = content.split("\n")[2].trim();
                mission["content"] = content.split("\n").splice(3).join("\n");
                this.missions = [...this.missions, mission];
            });
            this.missions = this.missions.sort(function (a, b) {
                return b["slug"] - a["slug"];
            })
        },
        async importFactions(files) {
            let filePromises = Object.keys(files).map(path => files[path]());
            let fileContents = await Promise.all(filePromises);
            fileContents.forEach(content => {
                let faction = {};
                faction["title"] = content.split("\n")[0];
                faction["location"] = content.split("\n")[1];
                faction["time"] = content.split("\n")[2];
                faction["thumbnail"] = content.split("\n")[3];
                faction["content"] = content.split("\n").splice(4).join("\n");
                this.factions = [...this.factions, faction];
            });

        },
        async importClocks(files) {
            let filePromises = Object.keys(files).map(path => files[path]());
            let fileContents = await Promise.all(filePromises);
            fileContents.forEach(content => {
                this.clocks = JSON.parse(JSON.stringify(content)).default;
            });
        },
        async importReserves(files) {
            let filePromises = Object.keys(files).map(path => files[path]());
            let fileContents = await Promise.all(filePromises);
            fileContents.forEach(content => {
                this.reserves = JSON.parse(JSON.stringify(content)).default;
            });
        },
        async importPilots(files) {
            let filePromises = Object.keys(files).map(path => files[path]());
            let fileContents = await Promise.all(filePromises);
            fileContents.forEach(content => {
                let pilotFromJson = JSON.parse(JSON.stringify(content));
                // In case the pilot was added from a copy on compcon via sharecode, remove the "reference mark" symbol
                pilotFromJson.name = pilotFromJson.name.replace("※", "");
                pilotFromJson.callsign = pilotFromJson.callsign.replace("※", "");
                let pilotFromVue = this.pilotSpecialInfo[pilotFromJson.callsign.toUpperCase()];
                let pilot = {
                    ...pilotFromJson,
                    ...pilotFromVue,
                };
                this.pilots = [...this.pilots, pilot];
                pilot.clocks.forEach(content => {
                    let clock = {};
                    clock["type"] = `Pilot Project // ${pilot.callsign}`;
                    clock["result"] = "";
                    clock["name"] = content.title;
                    clock["description"] = content.description;
                    clock["value"] = content.progress;
                    clock["max"] = content.segments;
                    clock["color"] = "#3CB043";
                    this.clocks = [...this.clocks, clock];
                });

                pilot.reserves.forEach(content => {
                    let reserve = {};
                    reserve["type"] = content.type;
                    reserve["name"] = content.name;
                    reserve["description"] = content.description;
                    reserve["label"] = content.label;
                    reserve["cost"] = content.cost;
                    reserve["notes"] = content.notes;
                    reserve["callsign"] = pilot.callsign.toUpperCase();
                    this.reserves = [...this.reserves, reserve];
                });
            });
        },
        async importMessages(files) {
            let filePromises = Object.keys(files).map(path => files[path]());
            let fileContents = await Promise.all(filePromises);
            fileContents.forEach(content => {
                let message = {};
                // Format:
                // ID
                // Title
                // Sender // Date
                // ... Content
                let lines = content.split("\n");
                message["id"] = lines[0].trim();
                message["title"] = lines[1].trim();
                
                let meta = lines[2].split("//");
                message["sender"] = meta[0] ? meta[0].trim() : "UNKNOWN";
                message["date"] = meta[1] ? meta[1].trim() : "UNKNOWN";

                message["content"] = lines.splice(3).join("\n");
                this.messages = [...this.messages, message];
            });
        },
    },
};
</script>

<style>
/* --- CRITICAL LAYOUT FIXES (To prevent boxes from being empty/collapsed) --- */
html {
    overflow: hidden !important;
    width: 100%;
    height: 100%;
}

body {
    margin: 0;
    padding: 0;
    
    /* SCALE WHOLE SITE */
    transform: scale(0.8);
    transform-origin: top left;
    width: 125%; /* 100 / 0.8 = 125% to fill width */
    height: 125vh; /* 100 / 0.8 = 125vh to fill height */
    overflow-x: hidden;
}

#app {
	min-height: 100vh;
	overflow: hidden !important;
    display: block; 
}

.page-wrapper {
    /* Locks Header/Sidebar in place */
    position: fixed; 
    top: 0;
    left: 0;
    width: 100%; 
    height: 100%; 
    z-index: 100;
    pointer-events: none; /* Let clicks pass through */
}

.page-wrapper > * {
    pointer-events: auto; /* Re-enable clicks for Header/Sidebar */
}

#router-view-container {
    /* Offsets content away from the fixed sidebar and header */
    margin-left: 100px; /* ASSUMPTION: Adjust this to your Sidebar width */
    padding-top: 50px;  /* ASSUMPTION: Adjust this to your Header height */

    position: relative;
    height: 100%; /* Takes full parent height (125vh) -> 100vh visual */
    width: auto; 
    overflow-y: auto; 
}
/* --- END CRITICAL LAYOUT FIXES --- */


/* --- CENTERED COUNTDOWN STYLE --- */
.header-countdown-box {
    /* Positioning for Centering */
    position: absolute; 
    top: 10px; /* Vertical position */
    left: 50%; 
    transform: translateX(-50%); /* True centering */
    z-index: 999; /* Ensure it is rendered on top */

    /* Compact Size and Look */
    display: inline-flex;
    align-items: center;
    gap: 8px;
    height: 30px; 
    padding: 0 12px;
    background: rgba(0, 0, 0, 0.5);
    border: 1px solid #333;
    border-left: 2px solid #39ff14; 
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

@media (max-width: 768px) {
    #router-view-container {
        margin-left: 0; /* Remove sidebar offset on mobile */
        padding-top: 0; /* Let flow naturally */
        padding-left: 10px;
        padding-right: 10px;
        position: relative; /* Override absolute positioning */
        top: auto; /* Reset top */
        left: auto; /* Reset left */
        width: 100%;
        height: auto; /* Allow full height */
        overflow-y: visible; /* Let body scroll */
    }
    
    .page-wrapper {
        position: relative; /* Unfix on mobile to allow flow */
        height: auto; /* Let it grow */
    }
    
    .header-countdown-box {
        position: relative; /* Stack naturally */
        top: auto;
        left: auto;
        transform: none;
        width: 100%;
        margin-bottom: 20px;
        justify-content: center;
        background: rgba(0, 0, 0, 0.8);
    }
}
</style>