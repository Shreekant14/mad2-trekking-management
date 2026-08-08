<template>
  <div class="container-fluid p-4">

    <!-- Header -->
    <div class="d-flex flex-wrap justify-content-between align-items-center mb-4">
      <div>
        <h1 class="dashboard-title mb-1">
          Admin Dashboard
        </h1>

        <p class="text-muted mb-0">
          Overview of your trekking management system.
        </p>
      </div>

      <button
        class="btn btn-success mt-3 mt-md-0"
        @click="loadDashboard"
        :disabled="loading"
      >
        <i class="bi bi-arrow-clockwise me-2"></i>
        {{ loading ? 'Refreshing...' : 'Refresh' }}
      </button>
    </div>

    <!-- Error -->
    <div
      v-if="error"
      class="alert alert-danger"
    >
      <i class="bi bi-exclamation-triangle me-2"></i>
      {{ error }}
    </div>

    <!-- Loading -->
    <div
      v-if="loading && !hasData"
      class="text-center py-5"
    >
      <div class="spinner-border text-success"></div>

      <p class="text-muted mt-3">
        Loading dashboard...
      </p>
    </div>

    <!-- KPI Cards -->
    <div
      v-else
      class="row g-4"
    >

      <div
        v-for="card in dashboardCards"
        :key="card.key"
        class="col-12 col-sm-6 col-xl-3"
      >
        <div
          class="card dashboard-card h-100"
          :class="`accent-${card.type}`"
        >

          <div class="card-body">

            <div class="d-flex justify-content-between align-items-start">

              <div>
                <div class="card-label">
                  {{ card.label }}
                </div>

                <div class="card-value">
                  {{ card.value }}
                </div>
              </div>

              <div class="card-icon">
                <i :class="card.icon"></i>
              </div>

            </div>

          </div>

        </div>
      </div>

    </div>

    <!-- Empty state -->
    <div
      v-if="!loading && !hasData && !error"
      class="card border-0 shadow-sm mt-4"
    >
      <div class="card-body text-center py-5">

        <i class="bi bi-bar-chart fs-1 text-muted"></i>

        <h5 class="mt-3">
          No dashboard data available
        </h5>

        <p class="text-muted mb-0">
          There is currently no statistical data to display.
        </p>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../services/api'

const dashboardData = ref({})
const loading = ref(false)
const error = ref('')

const hasData = computed(() => {
  return Object.keys(dashboardData.value).length > 0
})

const dashboardCards = computed(() => {

  const entries = Object.entries(dashboardData.value)

  const icons = [
    'bi bi-map',
    'bi bi-people',
    'bi bi-calendar-check',
    'bi bi-cash-stack'
  ]

  const types = [
    'green',
    'blue',
    'amber',
    'pine'
  ]

  return entries
    .filter(([, value]) => {
      return typeof value === 'number'
    })
    .map(([key, value], index) => {

      const label = key
        .replace(/_/g, ' ')
        .replace(/\b\w/g, char => char.toUpperCase())

      return {
        key,
        label,
        value,
        icon: icons[index % icons.length],
        type: types[index % types.length]
      }
    })
})

async function loadDashboard() {

  loading.value = true
  error.value = ''

  try {

    const response = await api.get('/admin/dashboard')

    dashboardData.value = response.data

    console.log('Dashboard API response:', response.data)

  } catch (err) {

    console.error('Dashboard error:', err)

    error.value =
      err.response?.data?.message ||
      'Unable to load dashboard data.'

  } finally {

    loading.value = false

  }
}

onMounted(() => {
  loadDashboard()
})
</script>

<style scoped>

.dashboard-title {
  color: var(--tm-text);
  font-weight: 700;
}

.dashboard-card {
  border: 1px solid #e1e5e2;
  border-left-width: 4px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.accent-green {
  border-left-color: #2E7D32;
}

.accent-blue {
  border-left-color: #607D8B;
}

.accent-amber {
  border-left-color: #FFC107;
}

.accent-pine {
  border-left-color: #1B5E20;
}

.card-label {
  color: #6c757d;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.card-value {
  margin-top: 8px;
  color: #212529;
  font-size: 2rem;
  font-weight: 700;
}

.card-icon {
  width: 46px;
  height: 46px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background-color: var(--tm-primary-light);
  color: var(--tm-primary);

  font-size: 1.2rem;
}

</style>