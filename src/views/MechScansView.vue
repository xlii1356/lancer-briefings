<template>
  <div id="mechScansView" :class="{ animate: animateView }" class="content-container">
    
    <!-- List Section -->
    <section id="scans-list" :class="{ animate: animate }" class="section-container">
      <div class="section-header clipped-medium-backward">
        <img src="/icons/mech.svg" />
        <h1>MECH DATABASE</h1>
      </div>
      <div class="section-content-container">
        <div class="items-list-container">
          <div 
            v-for="scan in sortedScans" 
            :key="scan.id" 
            class="scan-item" 
            :class="{ active: selectedScan && selectedScan.id === scan.id }"
            @click="selectScan(scan)"
          >
            <div class="scan-name">{{ scan.name }}</div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Content Section -->
    <section id="scan-content" :class="{ animate: animate }" class="section-container">
      <div style="height: 52px; overflow: hidden">
        <div class="section-header clipped-info-backward">
          <img src="/icons/mech.svg" />
          <h1>SCAN RESULTS</h1>
        </div>
        <div class="rhombus-back">&nbsp;</div>
      </div>
      
      <div class="section-content-container extra-margins scan-display-container">
        <div class="scan-detail" v-if="selectedScan">
           <!-- The JSON content is pre-formatted HTML from Foundry -->
           <div class="foundry-content" v-html="selectedScan.content"></div>
        </div>
        <div v-else class="empty-state">
            <p>Select a target to analyze.</p>
        </div>
      </div>
    </section>

  </div>
</template>

<script>
import MechScanModal from "@/components/modals/MechScanModal.vue";

export default {
  name: "MechScansView",
  props: {
    animate: { type: Boolean, required: true },
    scans: { type: Array, required: true },
  },
  data() {
    return {
      selectedScan: null,
      animateView: this.animate,
    };
  },
  computed: {
    sortedScans() {
        return [...this.scans].sort((a, b) => a.name.localeCompare(b.name));
    }
  },
  mounted() {
     this.checkUrlForScan();
  },
  watch: {
      scans: {
          handler() {
               this.checkUrlForScan();
          },
          immediate: true
      }
  },
  updated() {
      this.handleImageErrors();
  },
  methods: {
    checkUrlForScan() {
        if (this.$route.query.scan && this.scans.length > 0) {
            // Try ID match first
            let target = this.scans.find(s => s.id === this.$route.query.scan);
            // Fallback to name match (case insensitive) if ID fails, just in case
            if (!target) {
                target = this.scans.find(s => s.name.toLowerCase() === this.$route.query.scan.toLowerCase());
            }

            if (target) {
                this.selectScan(target);
            }
        } else if (this.sortedScans.length > 0 && !this.selectedScan) {
            this.selectedScan = this.sortedScans[0];
        }
    },
    selectScan(scan) {
        if (window.innerWidth <= 768) {
            this.$oruga.modal.open({
                component: MechScanModal,
                custom: true,
                trapFocus: true,
                props: { 
                    scan: scan,
                },
                class: 'custom-modal',
                width: 1920,
            });
        } else {
            this.selectedScan = scan;
        }
    },
    handleImageErrors() {
        // Wait for DOM to update with new v-html
        this.$nextTick(() => {
            const container = this.$el.querySelector('.foundry-content');
            if (!container) return;

            const images = container.querySelectorAll('img');
            images.forEach(img => {
                img.onerror = () => {
                    // Start by hiding the image to avoid broken icon
                    img.style.display = 'none';
                    
                    // If it's wrapped in a P tag that only contains this image, hide the P too
                    // to prevent empty block spacing
                    if (img.parentElement && img.parentElement.tagName === 'P' && img.parentElement.childNodes.length <= 1) {
                        img.parentElement.style.display = 'none';
                    }
                };
            });
        });
    }
  }
};
</script>

<style scoped>
/* List Styling */
.items-list-container {
    padding: 10px;
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow-y: auto;
}

.scan-item {
    padding: 10px;
    cursor: pointer;
    border-bottom: 1px solid #333;
    transition: background 0.2s;
}

.scan-item:hover {
    background: rgba(255, 255, 255, 0.05);
}

.scan-item.active {
    background: rgba(57, 255, 20, 0.1);
    border-left: 3px solid #39ff14;
}

.scan-name {
    font-family: 'Fragment Mono', monospace;
    color: #eee;
    font-size: 0.9rem;
}

/* Content Styling */
#scans-list {
    width: 350px;
    margin: 50px 30px;
    height: 75vh;
}

#scan-content {
    width: 1100px;
    margin: 50px 30px;
    height: 75vh;
}

.scan-display-container {
    background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent dark bg */
    color: #eee; /* Light text */
    overflow-y: auto;
    padding: 0;
    border: 1px solid #333;
}

.foundry-content {
    padding: 20px;
    font-family: 'Rubik', sans-serif; /* Match app font */
    line-height: 1.6;
}

/* Foundry HTML Specific Overrides */
/* Brute force all text to be light to override inline styles */
.foundry-content :deep(*) {
    color: #eee !important;
}

.foundry-content :deep(h2) {
    font-family: 'Fragment Mono', monospace;
    color: #39ff14 !important; /* Standard green accent */
    border-bottom: 1px solid #333;
    margin-top: 20px;
    margin-bottom: 15px;
    font-size: 1.4rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.foundry-content :deep(h3) {
    font-family: 'Fragment Mono', monospace;
    color: #00d1b2 !important; /* Cyan/Teal secondary accent */
    margin-top: 15px;
    margin-bottom: 10px;
    font-size: 1.1rem;
    text-transform: uppercase;
}

.foundry-content :deep(p) {
    margin-bottom: 10px;
}

.foundry-content :deep(img) {
    max-width: 100%;
    border: 1px solid #333 !important; /* Override inline borders */
    filter: brightness(0.9); /* Slight dim to fit dark theme */
}

.foundry-content :deep(div[style]) {
    width: 100% !important; /* Override fixed widths like 65% */
    float: none !important; /* Disable float for better stacking */
}

.foundry-content :deep(table) {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    font-size: 0.9rem;
    background: rgba(0,0,0,0.2) !important;
    font-family: 'Fragment Mono', monospace;
}

.foundry-content :deep(th) {
    background-color: rgba(57, 255, 20, 0.1) !important; /* Low opacity green */
    color: #39ff14 !important;
    font-weight: bold;
    text-align: left;
    padding: 8px;
    border: 1px solid #444;
    text-transform: uppercase;
}

.foundry-content :deep(td) {
    padding: 8px;
    border: 1px solid #444;
    color: #ccc !important;
}

.foundry-content :deep(details) {
    margin-bottom: 10px;
    border: 1px solid #333;
    padding: 10px;
    background: rgba(0,0,0,0.3) !important;
}

.foundry-content :deep(summary) {
    cursor: pointer;
    font-weight: bold;
    color: #00d1b2 !important; /* Cyan accent */
    font-family: 'Fragment Mono', monospace;
    outline: none;
}

.foundry-content :deep(summary:hover) {
    color: #39ff14 !important;
}

.empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #555;
    font-family: 'Fragment Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* Mobile Overrides */
@media (max-width: 768px) {
    #scans-list, #scan-content {
        width: auto;
        margin: 20px 10px;
        height: auto;
    }

    .foundry-content {
        padding: 10px;
    }
}
</style>
