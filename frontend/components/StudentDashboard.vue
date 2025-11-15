<template>
  <div v-if="localUser && localUser.name">
  
    <!-- ✅ Semester & Section Setup -->
    <div class="card setup-box" v-if="!localUser.semester || !localUser.section">
      <h3>Select Your Semester & Section</h3>

      <div class="form-group">
        <label>Semester</label>
        <select v-model="form.semester" class="form-select">
          <option disabled value="">Select Semester</option>
          <option v-for="n in 8" :key="n" :value="n">{{ n }}</option>
        </select>
      </div>

      <div class="form-group">
        <label>Section</label>
        <input
          v-model="form.section"
          class="form-input"
          placeholder="Ex: A / B / C"
        />
      </div>

      <button class="btn btn-primary" @click="saveProfile">Save</button>
    </div>

    <!-- ✅ Routine Display Section -->
    <div v-else>
      <div class="section-header">
        <h3>My Weekly Class Routine</h3>
        <button class="btn btn-outline" @click="editProfile">
          Change Details
        </button>
      </div>

      <!-- 🎨 COLORFUL FILTER BAR -->
      <div class="card filter-box">
        <div class="filter-row">
          <div class="form-group">
            <label>Day Filter</label>
            <select v-model="filterDay" class="form-select">
              <option value="">All Days</option>
              <option>Monday</option>
              <option>Tuesday</option>
              <option>Wednesday</option>
              <option>Thursday</option>
              <option>Friday</option>
              <option>Saturday</option>
            </select>
          </div>

          <div class="form-group">
            <label>Search Subject</label>
            <input
              v-model="filterSubject"
              type="text"
              class="form-input"
              placeholder="Enter subject name"
            />
          </div>

          <button class="btn btn-primary export-btn" @click="exportPDF">
            Export PDF
          </button>
        </div>
      </div>

      <!-- ✅ Table View -->
      <div class="card table-container">
        <div
          v-for="(classes, day) in groupedRoutines"
          :key="day"
          class="day-section"
          :class="day.toLowerCase()"
        >
          <h4 class="day-title">{{ day }}</h4>

          <table class="routine-table">
            <thead>
              <tr>
                <th>Start Time</th>
                <th>End Time</th>
                <th>Subject</th>
                <th>Room</th>
                <th>Faculty</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in classes" :key="r.id">
                <td>{{ r.start_time }}</td>
                <td>{{ r.end_time }}</td>
                <td>{{ r.subject }}</td>
                <td>{{ r.room }}</td>
                <td>{{ r.faculty_name || "—" }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <p v-if="filteredRoutines.length === 0" class="no-data">
          No routines found.
        </p>
      </div>
    </div>
  </div>

  <div v-else class="loading-screen">
    <p>Loading student data...</p>
  </div>
</template>

<script>
import jsPDF from "jspdf";
import "jspdf-autotable";

export default {
  props: ["user"],

  data() {
    return {
      localUser: this.user
        ? { ...this.user }
        : { name: "", semester: "", section: "", id: null, department_id: null },
      routines: [],
      form: { semester: "", section: "" },
      filterDay: "",
      filterSubject: "",
    };
  },

  computed: {
    filteredRoutines() {
      let r = this.routines || [];
      if (this.filterDay) r = r.filter((x) => x.day === this.filterDay);
      if (this.filterSubject)
        r = r.filter((x) =>
          x.subject.toLowerCase().includes(this.filterSubject.toLowerCase())
        );
      return r;
    },

    groupedRoutines() {
      const groups = {};
      (this.filteredRoutines || []).forEach((r) => {
        if (!groups[r.day]) groups[r.day] = [];
        groups[r.day].push(r);
      });
      Object.keys(groups).forEach((day) => {
        groups[day].sort((a, b) => a.start_time.localeCompare(b.start_time));
      });
      return groups;
    },
  },

  mounted() {
    const saved = localStorage.getItem("user");
    if (saved && !this.localUser.name) {
      this.localUser = JSON.parse(saved);
    }

    if (!this.localUser.department_id) {
      this.localUser.department_id = 1;
    }

    if (this.localUser.semester && this.localUser.section) {
      this.fetchRoutine();
    }
  },

  methods: {
    async saveProfile() {
      try {
        this.localUser.semester = this.form.semester;
        this.localUser.section = this.form.section;
        localStorage.setItem("user", JSON.stringify(this.localUser));

        await this.fetchRoutine();
        this.$forceUpdate();
      } catch (err) {
        console.error("Failed to save profile:", err);
      }
    },

    editProfile() {
      this.localUser.semester = null;
      this.localUser.section = null;
      localStorage.setItem("user", JSON.stringify(this.localUser));
    },

    async fetchRoutine() {
      try {
        const { semester, section, department_id } = this.localUser;

        const params = new URLSearchParams({
          role: "student",
          department_id,
          semester,
          section,
        }).toString();

        const url = `http://127.0.0.1:5000/api/routines?${params}`;

        const res = await fetch(url);
        const data = await res.json();

        this.routines = Array.isArray(data) ? data : [];
      } catch (err) {
        console.error("Failed to fetch routines:", err);
      }
    },

    exportPDF() {
      const doc = new jsPDF();
      doc.setFontSize(16);
      doc.text(`Class Routine - ${this.localUser.name}`, 14, 15);

      const rows = (this.filteredRoutines || []).map((r) => [
        r.day,
        r.start_time,
        r.end_time,
        r.subject,
        r.room,
        r.faculty_name || "—",
      ]);

      doc.autoTable({
        head: [["Day", "Start", "End", "Subject", "Room", "Faculty"]],
        body: rows,
        startY: 25,
      });

      doc.save(`Routine_${this.localUser.name}.pdf`);
    },
  },
};
</script>

<style scoped>
.loading-screen {
  text-align: center;
  padding: 4rem;
  font-size: 1.2rem;
  color: #555;
}

.setup-box {
  margin: 1rem 0;
  padding: 1.5rem;
}

.section-header {
  margin: 1rem 0;
  display: flex;
  justify-content: space-between;
}

/* 🎨 FILTER BOX STYLING */
.filter-box {
  margin-bottom: 1rem;
  padding: 1.2rem;
  background: linear-gradient(135deg, #e3f2ff, #f7faff);
  border-radius: 12px;
  border: 1px solid #d0e6ff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.filter-box label {
  font-weight: 600;
  color: #1e293b;
}

.filter-box .form-input,
.filter-box .form-select {
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 0.55rem 0.7rem;
  font-size: 0.95rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}

.export-btn {
  background: #ff006e;
  border-radius: 8px;
  padding: 0.55rem 1rem;
  font-weight: 600;
  transition: 0.2s;
}

.export-btn:hover {
  transform: translateY(-2px);
  opacity: 0.9;
}

/* ============================================
   🎨 COLORFUL DAY HEADERS
============================================ */
.day-section {
  border-radius: 0.5rem;
  overflow: hidden;
  margin-bottom: 2rem;
}

.monday .day-title {
  background-color: #2563eb;
  color: white;
}

.tuesday .day-title {
  background-color: #ef4444;
  color: white;
}

.wednesday .day-title {
  background-color: #22c55e;
  color: white;
}

.thursday .day-title {
  background-color: #a855f7;
  color: white;
}

.friday .day-title {
  background-color: #facc15;
  color: black;
}

.saturday .day-title {
  background-color: #14b8a6;
  color: white;
}

.day-title {
  font-size: 1.1rem;
  font-weight: 600;
  padding: 0.5rem 1rem;
}

.table-container {
  margin-top: 1rem;
}

.routine-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 0 0 0.5rem 0.5rem;
  overflow: hidden;
}

.routine-table th,
.routine-table td {
  border: 1px solid #e5e7eb;
  padding: 0.75rem;
  text-align: center;
  font-size: 0.95rem;
}

.routine-table th {
  background-color: #f3f4f6;
  font-weight: 600;
}

.routine-table tr:nth-child(even) {
  background-color: #f9fafb;
}

.routine-table tr:hover {
  background-color: #eef2ff;
  transition: 0.2s;
}

.no-data {
  text-align: center;
  color: #6b7280;
  margin-top: 1rem;
}
</style>
