<template>
  <div class="page-container">
    <h1 class="title">All Faculty Swap Requests</h1>

    <div v-if="loading" class="loading">Loading swap requests...</div>

    <div v-else class="card">
      <table class="table">
        <thead>
          <tr>
            <th>Requester Faculty</th>
            <th>Swap With Faculty</th>
            <th>Requester Subject</th>
            <th>Swap With Subject</th>
            <th>Requester Section</th>
            <th>Swap With Section</th>
            <th>Status</th>
            <th>Actions</th>
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
            <td>
              <button
                v-if="r.status === 'Pending'"
                class="btn btn-success"
                @click="approve(r.id)"
              >
                Approve
              </button>
              <button
                v-if="r.status === 'Pending'"
                class="btn btn-danger"
                @click="reject(r.id)"
              >
                Reject
              </button>
            </td>
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
      requests: [],
      loading: true
    };
  },
  async mounted() {
    try {
      const res = await fetch("http://127.0.0.1:5000/api/swap-requests");
      this.requests = await res.json();
    } catch (err) {
      console.error("Error fetching swap requests:", err);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async approve(id) {
      if (!confirm("Approve this swap request?")) return;
      try {
        const res = await fetch(`http://127.0.0.1:5000/api/swap-request/${id}/approve`, {
          method: "POST"
        });
        const data = await res.json();
        if (res.ok) {
          alert("✅ Swap request approved successfully!");
          this.requests = this.requests.map(r =>
            r.id === id ? { ...r, status: "Approved" } : r
          );
        } else {
          alert("❌ " + (data.message || "Failed to approve."));
        }
      } catch (err) {
        console.error("Error approving swap:", err);
      }
    },

    async reject(id) {
      if (!confirm("Reject this swap request?")) return;
      try {
        const res = await fetch(`http://127.0.0.1:5000/api/swap-request/${id}/reject`, {
          method: "POST"
        });
        const data = await res.json();
        if (res.ok) {
          alert("❌ Swap request rejected.");
          this.requests = this.requests.map(r =>
            r.id === id ? { ...r, status: "Rejected" } : r
          );
        } else {
          alert("❌ " + (data.message || "Failed to reject."));
        }
      } catch (err) {
        console.error("Error rejecting swap:", err);
      }
    },

    statusClass(status) {
      return {
        Approved: "status-approved",
        Rejected: "status-rejected",
        Pending: "status-pending"
      }[status] || "";
    },

    formatDate(dt) {
      if (!dt) return "";
      return new Date(dt).toLocaleString();
    }
  }
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
.card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  padding: 1rem;
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
.btn {
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  margin-right: 0.5rem;
}
.btn-success {
  background: #16a34a;
  color: white;
}
.btn-danger {
  background: #dc2626;
  color: white;
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
.loading {
  text-align: center;
  color: #4b5563;
}
</style>
