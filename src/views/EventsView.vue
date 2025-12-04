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
import PilotModal from '@/components/modals/PilotModal.vue'; // 1. Import Modal

export default {
  components: {
    VueMarkdownIt,
    Event,
  },
  props: {
    animate: { type: Boolean, required: true },
    events: { type: Array, required: true },
    pilots: { type: Array, required: true }, // Ensure this prop exists in App.vue passed down
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
    // 2. Add the Click Handler
    handleMarkdownClick(event) {
      const link = event.target.closest('a');
      if (!link) return;

      const href = link.getAttribute('href');
      
      // -- HANDLE PILOT LINKS --
      if (href && href.startsWith('pilot://')) {
        event.preventDefault();
        
        // 1. Remove the prefix
        let rawCallsign = href.replace('pilot://', '');
        
        // 2. DECODE THE URL (Turns "GRAN%20GRAN" back into "GRAN GRAN")
        const callsign = decodeURIComponent(rawCallsign).toUpperCase();
        
        const pilot = this.pilots.find(p => p.callsign.toUpperCase() === callsign);
        
        if (pilot) {
          this.$oruga.modal.open({
            component: PilotModal,
            custom: true,
            trapFocus: true,
            props: {
              pilot: pilot,
              talents: this.$root.talents || [],
              skills: this.$root.skills || [],
              frames: this.$root.frames || []
            },
            class: 'custom-modal',
            width: 1920,
          });
        } else {
          console.warn("Pilot not found:", callsign);
        }
      }

      // -- HANDLE MISSION LINKS --
      else if (href && href.startsWith('mission://')) {
        event.preventDefault();
        // Decode mission slugs just in case they have weird characters too
        const slug = decodeURIComponent(href.replace('mission://', ''));
        
        // If we are already on StatusView, just select it
        if (this.selectMission) {
           this.selectMission(slug);
        } 
        // If we are on EventsView, route to StatusView
        else {
           this.$router.push({ path: '/status', query: { mission: slug } });
        }
      }
    },
  }
};
</script>

<style scoped>
/* Link Styles */
::v-deep .markdown a[href^="pilot://"] {
  color: #FFC107;
  font-weight: bold;
  text-decoration: none;
  border-bottom: 1px dotted #FFC107;
}
::v-deep .markdown a[href^="pilot://"]:hover {
  background-color: rgba(255, 193, 7, 0.2);
  cursor: pointer;
}
</style>