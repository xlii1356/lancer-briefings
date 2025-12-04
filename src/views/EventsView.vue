<template>
  <div id="eventsView" :class="{ animate: animateView }" :style="{ 'animation-delay': animationDelay }" class="content-container">
    <section id="events" :class="{ animate: animate }" class="section-container">
      <div class="section-header clipped-medium-backward">
        <img src="/icons/license.svg" />
        <h1>KNOWN FACTIONS</h1>
      </div>
      <div class="section-content-container">
        <div class="events-list-container">
          <Event
            v-for="item in events"
            :key="item.title"
            :event="item"
            :animate="animate"
            @select-event="selectEvent(item)" />
        </div>
      </div>
    </section>
    
    <section id="events-logs" :class="{ animate: animate }" class="section-container">
      <div style="height: 52px; overflow: hidden">
        <div class="section-header clipped-medium-backward-events-logs">
          <img src="/icons/conversation.svg" />
          <h1>KNOWN DETAILS</h1>
        </div>
        <div class="rhombus-back">&nbsp;</div>
      </div>
      
      <div class="section-content-container extra-margins" @click="handleMarkdownClick">
        <div class="event" v-if="selectedEvent.title">
          <div class="name">
            <h1>{{ selectedEvent.location }} // {{ selectedEvent.time }}</h1>
            <h2>{{ selectedEvent.title }}</h2>
          </div>
          <vue-markdown-it :source="selectedEvent.content" class="markdown" />
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { VueMarkdownIt } from '@f3ve/vue-markdown-it';
import Event from "@/components/Event.vue";
import PilotModal from '@/components/modals/PilotModal.vue'; // 1. Import the Modal

export default {
  components: {
    VueMarkdownIt,
    Event,
  },
  props: {
    animate: { type: Boolean, required: true },
    events: { type: Array, required: true },
    // 2. THIS WAS MISSING: Allow the view to receive pilot data
    pilots: { type: Array, required: true, default: () => [] }, 
  },
  data() {
    return {
      selectedEvent: { type: Object }
    };
  },
  methods: {
    selectEvent(event) {
      this.selectedEvent = event;
    },
    // 3. The Click Handler Logic
    handleMarkdownClick(event) {
      // Find the closest link element
      const link = event.target.closest('a');
      if (!link) return;

      const href = link.getAttribute('href');
      
      // -- HANDLE PILOT LINKS --
      if (href && href.startsWith('pilot://')) {
        event.preventDefault();
        console.log("Pilot Link Clicked:", href); // Debug Log

        // Remove prefix and fix spaces (%20 -> Space)
        const rawCallsign = href.replace('pilot://', '');
        const callsign = decodeURIComponent(rawCallsign).toUpperCase();
        
        console.log("Searching for pilot:", callsign); // Debug Log

        // Find the pilot in the data passed from App.vue
        const pilot = this.pilots.find(p => p.callsign.toUpperCase() === callsign);
        
        if (pilot) {
          console.log("Pilot found, opening modal."); // Debug Log
          this.$oruga.modal.open({
            component: PilotModal,
            custom: true,
            trapFocus: true,
            props: { 
              pilot: pilot,
              // Pass empty arrays for these if they aren't available in this view
              talents: [], 
              skills: [], 
              frames: [] 
            },
            class: 'custom-modal',
            width: 1920,
          });
        } else {
          console.warn("Pilot not found in data:", callsign);
          alert(`Error: Pilot '${callsign}' not found in roster.`);
        }
      }

      // -- HANDLE MISSION LINKS --
      else if (href && href.startsWith('mission://')) {
        event.preventDefault();
        console.log("Mission Link Clicked:", href); // Debug Log
        const slug = href.replace('mission://', '');
        
        // Redirect to Status page with the mission selected
        this.$router.push({ path: '/status', query: { mission: slug } });
      }
    }
  }
};
</script>

<style scoped>
/* STYLING FOR SPECIAL LINKS */
::v-deep .markdown a[href^="pilot://"] {
  color: #FFC107;
  font-weight: bold;
  text-decoration: none;
  border-bottom: 1px dotted #FFC107;
  transition: background 0.2s;
}

::v-deep .markdown a[href^="pilot://"]:hover {
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
</style>