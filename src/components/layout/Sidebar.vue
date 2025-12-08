<template>
	<div class="sidebar-page">
		<section class="sidebar-layout" :class="{ open: isOpen }">
            <!-- Mobile Toggle Button -->
            <button class="mobile-toggle" @click="toggleSidebar">
                <img src="/icons/menu.svg" alt="Menu" v-if="!isOpen"/>
                <img src="/icons/close.svg" alt="Close" v-if="isOpen"/>
            </button>

			<o-sidebar
			  id="sidebar"
			  position="static"
			  :animate="animate"
			  :mobile="mobile"
			  :expand-on-hover="expandOnHover"
			  :reduce="reduce"
			  open>
				<router-link class="clipped-bottom-right" to="/status">
					<img src="/icons/orbital.svg" />
					<span>Status</span>
				</router-link>
				<router-link class="clipped-bottom-right" to="/pilots">
					<img src="/icons/pilot.svg" />
					<span>Pilots</span>
				</router-link>
				<router-link class="clipped-bottom-right" to="/events">
					<img src="/faction-logos/barony.svg" />
					<span>Factions</span>
				</router-link>
				<router-link class="clipped-bottom-right" to="/messages">
					<img src="/icons/conversation.svg" />
					<span>Messages</span>
				</router-link>
			</o-sidebar>
		</section>
	</div>
</template>

<script>
export default {
	props: {
		animate: {
			type: Boolean,
			required: true,
		},
	},
	data() {
		return {
			expandOnHover: false,
			mobile: "reduced",
			reduce: false,
            isOpen: false, // New state for mobile toggle
		};
	},
    methods: {
        toggleSidebar() {
            this.isOpen = !this.isOpen;
        }
    }
};
</script>

<style scoped>
.sidebar-page,
.sidebar-layout {
	pointer-events: none;
	height: 100%; /* Ensure it doesn't collapse but allows clicks through */
	width: 100%;
}

#sidebar {
	pointer-events: auto;
    transition: transform 0.3s ease;
}

/* Mobile Toggle Styles */
.mobile-toggle {
    display: none; /* Hidden by default on desktop */
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 2000; /* Above everything */
    background: rgba(0, 0, 0, 0.8);
    border: 1px solid #333;
    padding: 8px;
    cursor: pointer;
    border-radius: 4px;
    pointer-events: auto;
}

.mobile-toggle img {
    width: 24px;
    height: 24px;
    display: block;
}

/* Mobile Breakpoint */
@media (max-width: 768px) {
    .mobile-toggle {
        display: block;
    }

    /* Reset width to avoid full-screen blocking on mobile if closed */
    .sidebar-layout {
        width: 0 !important; 
    }

    /* When open, it can take space (for the overlay) */
    .sidebar-layout.open {
        width: 100% !important;
        background: rgba(0,0,0,0.5); /* Backdrop */
        pointer-events: auto; /* Catch clicks on backdrop */
    }

    /* Hide sidebar off-screen by default */
    #sidebar {
        position: fixed;
        top: 0;
        left: 0;
        height: 100%;
        width: 250px !important; /* Fixed width for mobile menu */
        transform: translateX(-100%);
        z-index: 1001;
    }

    /* Slide in when open */
    .sidebar-layout.open #sidebar {
        transform: translateX(0);
    }
}
</style>
