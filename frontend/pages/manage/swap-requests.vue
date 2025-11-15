<template>
  <div class="page-container">
    <h1 class="title">My Swap Requests</h1>

    <div v-if="loading" class="loading">Loading your swap requests...</div>

    <div v-else class="card">
      <table class="table">
        <thead>
          <tr>
            <th>Requester Faculty</th>
            <th>Swap With Faculty</th>
            <th>Your Class</th>
            <th>Swap With Class</th>
            <th>Your Section</th>
            <th>Swap With Section</th>
            <th>Status</th>
            <th>Requested On</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in requests" :key="r.id">
            <td>{{ r.faculty_name }}</td>
            <td>{{ r.swap_with_faculty }}</td>
            <td>{{ r.subject }}</td>
            <td>{{ r.swap_with_subject }}</td>
            <td>{{ r.section }}</td>
            <td>{{ r.swap_with_section }}</td>
            <td :class="statusClass(r.status)">{{ r.status }}</td>
            <td>{{ formatDate(r.created_at) }}</td>
          </tr>
        </tbody>
      </table>

      <p v-if="!requests.length" class="empty">No swap requests found.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: null,
      requests: [],
      loading: true,
    };
  },
  async mounted() {
    try {
      this.user = JSON.parse(localStorage.getItem("user"));
      const res = await fetch(`http://127.0.0.1:5000/api/swap-requests/faculty/${encodeURIComponent(this.user.name)}`);
      this.requests = await res.json();
    } catch (err) {
      console.error("Error fetching swap requests:", err);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    formatDate(dt) {
      if (!dt) return "";
      return new Date(dt).toLocaleString();
    },
    statusClass(status) {
      return {
        Approved: "status-approved",
        Rejected: "status-rejected",
        Pending: "status-pending",
      }[status] || "";
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
  margin-bottom: 1rem;
}
.table {
  width: 100%;
  border-collapse: collapse;
}
.table th,
.table td {
  border: 1px solid #e5e7eb;
  padding: 0.8rem;
  text-align: center;
}
.table th {
  background: #f3f4f6;
}
.status-approved {
  color: #16a34a;
  font-weight: 600;
}
.status-rejected {
  color: #dc2626;
  font-weight: 600;
}
.status-pending {
  color: #92400e;
  font-weight: 600;
}
.empty {
  text-align: center;
  padding: 1rem;
  color: #6b7280;
}
.card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  padding: 1rem;
}
.loading {
  color: #6b7280;
  font-style: italic;
}
</style>
