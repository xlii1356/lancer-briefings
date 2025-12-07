<template>
	<div class="sidebar-page">
		<section class="sidebar-layout">
			<o-sidebar
			  id="sidebar"
			  position="static"
			  :animate="animate"
			  :mobile="mobile"
			  :expand-on-hover="expandOnHover"
			  :reduce="reduce"
			  open>
				<router-link class="clipped-bottom-right" to="/status">
					<img src="/icons/orbital.svg" />
					<span>Status</span>
				</router-link>
				<router-link class="clipped-bottom-right" to="/pilots">
					<img src="/icons/pilot.svg" />
					<span>Pilots</span>
				</router-link>
				<router-link class="clipped-bottom-right" to="/events">
					<img src="/faction-logos/barony.svg" />
					<span>Factions</span>
				</router-link>
			</o-sidebar>
		</section>
	</div>
</template>

<script>
export default {
	props: {
		animate: {
			type: Boolean,
			required: true,
		},
	},
	data() {
		return {
			expandOnHover: false,
			mobile: "reduced",
			reduce: false,
		};
	},
};
</script>

<style scoped>
.sidebar-page,
.sidebar-layout {
	pointer-events: none;
	height: 100%; /* Ensure it doesn't collapse but allows clicks through */
	width: 100%;
}

#sidebar {
	pointer-events: auto;
}
</style>
