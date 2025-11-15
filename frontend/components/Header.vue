<template>
  <header class="header">
    <nav class="navbar">

      <!-- Logo + App Name -->
      <div class="logo-section">
        <img
          src="/logo.png"
          alt="ClassSync Logo"
          class="logo"
        />
        <h1 class="app-title">ClassSync</h1>
      </div>

      <!-- Navigation Links -->
      <ul class="nav-links">
        <li>
          <nuxt-link to="/dashboard" exact-active-class="active">
            Dashboard
          </nuxt-link>
        </li>

        <li v-if="userRole !== 'student'">
          <nuxt-link to="/routines" exact-active-class="active">
            Routines
          </nuxt-link>
        </li>

        <li>
          <nuxt-link to="/notifications" exact-active-class="active">
            Notifications
          </nuxt-link>
        </li>
      </ul>

      <!-- User Dropdown -->
      <div class="dropdown" @click="toggleDropdown">
        <div class="dropdown-btn">
          <span class="username">{{ username }}</span>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="icon"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </div>

        <div v-if="isOpen" class="dropdown-content">
          <button class="logout-btn" @click="logout">Logout</button>
        </div>
      </div>

    </nav>
  </header>
</template>

<script>
export default {
  props: {
    username: {
      type: String,
      default: "User",
    },
  },
  data() {
    return {
      isOpen: false,
      userRole: null,
    };
  },
  mounted() {
    const user = JSON.parse(localStorage.getItem("user"));
    if (user && user.role) {
      this.userRole = user.role.toLowerCase();
    }
  },
  methods: {
    toggleDropdown() {
      this.isOpen = !this.isOpen;
    },
    logout() {
      localStorage.removeItem('user');
      if (this.$store && this.$store.commit) {
        this.$store.commit('setUser', null);
      }
      this.$router.push('/');
    },
  },
};
</script>

<style scoped>

/* Header Container */
.header {
  background: var(--header-bg);
  border-bottom: 1px solid rgba(255,255,255,0.04);
  box-shadow: 0 3px 12px rgba(11, 6, 30, 0.55);
  padding: 0.6rem 1.25rem;
  position: sticky;
  top: 0;
  z-index: 60;
}

/* Navbar Layout */
.navbar {
  width: 100%;
  max-width: 1200px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: auto;
}

/* Logo Section */
.logo-section {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

/* Final Corrected Logo CSS */
.logo {
  height: 42px;
  width: auto;
  object-fit: contain;
  border-radius: 0;
  display: block;
  filter: none !important;
}

.app-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #fff;
  letter-spacing: 0.4px;
}

/* Navigation Links */
.nav-links {
  display: flex;
  gap: 1.8rem;
  list-style: none;
}

.nav-links a {
  text-decoration: none;
  color: rgba(255,255,255,0.87);
  font-weight: 600;
  font-size: 0.95rem;
  transition: color 0.15s, transform 0.15s;
}

.nav-links a:hover {
  color: var(--accent);
  transform: translateY(-2px);
}

.active {
  color: var(--accent);
  border-bottom: 2px solid var(--accent);
  padding-bottom: 4px;
}

/* User Dropdown */
.dropdown {
  position: relative;
  cursor: pointer;
}

.dropdown-btn {
  display: flex;
  align-items: center;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 8px;
  padding: 0.4rem 0.8rem;
  gap: 0.4rem;
  transition: all 0.12s ease;
}

.dropdown-btn:hover {
  background: rgba(255,255,255,0.12);
}

.username {
  font-weight: 600;
  color: #fff;
}

.icon {
  width: 18px;
  height: 18px;
  color: #374151;
}

.dropdown-content {
  position: absolute;
  right: 0;
  top: 110%;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 0.5rem;
  width: 120px;
}

.logout-btn {
  width: 100%;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.45rem 0;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.12s, transform 0.12s;
}

.logout-btn:hover {
  background: var(--accent-dark);
  transform: translateY(-2px);
}
</style>
