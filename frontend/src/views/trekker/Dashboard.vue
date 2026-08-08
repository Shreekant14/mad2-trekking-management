<template>
  <div class="container-fluid p-4">

    <div class="mb-4">
      <h1 class="page-title mb-1">Trekker Dashboard</h1>
      <p class="text-muted mb-0">
        Overview of your trekking bookings.
      </p>
    </div>

    <div
      v-if="error"
      class="alert alert-danger"
    >
      <i class="bi bi-exclamation-triangle me-2"></i>
      {{ error }}
    </div>

    <div
      v-if="loading"
      class="text-center py-5"
    >
      <div class="spinner-border text-success"></div>
      <p class="text-muted mt-3">
        Loading dashboard...
      </p>
    </div>

    <div
      v-else
      class="row g-4"
    >

      <!-- Total -->
      <div class="col-12 col-md-4">
        <div class="card stat-card h-100">
          <div class="card-body">

            <div class="d-flex justify-content-between">

              <div>
                <div class="stat-label">
                  Total Bookings
                </div>

                <div class="stat-value">
                  {{ dashboard.total_bookings ?? 0 }}
                </div>
              </div>

              <div class="stat-icon">
                <i class="bi bi-calendar-check"></i>
              </div>

            </div>

          </div>
        </div>
      </div>

      <!-- Confirmed -->
      <div class="col-12 col-md-4">
        <div class="card stat-card confirmed h-100">
          <div class="card-body">

            <div class="d-flex justify-content-between">

              <div>
                <div class="stat-label">
                  Confirmed
                </div>

                <div class="stat-value">
                  {{ dashboard.confirmed ?? 0 }}
                </div>
              </div>

              <div class="stat-icon">
                <i class="bi bi-check-circle"></i>
              </div>

            </div>

          </div>
        </div>
      </div>

      <!-- Cancelled -->
      <div class="col-12 col-md-4">
        <div class="card stat-card cancelled h-100">
          <div class="card-body">

            <div class="d-flex justify-content-between">

              <div>
                <div class="stat-label">
                  Cancelled
                </div>

                <div class="stat-value">
                  {{ dashboard.cancelled ?? 0 }}
                </div>
              </div>

              <div class="stat-icon">
                <i class="bi bi-x-circle"></i>
              </div>

            </div>

          </div>
        </div>
      </div>

    </div>

    <!-- Quick action -->
    <div class="card border-0 shadow-sm mt-4">
      <div class="card-body d-flex flex-wrap justify-content-between align-items-center">

        <div>
          <h5 class="fw-bold mb-1">
            Ready for your next trek?
          </h5>

          <p class="text-muted mb-0">
            Explore available trekking programs and make a booking.
          </p>
        </div>

        <router-link
          to="/trekker/treks"
          class="btn btn-success mt-3 mt-md-0"
        >
          <i class="bi bi-compass me-2"></i>
          Explore Treks
        </router-link>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'

const dashboard = ref({})
const loading = ref(false)
const error = ref('')

async function loadDashboard() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/trekker/dashboard')
    dashboard.value = response.data
  } catch (err) {
    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to load trekker dashboard.'
  } finally {
    loading.value = false
  }
}

onMounted(loadDashboard)
</script>

<style scoped>
.page-title {
  color: var(--tm-text);
  font-weight: 700;
}

.stat-card {
  border: 0;
  border-left: 4px solid var(--tm-primary);
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-card.confirmed {
  border-left-color: #2E7D32;
}

.stat-card.cancelled {
  border-left-color: #dc3545;
}

.stat-label {
  color: #6c757d;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  margin-top: 8px;
  font-size: 2rem;
  font-weight: 700;
}

.stat-icon {
  width: 44px;
  height: 44px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background: var(--tm-primary-light);
  color: var(--tm-primary);

  font-size: 1.1rem;
}
</style>