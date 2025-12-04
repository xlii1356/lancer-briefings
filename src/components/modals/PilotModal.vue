<template>
  <div class="pilot-modal">
    <div class="pilot-header-container">
      <div class="section-header clipped-medium-backward-bio">
        <img src="/icons/pilot.svg" />
        <h1>{{ pilot.name }} [{{ pilot.callsign }}]</h1>
      </div>
      <div class="rhombus-back">&nbsp;</div>
    </div>
    <div class="pilot markdown">
      <div v-html="getHistory()"/>
    </div>
  </div>
  <div class="pilot-modal portrait">
    <div class="pilot-header-container">
      <div class="section-header clipped-medium-backward-pilot">
        <img src="/icons/portrait.svg" />
        <h1>Pilot Artwork</h1>
      </div>
      <div class="rhombus-back">&nbsp;</div>
    </div>
    <div class="pilot">
      <img :src="pilotPortrait" class="portrait" />
    </div>
  </div>
</template>

<script>
import { VueMarkdownIt } from '@f3ve/vue-markdown-it';

export default {
  name: 'PilotModal',
  components: {
    VueMarkdownIt,
  },
  inheritAttrs: false,
  props: {
    pilot: {
      type: Object,
      required: true,
    },
    // Added these optional props so the modal can look up specific data if needed later
    talents: {
      type: Array,
      required: false,
      default: () => []
    },
    skills: {
      type: Array,
      required: false,
      default: () => []
    },
    frames: {
      type: Array,
      required: false,
      default: () => []
    }
  },
  data() {
    return {
      markdownHtml: true,
    };
  },
  computed: {
    pilotPortrait() {
      // Priority: 1. Cloud/External URL (from JSON), 2. Local File (fallback)
      if (this.pilot.cloud_portrait) {
        return this.pilot.cloud_portrait;
      }
      return `/pilots/${this.pilot.callsign.toUpperCase()}.webp`;
    },
    mechPortrait() {
      return `/mechs/${this.pilot.callsign.toUpperCase()}.webp`;
    },
  },
  methods: {
    getHistory() {
      // Safety check for empty history/appearance
      if ((!this.pilot.history || this.pilot.history === "") && 
          (!this.pilot.text_appearance || this.pilot.text_appearance === "")) {
        return `<p> <h2> [ERR: REDACTED] </h2> </p>`;
      }

      let response = "<p>";
      
      if (this.pilot.text_appearance && this.pilot.text_appearance !== "") {
        response += `<h2>APPEARANCE</h2> ${this.pilot.text_appearance} <hr>`;
      }

      if (this.pilot.history && this.pilot.history !== "") {
        response += `<h2>HISTORY</h2> ${this.pilot.history} <hr>`;
      }

      response += "</p>";

      return response;
    }
  },
};
</script>

<style scoped>
/* Ensure images in the modal fit correctly */
.pilot-modal.portrait .portrait {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top;
}
</style>