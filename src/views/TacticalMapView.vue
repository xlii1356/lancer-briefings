<template>
  <div id="tacticalMapView" :class="{ animate: animateView }" :style="{ 'animation-delay': animationDelay }" class="content-container">
    <section id="map-display" :class="{ animate: animate }" class="section-container full-height">
      <div class="section-header clipped-medium-backward">
        <img src="/icons/orbital.svg" />
        <h1>TACTICAL MAP</h1>
        
        <div class="label-toggle-container">
            <button 
                @click="toggleLabels" 
                :class="{ 'is-active': showAllLabels }"
                class="toggle-btn clipped-medium-backward" 
            >
                <img src="/icons/factions.svg" alt="Faction Icon" class="toggle-icon" /> 
                <span class="toggle-label-text">
                    {{ showAllLabels ? 'HIDE ALL LABELS' : 'SHOW ALL LABELS' }}
                </span>
            </button>
        </div>
        </div>

<div class="map-container custom-scroll">
<div class="map-wrapper" :class="{ 'labels-visible': showAllLabels }">
<img src="/world_map.webp" class="world-map" alt="Tactical Map" /> 

<div 
v-for="loc in locations" 
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
    };
  },
  mounted() {
    this.animateView = true;
    if (this.$route.query.highlight) {
        this.highlightedId = this.$route.query.highlight;
        
        this.$nextTick(() => {
            const container = this.$el.querySelector('.map-container');
            const target = this.$el.querySelector('.is-highlighted');
            
            if (container && target) {
                // Calculate scroll position to center the target
                // We use offsetLeft/Top which are relative to the map-wrapper
                // We want that position to be in the middle of the container
                
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
  methods: {
    toggleLabels() {
      this.showAllLabels = !this.showAllLabels;
    },
    handlePointClick(loc) {
        if (loc.type === 'mission') {
            this.$router.push({ path: '/status', query: { mission: loc.target } });
        } else if (loc.type === 'faction') {
            this.$router.push({ path: '/factions', query: { faction: loc.target } }); 
        }
    }
  }
};
</script>


<style scoped>
/* ======================================= */
/* 1. Structural and General Map Styles */
/* ======================================= */

.full-height {
    height: 100%;
    display: flex;
    flex-direction: column;
}

/* Header Adjustments for Toggle Button */
.section-header {
    display: flex;
    align-items: center;
    justify-content: flex-start; /* Ensure elements flow left-to-right */
}

/* Position the toggle button group to the far right */
.label-toggle-container {
    margin-left: auto; /* Pushes it to the far right */
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
    /* Glitch Animation applied here */
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
/* 2. Hologram/CRT Effects */
/* ======================================= */

/* 1. Container for the flicker effect */
#map-display {
    position: relative;
    overflow: hidden;
    animation: flicker 10s infinite alternate; /* Gentle overall flicker */
}

/* 2. Scan Lines (Subtle Look) */
#map-display::after {
    content: "";
    pointer-events: none;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 50; /* Ensure it is on top of the map content */

    /* Very subtle, thin lines (1px dark, 2px transparent gap) */
    background: repeating-linear-gradient(
        0deg,
        rgba(0, 0, 0, 0.15), /* Subtle dark line start */
        rgba(0, 0, 0, 0.15) 1px, /* Dark line ends at 1px */
        transparent 1px,
        transparent 3px /* Total height of the pattern is 3px */
    );
    
    background-size: 100% 3px; 
    opacity: 1; /* Let the gradient colors handle the subtlety */
}

/* 3. Screen Glow/Curvature */
#map-display::before {
    content: "";
    pointer-events: none;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 51;
    
    /* Subtle screen glow/bloom */
    box-shadow: inset 0 0 50px rgba(0, 255, 255, 0.3), 
                inset 0 0 20px rgba(0, 255, 0, 0.2); 
    
    /* Simulating CRT screen curvature */
    border-radius: 5%; 
    filter: brightness(1.2); 
}

/* ======================================= */
/* 3. Toggle Button and Label Visibility */
/* ======================================= */

/* Style the button container to look like header text */
.toggle-btn {
    background: none;
    border: none; /* Remove default button border */
    color: white;
    cursor: pointer;
    
    /* Make the button content display like a row */
    display: flex; 
    align-items: center;
    gap: 8px; /* Space between icon and text */
    
    /* Font styling to match the header's H1/H2 */
    font-size: 1.1rem; 
    font-weight: bold;
    letter-spacing: 0.15em; 
    
    padding: 0 10px; 
    transition: background-color 0.2s;
}

.toggle-btn:hover {
    background-color: rgba(255, 255, 255, 0.05); /* Subtle hover effect */
}

.toggle-btn.is-active {
    background-color: rgba(0, 255, 255, 0.1); 
    color: var(--primary-color, #00ffff);
}

.toggle-icon {
    height: 20px; 
    width: auto;
    filter: brightness(0) invert(1); /* Assume SVG is black and needs to be white */
}

/* Force all labels visible when the toggle class is active */
.map-wrapper.labels-visible .map-point .point-label {
    opacity: 1 !important;
    pointer-events: auto;
}

/* ======================================= */
/* 4. Map Points and Labels */
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
    /* Updated for larger size */
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
/* 5. Keyframe Animations */
/* ======================================= */

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

/* Gentle brightness flicker for the whole display */
@keyframes flicker {
    0%, 100% { opacity: 1; }
    5% { opacity: 0.95; }
    10% { opacity: 1; }
    15% { opacity: 0.9; }
    20% { opacity: 1; }
    25% { opacity: 0.98; }
    30% { opacity: 1; }
}

/* Position/Color glitch for the map content */
@keyframes map-glitch {
    0% {
        transform: translate(0);
        filter: hue-rotate(0deg) contrast(1);
    }
    1% {
        transform: translate(2px, -2px);
        filter: hue-rotate(5deg) contrast(1.2);
    }
    2% {
        transform: translate(-3px, 3px);
        filter: hue-rotate(15deg) saturate(1.5);
    }
    2.1% {
        transform: translate(0);
        filter: hue-rotate(0deg) contrast(1);
    }
    3% {
        transform: translate(1px, 0);
    }
    3.1% {
        transform: translate(0);
    }
    99% {
        transform: translate(0);
        filter: hue-rotate(0deg) contrast(1);
    }
    100% {
        transform: translate(0);
        filter: hue-rotate(0deg) contrast(1);
    }
}

/* Existing highlight styles (copied for completeness) */
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