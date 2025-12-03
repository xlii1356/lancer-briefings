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
      return this.lockedSquad && this.lockedSquad.length > 0;
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
  watch: {
    missionId: 'loadSelection',
    lockedSquad: 'loadSelection'
  },
  mounted() {
    this.loadSelection();
  },
  methods: {
    // --- FIX START ---
    isSelected(callsign) {
      // Compare both strings in Uppercase so "Reiko" matches "REIKO"
      return this.selectedCallsigns.some(c => c.toUpperCase() === callsign.toUpperCase());
    },
    // --- FIX END ---

    loadSelection() {
      if (this.isLocked) {
        this.selectedCallsigns = [...this.lockedSquad];
        return; 
      }

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
      if (this.isLocked) return;

      if (this.isSelected(callsign)) {
        // Remove pilot (Case insensitive filter)
        this.selectedCallsigns = this.selectedCallsigns.filter(c => c.toUpperCase() !== callsign.toUpperCase());
      } else {
        this.selectedCallsigns.push(callsign);
      }
      
      localStorage.setItem(this.storageKey, JSON.stringify(this.selectedCallsigns));
    }
  }
};
</script>

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

<style scoped>
/* Same CSS as before */
.pilot-selector {
  display: flex;
  flex-wrap: nowrap;
  gap: 8px;
  padding: 8px 5px;
  margin-top: 5px;
  overflow-x: auto;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  
  /* Scrollbar hiding logic */
  scrollbar-width: none; 
  -ms-overflow-style: none;
}
.pilot-selector::-webkit-scrollbar { 
  display: none; 
}

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
  flex-shrink: 0;
  width: 45px; 
}

.pilot-selector:not(.is-locked) .pilot-token:hover {
  opacity: 0.8;
  transform: scale(1.0);
}

.pilot-token.active {
  opacity: 1;
  filter: grayscale(0%);
  transform: scale(1.05);
  order: -1; 
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
  border-color: #FFC107;
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