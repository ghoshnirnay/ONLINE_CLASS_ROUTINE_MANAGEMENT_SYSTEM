<template>
  <div>
    <!-- ✅ Stats Section -->
    <div class="stats-grid">
      <div class="stat-card card" v-for="s in statList" :key="s.label">
        <div class="stat-icon" :style="{ background: s.bg }">{{ s.icon }}</div>
        <div class="stat-content">
          <div class="stat-value">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </div>
      </div>
    </div>

    <!-- ✅ Quick Actions -->
    <div class="dashboard-actions">
      <h3 class="section-title">Quick Actions</h3>

      <div class="action-grid">
        <nuxt-link to="/manage/routines/create" class="action-card card">
          <span class="action-icon">➕</span>
          <span class="action-label">Create Routine</span>
        </nuxt-link>

        <nuxt-link to="/manage/subjects" class="action-card card">
          <span class="action-icon">📖</span>
          <span class="action-label">Manage Subjects</span>
        </nuxt-link>

        <nuxt-link to="/manage/rooms" class="action-card card">
          <span class="action-icon">🚪</span>
          <span class="action-label">Manage Rooms</span>
        </nuxt-link>

        <nuxt-link to="/manage/time-slots" class="action-card card">
          <span class="action-icon">⏰</span>
          <span class="action-label">Time Slots</span>
        </nuxt-link>

        <nuxt-link to="/manage/swap-requests" class="action-card card">
          <span class="action-icon">🔄</span>
          <span class="action-label">Swap Requests</span>
        </nuxt-link>

        <nuxt-link to="/manage/faculty-subjects" class="action-card card">
          <span class="action-icon">👨‍🏫</span>
          <span class="action-label">Assign Faculty Subjects</span>
        </nuxt-link>
      </div>
    </div>

    <!-- ✅ View Routines -->
    <div class="dashboard-routines">
      <h3 class="section-title">View Routines</h3>

      <!-- Filters -->
      <div class="filter-bar">
        <select v-model="selectedDept" @change="filterRoutines">
          <option value="">All Departments</option>
          <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
        </select>

        <select v-model="selectedSem" @change="filterRoutines">
          <option value="">All Semesters</option>
          <option v-for="s in [1,2,3,4,5,6,7,8]" :key="s">{{ s }}</option>
        </select>

        <select v-model="selectedSec" @change="filterRoutines">
          <option value="">All Sections</option>
          <option v-for="sec in ['A','B','C']" :key="sec">{{ sec }}</option>
        </select>
      </div>

      <!-- ✅ Routines Table -->
      <table class="routine-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Day</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Subject</th>
            <th>Faculty</th>
            <th>Room</th>
            <th>Department</th>
            <th>Semester</th>
            <th>Section</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="r in filteredRoutines" :key="r.id">
            <td>{{ r.id }}</td>
            <td>{{ r.day }}</td>
            <td>{{ r.start_time }}</td>
            <td>{{ r.end_time }}</td>
            <td>{{ r.subject }}</td>
            <td>{{ r.faculty_name || "—" }}</td>
            <td>{{ r.room || "—" }}</td>
            <td>{{ getDepartmentName(r.department_id) }}</td>
            <td>{{ r.semester }}</td>
            <td>{{ r.section }}</td>
            <td>
              <button class="btn btn-danger btn-sm" @click="deleteRoutine(r.id)">
                🗑 Delete
              </button>
            </td>
          </tr>

          <tr v-if="filteredRoutines.length === 0">
            <td colspan="11" class="no-data">No routines found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      stats: {
        totalRoutines: 0,
        totalFaculty: 0,
        totalStudents: 0,
        pendingSwaps: 0,
      },
      routines: [],
      filteredRoutines: [],
      departments: [
        { id: 1, name: "CSE" },
        { id: 2, name: "ECE" },
        { id: 3, name: "EEE" },
        { id: 4, name: "ME" },
        { id: 5, name: "CE" },
      ],
      selectedDept: "",
      selectedSem: "",
      selectedSec: "",
      API_BASE: "http://127.0.0.1:5000/api",
    };
  },

  computed: {
    statList() {
      return [
        { icon: "📚", label: "Total Routines", value: this.stats.totalRoutines, bg: "#dbeafe" },
        { icon: "👨‍🏫", label: "Faculty Members", value: this.stats.totalFaculty, bg: "#d1fae5" },
        { icon: "👥", label: "Students", value: this.stats.totalStudents, bg: "#fef3c7" },
        { icon: "🔄", label: "Pending Swaps", value: this.stats.pendingSwaps, bg: "#fee2e2" },
      ];
    },
  },

  async mounted() {
    await this.fetchStats();
    await this.fetchRoutines();
  },

  methods: {
    async fetchStats() {
      const routines = await (await fetch(`${this.API_BASE}/routines`)).json();
      const users = await (await fetch(`${this.API_BASE}/users`)).json();

      this.stats.totalRoutines = routines.length;
      this.stats.totalFaculty = users.filter((u) => u.role === "faculty").length;
      this.stats.totalStudents = users.filter((u) => u.role === "student").length;
    },

    async fetchRoutines() {
      try {
        const res = await fetch(`${this.API_BASE}/routines`);
        const data = await res.json();
        this.routines = data;
        this.filteredRoutines = data;
      } catch (err) {
        console.error("Failed to fetch routines:", err);
      }
    },

    filterRoutines() {
      this.filteredRoutines = this.routines.filter((r) => {
        const dept = r.department_id;
        const sem = r.semester;
        const sec = r.section;
        return (
          (!this.selectedDept || Number(dept) === Number(this.selectedDept)) &&
          (!this.selectedSem || String(sem) === String(this.selectedSem)) &&
          (!this.selectedSec || sec === this.selectedSec)
        );
      });
    },

    getDepartmentName(id) {
      const dept = this.departments.find((d) => d.id === id);
      return dept ? dept.name : id;
    },

    // ✅ Delete Routine (Fixed)
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
        console.error("Delete routine failed:", err);
        alert("⚠️ Server error while deleting routine");
      }
    },
  },
};
</script>

<style scoped>
/* styling same as before */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}
.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
}
.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
}
.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--gray-900);
}
.stat-label {
  font-size: 0.875rem;
  color: var(--gray-600);
}
.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
}
.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
}
.action-card {
  text-decoration: none;
  padding: 1.25rem;
  text-align: center;
  border-radius: 8px;
  transition: 0.2s;
}
.filter-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}
.routine-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
}
.routine-table th,
.routine-table td {
  border: 1px solid #ddd;
  padding: 0.75rem;
  text-align: center;
}
.btn-danger {
  background-color: #dc2626;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.3rem 0.6rem;
  cursor: pointer;
}
.btn-danger:hover {
  background-color: #b91c1c;
}
.no-data {
  text-align: center;
  padding: 1rem;
  color: gray;
}
</style>
