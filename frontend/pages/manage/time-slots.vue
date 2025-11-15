<template>
  <div class="container page-content">
    <h1>Manage Time Slots</h1>

    <div class="form-row">
      <input v-model="label" class="form-input" placeholder="Label (ex: Period 1)" />
      <input v-model="start" type="time" class="form-input" />
      <input v-model="end" type="time" class="form-input" />
      <button class="btn btn-primary" @click="create">Add</button>
    </div>

    <table class="table">
      <thead>
        <tr><th>Label</th><th>Start</th><th>End</th><th>Action</th></tr>
      </thead>
      <tbody>
        <tr v-for="t in slots" :key="t.id">
          <td>{{ t.label }}</td>
          <td>{{ t.start_time }}</td>
          <td>{{ t.end_time }}</td>
          <td><button class="btn btn-danger" @click="remove(t.id)">Delete</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return { slots: [], label: "", start: "", end: "" }
  },
  async mounted() {
    const u = JSON.parse(localStorage.getItem('user') || '{}')
    if (u.role !== 'admin') return this.$router.push('/dashboard')
    this.load()
  },
  methods: {
    async load() {
      this.slots = await this.$api.timeSlots()
    },
    async create() {
      if (!this.label || !this.start || !this.end) return alert("Fill all fields")
      await this.$api.addTimeSlot(this.label, this.start, this.end)
      this.label = ""; this.start = ""; this.end = ""
      this.load()
    },
    async remove(id) {
      if (!confirm("Delete this time slot?")) return
      await this.$api.deleteTimeSlot(id)
      this.load()
    }
  }
}
</script>

<style scoped>
.page-content { padding: 1.5rem 0; }
.form-row { display: flex; gap: 10px; margin: 12px 0 18px; }
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 10px; border-bottom: 1px solid #e5e7eb; }
.btn-danger { background: #e74c3c; color: white; border-radius: 6px; padding: 6px 12px; }
.btn-primary { background: #3b82f6; color: white; border-radius: 6px; padding: 6px 12px; }
.form-input { border: 1px solid #d1d5db; padding: 8px; border-radius: 6px; }
</style>
