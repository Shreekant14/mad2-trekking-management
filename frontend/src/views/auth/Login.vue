<template>
  <div class="tm-login-page">
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100">

        <div class="col-12 col-md-7 col-lg-5 col-xl-4">

          <div class="text-center mb-4">
            <div class="tm-login-logo mx-auto mb-3">
              <i class="bi bi-tree-fill"></i>
            </div>

            <h1 class="h3 fw-bold mb-1">
              Trekking Management
            </h1>

            <p class="text-muted mb-0">
              Sign in to continue
            </p>
          </div>

          <div class="card tm-card border-0 shadow-sm">

            <div class="card-body p-4 p-md-5">

              <div
                v-if="error"
                class="alert alert-danger"
                role="alert"
              >
                {{ error }}
              </div>

              <form @submit.prevent="handleLogin">

                <div class="mb-3">
                  <label class="form-label fw-semibold">
                    Email
                  </label>

                  <input
                    v-model.trim="email"
                    type="email"
                    class="form-control"
                    placeholder="Enter your email"
                    required
                  />
                </div>

                <div class="mb-4">
                  <label class="form-label fw-semibold">
                    Password
                  </label>

                  <input
                    v-model="password"
                    type="password"
                    class="form-control"
                    placeholder="Enter your password"
                    required
                  />
                </div>

                <button
                  type="submit"
                  class="btn tm-btn-primary w-100"
                  :disabled="loading"
                >
                  <span
                    v-if="loading"
                    class="spinner-border spinner-border-sm me-2"
                  ></span>

                  {{ loading ? 'Signing in...' : 'Sign In' }}
                </button>

              </form>

            </div>
          </div>

          <p class="text-center text-muted small mt-4">
            Trekking Management System
          </p>

        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../../services/auth'

const router = useRouter()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  error.value = ''
  loading.value = true

  try {
    const user = await login(email.value, password.value)

    if (user.role === 'ADMIN') {
      router.push('/admin')
    } else if (user.role === 'STAFF') {
      router.push('/staff')
    } else {
      router.push('/trekker')
    }
  } catch (err) {
    error.value =
      err.response?.data?.message ||
      'Unable to login. Please check your credentials.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.tm-login-page {
  background-color: var(--tm-background);
}

.tm-login-logo {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  background-color: var(--tm-primary);
  border-radius: 16px;
  font-size: 1.7rem;
}
</style>