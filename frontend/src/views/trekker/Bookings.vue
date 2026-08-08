<template>
  <div class="container-fluid p-4">

    <div class="d-flex flex-wrap justify-content-between align-items-center mb-4">
      <div>
        <h1 class="page-title mb-1">My Bookings</h1>
        <p class="text-muted mb-0">
          View and manage your trekking bookings.
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

    <!-- Loading -->
    <div
      v-if="loading"
      class="text-center py-5"
    >
      <div class="spinner-border text-success"></div>

      <p class="text-muted mt-3 mb-0">
        Loading your bookings...
      </p>
    </div>

    <!-- Booking table -->
    <div
      v-else
      class="card border-0 shadow-sm"
    >

      <div class="card-header bg-white py-3">

        <div class="d-flex justify-content-between align-items-center">

          <h5 class="mb-0 fw-bold">
            Booking History
          </h5>

          <span class="badge bg-success-subtle text-success">
            {{ bookings.length }} Bookings
          </span>

        </div>

      </div>

      <div class="table-responsive">

        <table class="table table-hover align-middle mb-0">

          <thead class="table-light">

            <tr>
              <th>Trek</th>
              <th>People</th>
              <th>Booked On</th>
              <th>Status</th>
              <th class="text-end">Action</th>
            </tr>

          </thead>

          <tbody>

            <tr
              v-for="booking in bookings"
              :key="booking.id"
            >

              <!-- Trek -->
              <td>

                <div class="fw-semibold">
                  {{ booking.trek_title }}
                </div>

                <small class="text-muted">
                  Trek #{{ booking.trek_id }}
                </small>

              </td>

              <!-- People -->
              <td>

                <span class="badge bg-light text-dark border">
                  <i class="bi bi-people me-1"></i>
                  {{ booking.number_of_people }}
                </span>

              </td>

              <!-- Date -->
              <td>
                {{ formatDate(booking.booked_at) }}
              </td>

              <!-- Status -->
              <td>

                <span
                  class="badge"
                  :class="statusClass(booking.status)"
                >
                  {{ booking.status }}
                </span>

              </td>

              <!-- Action -->
              <td class="text-end">

                <button
                  v-if="booking.status === 'CONFIRMED'"
                  class="btn btn-sm btn-outline-danger"
                  @click="cancelBooking(booking)"
                  :disabled="cancellingId === booking.id"
                >

                  <span
                    v-if="cancellingId === booking.id"
                    class="spinner-border spinner-border-sm me-1"
                  ></span>

                  <i
                    v-else
                    class="bi bi-x-circle me-1"
                  ></i>

                  {{ cancellingId === booking.id
                    ? 'Cancelling...'
                    : 'Cancel'
                  }}

                </button>

                <span
                  v-else
                  class="text-muted small"
                >
                  No action
                </span>

              </td>

            </tr>

            <!-- Empty -->
            <tr v-if="bookings.length === 0">

              <td
                colspan="5"
                class="text-center py-5"
              >

                <i class="bi bi-calendar-x fs-1 text-muted"></i>

                <h6 class="mt-3">
                  No bookings found
                </h6>

                <p class="text-muted mb-3">
                  You haven't booked any treks yet.
                </p>

                <router-link
                  to="/trekker/treks"
                  class="btn btn-success btn-sm"
                >
                  Explore Available Treks
                </router-link>

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
import api from '../../services/api'

const bookings = ref([])

const loading = ref(false)
const cancellingId = ref(null)

const error = ref('')
const success = ref('')

async function loadBookings() {
  loading.value = true
  error.value = ''

  try {

    const response = await api.get('/trekker/bookings')

    bookings.value = response.data

  } catch (err) {

    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to load your bookings.'

  } finally {
    loading.value = false
  }
}

async function cancelBooking(booking) {

  const confirmed = confirm(
    `Are you sure you want to cancel your booking for "${booking.trek_title}"?`
  )

  if (!confirmed) return

  cancellingId.value = booking.id

  error.value = ''
  success.value = ''

  try {

    await api.delete(
      `/trekker/bookings/${booking.id}`
    )

    success.value =
      'Booking cancelled successfully.'

    await loadBookings()

  } catch (err) {

    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to cancel booking.'

  } finally {
    cancellingId.value = null
  }
}

function formatDate(value) {

  if (!value) return '—'

  return new Date(value).toLocaleString('en-IN')
}

function statusClass(status) {

  if (status === 'CONFIRMED') {
    return 'bg-success-subtle text-success'
  }

  if (status === 'CANCELLED') {
    return 'bg-danger-subtle text-danger'
  }

  if (status === 'PENDING') {
    return 'bg-warning-subtle text-warning-emphasis'
  }

  return 'bg-secondary-subtle text-secondary'
}

onMounted(loadBookings)
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
</style>