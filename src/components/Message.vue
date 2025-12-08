<template>
	<div class="message" @click="selectMessage">
		<div class="header">
			<span class="id">MSG // {{ message.id }}</span>
			<span class="meta">{{ message.sender }} // {{ message.date }}</span>
		</div>
		<div class="title">{{ message.title }}</div>
		<div class="preview">
			{{ getPreview }}
		</div>
	</div>
</template>

<script>
import removeMd from "remove-markdown";

export default {
	name: "Message",
	props: {
		message: {
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
			// Strip markdown and take first 100 chars
			return this.removeMd(this.message.content).substring(0, 100) + "...";
		},
	},
	methods: {
		selectMessage() {
			this.$emit('select-message', this.message)
		}
	}
}
</script>

<style scoped>
.message {
	background: rgba(0, 0, 0, 0.3);
	border: 1px solid #333;
	padding: 15px;
	cursor: pointer;
	transition: all 0.2s ease;
	margin-bottom: 10px;
    border-left: 3px solid #777;
}

.message:hover {
	background: rgba(255, 255, 255, 0.05);
	border-color: #555;
    border-left-color: #39ff14; /* Green accent on hover */
}

.header {
	display: flex;
	justify-content: space-between;
	font-family: 'Rubik', sans-serif;
	font-size: 0.75rem;
	color: #888;
	margin-bottom: 5px;
}

.id {
    color: #555;
}

.meta {
    text-transform: uppercase;
}

.title {
	font-family: 'Rubik', sans-serif;
	font-size: 1.1rem;
	font-weight: bold;
	color: #eee;
	margin-bottom: 8px;
}

.preview {
	font-family: 'Roboto', sans-serif;
	font-size: 0.9rem;
	color: #aaa;
	line-height: 1.4;
}
</style>
