<template>
  <div class="faculty-dashboard">
  
    <!-- ✨ Assigned Subjects -->
    <div class="assigned-subjects card">
      <h3 class="section-header">My Assigned Subjects</h3>
      <table class="routine-table">
        <thead>
          <tr><th>Subject</th></tr>
        </thead>
        <tbody>
          <tr v-for="s in assignedSubjects" :key="s.subject_name">
            <td>{{ s.subject_name }}</td>
          </tr>
          <tr v-if="assignedSubjects.length === 0">
            <td class="no-data">No subjects assigned yet.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ✨ Weekly Routine -->
    <div class="faculty-routines card">
      <h3 class="section-header">My Weekly Routine</h3>
      <table class="routine-table">
        <thead>
          <tr>
            <th>Day</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Subject</th>
            <th>Room</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in routines" :key="r.id">
            <td>{{ r.day }}</td>
            <td>{{ r.start_time }}</td>
            <td>{{ r.end_time }}</td>
            <td>{{ r.subject }}</td>
            <td>{{ r.room || '—' }}</td>
          </tr>
          <tr v-if="routines.length === 0">
            <td colspan="5" class="no-data">No routines found.</td>
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
      user: JSON.parse(localStorage.getItem("user")) || {},
      routines: [],
      assignedSubjects: [],
      API_BASE: "http://127.0.0.1:5000/api",
    };
  },

  async mounted() {
    if (!this.user?.id) return;
    await this.fetchAssignedSubjects();
    await this.fetchRoutines();
  },

  methods: {
    async fetchAssignedSubjects() {
      try {
        const res = await fetch(`${this.API_BASE}/faculty-subjects/${this.user.id}`);
        this.assignedSubjects = await res.json();
      } catch (err) {
        console.error("Failed to fetch assigned subjects:", err);
      }
    },

    async fetchRoutines() {
      try {
        const res = await fetch(
          `${this.API_BASE}/routines?role=faculty&name=${encodeURIComponent(this.user.name)}`
        );
        this.routines = await res.json();
      } catch (err) {
        console.error("Failed to fetch routines:", err);
      }
    },
  },
};
</script>

<style scoped>
.faculty-dashboard {
  padding: 2rem;
}

/* ✨ Card look improved */
.card {
  background: #ffffff;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border-radius: 14px;
  border: 1px solid #e3e8ef;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

/* ✨ Colored Section Header */
.section-header {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  padding-bottom: 0.4rem;
  border-left: 6px solid #2563eb;
  padding-left: 0.8rem;
  color: #1e293b;
}

/* ✨ Better Table Design */
.routine-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  overflow: hidden;
  border-radius: 8px;
}

.routine-table th {
  background: #f1f5ff;
  color: #1e3a8a;
  padding: 0.85rem;
  font-weight: 700;
  border-bottom: 2px solid #dbeafe;
}

.routine-table td {
  border: 1px solid #e5e7eb;
  padding: 0.75rem;
  text-align: center;
  font-size: 0.95rem;
}

/* alternate row color */
.routine-table tr:nth-child(even) {
  background: #f9fafb;
}

.routine-table tr:hover {
  background: #eef4ff;
  transition: 0.2s;
}

/* ✨ No Data Style */
.no-data {
  text-align: center;
  color: #6b7280;
  padding: 1rem;
}
</style>
