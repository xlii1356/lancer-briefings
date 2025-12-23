<template>
	<header>
		<div class="title clipped-x-large-forward">
			<img class="logo" src="/faction-logos/silvershard_outline.webp" />
			<div class="title-container">
				<div id="title-first-line" class="title-row">
					<span id="title-header">{{ header.headerTitle }}</span>
					<span id="title-subheader">{{ header.headerSubtitle }}</span>
				</div>
				<div class="title-row">
					<span id="subtitle-header">{{ header.subheaderTitle }}</span>
					<span id="subtitle-subheader">// {{ header.subheaderSubtitle }}</span>
				</div>
			</div>
		</div>
		<div class="rhombus"></div>
		<div class="planet-location-container">
			<video autoplay muted loop width="90px" height="90px">
				<source :src="`${planetPath}`" type="video/webm" />
			</video>
			<div class="location-info">
				<div id="planet-year" class="location-row">
					<div id="year">
						<h4>Year</h4>
						<span class="subtitle">{{ header.year }}</span>
					</div>
					<div id="planet">
						<h4>Deployment Info</h4>
						<span class="subtitle">{{ header.planet }}</span>
					</div>
				</div>
				<div id="system-gate-ring" class="location-row">
					<div id="ring">
						<h4>Ring</h4>
						<span class="subtitle">{{ header.ring }}</span>
					</div>
					<div id="gate">
						<h4>Gate</h4>
						<span class="subtitle">{{ header.gate }}</span>
					</div>
					<div id="system">
						<h4>System</h4>
						<span class="subtitle">{{ header.system }}</span>
					</div>
				</div>
			</div>
		</div>
	</header>
</template>

<script>
export default {
	components: {},
	props: {
		planetPath: {
			type: String,
			required: true,
		},
		header: {
			type: Object,
			required: true,
		},
	},
	data() {
		return {};
	},
	created() {},
	mounted() {},
};
</script>

<style scoped>
/* Add this to your style block */
.title {
	display: flex; /* Ensures the logo and text sit side-by-side */
	align-items: center; 
}

.logo {
	/* These lines prevent squishing */
	height: 80px;       /* Set a fixed height matching your header design */
	width: auto;        /* Let width calculate automatically based on height */
	object-fit: contain; /* Ensures the image scales correctly within bounds */
	flex-shrink: 0;     /* Tells flexbox NOT to shrink this item if space is tight */
	
	/* Optional spacing */
	margin-right: 15px; 
}
</style>