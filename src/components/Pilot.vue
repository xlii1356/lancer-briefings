<template>
  <div class="grid-item pilot-identity" style="color:white!important">
    <div class="header">
      <div class="col grow-max">
        <div class="heading h1">TACTICAL PROFILE // {{ pilot.callsign }}</div>
        <div class="heading h2">({{ pilot.name }}) </div>
      </div>
      <div class="col"><img src="/faction-logos/soteria.svg" style="height: 50px; width: auto;"></div>
    </div>
    <div class="body">
      <div class="add-padding"> Union Administrative RM-4 Pilot Identification Protocol (IDENT) Record
        {{ pilot.id }} </div>
      <div class="flex-container-rows">
        <div class="row add-padding">
          {{ reverse(this.pilot.name) }}:{{ pilot.id }}//NDL-C-BLIND-REACH
        </div>
        <div class="row flex-container-cols add-padding">
          <div class="col grow-max flex-container-rows" style="padding-top:5px">
            <div class="row flex-container-cols">
              <div class="col col-primary"><span class="flavor-text"> Callsign: <b class="accent--text">{{
                capitalize(pilot.callsign) }}</b><br> Name (or legal alias): <b class="accent--text">{{ pilot.name
                    }}</b><br> Background: <b class="accent--text"> {{ pilot.background }} </b></span></div>
              <div class="col">CALLSIGN AVAILABLE <br> IDENTITY
                VERIFIED <br> PH/HR DATA REGISTERED</div>
            </div>
            <div style="padding-top:5px"> FRAME CONFIGURATION OPTIONS <span class="subtle--text">("H.A.S.E"
                OMNINET VAULT REMIT)</span></div>
            <div class="row" style="padding-top:5px"><span style="font-size: 22px; line-height: 15px;"> [
                HULL: <span class="stat-text accent--text" style="font-size: 24px;"> {{ pilot.mechSkills[0] }} </span>
                AGI: <span class="stat-text accent--text" style="font-size: 24px;"> {{ pilot.mechSkills[1] }} </span>
                SYS: <span class="stat-text accent--text" style="font-size: 24px;"> {{ pilot.mechSkills[2] }} </span>
                ENG: <span class="stat-text accent--text" style="font-size: 24px;"> {{ pilot.mechSkills[3] }} </span> ]
              </span></div>
            <div class="row flex-container-cols">
              <div class="col col-share">
                <span>PILOT SKILL TRIGGER AUDIT</span>
                <br>
                <div class="chip-container" v-for="skill in pilot.skills" :key="skill.id">
                  <span class="chip"><i aria-hidden="true" class="notranslate cci cci-skill"></i>{{ getSkill(skill)
                  }}</span>
                </div>
              </div>
              <div class="col col-share">
                <span>PILOT TALENT AUDIT</span>
                <br>
                <div class="chip-container" v-for="talent in pilot.talents" :key="talent.id">
                  <span class="chip"><i aria-hidden="true" class="notranslate cci cci-talent"></i>{{
                    getTalent(talent.id, talent.rank) }}</span>
                </div>
              </div>
            </div>
            <div v-if="pilot.level > 0" class="row flex-container-cols">
              <div class="col" style="padding-top:5px">
                <span>PROCUREMENT LICENSE AUDIT: LEVEL {{ pilot.level }}</span>
                <br>
                <div class="chip-container" v-for="license in pilot.licenses" :key="license.id">
                  <span class="chip"><i aria-hidden="true" class="notranslate cci cci-license"></i>{{
                    getLicense(license.id, license.rank) }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="col split-frame-col" style="display: flex; flex-direction: column; gap: 20px;">
            <div 
                class="split-frame-container" 
                @mousemove="handleSplitHover" 
                @mouseleave="resetSplit"
                @click="handleSplitClick"
                :class="activeSide"
            >
                <!-- Mech Layer (Bottom) -->
                <div class="layer layer-mech">
                    <img :src="safeMechPortrait" @error="e => e.target.src = '/icons/clockwork.svg'" class="portrait" />
                    <div class="label-corner bottom-right">ACTIVE FRAME</div>
                </div>

                <!-- Pilot Layer (Top, Clipped) -->
                <div class="layer layer-pilot">
                    <img :src="pilotPortrait" @error="e => { e.target.src = '/icons/portrait.svg'; e.target.style.padding = '20px'; e.target.style.filter='invert(1)'; }" class="portrait" />
                    <div class="label-corner top-left">PILOT VISUAL</div>
                </div>
            </div>
            
            <div class="nhp-container" v-if="nhps.length > 0">
                 <div style="font-size: 0.8em; opacity: 0.7; border-bottom: 1px solid white; margin-bottom: 5px;">NHP COFFIN</div>
                 <div v-for="nhp in nhps" :key="nhp.name" style="display: flex; align-items: center; gap: 5px; margin-bottom: 2px;">
                      <img :src="nhp.icon || '/icons/clockwork.svg'" style="width: 20px; height: 20px; object-fit: contain; filter: brightness(0) invert(1);" />
                      <div style="font-size: 0.8em;">{{ nhp.name }}</div>
                 </div>
            </div>
          </div>
        </div>
      </div>
      <div class="flex-container-cols modal-buttons" style="display: none;">
      </div>
      <hr role="separator" aria-orientation="horizontal" class="ma-2 v-divider theme--dark">
      <div class="row row--dense"><span class="overline" style="line-height: 13px !important; opacity: 0.4;">
          Improper use of this IDENT record and/or its constituent data by the record holder or any other
          persons is punishable under the DoJ/HR A-645-c. This record is the property of the Union
          Administrative Office and the information herein must be transmitted on request under
          NDL-C-DISCORDANT-BREATH encryption protocols. This RM-4 record must be updated every five (5)
          Cradle
          Standard Years of objective time to retain GMS licensing rights. Far-field operatives that
          anticipate deployments lasting longer than five Cradle Standard Years that have not been issued
          a
          man-portable Omninet Hook should apply for the RM-11-B IDENT Supplemental (b) Extension. Contact
          your local Union Adminstrative Officer for any other matters regarding this
          record.  V-CDL//M-265-114-831 (A) </span></div>
    </div>
  </div>
</template>

<style scoped>
.larger::before {
  margin-top: 9px;
}

.mdi::before {
  margin-top: 9px;
}

.mech-record {
  margin-left: auto;
  text-align: right;
}

.split-frame-container {
    width: 250px !important;
    height: 350px !important;
    max-width: 250px !important;
    max-height: 350px !important;
    min-width: 250px !important;
    min-height: 350px !important;
    margin: 0 auto;
    overflow: hidden;
    cursor: pointer;
    border: 1px solid var(--primary-color);
    background: transparent;
    position: relative;
    flex: 0 0 auto;
    box-sizing: border-box;
    align-self: flex-start;
    flex-shrink: 0;
}

.col.split-frame-col {
    flex: 0 0 auto !important;
    align-items: center;
    align-self: flex-start !important;
    justify-content: flex-start;
    width: auto;
    min-height: 0;
}

.pilot-identity {
    position: relative !important;
    display: flex !important;
    flex-direction: column !important;
    min-height: 0 !important;
    padding-top: 0 !important; /* Lock top padding */
}

.pilot-identity .header {
    flex: 0 0 auto !important;
    align-self: stretch !important;
    margin-bottom: 0 !important; /* Prevent margin collapse */
}

.pilot-identity .body {
    flex: 1 1 auto !important;
    padding-top: 0 !important; /* Lock body top padding */
}

/* Prevent parent containers from shifting */
.pilot-identity .row.flex-container-cols.add-padding {
    align-items: flex-start !important;
}

.pilot-identity .flex-container-cols {
    align-items: flex-start !important;
}

.pilot-identity .col.grow-max {
    align-self: stretch !important;
}

.pilot-identity .flex-container-rows {
    align-items: flex-start !important;
}


.layer {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    transition: clip-path 0.4s ease;
    will-change: clip-path; /* Optimize clip-path animations */
}

.layer img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: contain; /* Keep image size consistent */
    object-position: center;
    max-width: 100%;
    max-height: 100%;
}

.layer-mech {
    z-index: 1;
    /* Bottom layer, always visible fully, but covered by pilot layer */
}

.layer-pilot {
    z-index: 2;
    /* Default Diagonal Split (Bottom-Left to Top-Right line) -> Top Left Triangle visible */
    clip-path: polygon(0 0, 100% 0, 0 100%);
    background: #000; /* Fallback */
    transition: clip-path 0.4s ease; /* Ensure transition applies */
}

/* Hover States */
.split-frame-container.pilot .layer-pilot {
    clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); /* Full Reveal */
}

.split-frame-container.mech .layer-pilot {
    clip-path: polygon(0 0, 0 0, 0 0); /* Hide completely -> Reveal Mech */
}

.label-corner {
    position: absolute;
    background: rgba(0,0,0,0.7);
    color: white;
    font-size: 0.8rem;
    padding: 2px 5px;
    pointer-events: none;
    z-index: 3;
    font-weight: bold;
}

.label-corner.top-left {
    top: 0;
    left: 0;
    border-bottom-right-radius: 5px;
}

.label-corner.bottom-right {
    bottom: 0;
    right: 0;
    border-top-left-radius: 5px;
}
</style>

<script>
import 'external-svg-loader'
import lancerData from '@massif/lancer-data'
import ktbData from 'lancer-ktb-data'
import nrfawData from 'lancer-nrfaw-data'
import longrimData from 'lancer-longrim-data'

import wallflowerData from '@/assets/LCPs/wallflower-data-2.0.5'
/*Append the datasets within computed if your LCP has new items.
EX:
pilotGear() {
  return [...lancerData.pilot_gear, ...wallflowerData.pilot_gear]
},
*/

import PilotModal from '@/components/modals/PilotModal.vue'
import MechModal from '@/components/modals/MechModal.vue'

import Typer from '@/components/Typer.vue'

import ProgressBar from '@/components/ProgressBar.vue'
import Burden from '@/components/Burden.vue'

export default {
  components: {
    Burden,
    ProgressBar,
    Typer,
  },
  props: {
    animate: {
      type: Boolean,
      required: true,
    },
    pilot: {
      type: Object,
      required: true,
    },
    nhps: {
        type: Array,
        default: () => []
    }
  },
  data() {
    return {
      activeMech: {},
      bond: {},
      activeSide: null, // 'pilot' or 'mech'
    }
  },
  computed: {
    pilotPortrait() {
      return `/pilots/${this.pilot.callsign.toUpperCase()}.webp`
    },
    safeMechPortrait() {
      return `/mechs/${encodeURIComponent(this.pilot.callsign.toUpperCase())}.webp`
    },
    pilotGear() {
      return [...lancerData.pilot_gear]
    },
    mechWeapons() {
      return [...lancerData.weapons, ...ktbData.weapons, ...nrfawData.weapons, ...longrimData.weapons]
    },
    mechSystems() {
      return [...lancerData.systems, ...ktbData.systems, ...nrfawData.systems, ...longrimData.systems]
    },
    talents() {
      return [...lancerData.talents, ...ktbData.talents, ...nrfawData.talents, ...longrimData.talents]
    },
    skills() {
      return [...lancerData.skills]    
    },
    bonds() {
      return [...ktbData.bonds]
    },
    frames() {
      return [...lancerData.frames, ...ktbData.frames, ...nrfawData.frames, ...longrimData.frames]
    },
    mechManufacturerIcon() {
      if (this.activeMech.manufacturer)
        return `/faction-logos/${this.activeMech.manufacturer.toLowerCase()}.svg`
      return ''
    },
    pilotCode() {
      const identNameParts = this.pilot.name.split(' ')
      const identFirstName = identNameParts[0]
      const identLastNameParts = identNameParts.slice(1)
      let identName = ''
      identLastNameParts.forEach((part) => {
        identName += `${part}.`
      })
      identName += identFirstName;
			return `Union Administrative RM-4 Pilot Identification Protocol (IDENT) Record ${identName}: ${this.pilot.id} // ${this.pilot.background} // LOADOUT ${this.pilot.loadout.id} - MECH ${this.pilot.mechs[0].id} // HARDPOINTS ${this.pilot.mechs[0].loadouts[0].id}`;
		},
    pilotInfo() {
      const info = this.pilot

      let resolveGear = (type, item, idx, arr) => {
        item = item || {id: "", flavorName: ""};
        const gear = this.pilotGear.find((obj) => { return item.id === obj.id }) || null;
        item.flavorName = gear?.name || "ERR: DATA NOT FOUND";
        arr[idx] = item;
      }

      info.loadout.armor.forEach((item, index, array) => resolveGear('armor', item, index, array));
      info.loadout.weapons.forEach((item, index, array) => resolveGear('weapon', item, index, array));
      info.loadout.gear.forEach((item, index, array) =>resolveGear('gear', item, index, array));

      return info;
    },
  },
  created() {
    this.getActiveMech();
    this.getBond();
  },
  watch: {
    pilot: {
      handler() {
        this.getActiveMech();
        this.getBond();
      },
      deep: true
    }
  },
  methods: {
    getBond() {
      this.bond = this.bonds.find((obj) => {
        return obj.id === this.pilot.bondId
      })
    },
    getActiveMech() {
      const activeMechID = this.pilot.state.active_mech_id
      const mech = this.pilot.mechs.find((obj) => {
        return obj.id === activeMechID
      })

      if (mech) {
        this.activeMech = mech
      }
      else {
        // default to missing frame in case pilot has no mechs
        this.pilot.mechs[0] ? this.activeMech = this.pilot.mechs[0] : lancerData.frames.find((obj) => { return obj.id === 'missing_frame' })
      }

      let frame = this.frames.find((obj) => {
        return obj.id === this.activeMech.frame
      })

      if (!frame)
        frame = lancerData.frames[0]

      this.activeMech.frame_description = frame.description
      this.activeMech.frame_name = frame.name
      this.activeMech.manufacturer = frame.source
      this.activeMech.mechtype = frame.mechtype.join(' // ')
    },
    getHistory() {
      if (this.pilot.history === "") {
        return `<p> <h2> [ERR: REDACTED] </h2> </p>`
      }

      let response = "<p>"

      if (this.pilot.text_appearance !== "") {
        response += `<h2>APPEARANCE</h2> ${this.pilot.text_appearance} </hr>`;
      }

      if (this.pilot.history !== "") {
        response += `<h2>HISTORY</h2> ${this.pilot.history} </hr>`;
      }

      response += "</p>"

      return response;
    },
  getSkill(skill) {
      // Try to find the skill in the database
      let sk = this.skills.find((x) => x.id == skill.id);
      
      // If found, use the official name. 
      // If NOT found (custom skill), use the ID from the JSON as the name.
      const skillName = sk ? sk.name : skill.id; 
      
      return skillName + " +" + (skill.rank * 2);
    },

    getTalent(id, value) {
      let talent = this.talents.find((x) => x.id == id);
      
      // Fallback: If talent is missing, use the ID so the UI doesn't crash
      let name = talent ? talent.name : id; 
      let response = name + " ";

      for (let i = 0; i < value; i++) {
        response += "I";
      }
      return response;
    },
    getLicense(id, value) {
      let frame = this.frames.find((x) => x.id == id);
      let response = frame.source + " " + frame.name + " "

      for (let i = 0; i < value; i++) {
        response += "I"
      }
      return response;
    },
    capitalize(str) {
      return str.split(' ').map(word => word[0].toUpperCase() + word.slice(1)).join(' ');
    },
    reverse(str) {
      const words = str.split(' ')
      const reversed = words.reverse()
      const reversedResult = words.join('.')
      return reversedResult
    },
    randomNumber(max, min) {
      const rand = Math.random() * (max - min) + min
      const power = Math.pow(10, 2)
      return Math.floor(rand * power) / power
    },
    timeStamp(str) {
      let date = new Date(str);
      let y = date.getFullYear();
      let m = date.getMonth();
      let d = date.getDate();
      let h = date.getHours();
      let mi = date.getMinutes();
      let s = date.getSeconds();
      let ms = date.getMilliseconds();
      let tz = date.getTimezoneOffset();
      y += 2990;
      return new Date(y, m, d, h, mi, s, ms).toISOString();
    },
    handleSplitHover(e) {
        // Calculate based on Diagonal from Bottom-Left (0, H) to Top-Right (W, 0)
        // Line equation: Y = H - (H/W)*X
        // If y < H - (H/W)*X, we are Top-Left (Pilot)
        // If y > H - (H/W)*X, we are Bottom-Right (Mech)
        
        const rect = e.currentTarget.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top; // y is 0 at top
        const w = rect.width;
        const h = rect.height;
        
        // Threshold Y at this X
        const thresholdY = h - (h / w) * x;
        
        if (y < thresholdY) {
            this.activeSide = 'pilot';
        } else {
            this.activeSide = 'mech';
        }
    },
    resetSplit() {
        this.activeSide = null;
    },
    handleSplitClick() {
        if (this.activeSide === 'pilot') {
            this.pilotModal();
        } else if (this.activeSide === 'mech') {
            this.mechModal();
        }
    },
    pilotModal() {
      this.$oruga.modal.open({
        component: PilotModal,
        custom: true,
        trapFocus: true,
        props: {
          pilot: this.pilot,
          talents: this.talents,
          skills: this.skills,
          frames: this.frames,
        },
        class: 'custom-modal',
        width: 1920,
      })
    },
    mechModal() {
      this.$oruga.modal.open({
        component: MechModal,
        custom: true,
        trapFocus: true,
        props: {
          animate: this.animate,
          mech: this.activeMech,
          systemsData: this.mechSystems,
          weaponsData: this.mechWeapons,
          pilot: this.pilot,
        },
        class: 'custom-modal',
        width: 1920,
      })
    },
  },
}
</script>
