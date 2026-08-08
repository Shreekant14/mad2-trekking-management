<template>
  <div class="container-fluid p-4">

    <div class="mb-4">
      <h1 class="page-title mb-1">Available Treks</h1>
      <p class="text-muted mb-0">
        Explore upcoming trekking programs and reserve your place.
      </p>
    </div>

    <div
      v-if="success"
      class="alert alert-success"
    >
      <i class="bi bi-check-circle me-2"></i>
      {{ success }}
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
        Loading available treks...
      </p>
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

          <div class="card-body d-flex flex-column">

            <div class="d-flex justify-content-between align-items-center mb-3">

              <span class="badge bg-success-subtle text-success">
                {{ trek.status }}
              </span>

              <span class="small text-muted">
                {{ trek.difficulty }}
              </span>

            </div>

            <h5 class="fw-bold mb-2">
              {{ trek.title }}
            </h5>

            <p class="text-muted mb-3">
              <i class="bi bi-geo-alt me-1"></i>
              {{ trek.location }}
            </p>

            <p class="description">
              {{ trek.description || 'No description available.' }}
            </p>

            <div class="row g-3 small mb-4">

              <div class="col-6">
                <div class="info-label">
                  Duration
                </div>
                <strong>
                  {{ trek.duration }} days
                </strong>
              </div>

              <div class="col-6">
                <div class="info-label">
                  Price
                </div>
                <strong>
                  ₹{{ trek.price }}
                </strong>
              </div>

              <div class="col-6">
                <div class="info-label">
                  Start Date
                </div>
                <strong>
                  {{ trek.start_date }}
                </strong>
              </div>

              <div class="col-6">
                <div class="info-label">
                  Available Slots
                </div>
                <strong>
                  {{ trek.available_slots }}
                </strong>
              </div>

            </div>

            <div class="mt-auto">

              <div
                v-if="trek.available_slots === 0"
                class="alert alert-secondary py-2 small mb-0"
              >
                No slots available.
              </div>

              <button
                v-else
                class="btn btn-success w-100"
                @click="openBooking(trek)"
              >
                <i class="bi bi-calendar-plus me-2"></i>
                Book Trek
              </button>

            </div>

          </div>

        </div>

      </div>

      <div
        v-if="treks.length === 0"
        class="col-12"
      >
        <div class="card border-0 shadow-sm">
          <div class="card-body text-center py-5">

            <i class="bi bi-compass fs-1 text-muted"></i>

            <h5 class="mt-3">
              No upcoming treks
            </h5>

            <p class="text-muted mb-0">
              There are currently no available trekking programs.
            </p>

          </div>
        </div>
      </div>

    </div>

    <!-- Booking Modal -->
    <div
      v-if="selectedTrek"
      class="modal-backdrop-custom"
      @click.self="closeBooking"
    >

      <div class="booking-modal">

        <div class="card border-0 shadow-lg">

          <div class="card-header bg-white d-flex justify-content-between align-items-center py-3">

            <h5 class="mb-0 fw-bold">
              Book Trek
            </h5>

            <button
              type="button"
              class="btn-close"
              @click="closeBooking"
            ></button>

          </div>

          <div class="card-body">

            <h5 class="fw-bold">
              {{ selectedTrek.title }}
            </h5>

            <p class="text-muted">
              <i class="bi bi-geo-alt me-1"></i>
              {{ selectedTrek.location }}
            </p>

            <div class="alert alert-light border">

              <div class="d-flex justify-content-between">
                <span>Price per person</span>
                <strong>₹{{ selectedTrek.price }}</strong>
              </div>

              <div class="d-flex justify-content-between mt-2">
                <span>Available slots</span>
                <strong>{{ selectedTrek.available_slots }}</strong>
              </div>

            </div>

            <label class="form-label fw-semibold">
              Number of People
            </label>

            <input
              v-model.number="numberOfPeople"
              type="number"
              min="1"
              :max="selectedTrek.available_slots"
              class="form-control"
            />

            <div class="mt-3 text-end">
              <span class="text-muted">
                Total:
              </span>

              <strong class="ms-2 fs-5">
                ₹{{ totalPrice }}
              </strong>
            </div>

          </div>

          <div class="card-footer bg-white d-flex justify-content-end gap-2">

            <button
              type="button"
              class="btn btn-outline-secondary"
              @click="closeBooking"
              :disabled="booking"
            >
              Cancel
            </button>

            <button
              type="button"
              class="btn btn-success"
              @click="confirmBooking"
              :disabled="booking"
            >

              <span
                v-if="booking"
                class="spinner-border spinner-border-sm me-2"
              ></span>

              {{ booking ? 'Booking...' : 'Confirm Booking' }}

            </button>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../services/api'

const treks = ref([])

const loading = ref(false)
const booking = ref(false)

const error = ref('')
const success = ref('')

const selectedTrek = ref(null)
const numberOfPeople = ref(1)

const totalPrice = computed(() => {
  if (!selectedTrek.value) return 0

  return (
    Number(selectedTrek.value.price) *
    Number(numberOfPeople.value || 0)
  )
})

async function loadTreks() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/trekker/treks')
    treks.value = response.data
  } catch (err) {
    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to load available treks.'
  } finally {
    loading.value = false
  }
}

function openBooking(trek) {
  selectedTrek.value = trek
  numberOfPeople.value = 1
  error.value = ''
  success.value = ''
}

function closeBooking() {
  if (!booking.value) {
    selectedTrek.value = null
  }
}

async function confirmBooking() {

  if (!selectedTrek.value) return

  const people = Number(numberOfPeople.value)

  if (
    !Number.isInteger(people) ||
    people < 1
  ) {
    error.value = 'Number of people must be at least 1.'
    return
  }

  if (
    people > selectedTrek.value.available_slots
  ) {
    error.value = 'Not enough slots available.'
    return
  }

  booking.value = true
  error.value = ''
  success.value = ''

  try {

    await api.post('/trekker/bookings', {
      trek_id: selectedTrek.value.id,
      number_of_people: people
    })

    selectedTrek.value = null

    success.value =
      'Booking successful! Your trek has been confirmed.'

    await loadTreks()

  } catch (err) {

    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to complete booking.'

  } finally {
    booking.value = false
  }
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
  transition: transform 0.15s ease;
}

.trek-card:hover {
  transform: translateY(-2px);
}

.description {
  color: #6c757d;
  font-size: 0.9rem;
  min-height: 42px;
}

.info-label {
  color: #6c757d;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 2px;
}

.modal-backdrop-custom {
  position: fixed;
  inset: 0;
  z-index: 1050;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 20px;

  background: rgba(0, 0, 0, 0.45);
}

.booking-modal {
  width: 100%;
  max-width: 500px;
}
</style>