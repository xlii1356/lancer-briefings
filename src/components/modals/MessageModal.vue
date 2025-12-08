<template>
	<div class="message-modal">
		<div class="header-container">
			<div class="section-header clipped-info-backward">
				<img src="/icons/protocol.svg" />
				<h1>DECODED TRANSMISSION</h1>
			</div>
			<div class="rhombus-back">&nbsp;</div>
		</div>
			<div class="modal-card-head" style="background-color: #0c090d">
				<p class="modal-card-title">{{ message.title }}</p>
                <div class="meta-info">
                    <span><strong>FROM:</strong> {{ message.sender }}</span>
                    <span><strong>DATE:</strong> {{ message.date }}</span>
                </div>
			</div>
			<div class="modal-card-body content-wrapper" style="background-color: #0c090d">
				<vue-markdown-it :source="message.content" class="markdown" />
			</div>
	</div>
</template>

<script>
import { VueMarkdownIt } from '@f3ve/vue-markdown-it';

export default {
	name: "MessageModal",
	components: {
		VueMarkdownIt,
	},
	props: {
		message: {
			type: Object,
			required: true,
		},
	},
};
</script>

<style scoped>
.message-modal {
    width: 100%;
    max-width: 85vw; /* Explicitly constrain width relative to viewport */
    max-height: 85vh; /* Limit height to allow scrolling within view */
    display: flex; /* Flexbox for scrolling body */
    flex-direction: column;
    overflow: hidden; /* Prevent horizontal scroll */
    box-sizing: border-box;
    margin: 0 auto; /* Center it */
}

.header-container {
    margin-bottom: 20px;
}

.modal-card-head {
    padding: 20px;
    border-bottom: 1px solid #444;
}

.modal-card-title {
    font-family: 'Rubik', sans-serif;
    font-size: 1.5rem;
    color: #eee; 
    text-transform: uppercase;
    margin: 0 0 10px 0;
}

.meta-info {
    font-family: 'Rubik', sans-serif;
    font-size: 0.9rem;
    color: #aaa;
    display: flex;
    gap: 20px;
}

.modal-card-body {
    padding: 20px;
    overflow-y: auto; /* Enable vertical scroll for content */
    color: #eee; /* Ensure text is light */
}

/* Use deep selector to ensure text color applies */
:deep(.markdown) {
    color: #eee;
    font-family: 'Rubik', sans-serif;
    line-height: 1.6;
}

:deep(.markdown p) {
    margin-bottom: 1em;
}
</style>
