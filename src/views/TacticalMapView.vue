<template>
  <div id="tacticalMapView" :class="{ animate: animateView }" :style="{ 'animation-delay': animationDelay }" class="content-container">
    <section id="map-display" :class="{ animate: animate }" class="section-container full-height">
      
      <div class="section-header clipped-medium-backward">
        <img src="/icons/orbital.svg" />
        
        <h1 class="text-tactical-header">TACTICAL MAP</h1>
        
        <div class="label-toggle-container">
            <button 
                @click="toggleLabels" 
                :class="{ 'is-active': showAllLabels }"
                class="toggle-btn clipped-medium-backward" 
            >
                <img src="/icons/factions.svg" alt="Faction Icon" class="toggle-icon" /> 
                
                <span class="toggle-label-text text-tactical-header">
                    {{ showAllLabels ? 'HIDE ALL LABELS' : 'SHOW ALL LABELS' }}
                </span>
            </button>
        </div>
      </div>

      <div class="map-container custom-scroll">
        <div class="map-wrapper" :class="{ 'labels-visible': showAllLabels }">
            <img src="/world_map.webp" class="world-map" alt="Tactical Map" /> 

            <div 
                v-for="loc in localLocations" 
                :key="loc.id"
                class="map-point"
                :style="{ top: loc.y + '%', left: loc.x + '%', '--point-color': loc.color }"
                :class="{ 'is-highlighted': highlightedId === loc.id }"
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
      highlightedId: null,
      showAllLabels: false,
      localLocations: [],
      animationFrameId: null,
    };
  },
  mounted() {
    this.animateView = true;
    this.checkHighlight();
    this.startAnimation();
  },
  beforeUnmount() {
    if (this.animationFrameId) {
        cancelAnimationFrame(this.animationFrameId);
    }
  },
  watch: {
    locations: {
        handler(newVal) {
             // Deep copy to break reference for local mutation
             this.localLocations = JSON.parse(JSON.stringify(newVal));
             this.checkHighlight();
        },
        immediate: true
    }
  },
  methods: {
    checkHighlight() {
        if (this.$route.query.highlight && this.locations.length > 0) {
            this.highlightedId = this.$route.query.highlight;
            
            this.$nextTick(() => {
                const container = this.$el.querySelector('.map-container');
                const target = this.$el.querySelector('.is-highlighted');
                
                if (container && target) {
                    const centerX = target.offsetLeft + (target.offsetWidth / 2);
                    const centerY = target.offsetTop + (target.offsetHeight / 2);
                    
                    container.scrollTo({
                        left: centerX - (container.clientWidth / 2),
                        top: centerY - (container.clientHeight / 2),
                        behavior: 'smooth'
                    });
                }
            });
        }
    },
    toggleLabels() {
      this.showAllLabels = !this.showAllLabels;
    },
    handlePointClick(loc) {
        if (loc.type === 'mission') {
            this.$router.push({ path: '/status', query: { mission: loc.target } });
        } else if (loc.type === 'faction') {
            this.$router.push({ path: '/factions', query: { faction: loc.target } }); 
        }
    },
    startAnimation() {
        const animate = () => {
            let needsUpdate = false;
            
            this.localLocations.forEach(loc => {
                if (loc.isMoving) {
                    const speedX = loc.speedX || 0;
                    const speedY = loc.speedY || 0;

                    if (speedX !== 0) {
                         loc.x += speedX;
                         if (loc.x > 100) loc.x = 0;
                         if (loc.x < 0) loc.x = 100;
                         needsUpdate = true;
                    }

                    if (speedY !== 0) {
                        loc.y += speedY;
                        if (loc.y > 100) loc.y = 0;
                        if (loc.y < 0) loc.y = 100;
                        needsUpdate = true;
                    }
                }
            });

            this.animationFrameId = requestAnimationFrame(animate);
        };
        this.animationFrameId = requestAnimationFrame(animate);
    }
  }
};
</script>

<style scoped>
/* ======================================= */
/* 0. Typography & Shared Headers          */
/* ======================================= */

.text-tactical-header {
    font-family: sans-serif; 
    font-weight: 800;             
    text-transform: uppercase;    
    letter-spacing: 0.15em;       
    color: #ffffff;
    
    /* Default Glow (White/Cyan mix) */
    text-shadow: 0 0 5px rgba(0, 255, 255, 0.5), 
                 0 0 10px rgba(0, 255, 255, 0.3);
    
    margin: 0;
    line-height: 1;
}

h1.text-tactical-header {
    font-size: 2rem; 
    margin-left: 15px;
}

.toggle-btn .text-tactical-header {
    font-size: 1.1rem; 
    cursor: pointer; 
}

/* ======================================= */
/* 1. Structural and General Map Styles    */
/* ======================================= */

.full-height {
    height: 100%;
    display: flex;
    flex-direction: column;
}

.section-header {
    display: flex;
    align-items: center;
    justify-content: flex-start; 
    padding: 10px; 
}

.label-toggle-container {
    margin-left: auto; 
    padding-right: 0; 
}

.map-container {
    flex: 1;
    min-height: 0;
    position: relative;
    overflow: auto;
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
}

.map-wrapper {
    position: relative;
    max-width: none;
    display: inline-block;
    margin: auto;
    animation: map-glitch 20s infinite step-end;
}

.world-map {
    display: block;
    width: 100%;
    height: auto;
    border: 1px solid #333;
    box-shadow: 0 0 20px rgba(0,0,0,0.5);
}

/* ======================================= */
/* 2. Hologram/CRT Effects                 */
/* ======================================= */

#map-display {
    position: relative;
    overflow: hidden;
    animation: flicker 10s infinite alternate; 
}

#map-display::after {
    content: "";
    pointer-events: none;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 50; 
    background: repeating-linear-gradient(
        0deg,
        rgba(0, 0, 0, 0.15), 
        rgba(0, 0, 0, 0.15) 1px, 
        transparent 1px,
        transparent 3px 
    );
    background-size: 100% 3px; 
    opacity: 1; 
}

#map-display::before {
    content: "";
    pointer-events: none;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 51;
    box-shadow: inset 0 0 50px rgba(0, 255, 255, 0.3), 
                inset 0 0 20px rgba(0, 255, 0, 0.2); 
    border-radius: 5%; 
    filter: brightness(1.2); 
}

/* ======================================= */
/* 3. Toggle Button and Label Visibility   */
/* ======================================= */

.toggle-btn {
    background: none;
    border: none; 
    cursor: pointer;
    display: flex; 
    align-items: center;
    gap: 10px; 
    padding: 5px 15px; 
    transition: all 0.2s ease; /* Smooth transition for color/bg */
    border: 1px solid transparent; /* Prevent layout shift if we add border later */
}

.toggle-btn:hover {
    background-color: rgba(255, 255, 255, 0.1); 
}

/* --- UPDATED ACTIVE STATE --- */
.toggle-btn.is-active {
    /* Add a visible background instead of changing text color */
    background-color: rgba(0, 255, 255, 0.2); 
    border: 1px solid rgba(0, 255, 255, 0.3);
}

.toggle-btn.is-active .text-tactical-header {
    /* Keep text WHITE for readability */
    color: #ffffff; 
    
    /* Stronger, tighter glow to show it's "ON" */
    text-shadow: 0 0 8px rgba(0, 255, 255, 1), 
                 0 0 20px rgba(0, 255, 255, 0.6);
}

.toggle-icon {
    height: 24px; 
    width: auto;
    filter: brightness(0) invert(1); 
}

.map-wrapper.labels-visible .map-point .point-label {
    opacity: 1 !important;
    pointer-events: auto;
}

/* ======================================= */
/* 4. Map Points and Labels                */
/* ======================================= */

.map-point {
    position: absolute;
    transform: translate(-50%, -50%);
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
    font-size: 1.2rem;
    white-space: nowrap;
    opacity: 0;
    transition: opacity 0.2s;
    pointer-events: none;
    border: 1px solid var(--point-color, #fff);
}

.map-point:hover .point-label {
    opacity: 1;
}

/* ======================================= */
/* 5. Keyframe Animations                  */
/* ======================================= */

@keyframes pulse {
    0% { transform: scale(1); opacity: 0.6; }
    50% { transform: scale(2); opacity: 0; }
    100% { transform: scale(1); opacity: 0; }
}

@keyframes flicker {
    0%, 100% { opacity: 1; }
    5% { opacity: 0.95; }
    10% { opacity: 1; }
    15% { opacity: 0.9; }
    20% { opacity: 1; }
    25% { opacity: 0.98; }
    30% { opacity: 1; }
}

@keyframes map-glitch {
    0% { transform: translate(0); filter: hue-rotate(0deg) contrast(1); }
    1% { transform: translate(2px, -2px); filter: hue-rotate(5deg) contrast(1.2); }
    2% { transform: translate(-3px, 3px); filter: hue-rotate(15deg) saturate(1.5); }
    2.1% { transform: translate(0); filter: hue-rotate(0deg) contrast(1); }
    3% { transform: translate(1px, 0); }
    3.1% { transform: translate(0); }
    99% { transform: translate(0); filter: hue-rotate(0deg) contrast(1); }
    100% { transform: translate(0); filter: hue-rotate(0deg) contrast(1); }
}

.map-point.is-highlighted .point-core {
    background-color: #fff !important;
    box-shadow: 0 0 10px #fff, 0 0 20px var(--point-color);
    transform: scale(1.5);
    transition: all 0.5s;
}

.map-point.is-highlighted .point-label {
    opacity: 1;
    background: var(--point-color);
    color: black;
    font-weight: bold;
    border: 2px solid white;
    z-index: 100;
}
</style>