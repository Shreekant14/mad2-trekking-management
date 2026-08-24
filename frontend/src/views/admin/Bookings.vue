<template>
  <div class="container-fluid py-4">

    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h1 class="fw-bold mb-1">Bookings</h1>
        <p class="text-muted mb-0">
          Manage trek booking records.
        </p>
      </div>

      <button
        class="btn btn-success"
        @click="loadBookings"
        :disabled="loading"
      >
        <i class="bi bi-arrow-clockwise me-2"></i>
        Refresh
      </button>
    </div>

    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-success"></div>
      <p class="text-muted mt-2">Loading bookings...</p>
    </div>

    <div v-else class="card border-0 shadow-sm">
      <div class="card-body">

        <div v-if="bookings.length === 0" class="text-center py-5">
          <i class="bi bi-calendar-x fs-1 text-muted"></i>
          <h5 class="mt-3">No booking records found</h5>
          <p class="text-muted mb-0">
            There are currently no bookings to display.
          </p>
        </div>

        <div v-else class="table-responsive">
          <table class="table table-hover align-middle mb-0">

            <thead>
              <tr>
                <th>ID</th>
                <th>Trekker</th>
                <th>Trek</th>
                <th>Participants</th>
                <th>Status</th>
                <th>Booked At</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="booking in bookings" :key="booking.id">

                <td>#{{ booking.booking_id || booking.id }}</td>

                <td>
                  {{ booking.trekker || booking.user || 'Unknown' }}
                </td>

                <td>
                  {{ booking.trek || booking.trek_title || 'Unknown' }}
                </td>

                <td>
                  {{ booking.number_of_people || 1 }}
                </td>

                <td>
                  <span
                    class="badge"
                    :class="statusClass(booking.status)"
                  >
                    {{ booking.status }}
                  </span>
                </td>

                <td>
                    {{ formatDateTime(booking.booked_at) }}
                </td>

              </tr>
            </tbody>

          </table>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'

const bookings = ref([])
const loading = ref(false)
const error = ref('')

async function loadBookings() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/admin/bookings')

    bookings.value = Array.isArray(response.data)
      ? response.data
      : response.data.bookings || []

  } catch (err) {
    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to load bookings.'
  } finally {
    loading.value = false
  }
}

function statusClass(status) {
  if (status === 'CONFIRMED') {
    return 'bg-success'
  }

  if (status === 'CANCELLED') {
    return 'bg-danger'
  }

  if (status === 'PENDING') {
    return 'bg-warning text-dark'
  }

  return 'bg-secondary'
}

function formatDateTime(value) {
  if (!value) {
    return '-'
  }

  return value
    .replace('T', ' ')
    .split('.')[0]
}

onMounted(loadBookings)
</script>