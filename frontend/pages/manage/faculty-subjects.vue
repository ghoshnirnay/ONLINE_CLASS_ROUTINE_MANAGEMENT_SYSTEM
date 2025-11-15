<template>
  <div>
    <Header :user="user" @logout="logout" />

    <div class="page-content">
      <div class="container">
        <h2>Assign Subjects to Faculty</h2>

        <!-- Select Faculty -->
        <div class="form-group">
          <label>Select Faculty</label>
          <select v-model="selectedFaculty" class="form-input" @change="loadAssignedSubjects">
            <option value="">-- Select Faculty --</option>
            <option v-for="f in faculty" :key="f.id" :value="f.id">
              {{ f.name }} ({{ f.email }})
            </option>
          </select>
        </div>

        <!-- Assign + Show List -->
        <div v-if="selectedFaculty">
          <h3>Assign a Subject</h3>
          <div class="assign-row">
            <select v-model="chosenSubject" class="form-input">
              <option value="">-- Select Subject --</option>
              <option v-for="s in subjects" :key="s.id" :value="s.id">
                {{ s.name }}
              </option>
            </select>
            <button class="btn btn-primary" @click="assignSubject">Assign</button>
          </div>

          <h3 class="mt-4">Assigned Subjects</h3>
          <table class="table">
            <thead>
              <tr>
                <th>Subject</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="a in assigned" :key="a.id">
                <!-- ✅ FIXED: show subject_name from backend -->
                <td>{{ a.subject_name }}</td>
                <td>
                  <button class="btn btn-danger" @click="removeSubject(a.id)">Remove</button>
                </td>
              </tr>

              <tr v-if="assigned.length === 0">
                <td colspan="2" class="no-data">No subjects assigned.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: null,
      faculty: [],
      subjects: [],
      assigned: [],
      selectedFaculty: "",
      chosenSubject: "",
    };
  },

  async mounted() {
    this.user = JSON.parse(localStorage.getItem("user"));
    if (!this.user || this.user.role !== "admin") {
      this.$router.push("/dashboard");
      return;
    }

    await this.loadFacultyList();
    this.subjects = await this.$api.subjects(); // ✅ get subjects
  },

  methods: {
    async loadFacultyList() {
      const res = await fetch("http://127.0.0.1:5000/api/users?role=faculty");
      this.faculty = await res.json();
    },

    async loadAssignedSubjects() {
      if (!this.selectedFaculty) return;
      const res = await fetch(`http://127.0.0.1:5000/api/faculty-subjects/${this.selectedFaculty}`);
      this.assigned = await res.json();
    },

    async assignSubject() {
      if (!this.chosenSubject) {
        alert("Please select a subject first.");
        return;
      }

      await fetch("http://127.0.0.1:5000/api/faculty-subjects", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          faculty_id: this.selectedFaculty,
          subject_id: this.chosenSubject
        })
      });

      this.chosenSubject = "";
      this.loadAssignedSubjects();
    },

    async removeSubject(id) {
      await fetch(`http://127.0.0.1:5000/api/faculty-subjects/${id}`, {
        method: "DELETE"
      });
      this.loadAssignedSubjects();
    },

    logout() {
      localStorage.removeItem("user");
      this.$router.push("/login");
    }
  }
};
</script>

<style scoped>
.assign-row {
  display: flex;
  gap: 10px;
  margin-bottom: 1rem;
}

.no-data {
  text-align: center;
  color: gray;
  padding: 0.5rem;
}
</style>
