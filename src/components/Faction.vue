<template>
	<div class="faction">
		<div class="name">
			<h1>{{ faction.location }} // {{ faction.time }}</h1>
			<h2>{{ faction.title }}</h2>
		</div>
		<img class="thumbnail" :src="faction.thumbnail" />
		<div class="preview">
			{{ getPreview }}
		</div>
		<a @click.prevent="selectFaction">Read More</a>
	</div>
</template>

<script>
<script>
import FactionModal from "@/components/modals/FactionModal.vue";

import removeMd from "remove-markdown";

export default {
	name: "Faction",
	components: {
		FactionModal,
	},
	props: {
		faction: {
			type: Object,
			required: true,
		},
	},
	data() {
		return {
			removeMd,
		};
	},
	computed: {
		getPreview() {
			return this.removeMd(this.faction.content).substring(0, 200) + "...";
		},
	},
	methods: {
		selectFaction() {
			this.$emit('select-faction', this.faction)
		}
	}
}
</script>
