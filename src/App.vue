<template>
	<div class="page-wrapper">
		<Header :planet-path="planetPath" :class="{ animate: animate }" :header="header" />
		<Sidebar :animate="animate" :class="{ animate: animate }" />
	</div>
	<div id="router-view-container">
		<!-- Ensure missions and pilots are passed down to router-view -->
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

<script>
import Header from "./components/layout/Header.vue";
import Sidebar from "./components/layout/Sidebar.vue";

export default {
	components: {
		Header,
		Sidebar,
	},
	data() {
		return {
			animate: false,
			planetPath: "/backgrounds/planet-01.png",
			initialSlug: "mission-01",
			header: {},
			missions: [],
			events: [],
			pilots: [],
			clocks: [],
			reserves: [],
			pilotSpecialInfo: {
				// Special info for pilots, e.g., portraits
				// NOTE: I am using placeholder images here. Replace with actual pilot data.
				"MAVERICK": { portraitUrl: "https://placehold.co/128x128/00ffc1/1a1a1a?text=MV" },
				"ECHO": { portraitUrl: "https://placehold.co/128x128/00ffc1/1a1a1a?text=EC" },
				"PHOENIX": { portraitUrl: "https://placehold.co/128x128/00ffc1/1a1a1a?text=PX" },
				"GHOST": { portraitUrl: "https://placehold.co/128x128/00ffc1/1a1a1a?text=GH" },
				"VIPER": { portraitUrl: "https://placehold.co/128x128/00ffc1/1a1a1a?text=VP" },
				"STRIKER": { portraitUrl: "https://placehold.co/128x128/00ffc1/1a1a1a?text=ST" },
			},
		};
	},
	mounted() {
		this.loadContent();
		setTimeout(() => {
			this.animate = true;
		}, 100);
	},
	methods: {
		async loadContent() {
			try {
				// Load Header
				let headerContent = await fetch("/content/header.json");
				this.header = await headerContent.json();

				// Load Missions
				let missionContent = await fetch("/content/missions.json");
				this.missions = await missionContent.json();

				// Load Events
				let eventContent = await fetch("/content/events.json");
				this.events = await eventContent.json();

				// Load Pilots/Clocks/Reserves (The Lancer Comp/Con Share Code structure)
				let pilotContent = await fetch("/content/sharecode.json");
				let pilotJsonArray = await pilotContent.json();

				pilotJsonArray.forEach(pilotData => {
					let pilotFromJson = JSON.parse(JSON.stringify(pilotData));
					// In case the pilot was added from a copy on compcon via sharecode, remove the "reference mark" symbol
					pilotFromJson.name = pilotFromJson.name.replace("※", "");
					pilotFromJson.callsign = pilotFromJson.callsign.replace("※", "");
					
					// Merge with local special info (like portraits)
					let pilotFromVue = this.pilotSpecialInfo[pilotFromJson.callsign.toUpperCase()] || {};
					let pilot = {
						...pilotFromJson,
						...pilotFromVue,
					};
					this.pilots = [...this.pilots, pilot];

					// Process Clocks
					(pilot.clocks || []).forEach(content => {
						let clock = {
							"type": `Pilot Project // ${pilot.callsign}`,
							"result": "",
							"name": content.title,
							"description": content.description,
							"value": content.progress,
							"max": content.segments,
							"color": "#3CB043",
						};
						this.clocks = [...this.clocks, clock];
					});

					// Process Reserves (The Lancer Comp/Con Share Code structure)
					(pilot.reserves || []).forEach(content => {
						let reserve = {
							"type": content.type,
							"name": content.name,
							"description": content.description,
							"label": content.label,
							"cost": content.cost,
							"notes": content.notes,
							"callsign": pilot.callsign.toUpperCase(),
						};
						this.reserves = [...this.reserves, reserve];
					});
				});

				// Set the initial mission slug to the first mission if it exists
				if (this.missions.length > 0) {
					this.initialSlug = this.missions[0].slug;
				}

			} catch (error) {
				console.error("Failed to load content:", error);
			}
		},
	},
};
</script>

<style>
/* Existing CSS from App.vue is not shown but assumed to be present */
</style>