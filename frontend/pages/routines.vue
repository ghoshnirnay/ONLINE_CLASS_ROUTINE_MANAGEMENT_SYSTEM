<template>
  <div>
    <Header />

    <div class="page-content">
      <div class="container">
        <div class="page-header">
          <h1 class="page-title">Class Routines</h1>

          <div class="header-buttons">
            <nuxt-link
              v-if="user?.role === 'admin'"
              to="/manage/routine/create"
              class="btn btn-primary"
            >
              + Create New Routine
            </nuxt-link>
            <button class="btn btn-secondary" @click="fetchRoutines">🔄 Refresh</button>
          </div>
        </div>

        <!-- Filter Card -->
        <div class="filter-card card">
          <div class="filter-grid">
            <div class="form-group">
              <label class="form-label">Department</label>
              <select v-model="filters.department_id" class="form-select">
                <option value="">All Departments</option>
                <option
                  v-for="dept in departments"
                  :key="dept.id"
                  :value="dept.id"
                >
                  {{ dept.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Semester</label>
              <select v-model="filters.semester" class="form-select">
                <option value="">All</option>
                <option v-for="n in 8" :key="n">{{ n }}</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Section</label>
              <select v-model="filters.section" class="form-select">
                <option value="">All</option>
                <option>A</option>
                <option>B</option>
                <option>C</option>
              </select>
            </div>

            <button class="btn btn-primary" @click="fetchRoutines">
              Apply Filter
            </button>
          </div>
        </div>

        <!-- Loading Spinner -->
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
        </div>

        <!-- Table -->
        <div v-else class="card">
          <table class="table">
            <thead>
              <tr>
                <th>Day</th>
                <th>Start</th>
                <th>End</th>
                <th>Subject</th>
                <th>Faculty</th>
                <th>Room</th>
                <th>Semester</th>
                <th>Section</th>
                <th v-if="user?.role === 'admin'">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="routine in routines" :key="routine.id">
                <td>{{ routine.day }}</td>
                <td>{{ routine.start_time }}</td>
                <td>{{ routine.end_time }}</td>
                <td>{{ routine.subject }}</td>
                <td>{{ routine.faculty_name || '—' }}</td>
                <td>{{ routine.room || '—' }}</td>
                <td>{{ routine.semester }}</td>
                <td>{{ routine.section }}</td>
                <td v-if="user?.role === 'admin'">
                  <button
                    class="btn btn-sm btn-outline btn-danger"
                    @click="deleteRoutine(routine.id)"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <div v-if="routines.length === 0" class="empty-state">
            No routines found
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: JSON.parse(localStorage.getItem("user")) || null,
      routines: [],
      departments: [],
      filters: {
        department_id: "",
        semester: "",
        section: "",
      },
      loading: true,
      API_BASE: "http://127.0.0.1:5000/api",
    };
  },
  async mounted() {
    await this.fetchDepartments();
    await this.fetchRoutines();

    // ✅ Automatically refresh when window regains focus
    window.addEventListener("focus", () => {
      this.fetchRoutines();
    });
  },
  methods: {
    async fetchDepartments() {
      try {
        const res = await fetch(`${this.API_BASE}/departments`);
        this.departments = await res.json();
      } catch (err) {
        console.error("Error fetching departments:", err);
      }
    },
    async fetchRoutines() {
      this.loading = true;
      try {
        const params = new URLSearchParams();
        if (this.filters.department_id)
          params.append("department_id", this.filters.department_id);
        if (this.filters.semester)
          params.append("semester", this.filters.semester);
        if (this.filters.section)
          params.append("section", this.filters.section);

        const res = await fetch(`${this.API_BASE}/routines?${params.toString()}`);
        this.routines = await res.json();
      } catch (err) {
        console.error("Error fetching routines:", err);
      } finally {
        this.loading = false;
      }
    },
    async deleteRoutine(id) {
      if (!confirm("Are you sure you want to delete this routine?")) return;
      try {
        const res = await fetch(`${this.API_BASE}/routines/${id}`, {
          method: "DELETE",
        });
        const result = await res.json();
        if (result.deleted || result.success) {
          alert("✅ Routine deleted successfully");
          await this.fetchRoutines();
        } else {
          alert(result.error || "❌ Failed to delete routine");
        }
      } catch (err) {
        console.error("Error deleting routine:", err);
        alert("⚠️ Server error while deleting routine");
      }
    },
  },
  watch: {
    filters: {
      deep: true,
      handler() {
        this.fetchRoutines();
      },
    },
  },
};
</script>

<style scoped>
.page-content {
  padding: 2rem 0;
}
.header-buttons {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.btn-secondary {
  background: #6b7280;
  color: white;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  cursor: pointer;
}
.btn-secondary:hover {
  background: #4b5563;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}
.page-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #2563eb;
}
.filter-card {
  margin-bottom: 2rem;
  padding: 1.5rem;
}
.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}
.table {
  width: 100%;
  border-collapse: collapse;
}
.table th {
  background: #2563eb;
  color: #fff;
  padding: 0.75rem;
  text-transform: uppercase;
}
.table td {
  padding: 0.75rem;
  border-bottom: 1px solid #e5e7eb;
  text-align: center;
}
tr:hover {
  background: #f3f4f6;
}
.btn-sm {
  padding: 0.4rem 0.7rem;
  font-size: 0.85rem;
}
.btn-danger {
  border: 1px solid #ef4444;
  color: #ef4444;
}
.btn-danger:hover {
  background: #ef4444;
  color: #fff;
}
.empty-state {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
  font-weight: 500;
}
.spinner {
  width: 36px;
  height: 36px;
  border: 4px solid #e5e7eb;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 2rem auto;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
