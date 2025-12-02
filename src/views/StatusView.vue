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
          <img src="/icons/protocol.svg" /> <h1>PRIME STATUS</h1>
          
          <div class="edit-toggle" @click="toggleEditMode">
            <span v-if="!editMode" class="edit-btn">⚙️ EDIT</span>
            <span v-else class="save-btn">💾 SAVE</span>
          </div>
        </div>

        <div class="section-content-container">
          
          <div v-if="!editMode" class="status-list-container">
            <div v-if="primeStatuses.length === 0" class="empty-state">
              SYSTEM NORMAL // NO ACTIVE STATUSES
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
              <input v-model="newName" placeholder="Name (e.g. Gorgon)" @keyup.enter="addStatus" />
              <input v-model="newCondition" placeholder="Status (e.g. STUNNED)" @keyup.enter="addStatus" />
              <button class="btn-add" @click="addStatus">+</button>
            </div>
            
            <div class="edit-list">
              <div v-for="(status, index) in primeStatuses" :key="index" class="edit-item">
                <span class="edit-text">{{ status.name }} : {{ status.condition }}</span>
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
import Reserve from "@/components/Reserve.vue";
// Note: We removed the import for Clock.vue

// Optional: Import your clocks.json if you want to use it for DEFAULT statuses
import defaultStatuses from '@/assets/clocks/clocks.json';

export default {
  components: {
    VueMarkdownIt,
    Mission,
    Event,
    Reserve,
  },
  props: {
    animate: { type: Boolean, required: true },
    initialSlug: { type: String, required: true },
    missions: { type: Array, required: true },
    events: { type: Array, required: true },
    pilots: { type: Array, required: true },
    clocks: { type: Array, required: true }, // Kept to prevent errors, but unused
    reserves: { type: Array, required: true },
  },
  data() {
    return {
      missionSlug: this.initialSlug,
      animateView: this.animate,
      animationDelay: "1.75s",
      missionMarkdown: "",

      // PRIME STATUS DATA
      editMode: false,
      newName: "",
      newCondition: "",
      primeStatuses: [] 
    };
  },
  created() {
    this.setAnimate();
    this.loadStatuses();
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
      if (m) this.missionMarkdown = m.content;
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
    
    // --- PRIME STATUS METHODS ---
    toggleEditMode() {
      this.editMode = !this.editMode;
    },
    addStatus() {
      if (this.newName && this.newCondition) {
        this.primeStatuses.push({
          name: this.newName,
          condition: this.newCondition
        });
        this.newName = "";
        this.newCondition = "";
        this.saveStatuses();
      }
    },
    removeStatus(index) {
      this.primeStatuses.splice(index, 1);
      this.saveStatuses();
    },
    saveStatuses() {
      localStorage.setItem('lancer-prime-statuses', JSON.stringify(this.primeStatuses));
    },
    loadStatuses() {
      // 1. Try to load from Local Storage (Browser memory)
      const saved = localStorage.getItem('lancer-prime-statuses');
      
      if (saved) {
        this.primeStatuses = JSON.parse(saved);
      } 
      // 2. If storage is empty, try to load defaults from clocks.json
      else if (defaultStatuses && defaultStatuses.length > 0) {
        // We filter to ensure the JSON has the right fields (name/condition)
        // This prevents crashes if clocks.json still has the old "val/max" format
        const validDefaults = defaultStatuses.filter(s => s.name && s.condition);
        this.primeStatuses = validDefaults;
      }
    }
  },
};
</script>

<style scoped>
/* --- PRIME STATUS STYLES --- */

/* Header Controls */
.edit-toggle {
  margin-left: auto;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: bold;
  opacity: 0.7;
  padding-right: 10px;
  transition: opacity 0.2s;
}
.edit-toggle:hover {
  opacity: 1;
  color: #FFC107;
}

/* View Mode List */
.status-list-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 10px;
}

.status-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px dashed rgba(255, 255, 255, 0.15);
  padding-bottom: 4px;
}

.status-name {
  font-weight: 700;
  color: #fff;
  font-size: 1.1em;
}

.dots-spacer {
  flex-grow: 1;
  border-bottom: 1px dotted #555;
  margin: 0 10px;
  height: 12px;
  opacity: 0.3;
}

.chip.status-chip {
  background: #C70000; /* Lancer Red */
  color: white;
  padding: 2px 8px;
  border-radius: 2px;
  font-weight: 700;
  font-size: 0.85em;
  letter-spacing: 1px;
  box-shadow: 1px 1px 3px rgba(0,0,0,0.5);
}

.empty-state {
  text-align: center;
  font-style: italic;
  opacity: 0.5;
  padding: 20px;
  font-size: 0.9em;
  border: 1px dashed #444;
}

/* Edit Mode Inputs */
.status-edit-container {
  padding: 10px;
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid #444;
}

.add-status-row {
  display: flex;
  gap: 5px;
  margin-bottom: 10px;
}

input {
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid #555;
  color: white;
  padding: 8px;
  flex-grow: 1;
  width: 40%;
  font-family: "Rubik", sans-serif; /* Matches Lancer font usually */
}
input:focus {
  outline: none;
  border-color: #FFC107;
  background: rgba(0, 0, 0, 0.8);
}

button {
  border: none;
  cursor: pointer;
  font-weight: bold;
  color: white;
  transition: background 0.2s;
}

.btn-add {
  background: #2E7D32;
  width: 40px;
  font-size: 1.2em;
}
.btn-add:hover { background: #388E3C; }

.btn-delete {
  background: #C62828;
  padding: 2px 8px;
  margin-left: 10px;
}
.btn-delete:hover { background: #D32F2F; }

.edit-list {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.edit-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.05);
  padding: 5px 10px;
  border-left: 2px solid #555;
}
.edit-text {
  font-size: 0.9em;
}
</style>