// In src/components/PilotSelector.vue

export default {
  name: "PilotSelector",
  props: {
    pilots: { type: Array, required: true },
    missionId: { type: String, required: true },
    
    // NEW PROP
    lockedSquad: {
      type: Array,
      default: () => null
    }
  },
  // ... data ...
  methods: {
    // ... isSelected ...

    loadSelection() {
      // 1. CHECK FOR JSON LOCK FIRST
      if (this.lockedSquad && this.lockedSquad.length > 0) {
        this.selectedCallsigns = this.lockedSquad;
        return; 
      }

      // 2. FALLBACK TO LOCAL STORAGE
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
      // OPTIONAL: Prevent editing if it comes from the JSON file
      if (this.lockedSquad) return; 

      if (this.isSelected(callsign)) {
        this.selectedCallsigns = this.selectedCallsigns.filter(c => c !== callsign);
      } else {
        this.selectedCallsigns.push(callsign);
      }
      localStorage.setItem(this.storageKey, JSON.stringify(this.selectedCallsigns));
    }
  }
};