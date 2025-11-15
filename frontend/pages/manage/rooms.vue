<template>
  <div class="container page-content">
    <h1>Manage Rooms</h1>

    <div class="form-row">
      <input v-model="name" class="form-input" placeholder="Room name (e.g., C-201)" />
      <input v-model.number="capacity" type="number" min="0" class="form-input" placeholder="Capacity (optional)" />
      <button class="btn btn-primary" @click="create">Add Room</button>
    </div>

    <table class="table">
      <thead>
        <tr><th>ID</th><th>Name</th><th>Capacity</th><th>Action</th></tr>
      </thead>
      <tbody>
        <tr v-for="r in rooms" :key="r.id">
          <td>{{ r.id }}</td>
          <td>{{ r.name }}</td>
          <td>{{ r.capacity ?? '-' }}</td>
          <td><button class="btn btn-danger" @click="remove(r.id)">Delete</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return { rooms: [], name: "", capacity: null }
  },
  async mounted() {
    const u = JSON.parse(localStorage.getItem('user') || '{}')
    if (!u.email) return this.$router.push('/login')
    if (u.role !== 'admin') return this.$router.push('/dashboard')
    this.load()
  },
  methods: {
    async load() {
      this.rooms = await this.$api.rooms()
    },
    async create() {
      if (!this.name.trim()) return
      const res = await this.$api.addRoom(this.name.trim(), this.capacity || null)
      if (!res.error) {
        this.name = ""; this.capacity = null
        this.load()
      } else {
        alert(res.error)
      }
    },
    async remove(id) {
      if (!confirm('Delete this room?')) return
      await this.$api.deleteRoom(id)
      this.rooms = this.rooms.filter(x => x.id !== id)
    }
  }
}
</script>

<style scoped>
.page-content { padding: 1.5rem 0; }
.form-row { display: flex; gap: 10px; margin: 12px 0 18px; }
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 10px; border-bottom: 1px solid #e5e7eb; }
.btn-danger { background: #e74c3c; color: #fff; border-radius: 6px; padding: 6px 12px; }
.btn-primary { background: #3b82f6; color: #fff; border-radius: 6px; padding: 6px 12px; }
.form-input { border: 1px solid #d1d5db; padding: 8px 10px; border-radius: 6px; }
</style>
