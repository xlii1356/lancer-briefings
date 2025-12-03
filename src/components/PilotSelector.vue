<template>
  <div class="pilot-selector" :class="{ 'is-locked': isLocked }">
    <div 
      v-for="pilot in sortedPilots" 
      :key="pilot.callsign" 
      class="pilot-token"
      :class="{ active: isSelected(pilot.callsign) }"
      @click.stop="togglePilot(pilot.callsign)"
    >
      <div class="image-wrapper">
        <img :src="pilot.cloud_portrait" :alt="pilot.callsign" />
        <div v-if="isLocked && isSelected(pilot.callsign)" class="lock-indicator">
          <i class="fas fa-lock"></i>
        </div>
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
    missionId: {
      type: String,
      required: true
    },
    lockedSquad: {
      type: Array,
      default: () => null,
      required: false
    }
  },
  data() {
    return {
      selectedCallsigns: []
    };
  },
  computed: {
    storageKey() {
      return `squad_selection_${this.missionId}`;
    },
    isLocked() {
      // Returns true if this mission is controlled by the JSON file
      return this.lockedSquad && this.lockedSquad.length > 0;
    },
    sortedPilots() {
      return [...this.pilots].sort((a, b) => {
        const aSelected = this.isSelected(a.callsign);
        const bSelected = this.isSelected(b.callsign);
        
        // If both selected or both unselected, sort alphabetically or keep order
        if (aSelected === bSelected) return 0;
        
        // Selected pilots move to the front (-1)
        return aSelected ? -1 : 1;
      });
    }
  },
  watch: {
    // If the mission or the JSON data changes, reload the state
    missionId: 'loadSelection',
    lockedSquad: 'loadSelection'
  },
  mounted() {
    this.loadSelection();
  },
  methods: {
    isSelected(callsign) {
      return this.selectedCallsigns.includes(callsign);
    },
    loadSelection() {
      // PRIORITY 1: Check if this mission has a hard-coded squad in JSON
      if (this.isLocked) {
        // Clone the array to avoid reference issues
        this.selectedCallsigns = [...this.lockedSquad];
        return; 
      }

      // PRIORITY 2: Check Local Storage (User preferences)
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
      // If locked via JSON, do not allow user changes
      if (this.isLocked) return;

      if (this.isSelected(callsign)) {
        this.selectedCallsigns = this.selectedCallsigns.filter(c => c !== callsign);
      } else {
        this.selectedCallsigns.push(callsign);
      }
      
      // Save the user's choice to browser memory
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
  padding: 8px 5px;
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

/* Change cursor if the list is locked vs editable */
.pilot-selector.is-locked .pilot-token {
  cursor: default;
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
  width: 45px; 
}

/* HOVER STATE (Only if not locked) */
.pilot-selector:not(.is-locked) .pilot-token:hover {
  opacity: 0.8;
  transform: scale(1.0);
}

/* ACTIVE (SELECTED) STATE */
.pilot-token.active {
  opacity: 1;
  filter: grayscale(0%);
  transform: scale(1.05);
  order: -1; /* Flexbox sorting visual helper */
}

.image-wrapper {
  position: relative;
  width: 35px;
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
  border-color: #FFC107; /* Lancer Gold */
  box-shadow: 0 0 5px rgba(255, 193, 7, 0.6);
}

.lock-indicator {
  position: absolute;
  bottom: -2px;
  right: -2px;
  font-size: 8px;
  color: #FFC107;
  background: rgba(0,0,0,0.8);
  border-radius: 50%;
  padding: 2px;
}

.callsign {
  font-size: 0.5rem;
  margin-top: 3px;
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