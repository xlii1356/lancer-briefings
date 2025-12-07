<template>
	<div class="event-modal">
		<div class="event-header-container">
			<div class="section-header clipped-medium-backward-bio">
				<img src="/icons/events.svg" />
				<h1>KNOWN DETAILS</h1>
			</div>
			<div class="rhombus-back">&nbsp;</div>
		</div>
		<div class="event" @click="handleMarkdownClick">
			<div class="name">
				<h1>{{ event.location }} // {{ event.time }}</h1>
				<h2>{{ event.title }}</h2>
			</div>
			<vue-markdown-it :source="event.content" class="markdown" />
		</div>
	</div>
</template>

<script>
import { VueMarkdownIt } from '@f3ve/vue-markdown-it';
import PilotModal from '@/components/modals/PilotModal.vue';
import PrimeModal from '@/components/modals/PrimeModal.vue';
import primeDataList from '@/assets/prime/prime.json';

export default {
	name: "EventModal",
	components: {
		VueMarkdownIt,
	},
	props: {
		event: {
			type: Object,
			required: true,
		},
        // We need pilots data to resolve pilot links
        pilots: {
            type: Array,
            required: false,
            default: () => [] 
        },
        // We need events data if we want to resolve event:// links to OTHER events (though tricky in a modal)
        events: {
            type: Array,
            required: false,
            default: () => []
        }
	},
    data() {
        return {
            primeData: primeDataList
        };
    },
    methods: {
        handleMarkdownClick(event) {
            const link = event.target.closest('a');
            if (!link) return;

            const href = link.getAttribute('href');
            
            // --- HANDLE PILOT LINKS ---
            if (href && (href.startsWith('pilot://') || href.startsWith('pilots://'))) {
                event.preventDefault();
                let rawCallsign = href.replace(/^pilots?:\/\//, '');
                const callsign = decodeURIComponent(rawCallsign).toUpperCase();
                
                // We rely on the parent passing 'pilots' prop, OR we could try to inject/find it.
                // Assuming we update the caller to pass it.
                const pilot = this.pilots.find(p => p.callsign.toUpperCase() === callsign);
                
                if (pilot) {
                    this.$oruga.modal.open({
                        component: PilotModal,
                        custom: true,
                        trapFocus: true,
                        props: { pilot: pilot, talents: [], skills: [], frames: [] },
                        class: 'custom-modal',
                        width: 1920,
                    });
                }
            }

            // --- HANDLE MISSION LINKS (Navigate normally) ---
            else if (href && href.startsWith('mission://')) {
                event.preventDefault();
                const slug = decodeURIComponent(href.replace('mission://', ''));
                this.$router.push({ path: '/status', query: { mission: slug } });
                this.$emit('close'); // Close modal on navigation
            }

            // --- HANDLE PRIME LINKS ---
            else if (href && href.startsWith('prime://')) {
                event.preventDefault();
                const rawAlias = href.replace('prime://', '');
                const targetAlias = decodeURIComponent(rawAlias).toUpperCase();
                const primeEntry = this.primeData.find(p => p.alias.toUpperCase() === targetAlias);

                if (primeEntry) {
                    this.$oruga.modal.open({
                        component: PrimeModal,
                        custom: true,
                        trapFocus: true,
                        props: { prime: primeEntry },
                        class: 'custom-modal',
                        width: 1920,
                    });
                }
            }
             // --- HANDLE EVENT LINKS ---
            else if (href && href.startsWith('event://')) {
                event.preventDefault();
                const titleRaw = href.replace('event://', '');
                const title = decodeURIComponent(titleRaw);
                // Find existing event from the passed event list
                const targetEvent = this.events.find(e => e.title.trim() === title.trim());

                if (targetEvent) {
                    // Open a new modal stacked on top for the linked event
                     this.$oruga.modal.open({
                        component: this.$options, // Self-reference for recursion
                        custom: true,
                        trapFocus: true,
                        props: { 
                            event: targetEvent,
                            pilots: this.pilots,
                            events: this.events
                        },
                        class: 'custom-modal',
                        width: 1920,
                    });
                }
            }
        }
    }
};
</script>

<style scoped>
/* Ensure the modal content wraps correctly on mobile */
.event-modal {
    max-width: 100%;
}

/* Override fixed widths that might be forcing the modal wide */
:deep(.clipped-medium-backward-bio) {
    width: 100% !important;
    max-width: 100% !important;
    clip-path: none !important; /* Optional: remove complex clip path if it messes up responsive width, or adjust */
}

/* Ensure the modal stays within bounds */
.event-modal {
    width: 100%;
    max-width: 85vw; /* Explicitly constrain width relative to viewport */
    overflow-x: hidden; /* Prevent horizontal scroll */
    box-sizing: border-box;
    margin: 0 auto; /* Center it */
}

.event-modal .event {
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
}

.event-modal .markdown {
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
}

/* Use deep selector to ensure styles apply to elements INSIDE the markdown component */
/* Note: Using :deep() for Vue 3 compliance */
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

/* Re-apply link styles since this component might be scoped differently or need explicit targetting */
::v-deep .markdown a[href^="pilot://"],
::v-deep .markdown a[href^="pilots://"] {
  color: #FFC107;
  font-weight: bold;
  text-decoration: none;
  border-bottom: 1px dotted #FFC107;
  transition: background 0.2s;
}
::v-deep .markdown a[href^="pilot://"]:hover,
::v-deep .markdown a[href^="pilots://"]:hover {
  background-color: rgba(255, 193, 7, 0.2);
  cursor: pointer;
}

::v-deep .markdown a[href^="mission://"] {
  color: #7dbbbb;
  font-weight: bold;
  text-decoration: none;
  border-bottom: 1px dotted #7dbbbb;
}
::v-deep .markdown a[href^="mission://"]:hover {
  background-color: rgba(125, 187, 187, 0.2);
  cursor: pointer;
}

::v-deep .markdown a[href^="event://"] {
  color: #bd93f9; 
  font-weight: bold;
  text-decoration: none;
  border-bottom: 1px dotted #bd93f9;
}
::v-deep .markdown a[href^="event://"]:hover {
  background-color: rgba(189, 147, 249, 0.2);
  cursor: pointer;
}

::v-deep .markdown a[href^="prime://"] {
  color: #ff5555; 
  font-weight: bold;
  text-decoration: none;
  border-bottom: 1px dotted #ff5555;
}
::v-deep .markdown a[href^="prime://"]:hover {
  background-color: rgba(255, 85, 85, 0.2);
  cursor: pointer;
}
</style>
