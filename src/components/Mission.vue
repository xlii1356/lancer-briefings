<template>

  <div class="mission" :class="[{ active: isActive }, mission.status]">
    
    <div class="mission-header">
      <div class="name">
        <h1>Mission // {{ mission.slug }}</h1>
        <h2>{{ mission.name }}</h2>
      </div>
      <div class="status" :class="mission.status">
        {{ missionStatus }}
        <img :src="icon" />
      </div>
    </div>

    <div class="squad-container">
      <PilotSelector 
    :pilots="pilots" 
    :mission-id="mission.slug" 
    :locked-squad="lockedSquad" 
      />
    </div>

  </div>
</template>

<script>
import PilotSelector from "@/components/PilotSelector.vue";

export default {
  components: {
    PilotSelector,
  },
  props: {
    mission: {
      type: Object,
      required: true,
    },
    selected: {
      type: String,
      required: true,
    },
    pilots: {
      type: Array,
      required: true,
    },
    lockedSquad: {
      type: Array,
      default: () => null,
      required: false
    }
  },
  computed: {
    icon() {
      return `/icons/mission-${this.mission.status}.svg`;
    },
    missionStatus() {
      if (this.mission.status === "start") return "Current\nBriefing";
      if (this.mission.status === "partial-success") return "Partial\nSuccess";
      if (this.mission.status === "success") return "Mission\nSuccess";
      if (this.mission.status === "failure") return "Mission\nFailure";
      return "";
    },
    isActive() {
      return this.mission.slug === this.selected;
    },
  },
};
</script>

<style scoped>
/* 1. Force the main container to stack vertically */
.mission {
  display: flex !important;
  flex-direction: column !important;
  align-items: stretch !important;
  height: auto !important; /* Allow box to grow */
  padding-bottom: 10px; /* Extra space at bottom */
}

/* 2. Keep the Header (Name + Status) in a horizontal row */
.mission-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

/* 3. Style the Squad Container */
.squad-container {
  width: 100%;
  margin-top: 5px;
  /* Optional: Indent slightly to align with text */
  padding-left: 10px; 
  padding-right: 10px;
}

/* Ensure Name takes up available space in the header row */
.name {
  flex-grow: 1;
}
</style>