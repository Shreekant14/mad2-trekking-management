<template>
  <div class="container-fluid p-4">

    <div class="mb-4">
      <h1 class="page-title mb-1">My Treks</h1>
      <p class="text-muted mb-0">
        Treks currently assigned to you.
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
      <p class="text-muted mt-3">Loading your treks...</p>
    </div>

    <div
      v-else
      class="row g-4"
    >

      <div
        v-for="trek in treks"
        :key="trek.id"
        class="col-12 col-md-6 col-xl-4"
      >

        <div class="card trek-card h-100">

          <div class="card-body">

            <div class="d-flex justify-content-between mb-3">

              <span class="badge bg-success-subtle text-success">
                {{ trek.status }}
              </span>

              <span class="text-muted small">
                #{{ trek.id }}
              </span>

            </div>

            <h5 class="fw-bold">
              {{ trek.title }}
            </h5>

            <p class="text-muted mb-3">
              <i class="bi bi-geo-alt me-1"></i>
              {{ trek.location }}
            </p>

            <div class="row g-2 small">

              <div class="col-6">
                <div class="info-label">Difficulty</div>
                <strong>{{ trek.difficulty }}</strong>
              </div>

              <div class="col-6">
                <div class="info-label">Duration</div>
                <strong>{{ trek.duration }} days</strong>
              </div>

              <div class="col-6">
                <div class="info-label">Start</div>
                <strong>{{ trek.start_date }}</strong>
              </div>

              <div class="col-6">
                <div class="info-label">Slots</div>
                <strong>
                  {{ trek.available_slots }} /
                  {{ trek.total_slots }}
                </strong>
              </div>

            </div>

            <button
              class="btn btn-outline-success w-100 mt-4"
              @click="viewParticipants(trek.id)"
            >
              <i class="bi bi-people me-2"></i>
              View Participants
            </button>

          </div>

        </div>

      </div>

      <div
        v-if="treks.length === 0"
        class="col-12"
      >
        <div class="card border-0 shadow-sm">
          <div class="card-body text-center py-5">

            <i class="bi bi-map fs-1 text-muted"></i>

            <h5 class="mt-3">
              No treks assigned
            </h5>

            <p class="text-muted mb-0">
              You currently have no assigned trekking programs.
            </p>

          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../services/api'

const router = useRouter()

const treks = ref([])
const loading = ref(false)
const error = ref('')

async function loadTreks() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/staff/my-treks')
    treks.value = response.data
  } catch (err) {
    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to load assigned treks.'
  } finally {
    loading.value = false
  }
}

function viewParticipants(trekId) {
  router.push(`/staff/treks/${trekId}/participants`)
}

onMounted(loadTreks)
</script>

<style scoped>
.page-title {
  color: var(--tm-text);
  font-weight: 700;
}

.trek-card {
  border: 0;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.info-label {
  color: #6c757d;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 2px;
}
</style>