<template>
  <div class="mission" :class="[{ active: isActive }, mission.status]">
    <div class="name">
      <h1>Mission // {{ mission.slug }}</h1>
      <h2>{{ mission.name }}</h2>
    </div>
    
    <div class="squad-container">
      <PilotSelector :pilots="pilots" :mission-id="mission.slug" />
    </div>

    <div class="status" :class="mission.status">
      {{ missionStatus }}
      <img :src="icon" />
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
    // New Prop to receive pilot data
    pilots: {
      type: Array,
      required: true,
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
/* Optional: Ensure the selector doesn't break the layout */
.squad-container {
  width: 100%;
  margin-top: 5px;
  margin-bottom: 5px;
}
</style>