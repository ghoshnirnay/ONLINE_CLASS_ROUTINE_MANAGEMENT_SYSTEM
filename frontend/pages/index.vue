<template>
  <div class="landing-page">
    <div class="landing-content container">
      <!-- Hero: two-column layout (text + illustration) -->
      <div class="hero-grid">
        <div class="hero-section">
          <h1 class="hero-title">ClassSync</h1>
          <h2 class="hero-subtitle-main">Class Routine Management System</h2>
    <p class="hero-author">Prepared by <strong>Nirnay Ghosh</strong></p>

          <p class="hero-subtitle">
            Streamline your institution's scheduling with an easy-to-use routine management platform — fast, secure, and collaborative.
          </p>

          <div class="hero-actions">
            <button class="btn btn-primary btn-lg" @click="openModal('login')">Get Started</button>
            <button class="btn btn-outline btn-lg" @click="openModal('register')">Create Account</button>
          </div>

          <div class="hero-features-quick">
            <div class="pill">📅 Automated</div>
            <div class="pill">🔔 Notifications</div>
            <div class="pill">🔐 Secure</div>
          </div>
        </div>

        <div class="hero-illustration" aria-hidden="true">
          <!-- Use the SVG logo as a pleasant illustration on larger screens -->
          <Logo class="logo-illustration" />
        </div>
      </div>

      <!-- Features grid -->
      <div class="features-wrapper">
        <div class="features-section">
        <div
          v-for="(feature, index) in features"
          :key="index"
          class="feature-card card"
        >
          <div class="feature-icon">{{ feature.icon }}</div>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.desc }}</p>
        </div>
        </div>
      </div>
    </div>

    <!-- Floating Login Modal -->
    <div v-if="activeModal === 'login'" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <Suspense>
          <component :is="LoginPage" />
        </Suspense>
      </div>
    </div>

    <!-- Floating Register Modal -->
    <div v-if="activeModal === 'register'" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <Suspense>
          <component :is="RegisterPage" />
        </Suspense>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineAsyncComponent } from "vue";
import Logo from "~/components/Logo.vue";

// Load login and register pages lazily into modals
const LoginPage = defineAsyncComponent(() => import("~/pages/login.vue"));
const RegisterPage = defineAsyncComponent(() => import("~/pages/register.vue"));

const activeModal = ref(null);

function openModal(type) {
  activeModal.value = type;
}

function closeModal() {
  activeModal.value = null;
}

// Feature list
const features = [
  { icon: "📅", title: "Automated Scheduling", desc: "Efficiently manage class routines with conflict detection and real-time updates." },
  { icon: "🔔", title: "Real-time Notifications", desc: "Stay informed with instant alerts on schedule changes and updates." },
  { icon: "👥", title: "Multi-role Access", desc: "Role-based dashboards for admins, faculty, and students." },
  { icon: "📊", title: "Reports & Analytics", desc: "Generate downloadable schedules and comprehensive reports." },
  { icon: "🧭", title: "Smart Conflict Detection", desc: "Automatically identifies overlapping schedules and prevents timetable clashes." },
  { icon: "💬", title: "Feedback & Communication", desc: "Enable students and faculty to share feedback directly within the system." },
  { icon: "☁️", title: "Cloud Backup & Sync", desc: "Securely store and sync all data across devices and sessions." },
  { icon: "🔐", title: "Secure Authentication", desc: "Protect user data with encrypted, role-based authentication." },
];
</script>

<style scoped>
/* Background */
.landing-page {
  min-height: 100vh;
  /* deeper purple hero to match reference */
  background: linear-gradient(135deg, #5b00d6 0%, #7a14d6 100%);
  /* reduce top padding so content appears higher on the page */
  padding: 1.2rem 1rem 2.5rem 1rem;
  overflow-x: hidden;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Hero Grid */
.hero-grid {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 1.2rem;
  align-items: center;
  /* allow the whole content to fit in a single viewport more easily */
  min-height: 50vh;
}

.hero-section {
  color: white;
  padding: 0.1rem 0;
  /* lift hero content upward so more fits in the first viewport */
  transform: translateY(-34px);
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 0.25rem;
  letter-spacing: -1px;
  display: inline-block;
  background: #0b5fe6; /* blue highlight behind the title like the screenshot */
  padding: 0.12rem 0.6rem;
  border-radius: 4px;
  box-shadow: 0 6px 18px rgba(11,95,230,0.12);
}

.hero-subtitle-main {
  font-size: 1.18rem;
  font-weight: 700;
  margin-bottom: 0.55rem;
  color: #e6eefc;
  display: inline-block;
  background: rgba(11,95,230,0.9);
  padding: 0.08rem 0.5rem;
  border-radius: 3px;
}

.hero-author {
  font-size: 0.95rem;
  margin-bottom: 0.6rem;
  color: #ffffff;
  display: inline-block;
  background: rgba(11,95,230,0.95);
  padding: 0.18rem 0.6rem;
  border-radius: 4px;
  font-weight: 700;
  text-shadow: 0 1px 1px rgba(0,0,0,0.35);
}

.hero-author strong {
  font-weight: 800;
  color: #fff;
}

.hero-subtitle {
  font-size: 0.96rem;
  margin-bottom: 0.95rem;
  opacity: 0.98;
  max-width: 640px;
  line-height: 1.45;
}

.hero-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.btn-lg {
  padding: 0.85rem 1.6rem;
  font-size: 0.98rem;
  border-radius: 0.6rem;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.btn-primary {
  background: linear-gradient(90deg, var(--accent), var(--accent-dark));
  color: white;
  border: none;
  box-shadow: 0 10px 24px rgba(255,42,143,0.18);
}

.btn-primary:hover {
  transform: translateY(-3px);
}

.btn-outline {
  border: 2px solid rgba(255,255,255,0.85);
  color: white;
  background: transparent;
}

.btn-outline:hover {
  background: rgba(255,255,255,0.95);
  color: var(--accent);
  transform: translateY(-3px);
}

.hero-features-quick {
  margin-top: 0.9rem;
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.pill {
  background: rgba(255,255,255,0.12);
  color: #fff;
  padding: 0.45rem 0.8rem;
  border-radius: 999px;
  font-weight: 600;
  font-size: 0.9rem;
}

/* Illustration */
.hero-illustration {
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-illustration {
  width: 320px;
  max-width: 100%;
  margin-top: -18px; /* nudge the illustration up a bit to match lifted text */
  filter: drop-shadow(0 12px 22px rgba(0,0,0,0.22));
}

/* Features grid */
.features-wrapper {
  /* different background for the features area to visually separate sections */
  background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
  padding: 0.8rem;
  border-radius: 14px;
  /* pull up into the hero for a compact, single-window feel */
  margin-top: -3.2rem;
  box-shadow: 0 18px 40px rgba(2,6,23,0.14);
}

.features-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
  margin-top: 0;
  padding: 0.5rem;
}

.feature-card {
  background: rgba(255,255,255,0.98);
  border-radius: 12px;
  padding: 1rem;
  text-align: left;
  transition: transform 0.22s ease, box-shadow 0.22s ease;
  box-shadow: 0 6px 14px rgba(2,6,23,0.08);
  transform: translateY(-10px); /* lift cards slightly so icons/text appear higher */
}

.feature-card:hover {
  transform: translateY(-12px);
  box-shadow: 0 18px 30px rgba(2,6,23,0.14);
}

.feature-icon {
  font-size: 1.6rem;
  width: 48px;
  height: 48px;
  display: inline-grid;
  place-items: center;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(14,165,233,0.14), rgba(236,72,153,0.06));
  margin-bottom: 0.8rem;
}

.feature-card h3 {
  margin: 0.25rem 0 0.5rem 0;
  font-size: 1.05rem;
}

.feature-card p {
  margin: 0;
  color: #374151;
  font-size: 0.95rem;
}

/* Modals remain similar */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(10, 10, 10, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: rgba(255, 255, 255, 0.98);
  padding: 1.75rem;
  border-radius: 0.9rem;
  width: 92%;
  max-width: 520px;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

@media (max-width: 900px) {
  .hero-grid {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero-illustration {
    margin-top: 1rem;
  }
}

</style>
