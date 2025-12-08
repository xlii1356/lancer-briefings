@ -1,326 +1,329 @@
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
          <Mission 
            v-for="item in sortedMissions" 
            :key="item.slug" 
            :mission="item" 
            :selected="missionSlug"
            :pilots="pilots"
            :locked-squad="getSquadForMission(item.slug)" 
            @click="selectMission(item.slug)" 
          />
        </div>
      </div>
    </section>

    <section id="assignment" class="section-container" :style="{ 'animation-delay': animationDelay }">
      <div class="section-header clipped-medium-backward">
        <img src="/icons/deployable.svg" />
        <h1>Current Assignment</h1>
      </div>
      
      <div class="section-content-container" style="overflow: hidden; position: relative;">
        <Transition name="slide-right" mode="out-in">
          <div :key="missionSlug" class="assignment-content">
            <vue-markdown-it :source="missionMarkdown || 'No mission selected.'" class="markdown" />
          </div>
        </Transition>
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
            <Reserve 
              v-for="item in visibleReserves" 
              :key="item.name" 
              :reserve="item" 
              :pilots="pilots" 
            />
          </div>
        </div>
      </section>

      <section id="clocks" class="section-container" :style="{ 'animation-delay': animationDelay }">
        <div class="section-header clipped-medium-backward">
          <img src="/icons/reflection.svg" />
          <h1>PRIME STATUS</h1>
        </div>
        <div class="section-content-container">
          <div class="prime-list-container">
            <div v-for="(item, index) in primeData" :key="index" class="prime-row">
              <div class="row-line">
                <span class="label">Current Alias:</span> 
                <span class="value">{{ item.alias }}</span>
              </div>
              <div class="row-line">
                <span class="label">Echo:</span> 
                <span class="value">{{ item.echo }}</span>
              </div>
              <div class="row-line">
                <span class="label">Current Status:</span>
                <span :class="getStatusClass(item.status)">
                  {{ item.status.toUpperCase() }}
                </span>
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

import Reserve from "@/components/Reserve.vue";

import primeDataList from '@/assets/prime/prime.json';
import missionSquads from '@/assets/missions/squads.json';

export default {
  components: {
    VueMarkdownIt,
    Mission,

    Reserve,
  },
  props: {
    animate: { type: Boolean, required: true },
    initialSlug: { type: String, required: true },
    missions: { type: Array, required: true },

    pilots: { type: Array, required: true },
    clocks: { type: Array, required: true },
    reserves: { type: Array, required: true },
  },
  computed: {
    sortedMissions() {
      return [...this.missions].sort((a, b) => Number(a.slug) - Number(b.slug));
    },
    // FIX: Filter the reserves here instead of in the HTML
    visibleReserves() {
      if (!this.reserves) return [];
      return this.reserves.filter(item => item && item.name !== 'Skill Point');
    }
  },
  data() {
    return {
      missionSlug: this.initialSlug,
      animateView: this.animate,
      animationDelay: "1.75s",
      clockAnimationDelay: "2500",
      missionMarkdown: "",
      primeData: primeDataList,
      squadData: missionSquads, 
    };
  },
  created() {
    this.setAnimate();
    this.setClockAnimateDelay();
  },
  beforeUpdate() {
    this.selectMission(this.missionSlug);
  },
  mounted() {
    if (this.$route.query.mission) {
      this.selectMission(this.$route.query.mission);
    } else if (this.missions.length > 0) {
      this.selectMission(this.missions[0].slug);
    }
  },
  methods: {
    getSquadForMission(slug) {
      const record = this.squadData.find(s => s.missionSlug === slug);
      return record ? record.pilots : null;
    },
    getStatusClass(status) {
      const s = status.toLowerCase();
      if (s === 'active') return 'status-active';
      if (s === 'deceased') return 'status-deceased';
      if (s === 'neutralized') return 'status-neutralized';
      if (s === 'unknown') return 'status-unknown';
      return '';
    },
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
    setClockAnimateDelay() {
      let delayToFloat = parseFloat(this.animationDelay.replace("s", ""));
      let finalClockDelay = delayToFloat * 600 + 600;
      this.clockAnimationDelay = finalClockDelay.toString();
    },
  },
};
</script>

<style scoped>
/* --- ANIMATION STYLES (MOVE RIGHT) --- */
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.slide-right-enter-from {
  transform: translateX(-50px);
  opacity: 0;
}
.slide-right-leave-to {
  transform: translateX(50px);
  opacity: 0;
}
.assignment-content {
  width: 100%;
  height: 100%;
}

/* --- EXISTING STYLES --- */
.prime-list-container {
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.prime-row {
  border-left: 2px solid #555;
  padding-left: 10px;
  background: rgba(0, 0, 0, 0.2);
  padding: 10px;
}
.row-line {
  margin-bottom: 2px;
  font-family: 'Rubik', sans-serif;
}
.label {
  color: #888;
  margin-right: 8px;
  font-size: 0.9em;
  text-transform: uppercase;
}
.value {
  color: white;
  font-weight: bold;
}

/* --- STATUS COLORS --- */
.status-active {
  color: #00ff00;
  font-weight: bold;
  text-shadow: 0 0 5px #00ff00;
}
.status-deceased {
  color: #ff0000;
  font-weight: bold;
  text-shadow: 0 0 5px #ff0000;
}
.status-neutralized {
  color: #FFC107;
  font-weight: bold;
  text-shadow: 0 0 5px #FFC107;
}

/* --- GLITCH EFFECT --- */
.status-unknown {
  color: white;
  font-weight: bold;
  position: relative;
  display: inline-block;
  animation: glitch-skew 1s infinite linear alternate-reverse;
}
.status-unknown::before,
.status-unknown::after {
  content: "UNKNOWN";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.status-unknown::before {
  left: 2px;
  text-shadow: -1px 0 #ff00c1;
  clip: rect(44px, 450px, 56px, 0);
  animation: glitch-anim 5s infinite linear alternate-reverse;
}
.status-unknown::after {
  left: -2px;
  text-shadow: -1px 0 #00fff9;
  clip: rect(44px, 450px, 56px, 0);
  animation: glitch-anim2 5s infinite linear alternate-reverse;
}

@keyframes glitch-anim {
  0% { clip: rect(31px, 9999px, 94px, 0); transform: skew(0.85deg); }
  5% { clip: rect(70px, 9999px, 11px, 0); transform: skew(0.06deg); }
  10% { clip: rect(6px, 9999px, 83px, 0); transform: skew(0.36deg); }
  15% { clip: rect(25px, 9999px, 92px, 0); transform: skew(0.12deg); }
  20% { clip: rect(48px, 9999px, 36px, 0); transform: skew(0.97deg); }
  25% { clip: rect(2px, 9999px, 2px, 0); transform: skew(0.82deg); }
  30% { clip: rect(65px, 9999px, 7px, 0); transform: skew(0.53deg); }
  35% { clip: rect(10px, 9999px, 29px, 0); transform: skew(0.35deg); }
  40% { clip: rect(49px, 9999px, 1px, 0); transform: skew(0.11deg); }
  45% { clip: rect(32px, 9999px, 33px, 0); transform: skew(0.04deg); }
  50% { clip: rect(26px, 9999px, 15px, 0); transform: skew(0.24deg); }
  55% { clip: rect(76px, 9999px, 86px, 0); transform: skew(0.68deg); }
  60% { clip: rect(6px, 9999px, 57px, 0); transform: skew(0.89deg); }
  65% { clip: rect(80px, 9999px, 93px, 0); transform: skew(0.68deg); }
  70% { clip: rect(93px, 9999px, 39px, 0); transform: skew(0.14deg); }
  75% { clip: rect(88px, 9999px, 22px, 0); transform: skew(0.11deg); }
  80% { clip: rect(3px, 9999px, 92px, 0); transform: skew(0.36deg); }
  85% { clip: rect(22px, 9999px, 49px, 0); transform: skew(0.27deg); }
  90% { clip: rect(78px, 9999px, 63px, 0); transform: skew(0.48deg); }
  95% { clip: rect(96px, 9999px, 10px, 0); transform: skew(0.61deg); }
  100% { clip: rect(23px, 9999px, 66px, 0); transform: skew(0.11deg); }
}

@keyframes glitch-anim2 {
  0% { clip: rect(65px, 9999px, 100px, 0); transform: skew(0.31deg); }
  5% { clip: rect(52px, 9999px, 74px, 0); transform: skew(0.45deg); }
  10% { clip: rect(79px, 9999px, 85px, 0); transform: skew(0.87deg); }
  15% { clip: rect(10px, 9999px, 45px, 0); transform: skew(0.92deg); }
  20% { clip: rect(5px, 9999px, 26px, 0); transform: skew(0.23deg); }
  25% { clip: rect(34px, 9999px, 9px, 0); transform: skew(0.04deg); }
  30% { clip: rect(56px, 9999px, 69px, 0); transform: skew(0.99deg); }
  35% { clip: rect(13px, 9999px, 87px, 0); transform: skew(0.19deg); }
  40% { clip: rect(94px, 9999px, 6px, 0); transform: skew(0.34deg); }
  45% { clip: rect(35px, 9999px, 18px, 0); transform: skew(0.42deg); }
  50% { clip: rect(2px, 9999px, 84px, 0); transform: skew(0.71deg); }
  55% { clip: rect(26px, 9999px, 46px, 0); transform: skew(0.49deg); }
  60% { clip: rect(57px, 9999px, 96px, 0); transform: skew(0.71deg); }
  65% { clip: rect(40px, 9999px, 61px, 0); transform: skew(0.61deg); }
  70% { clip: rect(56px, 9999px, 42px, 0); transform: skew(0.64deg); }
  75% { clip: rect(11px, 9999px, 75px, 0); transform: skew(0.87deg); }
  80% { clip: rect(19px, 9999px, 76px, 0); transform: skew(0.64deg); }
  85% { clip: rect(77px, 9999px, 16px, 0); transform: skew(0.79deg); }
  90% { clip: rect(69px, 9999px, 57px, 0); transform: skew(0.55deg); }
  95% { clip: rect(34px, 9999px, 5px, 0); transform: skew(0.81deg); }
  100% { clip: rect(24px, 9999px, 78px, 0); transform: skew(0.43deg); }
}
</style>