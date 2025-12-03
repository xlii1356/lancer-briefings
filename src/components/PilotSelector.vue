<template>
  <div class="pilot-selector">
    <div 
      v-for="pilot in sortedPilots" 
      :key="pilot.id" 
      class="pilot-token"
      :class="{ active: isSelected(pilot.id) }"
      @click="togglePilot(pilot.id)"
    >
      <img :src="pilot.cloud_portrait" :alt="pilot.callsign" />
      <span class="callsign">{{ pilot.callsign }}</span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    pilots: { type: Array, required: true }
  },
  data() {
    return {
      selectedPilotIds: []
    };
  },
  computed: {
    sortedPilots() {
      // Return a new array sorted so selected pilots are first
      return [...this.pilots].sort((a, b) => {
        const aSelected = this.isSelected(a.id);
        const bSelected = this.isSelected(b.id);
        if (aSelected === bSelected) return 0;
        return aSelected ? -1 : 1;
      });
    }
  },
  created() {
    // Load from local storage on startup
    const saved = localStorage.getItem('active_squad_ids');
    if (saved) {
      this.selectedPilotIds = JSON.parse(saved);
    }
  },
  methods: {
    isSelected(id) {
      return this.selectedPilotIds.includes(id);
    },
    togglePilot(id) {
      if (this.isSelected(id)) {
        this.selectedPilotIds = this.selectedPilotIds.filter(pid => pid !== id);
      } else {
        this.selectedPilotIds.push(id);
      }
      // Save to local storage
      localStorage.setItem('active_squad_ids', JSON.stringify(this.selectedPilotIds));
    }
  }
};
</script>

<style scoped>
.pilot-selector {
  display: flex;
  gap: 10px;
  padding: 10px;
  background: rgba(0, 0, 0, 0.3);
  overflow-x: auto;
  min-height: 80px;
  align-items: center;
}

.pilot-token {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  opacity: 0.6;
  filter: grayscale(100%);
  transform: scale(0.9);
}

.pilot-token.active {
  opacity: 1;
  filter: grayscale(0%);
  transform: scale(1.05);
  order: -1; /* Flexbox trick to ensure they visually move to start if sort doesn't catch it immediately */
}

.pilot-token img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 2px solid #555;
  object-fit: cover;
}

.pilot-token.active img {
  border-color: #FFC107; /* Lancer Gold/Yellow */
  box-shadow: 0 0 10px rgba(255, 193, 7, 0.5);
}

.callsign {
  font-size: 0.7rem;
  margin-top: 4px;
  font-family: 'Rubik', sans-serif;
  text-transform: uppercase;
}
</style>