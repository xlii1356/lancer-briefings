import { createMemoryHistory, createWebHistory, createRouter } from "vue-router";

import StatusView from "../views/StatusView.vue";
import PilotsView from "../views/PilotsView.vue";
import FactionsView from "../views/FactionsView.vue"; // added
import MessagesView from "../views/MessagesView.vue";
import MechScansView from "../views/MechScansView.vue";
import TacticalMapView from "../views/TacticalMapView.vue";
import Config from "@/assets/info/general-config.json";

const DEFAULT_TITLE = Config.defaultTitle;
const routes = [
	{
		path: "/",
		redirect: "/status",
	},
	{
		path: "/status",
		name: "Mission Status",
		component: StatusView,
		props: true,
		meta: { title: `${DEFAULT_TITLE} MISSION STATUS` },
	},
	{
		path: "/pilots",
		name: "pilots",
		component: PilotsView,
		props: true,
		meta: { title: `${DEFAULT_TITLE} PILOT ROSTER` },
	},
	{
		path: "/messages",
		name: "messages",
		component: MessagesView,
		props: true,
		meta: { title: `${DEFAULT_TITLE} MESSAGES` },
	},
	{
		path: "/factions",
		name: "Factions",
		component: FactionsView,
		props: true,
		meta: { title: `${DEFAULT_TITLE} FACTIONS LOG` },
	},
	{
		path: "/scans",
		name: "scans",
		component: MechScansView,
		props: true,
		meta: { title: `${DEFAULT_TITLE} MECH SCANS` },
	},
	{
		path: "/map",
		name: "Map",
		component: TacticalMapView,
		props: true,
		meta: { title: `${DEFAULT_TITLE} TACTICAL MAP` },
	},
];

const router = createRouter({
	history: import.meta.env.SSR ? createMemoryHistory() : createWebHistory(),
	routes,
	scrollBehavior(to, from, savedPosition) {
		if (to.hash) {
			return {
				el: to.hash,
				behavior: "smooth",
			};
		}
	},
});

router.beforeEach((to, from, next) => {
	// Use next tick to handle router history correctly
	// see: https://github.com/vuejs/vue-router/issues/914#issuecomment-384477609
	document.title = `${to.meta.title}`;
	next();
});

export default router;
