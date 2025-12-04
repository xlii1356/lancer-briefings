<template>
  <div class="prime-modal">
    <div class="header-container">
      <div class="section-header clipped-medium-backward-bio">
        <img src="/icons/reflection.svg" />
        <h1>PRIME DOSSIER // {{ prime.alias.toUpperCase() }}</h1>
      </div>
      <div class="rhombus-back">&nbsp;</div>
    </div>

    <div class="prime-content">
      <div class="prime-row">
        <div class="row-line">
          <span class="label">Current Alias:</span> 
          <span class="value">{{ prime.alias }}</span>
        </div>
        <div class="row-line">
          <span class="label">Echo:</span> 
          <span class="value">{{ prime.echo }}</span>
        </div>
        <div class="row-line">
          <span class="label">Current Status:</span>
          <span :class="getStatusClass(prime.status)">
            {{ prime.status.toUpperCase() }}
          </span>
        </div>
      </div>
      
      <div v-if="prime.description" class="prime-description">
        <hr>
        <p>{{ prime.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PrimeModal',
  props: {
    prime: {
      type: Object,
      required: true,
    },
  },
  methods: {
    getStatusClass(status) {
      const s = status.toLowerCase();
      if (s === 'active') return 'status-active';
      if (s === 'deceased') return 'status-deceased';
      if (s === 'neutralized') return 'status-neutralized';
      if (s === 'unknown') return 'status-unknown';
      return '';
    }
  }
};
</script>

<style scoped>
/* Modal Container Styling */
.prime-modal {
  position: relative;
  width: 600px; /* Compact width */
  margin: 0 auto;
}

.header-container {
  display: flex;
}

.prime-modal .section-header {
  background-color: var(--primary-color);
  height: 52px;
  display: inline-flex;
  gap: 15px;
  padding-left: 16px;
  margin-top: -38px !important;
  /* Clip path matching other modals */
  width: 582px;
	clip-path: polygon(0 0, 530px 0, 582px 100%, 0% 100%);
	-webkit-clip-path: polygon(0 0, 530px 0, 582px 100%, 0% 100%);
}

.prime-modal .section-header h1 {
  font-size: 26px;
  margin: 0;
  align-self: center;
  font-family: "Big Shoulders Display", cursive;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-headers);
}

.prime-modal .section-header img {
  width: 36px;
  height: 36px;
  align-self: center;
}

.rhombus-back {
  transform: skew(0.785398rad) !important;
  background-color: var(--primary-color);
  width: 40px;
  height: 52px;
  display: inline-block;
  position: relative;
  left: -10px;
  top: -38px;
}

/* Content Area */
.prime-content {
  background-color: var(--secondary-color);
  border: 1px solid var(--primary-color);
  margin-top: -38px;
  padding: 20px;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.prime-row {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 10px;
  border-left: 4px solid var(--primary-color);
  background: rgba(255, 255, 255, 0.05);
}

.row-line {
  font-family: 'Rubik', sans-serif;
  font-size: 1.2rem;
}

.label {
  color: #888;
  margin-right: 10px;
  font-size: 0.9em;
  text-transform: uppercase;
}

.value {
  color: white;
  font-weight: bold;
}

.prime-description {
  margin-top: 20px;
  font-family: "Titillium Web", sans-serif;
  color: #ccc;
}

.prime-description hr {
  border-color: var(--primary-color);
  opacity: 0.3;
}

/* --- STATUS COLORS --- */
.status-active { color: #00ff00; font-weight: bold; text-shadow: 0 0 10px #00ff00; }
.status-deceased { color: #ff0000; font-weight: bold; text-shadow: 0 0 10px #ff0000; }
.status-neutralized { color: #FFC107; font-weight: bold; text-shadow: 0 0 10px #FFC107; }

/* --- GLITCH EFFECT --- */
.status-unknown {
  color: white;
  font-weight: bold;
  position: relative;
  display: inline-block;
  animation: glitch-skew 1s infinite linear alternate-reverse;
}
.status-unknown::before, .status-unknown::after {
  content: "UNKNOWN";
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
}
.status-unknown::before {
  left: 2px; text-shadow: -1px 0 #ff00c1; clip: rect(44px, 450px, 56px, 0);
  animation: glitch-anim 5s infinite linear alternate-reverse;
}
.status-unknown::after {
  left: -2px; text-shadow: -1px 0 #00fff9; clip: rect(44px, 450px, 56px, 0);
  animation: glitch-anim2 5s infinite linear alternate-reverse;
}
@keyframes glitch-anim {
  0% { clip: rect(31px, 9999px, 94px, 0); transform: skew(0.85deg); }
  5% { clip: rect(70px, 9999px, 11px, 0); transform: skew(0.06deg); }
  10% { clip: rect(6px, 9999px, 83px, 0); transform: skew(0.36deg); }
  /* ... simplified standard glitch frames ... */
  50% { clip: rect(26px, 9999px, 15px, 0); transform: skew(0.24deg); }
  100% { clip: rect(23px, 9999px, 66px, 0); transform: skew(0.11deg); }
}
@keyframes glitch-anim2 {
  0% { clip: rect(65px, 9999px, 100px, 0); transform: skew(0.31deg); }
  50% { clip: rect(2px, 9999px, 84px, 0); transform: skew(0.71deg); }
  100% { clip: rect(24px, 9999px, 78px, 0); transform: skew(0.43deg); }
}
</style>