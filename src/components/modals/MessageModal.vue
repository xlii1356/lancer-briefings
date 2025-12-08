<template>
	<div class="event-modal">
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
/* Ensure the modal content wraps correctly on mobile */
.event-modal {
    max-width: 100%;
}

/* Force header scale down */
:deep(.section-header) {
    height: 40px !important;
    width: 100% !important;
    clip-path: none !important;
}
:deep(.section-header img) {
    height: 24px !important;
    width: 24px !important;
}
:deep(.section-header h1) {
    font-size: 1rem !important;
    line-height: 40px !important;
}
:deep(.rhombus-back) {
    display: none !important;
}

/* Override fixed widths that might be forcing the modal wide */
:deep(.clipped-info-backward) {
    width: 100% !important;
    max-width: 100% !important;
    clip-path: none !important;
}

/* Ensure the modal stays within bounds */
.event-modal {
    width: 100%;
    max-width: 85vw; /* Explicitly constrain width relative to viewport */
    max-height: 85vh; /* Limit height to allow scrolling within view */
    display: flex; /* Flexbox for scrolling body */
    flex-direction: column;
    overflow: hidden; /* Prevent horizontal scroll, internal scroll on body */
    box-sizing: border-box;
    margin: 0 auto; /* Center it */
}

/* .event class styles if needed for legacy */
.event-modal .event {
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
    color: #eee;
    overflow-y: auto; 
}

.modal-card-body {
    padding: 20px;
    overflow-y: auto;
    color: #eee;
    flex: 1;
    min-height: 0;
}

.event-modal .markdown {
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
}

/* Meta info styling specific to messages */
.meta-info {
    font-family: 'Rubik', sans-serif;
    font-size: 0.9rem;
    color: #aaa;
    display: flex;
    gap: 20px;
    margin-top: 5px;
}

.modal-card-title {
    font-family: 'Rubik', sans-serif;
    font-size: 1.5rem;
    color: #eee; 
    text-transform: uppercase;
    margin: 0 0 10px 0;
}

/* Use deep selector to ensure styles apply to elements INSIDE the markdown component */
:deep(.markdown),
:deep(.markdown p),
:deep(.markdown div),
:deep(.markdown span),
:deep(.markdown h1),
:deep(.markdown h2),
:deep(.markdown h3),
:deep(.markdown h4),
:deep(.markdown li) {
    white-space: pre-wrap !important; /* Preserve line breaks but wrap text */
    word-break: break-word !important; /* Break long words if necessary */
    overflow-wrap: anywhere !important; /* Force break if line is too long */
    max-width: 100%;
    box-sizing: border-box;
}
</style>
