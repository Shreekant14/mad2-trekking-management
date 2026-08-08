<template>
  <div class="container-fluid p-4">

    <!-- Header -->
    <div class="d-flex flex-wrap justify-content-between align-items-center mb-4">

      <div>
        <button
          class="btn btn-sm btn-outline-secondary mb-3"
          @click="goBack"
        >
          <i class="bi bi-arrow-left me-2"></i>
          Back to My Treks
        </button>

        <h1 class="page-title mb-1">
          Trek Participants
        </h1>

        <p class="text-muted mb-0">
          Confirmed participants for this trekking program.
        </p>
      </div>

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
      v-if="loading"
      class="text-center py-5"
    >
      <div class="spinner-border text-success"></div>

      <p class="text-muted mt-3 mb-0">
        Loading participants...
      </p>
    </div>

    <!-- Participants -->
    <div
      v-else
      class="card border-0 shadow-sm"
    >

      <div class="card-header bg-white py-3">

        <div class="d-flex justify-content-between align-items-center">

          <h5 class="mb-0 fw-bold">
            Participants
          </h5>

          <span class="badge bg-success-subtle text-success">
            {{ participants.length }} Bookings
          </span>

        </div>

      </div>

      <div class="table-responsive">

        <table class="table table-hover align-middle mb-0">

          <thead class="table-light">

            <tr>
              <th>Participant</th>
              <th>Email</th>
              <th>Phone</th>
              <th>People</th>
              <th>Booking</th>
            </tr>

          </thead>

          <tbody>

            <tr
              v-for="participant in participants"
              :key="participant.booking_id"
            >

              <td>

                <div class="d-flex align-items-center gap-2">

                  <div class="participant-avatar">
                    {{ initials(participant.name) }}
                  </div>

                  <div>
                    <div class="fw-semibold">
                      {{ participant.name }}
                    </div>

                    <small class="text-muted">
                      Booking #{{ participant.booking_id }}
                    </small>
                  </div>

                </div>

              </td>

              <td>
                {{ participant.email }}
              </td>

              <td>
                {{ participant.phone || '—' }}
              </td>

              <td>
                <span class="badge bg-success-subtle text-success">
                  {{ participant.people }}
                </span>
              </td>

              <td>
                <span class="badge bg-primary-subtle text-primary">
                  CONFIRMED
                </span>
              </td>

            </tr>

            <!-- Empty -->
            <tr v-if="participants.length === 0">

              <td
                colspan="5"
                class="text-center py-5"
              >

                <i class="bi bi-people fs-1 text-muted"></i>

                <h6 class="mt-3">
                  No confirmed participants
                </h6>

                <p class="text-muted mb-0">
                  There are currently no confirmed bookings for this trek.
                </p>

              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../services/api'

const route = useRoute()
const router = useRouter()

const participants = ref([])
const loading = ref(false)
const error = ref('')

async function loadParticipants() {
  loading.value = true
  error.value = ''

  try {

    const trekId = route.params.trekId

    const response = await api.get(
      `/staff/treks/${trekId}/participants`
    )

    participants.value = response.data

  } catch (err) {

    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to load participants.'

  } finally {
    loading.value = false
  }
}

function initials(name) {

  if (!name) return 'TR'

  const parts = name.trim().split(' ')

  if (parts.length >= 2) {
    return (
      parts[0][0] +
      parts[1][0]
    ).toUpperCase()
  }

  return name.substring(0, 2).toUpperCase()
}

function goBack() {
  router.push('/staff/my-treks')
}

onMounted(loadParticipants)
</script>

<style scoped>

.page-title {
  color: var(--tm-text);
  font-weight: 700;
}

.card {
  border-radius: 10px;
}

.table th {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #6c757d;
}

.table td {
  font-size: 0.9rem;
}

.participant-avatar {
  width: 38px;
  height: 38px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background-color: var(--tm-primary-light);
  color: var(--tm-primary-dark);

  font-size: 0.8rem;
  font-weight: 700;
}

</style>