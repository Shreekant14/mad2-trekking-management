<template>
  <div class="register-page d-flex align-items-center justify-content-center min-vh-100">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-12 col-sm-10 col-md-7 col-lg-5">

          <div class="text-center mb-4">
            <div class="brand-icon mx-auto mb-3">
              <i class="bi bi-tree-fill"></i>
            </div>

            <h1 class="fw-bold brand-text mb-1">
              Trekking Management System
            </h1>

            <p class="text-muted mb-0">
              Create your Trekker account
            </p>
          </div>

          <div class="card border-0 shadow-sm">
            <div class="card-body p-4 p-md-5">

              <h3 class="fw-bold mb-1">
                Create Account
              </h3>

              <p class="text-muted mb-4">
                Register to explore and book treks.
              </p>

              <!-- Success -->
              <div
                v-if="success"
                class="alert alert-success"
              >
                <i class="bi bi-check-circle me-2"></i>
                {{ success }}
              </div>

              <!-- Error -->
              <div
                v-if="error"
                class="alert alert-danger"
              >
                <i class="bi bi-exclamation-triangle me-2"></i>
                {{ error }}
              </div>

              <form @submit.prevent="register">

                <!-- Full Name -->
                <div class="mb-3">
                  <label class="form-label fw-semibold">
                    Full Name
                  </label>

                  <input
                    v-model.trim="form.full_name"
                    type="text"
                    class="form-control"
                    placeholder="Enter your full name"
                    required
                  />
                </div>

                <!-- Email -->
                <div class="mb-3">
                  <label class="form-label fw-semibold">
                    Email
                  </label>

                  <input
                    v-model.trim="form.email"
                    type="email"
                    class="form-control"
                    placeholder="Enter your email"
                    required
                  />
                </div>

                <!-- Phone -->
                <div class="mb-3">
                  <label class="form-label fw-semibold">
                    Phone
                  </label>

                  <input
                    v-model.trim="form.phone"
                    type="tel"
                    class="form-control"
                    placeholder="Enter your phone number"
                    required
                  />
                </div>

                <!-- Password -->
                <div class="mb-3">
                  <label class="form-label fw-semibold">
                    Password
                  </label>

                  <input
                    v-model="form.password"
                    type="password"
                    class="form-control"
                    placeholder="Create a password"
                    minlength="6"
                    required
                  />
                </div>

                <!-- Confirm Password -->
                <div class="mb-3">
                  <label class="form-label fw-semibold">
                    Confirm Password
                  </label>

                  <input
                    v-model="confirmPassword"
                    type="password"
                    class="form-control"
                    placeholder="Confirm your password"
                    required
                  />
                </div>

                <!-- Role -->
                <div class="mb-4">
                  <label class="form-label fw-semibold">
                    Account Type
                  </label>

                  <input
                    type="text"
                    class="form-control"
                    value="Trekker"
                    disabled
                  />

                  <div class="form-text">
                    Staff accounts are created by an administrator.
                  </div>
                </div>

                <button
                  type="submit"
                  class="btn btn-success w-100 py-2"
                  :disabled="loading"
                >
                  <span
                    v-if="loading"
                    class="spinner-border spinner-border-sm me-2"
                  ></span>

                  {{ loading ? 'Creating Account...' : 'Create Account' }}
                </button>

              </form>

              <div class="text-center mt-4">
                <span class="text-muted">
                  Already have an account?
                </span>

                <router-link
                  to="/login"
                  class="fw-semibold text-success text-decoration-none ms-1"
                >
                  Login
                </router-link>
              </div>

            </div>
          </div>

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

const form = ref({
  full_name: '',
  email: '',
  password: '',
  phone: '',
  role: 'TREKKER'
})

const confirmPassword = ref('')

const loading = ref(false)
const error = ref('')
const success = ref('')

async function register() {
  error.value = ''
  success.value = ''

  if (form.value.password !== confirmPassword.value) {
    error.value = 'Passwords do not match.'
    return
  }

  loading.value = true

  try {
    await api.post('/auth/register', form.value)

    success.value =
      'Registration successful. Redirecting to login...'

    setTimeout(() => {
      router.push('/login')
    }, 1200)

  } catch (err) {
    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to create account. Please try again.'

  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  background-color: #f8f9fa;
}

.brand-icon {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  background-color: #2e7d32;
  color: white;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 1.5rem;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.12);
}

.brand-text {
  color: #1b5e20;
}

.card {
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

.btn-success {
  background-color: #2e7d32;
  border-color: #2e7d32;
}
</style>