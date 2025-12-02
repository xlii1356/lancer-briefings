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
        <vue-markdown-it :source="missionMarkdown || 'No mission selected.'" class="markdown" />
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
              v-if="item && item.name !== 'Skill Point'" />
          </div>
        </div>
      </section>

      <section id="prime-status" class="section-container" :style="{ 'animation-delay': animationDelay }">
        <div class="section-header clipped-medium-backward">
          <img src="/icons/protocol.svg" />
          <h1>PRIME STATUS</h1>
          <div class="edit-toggle" @click="toggleEditMode">
            <span v-if="!editMode">⚙️ EDIT</span>
            <span v-else>💾 SAVE</span>
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
import Reserve from "@/components/Reserve.vue";

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
    events: { type: Array, required: true