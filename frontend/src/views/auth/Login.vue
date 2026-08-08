<template>
  <div class="min-vh-100 d-flex align-items-center bg-light">

    <div class="container">

      <div class="row justify-content-center">

        <div class="col-12 col-md-7 col-lg-5 col-xl-4">

          <!-- Logo / Heading -->
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

          <!-- Login Card -->
          <div class="card tm-card border-0 shadow-sm">

            <div class="card-body p-4 p-md-5">

              <!-- Error -->
              <div
                v-if="error"
                class="alert alert-danger"
                role="alert"
              >
                {{ error }}
              </div>

              <!-- Login Form -->
              <form @submit.prevent="handleLogin">

                <!-- Email -->
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

                <!-- Password -->
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

                <!-- Sign In -->
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

              <!-- Registration Link -->
              <div class="text-center mt-4">

                <span class="text-muted">
                  Don't have an account?
                </span>

                <router-link
                  to="/register"
                  class="fw-semibold text-success text-decoration-none ms-1"
                >
                  Register as Trekker
                </router-link>

              </div>

            </div>

          </div>

          <!-- Footer -->
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
import api from '../../services/api'

const router = useRouter()

const email = ref('')
const password = ref('')

const loading = ref(false)
const error = ref('')

async function handleLogin() {
  error.value = ''
  loading.value = true

  try {
    const response = await api.post('/auth/login', {
      email: email.value,
      password: password.value
    })

    const data = response.data

    // Store authentication information
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))

    // Redirect according to role
    const role = data.user.role

    if (role === 'ADMIN') {
      router.push('/admin')
    } else if (role === 'STAFF') {
      router.push('/staff')
    } else if (role === 'TREKKER') {
      router.push('/trekker')
    } else {
      error.value = 'Unknown user role.'
    }

  } catch (err) {

    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Invalid email or password.'

  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.tm-login-logo {
  width: 56px;
  height: 56px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 14px;

  background-color: #2e7d32;
  color: white;

  font-size: 1.6rem;

  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.12);
}

.tm-card {
  border-radius: 12px;
}

.form-control {
  border-radius: 8px;
  padding: 0.65rem 0.8rem;
}

.form-control:focus {
  border-color: #2e7d32;
  box-shadow: 0 0 0 0.2rem rgba(46, 125, 50, 0.15);
}

.tm-btn-primary {
  background-color: #2e7d32;
  border-color: #2e7d32;
  color: white;
}

.tm-btn-primary:hover {
  background-color: #1b5e20;
  border-color: #1b5e20;
  color: white;
}

.tm-btn-primary:disabled {
  background-color: #2e7d32;
  border-color: #2e7d32;
}
</style>