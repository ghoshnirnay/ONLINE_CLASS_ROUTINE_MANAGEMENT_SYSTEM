<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-blue-50">
    <!-- Header -->
    <Header :user="user" @logout="handleLogout" />

    <!-- Page Content -->
    <div class="page-content container mx-auto px-6 py-12">
      <h1 class="text-4xl font-bold text-center text-gray-800 mb-10 animate-fade-in-down">
        ⚙️ System Management
      </h1>

      <p class="text-center text-gray-600 mb-12 max-w-2xl mx-auto animate-fade-in">
        Manage every core aspect of your institution's routine system — from scheduling to user access,
        with smooth control and automation.
      </p>

      <!-- Grid Cards -->
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <nuxt-link
          v-for="item in items"
          :key="item.title"
          :to="item.link"
          class="card group animate-fade-in-up bg-white rounded-2xl shadow-md hover:shadow-xl hover:-translate-y-2 transition-all duration-300 p-8 text-center border border-gray-100"
        >
          <div class="text-5xl mb-4 text-indigo-600 group-hover:scale-110 transition-transform">
            {{ item.icon }}
          </div>
          <h3 class="text-xl font-semibold text-gray-800 mb-2">{{ item.title }}</h3>
          <p class="text-gray-500 text-sm">{{ item.desc }}</p>
        </nuxt-link>
      </div>
    </div>
  </div>
</template>

<script setup>
const items = [
  { icon: "📖", title: "Subjects", desc: "Manage courses and subjects", link: "/manage/subjects" },
  { icon: "🚪", title: "Rooms", desc: "Manage classrooms and labs", link: "/manage/rooms" },
  { icon: "⏰", title: "Time Slots", desc: "Configure class timings", link: "/manage/time-slots" },
  { icon: "📅", title: "Routines", desc: "Manage class schedules", link: "/manage/routines" },
  { icon: "🔄", title: "Swap Requests", desc: "Review and approve swap requests", link: "/manage/swap-requests" },
  { icon: "👥", title: "Users", desc: "Manage user accounts and roles", link: "/manage/users" },
  { icon: "💬", title: "Feedback", desc: "View and respond to user feedback", link: "/manage/feedback" },
];
</script>

<style scoped>
/* ✅ Animations */
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fade-in-down {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in { animation: fade-in 1s ease-in-out; }
.animate-fade-in-up { animation: fade-in-up 0.8s ease-in-out; }
.animate-fade-in-down { animation: fade-in-down 0.8s ease-in-out; }

/* ✅ Layout Styles */
.page-content {
  min-height: calc(100vh - 80px);
}

/* ✅ Card Styling */
.card {
  text-decoration: none;
  color: inherit;
  background: white;
  border-radius: 1rem;
  transition: all 0.3s ease-in-out;
}

.card:hover {
  background: linear-gradient(135deg, #eef2ff, #ffffff);
}

/* ✅ Typography */
h1.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}
</style>
