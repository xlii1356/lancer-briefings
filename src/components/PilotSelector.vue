<template>
  <div class="pilot-selector">
    <div 
      v-for="pilot in sortedPilots" 
      :key="pilot.callsign" 
      class="pilot-token"
      :class="{ active: isSelected(pilot.callsign) }"
      @click.stop="togglePilot(pilot.callsign)"
    >
      <div class="image-wrapper">
        <img :src="pilot.cloud_portrait" :alt="pilot.callsign" />
      </div>
      <span class="callsign">{{ pilot.callsign }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "PilotSelector",
  props: {
    pilots: {
      type: Array,
      required: true
    },
    // New Prop: Ensures storage is unique per mission
    missionId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      selectedCallsigns: []
    };
  },
  computed: {
    storageKey() {
      // Creates a unique ID like "squad_mission-1", "squad_mission-2"
      return `squad_selection_${this.missionId}`;
    },
    sortedPilots() {
      return [...this.pilots].sort((a, b) => {
        const aSelected = this.isSelected(a.callsign);
        const bSelected = this.isSelected(b.callsign);
        
        if (aSelected === bSelected) return 0;
        return aSelected ? -1 : 1;
      });
    }
  },
  mounted() {
    this.loadSelection();
  },
  watch: {
    // If the mission changes (unlikely inside a v-for, but safe to have), reload
    missionId() {
      this.loadSelection();
    }
  },
  methods: {
    isSelected(callsign) {
      return this.selectedCallsigns.includes(callsign);
    },
    loadSelection() {
      const saved = localStorage.getItem(this.storageKey);
      if (saved) {
        try {
          this.selectedCallsigns = JSON.parse(saved);
        } catch (e) {
          this.selectedCallsigns = [];
        }
      } else {
        this.selectedCallsigns = [];
      }
    },
    togglePilot(callsign) {
      if (this.isSelected(callsign)) {
        this.selectedCallsigns = this.selectedCallsigns.filter(c => c !== callsign);
      } else {
        this.selectedCallsigns.push(callsign);
      }
      localStorage.setItem(this.storageKey, JSON.stringify(this.selectedCallsigns));
    }
  }
};
</script>

<style scoped>
.pilot-selector {
  display: flex;
  flex-wrap: nowrap; /* Keep them in a single row */
  gap: 8px;
  padding: 5px 0;
  margin-top: 5px;
  overflow-x: auto; /* Allow scrolling if too many pilots */
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  /* Hide scrollbar for cleanliness */
  scrollbar-width: none; 
  -ms-overflow-style: none;
}
.pilot-selector::-webkit-scrollbar { 
  display: none; 
}

.pilot-token {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.4s ease;
  opacity: 0.4;
  filter: grayscale(100%);
  transform: scale(0.9);
  flex-shrink: 0; /* Prevent squishing */
  width: 45px; /* Smaller for the list view */
}

/* HOVER STATE */
.pilot-token:hover {
  opacity: 0.8;
  transform: scale(1.0);
}

/* ACTIVE (SELECTED) STATE */
.pilot-token.active {
  opacity: 1;
  filter: grayscale(0%);
  transform: scale(1.05);
  order: -1; 
}

.image-wrapper {
  position: relative;
  width: 35px; /* Compact Size */
  height: 35px;
}

.pilot-token img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid #555;
  object-fit: cover;
  transition: border-color 0.3s;
}

.pilot-token.active img {
  border-color: #FFC107; 
  box-shadow: 0 0 5px rgba(255, 193, 7, 0.6);
}

.callsign {
  font-size: 0.5rem; /* Tiny text for compact view */
  margin-top: 2px;
  font-family: 'Rubik', sans-serif;
  text-transform: uppercase;
  text-align: center;
  font-weight: bold;
  letter-spacing: 0.5px;
  color: #aaa;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.pilot-token.active .callsign {
  color: white;
}
</style>