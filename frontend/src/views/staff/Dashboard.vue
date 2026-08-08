<template>
  <div class="container-fluid p-4">

    <div class="mb-4">
      <h1 class="page-title mb-1">Staff Dashboard</h1>
      <p class="text-muted mb-0">
        Overview of your assigned trekking activities.
      </p>
    </div>

    <div
      v-if="error"
      class="alert alert-danger"
    >
      {{ error }}
    </div>

    <div
      v-if="loading"
      class="text-center py-5"
    >
      <div class="spinner-border text-success"></div>
      <p class="text-muted mt-3">Loading dashboard...</p>
    </div>

    <div
      v-else
      class="row g-4"
    >

      <div class="col-12 col-md-4">
        <div class="card stat-card h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <div class="stat-label">Assigned Treks</div>
                <div class="stat-value">
                  {{ dashboard.assigned_treks ?? 0 }}
                </div>
              </div>

              <div class="stat-icon">
                <i class="bi bi-map"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-4">
        <div class="card stat-card h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <div class="stat-label">Upcoming Treks</div>
                <div class="stat-value">
                  {{ dashboard.upcoming_treks ?? 0 }}
                </div>
              </div>

              <div class="stat-icon">
                <i class="bi bi-calendar-event"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-4">
        <div class="card stat-card h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <div class="stat-label">Completed Treks</div>
                <div class="stat-value">
                  {{ dashboard.completed_treks ?? 0 }}
                </div>
              </div>

              <div class="stat-icon">
                <i class="bi bi-check-circle"></i>
              </div>
            </div>
          </div>
        </div>
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
    const response = await api.get('/staff/dashboard')
    dashboard.value = response.data
  } catch (err) {
    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to load staff dashboard.'
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
}
</style>