<template>
  <div id="messagesView" :class="{ animate: animateView }" :style="{ 'animation-delay': animationDelay }" class="content-container">
    
    <!-- List Section -->
    <section id="message-list" :class="{ animate: animate }" class="section-container">
      <div class="section-header clipped-medium-backward">
        <img src="/icons/conversation.svg" />
        <h1>MESSAGE ARCHIVE</h1>
      </div>
      <div class="section-content-container">
        <div class="items-list-container">
          <Message
            v-for="item in sortedMessages"
            :key="item.id"
            :message="item"
            @select-message="selectMessage(item)" />
        </div>
      </div>
    </section>
    
    <!-- Content Section -->
    <section id="message-content" :class="{ animate: animate }" class="section-container">
      <div style="height: 52px; overflow: hidden">
        <div class="section-header clipped-info-backward">
          <img src="/icons/protocol.svg" />
          <h1>DECODED TRANSMISSION</h1>
        </div>
        <div class="rhombus-back">&nbsp;</div>
      </div>
      
      <div class="section-content-container extra-margins">
        <div class="message-detail" v-if="selectedMessage">
          <div class="detail-header">
            <h1>MSG // {{ selectedMessage.id }}</h1>
            <h2>{{ selectedMessage.title }}</h2>
             <div class="meta-info">
                <span><strong>FROM:</strong> {{ selectedMessage.sender }}</span>
                <span><strong>DATE:</strong> {{ selectedMessage.date }}</span>
             </div>
          </div>
          <hr class="divider"/>
          <vue-markdown-it :source="selectedMessage.content" class="markdown" />
        </div>
        <div v-else class="empty-state">
            <p>Select a transmission to decode.</p>
        </div>
      </div>
    </section>

  </div>
</template>

<script>
import { VueMarkdownIt } from '@f3ve/vue-markdown-it';
import Message from "@/components/Message.vue";
import MessageModal from "@/components/modals/MessageModal.vue";

export default {
  name: "MessagesView",
  components: {
    VueMarkdownIt,
    Message,
  },
  props: {
    animate: { type: Boolean, required: true },
    messages: { type: Array, required: true },
  },
  data() {
    return {
      selectedMessage: null,
      animateView: this.animate,
      animationDelay: "0.5s", // Slightly faster than others
    };
  },
  computed: {
    sortedMessages() {
        // Sort by ID descending (newest first)
        return [...this.messages].sort((a, b) => b.id.localeCompare(a.id));
    }
  },
  mounted() {
     if (this.sortedMessages.length > 0) {
         this.selectedMessage = this.sortedMessages[0];
     }
  },
  methods: {
    selectMessage(msg) {
      if (window.innerWidth <= 768) {
          this.$oruga.modal.open({
            component: MessageModal,
            custom: true,
            trapFocus: true,
            props: { 
                message: msg,
            },
            class: 'custom-modal',
            width: 1920,
          });
      } else {
        this.selectedMessage = msg;
      }
    }
  }
};
</script>

<style scoped>
/* Reuse layout struct from EventsView/StatusView via global CSS if available, 
   but specific styling here for the message view */

/* Ensure deep styling reaches the markdown component to make it fill space */
:deep(.markdown) {
    flex: 1; /* Push to fill remaining space */
    height: 100%;
}

.items-list-container {
    padding: 10px;
    display: flex;
    flex-direction: column;
    height: 100%; /* Fill parent */
    overflow-y: auto; /* Scroll internally if needed */
}

.message-detail {
    padding: 20px;
    color: #eee;
    height: 100%; /* Fill parent */
    display: flex;
    flex-direction: column;
}

/* ... (rest of file) */


.detail-header h1 {
    font-family: 'Fragment Mono', monospace;
    font-size: 1.2rem;
    color: #555;
    margin: 0;
}

.detail-header h2 {
    font-family: 'Rubik', sans-serif;
    font-size: 1.5rem;
    color: #eee; 
    text-transform: uppercase;
    margin: 5px 0 10px 0;
}

.meta-info {
    font-family: 'Rubik', sans-serif;
    font-size: 0.9rem;
    color: #aaa;
    display: flex; /* Key for spacing */
    gap: 20px;    /* Key for spacing */
    flex-wrap: wrap;
}

/* ... existing code ... */

.divider {
    border: 0;
    border-bottom: 1px solid #444;
    margin: 20px 0;
}

.empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #555;
    font-family: 'Fragment Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* Specific Section overrides */
#message-content {
    width: 1100px; /* Wider box */
    margin: 50px 30px;
    height: 75vh; /* Use more vertical space on desktop */
}

#message-list {
    height: 75vh; /* Match content height */
}

@media (max-width: 768px) {
    #message-content {
        height: auto;
        margin: 20px 10px;
        width: auto;
    }

    #message-list {
        height: 80vh !important; /* Force taller list on mobile */
        min-height: 600px;
    }
    
    .items-list-container {
        height: 100%; /* Ensure inner container fills the new height */
        overflow-y: auto;
    }
}
</style>
