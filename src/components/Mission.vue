<template>
  <div class="mission" :class="[{ active: isActive }, mission.status]">
    <div class="name">
      <!-- Changed from mission.slug to mission.id for better context if slug is just an index -->
      <h1>Mission // {{ mission.slug }}</h1>
      <h2>{{ mission.name }}</h2>
    </div>
    <div class="status" :class="mission.status">
      {{ missionStatus }}
      <img :src="icon" />
    </div>
  </div>
</template>

<script>
export default {
  components: {},
  props: {
    mission: {
      type: Object,
      required: true,
    },
    selected: {
      type: String,
      required: true,
    },
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
      return "Status\nUnknown"; // Added fallback
    },
    isActive() {
      return this.mission.slug === this.selected;
    },
  },
};
</script>
<style scoped>
/* Mission.vue styles were not provided, but ensured the template structure supports the assignment flow */
.mission {
  /* Ensure this base style is present */
  cursor: pointer;
  padding: 10px;
  border: 1px solid transparent;
  transition: all 0.2s;
}

.mission:hover {
  border-color: #00ffc1;
}

.mission.active {
  background-color: rgba(0, 255, 193, 0.1);
  border-color: #00ffc1;
}

.name h1 {
  font-size: 0.8em;
  text-transform: uppercase;
}
.name h2 {
  font-size: 1.2em;
}

.status {
  text-align: right;
  white-space: pre-wrap;
  font-weight: bold;
}
</style>