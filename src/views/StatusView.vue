<template>
  <div id="status" :class="{ animate: animateView }" :style="{ 'animation-delay': animationDelay }"
    class="content-container">
    <section id="missions" class="section-container" :style="{ 'animation-delay': animationDelay }">
      <div class="section-header clipped-medium-backward">
        <img src="/icons/campaign.svg" />
        <h1>Mission Log</h1>
      </div>
      <div class="section-content-container">
        <div class="mission-list-container">
          <Mission v-for="item in missions" :key="item.slug" :mission="item" :selected="missionSlug"
            @click="selectMission(item.slug)" />
        </div>
      </div>
    </section>
    <section id="assignment" class="section-container" :style="{ 'animation-delay': animationDelay }">
      <div class="section-header clipped-medium-backward">
        <img src="/icons/deployable.svg" />
        <h1>Current Assignment</h1>
      </div>
      <div class="section-content-container">
        <vue-markdown-it :source="missionMarkdown" class="markdown" />
      </div>
    </section>
    <div>
      <section id="reserves" class="section-container" :style="{ 'animation-delay': animationDelay }">
        <div class="section-header clipped-medium-backward">
          <img src="/icons/squad.svg" />
          <h1>Reserves</h1>
        </div>
        <div class="section-content-container">
          <div class="reserves-list-container">
            <Reserve v-for="item in reserves" :key="item.name" :reserve="item" :pilots="pilots"
              v-if="item.name !== 'Skill Point'" />
          </div>
        </div>
      </section>
      
      <section id="prime-status" class="section-container" :style="{ 'animation-delay': animationDelay }">
        <div class="section-header clipped-medium-backward">
          <img src="/icons/reflection.svg" />
          <h1>PRIME STATUS</h1>
          <div class="edit-toggle" @click="statusEditMode = !statusEditMode">
            <span v-if="!statusEditMode">⚙️ EDIT</span>
            <span v-else>💾 SAVE</span>
          </div>
        </div>
        <div class="section-content-container">
          
          <div v-if="!statusEditMode" class="status-list-container">
            <div v-if="primeStatuses.length === 0" class="empty-state">
              NO ACTIVE STATUSES
            </div>
            <div v-for="(status, index) in primeStatuses" :key="index" class="status-row">
              <div class="status-name">{{ status.name.toUpperCase() }}</div>
              <div class="dots-spacer"></div>
              <div class="status-condition">
                <span class="chip status-chip">{{ status.condition.toUpperCase() }}</span>
              </div>
            </div>
          </div>

          <div v-else class="status-edit-container">
            <div class="add-status-row">
              <input v-model="newStatusName" placeholder="Name (e.g. Gorgon)" @keyup.enter="addStatus" />
              <input v-model="newStatusCondition" placeholder="Condition (e.g. STUNNED)" @keyup.enter="addStatus" />
              <button class="btn-add" @click="addStatus">+</button>
            </div>
            <div class="edit-list">
              <div v-for="(status, index) in primeStatuses" :key="index" class="edit-item">
                <span>{{ status.name }} : {{ status.condition }}</span>
                <button class="btn-delete" @click="removeStatus(index)">×</button>
              </div>
            </div>
          </div>

        </div>
      </section>
    </div>
  </div>
</template>

<script>
import { VueMarkdownIt } from '@f3ve/vue-markdown-it';
import Mission from "@/components/Mission.vue";
import Event from "@/components/Event.vue";
// Clock is no longer used, but import kept if you revert later
// import Clock from "@/components/Clock.vue"; 
import Reserve from "@/components/Reserve.vue";

export default {
  components: {
    VueMarkdownIt,
    Mission,
    Event,
    // Clock,
    Reserve,
  },
  props: {
    animate: { type: Boolean, required: true },
    initialSlug: { type: String, required: true },
    missions: { type: Array, required: true },
    events: { type: Array, required: true },
    pilots: { type: Array, required: true },
    clocks: { type: Array, required: true },
    reserves: { type: Array, required: true },
  },
  data() {
    return {
      missionSlug: this.initialSlug,
      animateView: this.animate,
      animationDelay: "1.75s",
      missionMarkdown: "",
      
      // Prime Status Data
      statusEditMode: false,
      newStatusName: "",
      newStatusCondition: "",
      primeStatuses: [] 
    };
  },
  created() {
    this.setAnimate();
    // Load saved statuses from local storage if available
    const savedStatuses = localStorage.getItem('lancer-prime-statuses');
    if (savedStatuses) {
      this.primeStatuses = JSON.parse(savedStatuses);
    }
  },
  beforeUpdate() {
    this.selectMission(this.missionSlug);
  },
  mounted() {
    if (this.missions.length > 0) {
      this.selectMission(this.missions[0].slug);
    }
  },
  methods: {
    selectMission(slug) {
      this.missionSlug = slug;
      let m = this.missions.find(x => x.slug === this.missionSlug);
      if(m) this.missionMarkdown = m.content;
    },
    setAnimate() {
      if (this.animate) {
        this.animateView = true;
      }
      let statusAnimated = window.sessionStorage.getItem("statusAnimated");
      if (statusAnimated) {
        this.animationDelay = "0s";
      }
      if (statusAnimated === null) {
        window.sessionStorage.setItem("statusAnimated", true);
      }
    },
    
    // --- Prime Status Methods ---
    addStatus() {
      if (this.newStatusName && this.newStatusCondition) {
        this.primeStatuses.push({
          name: this.newStatusName,
          condition: this.newStatusCondition
        });
        this.newStatusName = "";
        this.newStatusCondition = "";
        this.saveStatuses();
      }
    },
    removeStatus(index) {
      this.primeStatuses.splice(index, 1);
      this.saveStatuses();
    },
    saveStatuses() {
      localStorage.setItem('lancer-prime-statuses', JSON.stringify(this.primeStatuses));
    }
  },
};
</script>

<style scoped>
/* Prime Status Specific Styles */
#prime-status .section-header {
  display: flex;
  align-items: center;
}

.edit-toggle {
  margin-left: auto;
  font-size: 0.8rem;
  opacity: 0.7;
  cursor: pointer;
  padding-right: 15px;
  font-weight: bold;
  letter-spacing: 1px;
}
.edit-toggle:hover {
  opacity: 1;
  color: #FFC107;
}

.status-list-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px;
}

.empty-state {
  text-align: center;
  opacity: 0.5;
  font-style: italic;
  padding: 20px;
}

.status-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px dashed rgba(255, 255, 255, 0.2);
  padding-bottom: 5px;
}

.status-name {
  font-weight: bold;
  font-size: 1.1em;
  color: #fff;
}

.dots-spacer {
  flex-grow: 1;
  margin: 0 10px;
  border-bottom: 1px dotted #444;
  height: 12px;
  opacity: 0.3;
}

.chip.status-chip {
  background: #C70000; /* Lancer Red */
  color: white;
  padding: 2px 8px;
  border-radius: 2px;
  font-weight: 700;
  font-size: 0.9em;
  letter-spacing: 1px;
  text-shadow: 1px 1px 2px black;
}

/* Edit Mode Styles */
.status-edit-container {
  padding: 10px;
  background: rgba(0, 0, 0, 0.2);
}

.add-status-row {
  display: flex;
  gap: 5px;
  margin-bottom: 15px;
}

input {
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid #555;
  color: white;
  padding: 8px;
  flex-grow: 1;
  font-family: inherit;
  width: 40%;
}
input:focus {
  outline: none;
  border-color: #FFC107;
}

button {
  cursor: pointer;
  background: #333;
  color: white;
  border: 1px solid #555;
  font-weight: bold;
  transition: all 0.2s;
}

.btn-add {
  background: #2E7D32;
  width: 40px;
}
.btn-add:hover { background: #388E3C; }

.btn-delete {
  background: #C62828;
  padding: 2px 8px;
  font-size: 1.2em;
  line-height: 1em;
}
.btn-delete:hover { background: #D32F2F; }

.edit-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  border-bottom: 1px solid #333;
  background: rgba(255,255,255,0.05);
}
.edit-item:nth-child(even) {
  background: rgba(255,255,255,0.02);
}
</style>