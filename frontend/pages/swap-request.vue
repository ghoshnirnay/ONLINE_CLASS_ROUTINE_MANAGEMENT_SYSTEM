<template>
  <div class="page-container">
    <h1 class="title">Request a Class Swap</h1>
    <p class="subtitle">
      Faculty can request to swap one of their classes with another faculty teaching on the same day.
    </p>

    <div v-if="loading" class="loading">Loading your routines and faculty data...</div>

    <div v-else class="form-card">
      <form @submit.prevent="submitSwap">
        <!-- Select your class -->
        <div class="form-group">
          <label for="routine">Your Class (Routine)</label>
          <select v-model="form.routine_id" @change="onMyRoutineSelect">
            <option disabled value="">-- Select Your Class --</option>
            <option
              v-for="r in myRoutines"
              :key="r.id"
              :value="r.id"
            >
              {{ r.day }} | {{ r.subject }} | {{ r.section }} | {{ r.start_time }}–{{ r.end_time }}
            </option>
          </select>
        </div>

        <!-- Select another faculty -->
        <div class="form-group">
          <label for="swap_with_faculty">Swap With Faculty</label>
          <select v-model="form.swap_with_faculty" @change="fetchSwapFacultyRoutines">
            <option disabled value="">-- Select Faculty --</option>
            <option
              v-for="f in otherFaculties"
              :key="f.id"
              :value="f.name"
            >
              {{ f.name }}
            </option>
          </select>
        </div>

        <!-- Select their class -->
        <div class="form-group">
          <label for="swap_with_routine">Swap With Faculty’s Class</label>
          <select v-model="form.swap_with_routine_id">
            <option disabled value="">-- Select Class to Swap With --</option>
            <option
              v-for="r in swapFacultyRoutines"
              :key="r.id"
              :value="r.id"
            >
              {{ r.day }} | {{ r.subject }} | {{ r.section }} | {{ r.start_time }}–{{ r.end_time }}
            </option>
          </select>
        </div>

        <!-- Submit -->
        <button type="submit" class="btn">Submit Swap Request</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: null,
      myRoutines: [],
      otherFaculties: [],
      swapFacultyRoutines: [],
      loading: true,
      form: {
        routine_id: "",
        swap_with_faculty: "",
        swap_with_routine_id: ""
      },
    };
  },
  async mounted() {
    this.user = JSON.parse(localStorage.getItem("user"));
    await this.loadInitialData();
  },
  methods: {
    async loadInitialData() {
      try {
        this.loading = true;

        // Fetch logged-in faculty routines
        const res = await fetch(`http://127.0.0.1:5000/api/routines/faculty/${encodeURIComponent(this.user.name)}`);
        this.myRoutines = await res.json();

        // Fetch all faculties
        const facultyRes = await fetch("http://127.0.0.1:5000/api/users?role=faculty");
        const allFaculties = await facultyRes.json();

        // Exclude self
        this.otherFaculties = allFaculties.filter(f => f.name !== this.user.name);
      } catch (err) {
        console.error("Error loading data:", err);
      } finally {
        this.loading = false;
      }
    },

    onMyRoutineSelect() {
      this.form.swap_with_faculty = "";
      this.swapFacultyRoutines = [];
      this.form.swap_with_routine_id = "";
    },

    async fetchSwapFacultyRoutines() {
      if (!this.form.swap_with_faculty || !this.form.routine_id) return;

      try {
        const res = await fetch(`http://127.0.0.1:5000/api/routines/faculty/${encodeURIComponent(this.form.swap_with_faculty)}`);
        let routines = await res.json();

        // Filter by same day as selected routine
        const selectedRoutine = this.myRoutines.find(r => r.id === this.form.routine_id);
        if (selectedRoutine) {
          routines = routines.filter(r => r.day === selectedRoutine.day);
        }

        this.swapFacultyRoutines = routines;
      } catch (err) {
        console.error("Error fetching faculty routines:", err);
      }
    },

    async submitSwap() {
      if (!this.form.routine_id || !this.form.swap_with_faculty || !this.form.swap_with_routine_id) {
        alert("⚠️ Please fill all fields before submitting.");
        return;
      }

      const selectedMyClass = this.myRoutines.find(r => r.id === this.form.routine_id);
      const selectedSwapClass = this.swapFacultyRoutines.find(r => r.id === this.form.swap_with_routine_id);

      if (!selectedMyClass || !selectedSwapClass) {
        alert("⚠️ Invalid class selection.");
        return;
      }

      const payload = {
        faculty_name: this.user.name,
        swap_with_faculty: this.form.swap_with_faculty,
        department_id: selectedMyClass.department_id,
        subject: selectedMyClass.subject,
        section: selectedMyClass.section,
        swap_with_section: selectedSwapClass.section,
        routine_id: selectedMyClass.id,
        swap_with_routine_id: selectedSwapClass.id,
      };

      try {
        const res = await fetch("http://127.0.0.1:5000/api/swap-request", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        const data = await res.json();

        if (res.ok) {
          alert("✅ Swap request submitted successfully!");
          this.form = { routine_id: "", swap_with_faculty: "", swap_with_routine_id: "" };
          this.swapFacultyRoutines = [];
        } else {
          alert("❌ Error: " + (data.error || data.message));
        }
      } catch (err) {
        console.error("Error submitting swap request:", err);
        alert("Failed to submit swap request. Please try again.");
      }
    },
  },
};
</script>

<style scoped>
.page-container {
  padding: 2rem;
}
.title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1e3a8a;
  margin-bottom: 0.5rem;
}
.subtitle {
  color: #6b7280;
  margin-bottom: 1.5rem;
}
.form-card {
  background: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  max-width: 700px;
}
.form-group {
  margin-bottom: 1rem;
}
label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}
select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
}
.btn {
  background-color: #2563eb;
  color: #fff;
  padding: 0.7rem 1.2rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}
.btn:hover {
  background-color: #1e40af;
}
.loading {
  color: #6b7280;
  font-style: italic;
}
</style>
