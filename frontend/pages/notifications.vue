<template>
  <div>
    <Header :user="user" @logout="handleLogout" />

    <div class="page-content">
      <div class="container">
        <div class="page-header">
          <h1 class="page-title">Notifications</h1>
          <button
            v-if="unreadCount > 0"
            class="btn btn-outline"
            @click="markAllAsRead"
          >
            Mark All as Read
          </button>
        </div>

        <!-- Loading Spinner -->
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
        </div>

        <!-- No Notifications -->
        <div v-else-if="notifications.length === 0" class="empty-state">
          No notifications yet 🎉
        </div>

        <!-- Notification List -->
        <div v-else class="notification-list card">
          <div
            v-for="n in notifications"
            :key="n.id"
            class="notification-item"
            :class="{ unread: n.read === 0 }"
            @click="markAsRead(n)"
          >
            <div class="notification-icon" :class="getTypeClass(n.type)">
              {{ getTypeIcon(n.type) }}
            </div>
            <div class="notification-content">
              <h4 class="notification-title">{{ n.title || "Notification" }}</h4>
              <p class="notification-message">{{ n.message }}</p>
              <span class="notification-time">{{ formatTime(n.created_at) }}</span>
            </div>
            <div v-if="n.read === 0" class="unread-badge"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/Header.vue";

export default {
  components: { Header },

  data() {
    return {
      user: null,
      notifications: [],
      loading: true
    };
  },

  computed: {
    unreadCount() {
      return this.notifications.filter(n => n.read === 0).length;
    }
  },

  async mounted() {
    this.loadUser();
  },

  methods: {
    loadUser() {
      const storedUser = localStorage.getItem("user");
      if (!storedUser) {
        this.$router.push("/login");
        return;
      }
      this.user = JSON.parse(storedUser);
      this.fetchNotifications();
    },

    async fetchNotifications() {
      try {
        const res = await fetch(`http://127.0.0.1:5000/api/notifications/${this.user.id}`);
        this.notifications = await res.json();
      } catch (err) {
        console.error("Error fetching notifications:", err);
      } finally {
        this.loading = false;
      }
    },

    async markAsRead(notification) {
      if (notification.read === 1) return;

      try {
        await fetch(`http://127.0.0.1:5000/api/notifications/read/${notification.id}`, {
          method: "POST"
        });
        notification.read = 1;
      } catch (err) {
        console.error("Error marking notification as read:", err);
      }
    },

    async markAllAsRead() {
      try {
        await fetch(`http://127.0.0.1:5000/api/notifications/mark-read/${this.user.id}`, {
          method: "POST"
        });
        this.notifications = this.notifications.map(n => ({ ...n, read: 1 }));
      } catch (err) {
        console.error("Error marking all as read:", err);
      }
    },

    getTypeIcon(type) {
      const icons = {
        routine_change: "📅",
        swap_request: "🔄",
        system: "⚙️",
        announcement: "📢"
      };
      return icons[type] || "📬";
    },

    getTypeClass(type) {
      return `type-${type}`;
    },

    formatTime(dateStr) {
      const date = new Date(dateStr);
      const diff = Date.now() - date.getTime();
      const mins = Math.floor(diff / 60000);
      const hours = Math.floor(mins / 60);
      const days = Math.floor(hours / 24);

      if (mins < 60) return `${mins} min ago`;
      if (hours < 24) return `${hours} hr ago`;
      if (days < 7) return `${days} days ago`;
      return date.toLocaleDateString();
    },

    handleLogout() {
      localStorage.removeItem("user");
      this.$router.push("/login");
    }
  }
};
</script>

<style scoped>
.page-content {
  padding: 2rem 0;
  min-height: calc(100vh - 80px);
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}
.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--gray-900);
}
.notification-list {
  display: flex;
  flex-direction: column;
}
.notification-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  padding: 1rem;
  border-bottom: 1px solid #ddd;
  cursor: pointer;
  transition: background 0.2s;
}
.notification-item.unread {
  background: #e0f2fe;
}
.notification-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}
.notification-content {
  flex: 1;
}
.notification-title {
  font-weight: 600;
  font-size: 1rem;
}
.notification-message {
  font-size: 0.9rem;
  color: #555;
}
.notification-time {
  font-size: 0.8rem;
  color: #888;
}
.unread-badge {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #2563eb;
  align-self: center;
}
.empty-state {
  text-align: center;
  color: #666;
  padding: 3rem 0;
}
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.2);
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 2rem auto;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
