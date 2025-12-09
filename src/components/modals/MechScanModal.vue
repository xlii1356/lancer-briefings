<template>
	<div class="mech-scan-modal">
		<div class="event-header-container">
			<div class="section-header clipped-medium-backward-bio">
				<img src="/icons/mech.svg" />
				<h1>SCAN DATA</h1>
			</div>
			<div class="rhombus-back">&nbsp;</div>
		</div>
		<div class="mech-scan-body">
			<div class="name">
				<h1>{{ scan.name }}</h1>
			</div>
             <!-- Reuse the same class for styling consistency -->
			<div class="foundry-content" v-html="scan.content"></div>
		</div>
	</div>
</template>

<script>
export default {
	name: "MechScanModal",
	props: {
		scan: {
			type: Object,
			required: true,
		}
	},
    updated() {
        this.handleImageErrors();
    },
    mounted() {
        this.handleImageErrors();
    },
    methods: {
        handleImageErrors() {
             // Logic to hide broken images, copied from MechScansView
             this.$nextTick(() => {
                const container = this.$el.querySelector('.foundry-content');
                if (!container) return;

                const images = container.querySelectorAll('img');
                images.forEach(img => {
                    img.onerror = () => {
                         img.style.display = 'none';
                         if (img.parentElement && img.parentElement.tagName === 'P' && img.parentElement.childNodes.length <= 1) {
                             img.parentElement.style.display = 'none';
                         }
                    };
                    // Trigger check immediately in case already failed
                    if (img.complete && img.naturalHeight === 0) {
                        img.onerror();
                    }
                });
            });
        }
    }
};
</script>

<style scoped>
/* Modal Container Styling (Copied/Adapted from EventModal) */
.mech-scan-modal {
    width: 100%;
    max-width: 85vw;
    max-height: 85vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-sizing: border-box;
    margin: 0 auto;
    z-index: 2147483647 !important;
    position: relative;
    background-color: #161c1d !important; /* Force opaque background */
    border: 1px solid #333;
}

.mech-scan-body {
    padding: 20px;
    overflow-y: auto;
    color: #eee;
    flex: 1;
    min-height: 0;
}

.name h1 {
    font-family: 'Fragment Mono', monospace;
    color: #39ff14;
    font-size: 1.2rem;
    margin-bottom: 20px;
    border-bottom: 1px solid #333;
    padding-bottom: 10px;
}

/* Header Overrides for Modal Context */
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
:deep(.clipped-medium-backward-bio) {
    width: 100% !important;
    max-width: 100% !important;
    clip-path: none !important;
}


/* --- FOUNDRY CONTENT STYLING (MATCHING MECHSCANSVIEW) --- */

.foundry-content {
    font-family: 'Rubik', sans-serif;
    line-height: 1.6;
}

/* Force Light Text */
:deep(*) {
    color: #eee !important;
}

:deep(h2) {
    font-family: 'Fragment Mono', monospace;
    color: #39ff14 !important;
    border-bottom: 1px solid #333;
    margin-top: 20px;
    margin-bottom: 15px;
    font-size: 1.4rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

:deep(h3) {
    font-family: 'Fragment Mono', monospace;
    color: #00d1b2 !important;
    margin-top: 15px;
    margin-bottom: 10px;
    font-size: 1.1rem;
    text-transform: uppercase;
}

:deep(p) {
    margin-bottom: 10px;
}

:deep(img) {
    max-width: 100%;
    border: 1px solid #333 !important;
    filter: brightness(0.9);
}

:deep(div[style]) {
    width: 100% !important;
    float: none !important;
}

:deep(table) {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    font-size: 0.9rem;
    background: rgba(0,0,0,0.2) !important;
    font-family: 'Fragment Mono', monospace;
}

:deep(th) {
    background-color: rgba(57, 255, 20, 0.1) !important;
    color: #39ff14 !important;
    font-weight: bold;
    text-align: left;
    padding: 8px;
    border: 1px solid #444;
    text-transform: uppercase;
}

:deep(td) {
    padding: 8px;
    border: 1px solid #444;
    color: #ccc !important;
}

:deep(details) {
    margin-bottom: 10px;
    border: 1px solid #333;
    padding: 10px;
    background: rgba(0,0,0,0.3) !important;
}

:deep(summary) {
    cursor: pointer;
    font-weight: bold;
    color: #00d1b2 !important;
    font-family: 'Fragment Mono', monospace;
    outline: none;
}

:deep(summary:hover) {
    color: #39ff14 !important;
}

</style>
