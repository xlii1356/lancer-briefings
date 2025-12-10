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
/* 0. Typography & Shared Headers          */
/* ======================================= */

/* This class applies to both the H1 and the Button Text 
   to ensure identical formatting (font, weight, glow).
*/
.text-tactical-header {
    /* Replace 'sans-serif' with your specific font like 'Orbitron' or 'Rajdhani' if you have one imported */
    font-family: sans-serif; 
    font-weight: 800;             /* Extra Bold */
    text-transform: uppercase;    /* All Caps */
    letter-spacing: 0.15em;       /* Wide "Tactical" spacing */
    color: #ffffff;
    
    /* Cyberpunk text glow */
    text-shadow: 0 0 5px rgba(0, 255, 255, 0.5), 
                 0 0 10px rgba(0, 255, 255, 0.3);
    
    margin: 0;
    line-height: 1;
}

/* Specific sizing for the Main H1 */
h1.text-tactical-header {
    font-size: 2rem; 
    margin-left: 15px; /* Spacing between the Orbital Icon and the Text */
}

/* Specific sizing for the Button Text (Smaller than H1, but same style) */
.toggle-btn .text-tactical-header {
    font-size: 1.1rem; 
    cursor: pointer; /* Ensures text acts like a button */
}

/* ======================================= */
/* 1. Structural and General Map Styles    */
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
    padding: 10px; /* Added padding for breathing room */
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
/* 2. Hologram/CRT Effects                 */
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
/* 3. Toggle Button and Label Visibility   */
/* ======================================= */

/* Style the button container to look like header text */
.toggle-btn {
    background: none;
    border: none; /* Remove default button border */
    /* Color and Font settings moved to .text-tactical-header */
    cursor: pointer;
    
    /* Make the button content display like a row */
    display: flex; 
    align-items: center;
    gap: 10px; /* Space between icon and text */
    
    padding: 5px 15px; /* Added padding for better hit area */
    transition: background-color 0.2s;
}

.toggle-btn:hover {
    background-color: rgba(255, 255, 255, 0.1); /* Subtle hover effect */
}

/* Active State: Make the text glow brighter */
.toggle-btn.is-active .text-tactical-header {
    color: var(--primary-color, #00ffff);
    text-shadow: 0 0 8px rgba(0, 255, 255, 0.8);
}

.toggle-icon {
    height: 24px; /* Slightly larger to match header feel */
    width: auto;
    filter: brightness(0) invert(1); /* Assume SVG is black and needs to be white */
}

/* Force all labels visible when the toggle class is active */
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
/* 5. Keyframe Animations                  */
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

/* Existing highlight styles */
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