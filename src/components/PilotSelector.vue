<template>
  <div class="pilot-selector" v-if="visiblePilots.length > 0">
    <div 
      v-for="pilot in visiblePilots" 
      :key="pilot.callsign" 
      class="pilot-token"
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
    // The list of strings ["Reiko", "Merlin"] from your squads.json
    lockedSquad: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    visiblePilots() {
      // If no squad is defined in JSON, show nothing
      if (!this.lockedSquad || this.lockedSquad.length === 0) return [];

      // Map the text names from JSON to the actual Pilot Objects
      // This preserves the order defined in your JSON file
      return this.lockedSquad.map(squadName => {
        return this.pilots.find(p => p.callsign.toUpperCase() === squadName.toUpperCase());
      }).filter(p => p); // Filter out undefined if a name in JSON doesn't match any pilot
    }
  }
};
</script>

<style scoped>
.pilot-selector {
  display: flex;
  flex-wrap: nowrap;
  gap: 12px;
  padding: 8px 10px;
  margin-top: 5px;
  overflow-x: auto;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
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
  /* Removed cursor: pointer since they aren't clickable */
  cursor: default;
  transition: transform 0.2s ease;
  flex-shrink: 0;
  width: 50px; 
}

/* Optional: Slight hover effect just to show it's interactive UI */
.pilot-token:hover {
  transform: scale(1.05);
}

.image-wrapper {
  position: relative;
  width: 40px; 
  height: 40px;
}

.pilot-token img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  /* Gold border to indicate they are the "Active" squad */
  border: 2px solid #FFC107; 
  box-shadow: 0 0 5px rgba(255, 193, 7, 0.4);
}

.callsign {
  font-size: 0.6rem;
  margin-top: 4px;
  font-family: 'Rubik', sans-serif;
  text-transform: uppercase;
  text-align: center;
  font-weight: bold;
  letter-spacing: 0.5px;
  color: white; /* White text since these are always active */
  text-shadow: 0 0 2px black;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}
</style>