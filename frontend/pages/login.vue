<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="card auth-card">
        <h1 class="auth-title">Class Routine Management</h1>
        <h2 class="auth-subtitle">Sign In</h2>

        <div v-if="error" class="alert alert-error">{{ error }}</div>

        <form @submit.prevent="handleLogin">
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
              placeholder="Enter password"
              required
            />
          </div>

          <button type="submit" class="btn btn-primary auth-btn" :disabled="loading">
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>

        <p class="auth-footer">
          Don't have an account?
          <nuxt-link to="/register">Register here</nuxt-link>
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
      email: '',
      password: '',
      loading: false,
      error: null
    }
  },

  methods: {
    async handleLogin() {
      this.loading = true
      this.error = null

      const res = await this.$api.login(this.email, this.password)

      if (res.error) {
        this.error = res.error
        this.loading = false
        return
      }

      // ✅ Store logged user in browser
      localStorage.setItem('user', JSON.stringify(res.user))

      // ✅ Redirect to dashboard
      this.$router.push('/dashboard')
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
  max-width: 420px;
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
</style>
