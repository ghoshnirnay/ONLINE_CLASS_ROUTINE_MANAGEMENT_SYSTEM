<template>
  <div class="container page-content">
    <h1>Manage Subjects</h1>

    <div class="form-group">
      <input v-model="name" class="form-input" placeholder="Enter subject name" />
      <button class="btn btn-primary" @click="addSubject">Add</button>
    </div>

    <table class="table">
      <tr>
        <th>ID</th><th>Name</th><th>Action</th>
      </tr>
      <tr v-for="s in subjects" :key="s.id">
        <td>{{ s.id }}</td>
        <td>{{ s.name }}</td>
        <td><button class="btn btn-danger" @click="deleteSubject(s.id)">Delete</button></td>
      </tr>
    </table>
  </div>
</template>

<script>
export default {
  data() { return { subjects: [], name: "" }; },
  async mounted() { this.load(); },
  methods: {
    async load() { this.subjects = await this.$api.subjects(); },
    async addSubject() {
      if (!this.name) return;
      await this.$api.addSubject(this.name);
      this.name = "";
      this.load();
    },
    async deleteSubject(id) {
      await this.$api.deleteSubject(id);
      this.load();
    }
  }
}
</script>
