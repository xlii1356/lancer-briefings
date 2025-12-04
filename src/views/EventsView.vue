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
      const link = event.target.closest('a');
      if (!link) return;

      const href = link.getAttribute('href');
      
      // --- HANDLE PILOT LINKS ---
      if (href && (href.startsWith('pilot://') || href.startsWith('pilots://'))) {
        event.preventDefault();
        let rawCallsign = href.replace(/^pilots?:\/\//, '');
        const callsign = decodeURIComponent(rawCallsign).toUpperCase();
        
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

      // --- HANDLE MISSION LINKS ---
      else if (href && href.startsWith('mission://')) {
        event.preventDefault();
        const slug = decodeURIComponent(href.replace('mission://', ''));
        this.$router.push({ path: '/status', query: { mission: slug } });
      }

      // --- NEW: HANDLE EVENT LINKS ---
      else if (href && href.startsWith('event://')) {
        event.preventDefault();
        // 1. Get the Event Title from the URL
        const titleRaw = href.replace('event://', '');
        const title = decodeURIComponent(titleRaw);

        // 2. Find the event object
        // Note: We use .trim() to avoid issues with extra spaces
        const targetEvent = this.events.find(e => e.title.trim() === title.trim());

        if (targetEvent) {
          // 3. Switch the view to this event
          console.log("Switching to event:", title);
          this.selectEvent(targetEvent);
          
          // Optional: Scroll back to top of the content area
          const container = document.querySelector('#events-logs .section-content-container');
          if(container) container.scrollTop = 0;
        } else {
          console.warn("Event not found:", title);
          alert(`Error: Event '${title}' not found.`);
        }
      }
    }
  }
};
</script>

<style scoped>
/* Pilots = Gold */
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

/* Missions = Teal */
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

/* Events = Purple (Distinct from Missions) */
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
</style>