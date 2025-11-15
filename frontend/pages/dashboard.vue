<template>
  <div>
    <!-- ✅ Header -->
    <Header :user="user" @logout="handleLogout" />

    <div class="dashboard-content">
      <div class="container">

        <!-- ✅ Loading Spinner -->
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
        </div>

        <!-- ✅ Dashboard Loaded -->
        <div v-else>
          <div class="dashboard-header">
            <div>
              <h1 class="dashboard-title">Welcome, {{ user.name }}</h1>
              <p class="dashboard-subtitle">{{ getRoleLabel(user.role) }} Dashboard</p>
            </div>

            <!-- ✅ Role Badge + Logout -->
            <div class="header-right">
              <span class="role-badge">{{ getRoleLabel(user.role) }}</span>
              <button class="btn btn-logout" @click="handleLogout">Logout</button>
            </div>
          </div>

          <!-- ✅ Admin Dashboard -->
          <div v-if="user.role === 'admin'" class="dashboard-grid">
            <AdminDashboard />
          </div>

          <!-- ✅ Faculty Dashboard -->
          <div v-else-if="user.role === 'faculty'" class="dashboard-grid">
            <FacultyDashboard :user="user" />
          </div>

          <!-- ✅ Student Dashboard -->
          <div v-else-if="user.role === 'student'" class="dashboard-grid">
            <StudentDashboard :user="user" />
          </div>

          <!-- ⚠️ Fallback -->
          <div v-else class="error-card card">
            <p>⚠️ Unknown role detected. Please contact admin.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminDashboard from "@/components/AdminDashboard.vue";
import FacultyDashboard from "@/components/FacultyDashboard.vue";
import StudentDashboard from "@/components/StudentDashboard.vue";
import Header from "@/components/Header.vue";

export default {
  components: {
    AdminDashboard,
    FacultyDashboard,
    StudentDashboard,
    Header
  },

  data() {
    return {
      user: null,
      loading: true
    };
  },

  mounted() {
    this.loadUser();
  },

  methods: {
    loadUser() {
      const storedUser = localStorage.getItem("user");
      if (!storedUser) {
        this.$router.push("/login");
        return;
      }

      try {
        this.user = JSON.parse(storedUser);

        // ✅ Ensure department_id exists (fallback)
        if (!this.user.department_id) {
          this.user.department_id = 1; // CSE default
          localStorage.setItem("user", JSON.stringify(this.user));
        }

        this.loading = false;
      } catch (error) {
        console.warn("Invalid user data, resetting session:", error);
        localStorage.removeItem("user");
        this.$router.push("/login");
      }
    },

    handleLogout() {
      localStorage.removeItem("user");
      this.$router.push("/login");
    },

    getRoleLabel(role) {
      const labels = {
        admin: "Administrator",
        faculty: "Faculty Member",
        student: "Student"
      };
      return labels[role] || "User";
    }
  }
};
</script>

<style scoped>
.dashboard-content {
  padding: 2rem 0;
  min-height: calc(100vh - 80px);
  background: #f9fafb;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.dashboard-title {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.25rem;
}

.dashboard-subtitle {
  font-size: 1rem;
  color: #6b7280;
}

.role-badge {
  background: #3b82f6;
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: 0.5rem;
  padding: 0.25rem 0.75rem;
}

.dashboard-grid {
  display: grid;
  gap: 1.5rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.2);
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 2rem auto;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.btn-logout {
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-weight: 500;
  transition: 0.2s;
}

.btn-logout:hover {
  background: #dc2626;
}

.error-card {
  background: #fee2e2;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  color: #b91c1c;
  font-weight: 500;
}
</style>
