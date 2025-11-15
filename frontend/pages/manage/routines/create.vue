<template>
  <div>
    <Header />

    <div class="page-content">
      <div class="container">

        <h1 class="page-title">Create Routine</h1>

        <!-- ✅ SUCCESS MESSAGE -->
        <div v-if="success" class="alert alert-success">{{ success }}</div>

        <!-- ❌ ERROR MESSAGE -->
        <div v-if="error" class="alert alert-error">{{ error }}</div>

        <form @submit.prevent="submitRoutine" class="form">

          <!-- Department -->
          <div class="form-group">
            <label>Department</label>
            <select v-model="department_id" class="form-input" required>
              <option disabled value="">Select Department</option>
              <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
            </select>
          </div>

          <!-- Semester -->
          <div class="form-group">
            <label>Semester</label>
            <input v-model="semester" type="number" min="1" max="8" class="form-input" required />
          </div>

          <!-- Section -->
          <div class="form-group">
            <label>Section</label>
            <input v-model="section" class="form-input" placeholder="Ex: A / B / C" required />
          </div>

          <!-- Day -->
          <div class="form-group">
            <label>Day</label>
            <select v-model="day" class="form-input" required>
              <option value="Monday">Monday</option>
              <option value="Tuesday">Tuesday</option>
              <option value="Wednesday">Wednesday</option>
              <option value="Thursday">Thursday</option>
              <option value="Friday">Friday</option>
              <option value="Saturday">Saturday</option>
            </select>
          </div>

          <!-- ✅ Subject -->
          <div class="form-group">
            <label>Subject</label>
            <select v-model="subject" class="form-input" required @change="handleSubjectChange">
              <option disabled value="">Select Subject</option>
              <option v-for="s in subjects" :key="s.id" :value="s.name">{{ s.name }}</option>
              <option value="Tiffin Break">🍱 Tiffin Break</option> <!-- ✅ Added -->
            </select>
          </div>

          <!-- ✅ Faculty -->
          <div class="form-group">
            <label>Faculty</label>
            <select v-model="faculty_name" class="form-input" :disabled="isTiffin">
              <option disabled value="">Select Faculty (Optional)</option>
              <option v-for="f in faculties" :key="f.id" :value="f.name">{{ f.name }}</option>
            </select>
          </div>

          <!-- ✅ Room -->
          <div class="form-group">
            <label>Room</label>
            <select v-model="room" class="form-input" :disabled="isTiffin" :required="!isTiffin">
              <option disabled value="">Select Room</option>
              <option v-for="r in rooms" :key="r.id" :value="r.name">{{ r.name }}</option>
            </select>
          </div>

          <!-- Start / End Time -->
          <div class="form-group">
            <label>Start Time</label>
            <input v-model="start_time" type="time" class="form-input" required />
          </div>

          <div class="form-group">
            <label>End Time</label>
            <input v-model="end_time" type="time" class="form-input" required />
          </div>

          <button type="submit" class="btn btn-primary">Save Routine</button>
        </form>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      departments: [],
      subjects: [],
      rooms: [],
      faculties: [],

      department_id: "",
      semester: "",
      section: "",
      day: "",
      subject: "",
      room: "",
      start_time: "",
      end_time: "",
      faculty_name: "",

      success: null,
      error: null
    };
  },

  computed: {
    // ✅ Detect if current subject is "Tiffin Break"
    isTiffin() {
      return this.subject === "Tiffin Break";
    }
  },

  async mounted() {
    this.departments = await this.$api.departments();
    this.subjects = await this.$api.subjects();
    this.rooms = await this.$api.rooms();
  },

  methods: {
    // ✅ Handle subject change
    async handleSubjectChange() {
      if (this.isTiffin) {
        this.faculties = [];
        this.faculty_name = "";
        this.room = "";
        return;
      }

      if (!this.subject) return;
      const res = await fetch(`http://127.0.0.1:5000/api/faculty-by-subject/${this.subject}`);
      this.faculties = await res.json();
    },

    // ✅ Submit routine
    async submitRoutine() {
      this.error = null;
      this.success = null;

      const payload = {
        department_id: this.department_id,
        semester: this.semester,
        section: this.section,
        day: this.day,
        subject: this.subject,
        start_time: this.start_time,
        end_time: this.end_time,
      };

      // ✅ Only send faculty and room if not tiffin
      if (!this.isTiffin) {
        payload.faculty_name = this.faculty_name || null;
        payload.room = this.room;
      }

      const res = await fetch("http://127.0.0.1:5000/api/routines", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const result = await res.json();

      if (res.status === 409) {
        this.error = result.error;
        return;
      }

      if (res.ok) {
        this.success = "✅ Routine created successfully!";
        setTimeout(() => (this.success = null), 2500);
      } else {
        this.error = "❌ Failed to create routine";
      }
    }
  }
};
</script>

<style scoped>
.page-content { padding: 2rem 0; }
.form { max-width: 600px; margin: auto; display: grid; gap: 1rem; }

.alert-error {
  background: #ffd4d4;
  padding: 10px;
  border-left: 4px solid #b30000;
  color: #7a0000;
}

.alert-success {
  background: #d9ffe0;
  padding: 10px;
  border-left: 4px solid #007c1c;
  color: #005a14;
}
</style>
