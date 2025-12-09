<template>
  <div id="tacticalMapView" :class="{ animate: animateView }" :style="{ 'animation-delay': animationDelay }" class="content-container">
    <section id="map-display" :class="{ animate: animate }" class="section-container full-height">
      <div class="section-header clipped-medium-backward">
        <img src="/icons/orbital.svg" />
        <h1>TACTICAL MAP</h1>
      </div>
      
      <div class="map-container custom-scroll">
          <div class="map-wrapper">
              <img src="/world_map.webp" class="world-map" alt="Tactical Map" />
              
              <div 
                v-for="loc in locations" 
                :key="loc.id"
                class="map-point"
                :style="{ top: loc.y + '%', left: loc.x + '%', '--point-color': loc.color }"
                @click="handlePointClick(loc)"
              >
                <div class="point-glow"></div>
                <div class="point-core"></div>
                <div class="point-label">{{ loc.label }}</div>
              </div>
          </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: "TacticalMapView",
  props: {
    animate: { type: Boolean, required: true },
    locations: { type: Array, required: true, default: () => [] },
  },
  data() {
    return {
      animateView: false,
      animationDelay: "0s",
    };
  },
  mounted() {
    this.animateView = true;
  },
  methods: {
    handlePointClick(loc) {
        if (loc.type === 'mission') {
            this.$router.push({ path: '/status', query: { mission: loc.target } });
        } else if (loc.type === 'faction') {
            // Need to trigger faction modal opening via query param or event?
            // The FactionsView handles "selection" internally.
            // If we route to /factions, we might need to pass a query param to auto-open.
            // For now, let's just route to factions.
            // Future improvement: Support query param selection on FactionsView.
            this.$router.push({ path: '/factions' }); 
            // NOTE: The user asked to "link to Missions or Factions". 
            // Linking to a specific Faction modal from here requires FactionsView to support it.
            // I will implement basic routing first.
        }
    }
  }
};
</script>



<style scoped>
.full-height {
    height: 100%;
    display: flex;
    flex-direction: column;
}

.map-container {
    flex: 1;
    min-height: 0; /* Crucial for nested flex scrolling */
    position: relative;
    overflow: auto; /* Allow scrolling if map is large */
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    /* justify-content: center; align-items: center;  <-- REMOVED: Causes clipping on overflow */
}

.map-wrapper {
    position: relative;
    max-width: none; 
    display: inline-block;
    margin: auto; /* Centers content when smaller than container, safe when larger */
}

.world-map {
    display: block;
    max-width: none; /* Allow native size */
    min-width: 100%; /* Ensure it fills at least the container */
    height: auto;
    border: 1px solid #333;
    box-shadow: 0 0 20px rgba(0,0,0,0.5);
}

.map-point {
    position: absolute;
    transform: translate(-50%, -50%); /* Center on coordinates */
    cursor: pointer;
    z-index: 10;
    width: 20px;
    height: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.point-core {
    width: 8px;
    height: 8px;
    background-color: var(--point-color, #fff);
    border-radius: 50%;
    z-index: 2;
}

.point-glow {
    position: absolute;
    width: 100%;
    height: 100%;
    background-color: var(--point-color, #fff);
    border-radius: 50%;
    opacity: 0.6;
    animation: pulse 2s infinite;
    z-index: 1;
}

.point-label {
    position: absolute;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.8);
    color: var(--point-color, #fff);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.8rem;
    white-space: nowrap;
    opacity: 0;
    transition: opacity 0.2s;
    pointer-events: none;
    border: 1px solid var(--point-color, #fff);
}

.map-point:hover .point-label {
    opacity: 1;
}

@keyframes pulse {
    0% {
        transform: scale(1);
        opacity: 0.6;
    }
    50% {
        transform: scale(2);
        opacity: 0;
    }
    100% {
        transform: scale(1);
        opacity: 0;
    }
}
</style>
