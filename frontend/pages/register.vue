<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="card auth-card">
        <h1 class="auth-title">Class Routine Management</h1>
        <h2 class="auth-subtitle">Create Account</h2>

        <div v-if="error" class="alert alert-error">{{ error }}</div>
        <div v-if="success" class="alert alert-success">{{ success }}</div>

        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label class="form-label">Full Name</label>
            <input
              v-model="fullName"
              type="text"
              class="form-input"
              placeholder="John Doe"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label">Email</label>
            <input
              v-model="email"
              type="email"
              class="form-input"
              placeholder="your.email@example.com"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label">Password</label>
            <input
              v-model="password"
              type="password"
              class="form-input"
              placeholder="Minimum 6 characters"
              required
              minlength="6"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Role</label>
            <select v-model="role" class="form-select" required>
              <option value="">Select Role</option>
              <option value="student">Student</option>
              <option value="faculty">Faculty</option>
              <option value="admin">Admin</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Department</label>
            <select v-model="departmentId" class="form-select" required>
              <option value="">Select Department</option>
              <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                {{ dept.name }}
              </option>
            </select>
          </div>

          <button type="submit" class="btn btn-primary auth-btn" :disabled="loading">
            {{ loading ? 'Creating Account...' : 'Register' }}
          </button>
        </form>

        <p class="auth-footer">
          Already have an account?
          <nuxt-link to="/login">Sign in here</nuxt-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  layout: 'auth',
  data() {
    return {
      fullName: '',
      email: '',
      password: '',
      role: '',
      departmentId: '',
      departments: [],
      error: null,
      success: null,
      loading: false
    }
  },

  async mounted() {
    const res = await this.$api.departments()   // ✅ Calls backend
    this.departments = res                      // ✅ Assign data directly
  },

  methods: {
    async handleRegister() {
      this.loading = true
      this.error = null
      this.success = null

      const payload = {
        name: this.fullName,
        email: this.email,
        password: this.password,
        role: this.role,
        department_id: this.departmentId     // ✅ store department
      }

      const res = await this.$api.register(payload)

      if (res.error) {
        this.error = res.error
        this.loading = false
        return
      }

      this.success = 'Account created successfully! Redirecting...'
      setTimeout(() => {
        this.$router.push('/login')
      }, 1500)

      this.loading = false
    }
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem;
}

.auth-container {
  width: 100%;
  max-width: 480px;
}

.auth-card {
  padding: 2.5rem;
}

.auth-title {
  font-size: 1.75rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 0.5rem;
  color: var(--gray-900);
}

.auth-subtitle {
  font-size: 1.25rem;
  font-weight: 600;
  text-align: center;
  margin-bottom: 2rem;
  color: var(--gray-700);
}

.auth-btn {
  width: 100%;
  padding: 0.875rem;
  font-size: 1rem;
  margin-top: 0.5rem;
}

.alert {
  padding: .75rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  text-align: center;
}

.alert-error {
  background: #ffcccc;
  color: #a10000;
}

.alert-success {
  background: #d8ffd6;
  color: #006400;
}
</style>
