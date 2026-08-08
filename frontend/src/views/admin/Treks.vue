<template>
  <div class="container-fluid p-4">

    <!-- Header -->
    <div class="d-flex flex-wrap justify-content-between align-items-center mb-4">
      <div>
        <h1 class="page-title mb-1">Treks</h1>
        <p class="text-muted mb-0">
          Manage trekking destinations and availability.
        </p>
      </div>

      <button
        class="btn btn-success mt-3 mt-md-0"
        @click="openCreateModal"
      >
        <i class="bi bi-plus-lg me-2"></i>
        Add Trek
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
      v-if="loading"
      class="text-center py-5"
    >
      <div class="spinner-border text-success"></div>
      <p class="text-muted mt-3">Loading treks...</p>
    </div>

    <!-- Trek Table -->
    <div
      v-else
      class="card border-0 shadow-sm"
    >

      <div class="card-header bg-white border-bottom py-3">
        <div class="d-flex justify-content-between align-items-center">

          <h5 class="mb-0 fw-bold">
            Trek List
          </h5>

          <span class="badge bg-success-subtle text-success">
            {{ treks.length }} Treks
          </span>

        </div>
      </div>

      <div class="table-responsive">

        <table class="table table-hover align-middle mb-0">

          <thead class="table-light">

            <tr>
              <th>Title</th>
              <th>Location</th>
              <th>Difficulty</th>
              <th>Dates</th>
              <th>Price</th>
              <th>Slots</th>
              <th>Status</th>
              <th class="text-end">Actions</th>
            </tr>

          </thead>

          <tbody>

            <tr
              v-for="trek in treks"
              :key="trek.id"
            >

              <td>
                <div class="fw-semibold">
                  {{ trek.title }}
                </div>

                <small class="text-muted">
                  #{{ trek.id }}
                </small>
              </td>

              <td>
                <i class="bi bi-geo-alt me-1 text-success"></i>
                {{ trek.location }}
              </td>

              <td>
                <span class="badge difficulty-badge">
                  {{ trek.difficulty }}
                </span>
              </td>

              <td>
                <small>
                  {{ trek.start_date }}
                  <br>
                  → {{ trek.end_date }}
                </small>
              </td>

              <td>
                <strong>₹{{ trek.price }}</strong>
              </td>

              <td>
                {{ trek.available_slots }} /
                {{ trek.total_slots }}
              </td>

              <td>
                <span
                  class="badge"
                  :class="statusClass(trek.status)"
                >
                  {{ trek.status }}
                </span>
              </td>

              <td class="text-end">

                <button
                  class="btn btn-sm btn-outline-success me-2"
                  @click="openEditModal(trek)"
                  title="Edit"
                >
                  <i class="bi bi-pencil"></i>
                </button>

                <button
                  class="btn btn-sm btn-outline-danger"
                  @click="deleteTrek(trek.id)"
                  title="Delete"
                >
                  <i class="bi bi-trash"></i>
                </button>

              </td>

            </tr>

            <!-- Empty -->
            <tr v-if="treks.length === 0">

              <td
                colspan="8"
                class="text-center py-5"
              >

                <i class="bi bi-map fs-1 text-muted"></i>

                <h6 class="mt-3">
                  No treks available
                </h6>

                <p class="text-muted mb-0">
                  Create your first trek to get started.
                </p>

              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </div>
  <!-- Create / Edit Trek Modal -->
<div
  v-if="showModal"
  class="modal-backdrop-custom"
  @click.self="closeModal"
>
  <div class="modal-dialog-custom">

    <div class="card border-0 shadow-lg">

      <div class="card-header bg-white d-flex justify-content-between align-items-center py-3">
        <h5 class="mb-0 fw-bold">
          {{ editing ? 'Edit Trek' : 'Add New Trek' }}
        </h5>

        <button
          type="button"
          class="btn-close"
          @click="closeModal"
        ></button>
      </div>

      <form @submit.prevent="saveTrek">

        <div class="card-body">

          <div class="row g-3">

            <div class="col-md-6">
              <label class="form-label">Trek Title</label>
              <input
                v-model="form.title"
                type="text"
                class="form-control"
                required
              >
            </div>

            <div class="col-md-6">
              <label class="form-label">Location</label>
              <input
                v-model="form.location"
                type="text"
                class="form-control"
                required
              >
            </div>

            <div class="col-md-4">
              <label class="form-label">Difficulty</label>

              <select
                v-model="form.difficulty"
                class="form-select"
                required
              >
                <option value="EASY">EASY</option>
                <option value="MODERATE">MODERATE</option>
                <option value="HARD">HARD</option>
              </select>
            </div>

            <div class="col-md-4">
              <label class="form-label">Duration (days)</label>

              <input
                v-model.number="form.duration"
                type="number"
                min="1"
                class="form-control"
                required
              >
            </div>

            <div class="col-md-4">
              <label class="form-label">Price (₹)</label>

              <input
                v-model.number="form.price"
                type="number"
                min="0"
                step="0.01"
                class="form-control"
                required
              >
            </div>

            <div class="col-md-6">
              <label class="form-label">Start Date</label>

              <input
                v-model="form.start_date"
                type="date"
                class="form-control"
                required
              >
            </div>

            <div class="col-md-6">
              <label class="form-label">End Date</label>

              <input
                v-model="form.end_date"
                type="date"
                class="form-control"
                required
              >
            </div>

            <div class="col-md-6">
              <label class="form-label">Total Slots</label>

              <input
                v-model.number="form.total_slots"
                type="number"
                min="1"
                class="form-control"
                required
              >
            </div>

            <div
              v-if="editing"
              class="col-md-6"
            >
              <label class="form-label">Available Slots</label>

              <input
                v-model.number="form.available_slots"
                type="number"
                min="0"
                class="form-control"
                required
              >
            </div>

            <div
              v-if="editing"
              class="col-md-6"
            >
              <label class="form-label">Status</label>

              <select
                v-model="form.status"
                class="form-select"
              >
                <option value="UPCOMING">UPCOMING</option>
                <option value="COMPLETED">COMPLETED</option>
                <option value="CANCELLED">CANCELLED</option>
              </select>
            </div>

            <div class="col-12">
              <label class="form-label">Description</label>

              <textarea
                v-model="form.description"
                class="form-control"
                rows="3"
              ></textarea>
            </div>

          </div>

        </div>

        <div class="card-footer bg-white d-flex justify-content-end gap-2">

          <button
            type="button"
            class="btn btn-outline-secondary"
            @click="closeModal"
            :disabled="saving"
          >
            Cancel
          </button>

          <button
            type="submit"
            class="btn btn-success"
            :disabled="saving"
          >
            <span
              v-if="saving"
              class="spinner-border spinner-border-sm me-2"
            ></span>

            {{ saving ? 'Saving...' : 'Save Trek' }}
          </button>

        </div>

      </form>

    </div>

  </div>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'

const treks = ref([])
const loading = ref(false)
const error = ref('')

const showModal = ref(false)
const editing = ref(false)
const saving = ref(false)

const form = ref({
  id: null,
  title: '',
  location: '',
  difficulty: 'MODERATE',
  duration: 1,
  price: '',
  description: '',
  start_date: '',
  end_date: '',
  total_slots: 1,
  available_slots: 1,
  status: 'UPCOMING'
})

function resetForm() {
  form.value = {
    id: null,
    title: '',
    location: '',
    difficulty: 'MODERATE',
    duration: 1,
    price: '',
    description: '',
    start_date: '',
    end_date: '',
    total_slots: 1,
    available_slots: 1,
    status: 'UPCOMING'
  }
}

async function loadTreks() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/admin/treks')
    treks.value = response.data
  } catch (err) {
    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to load treks.'
  } finally {
    loading.value = false
  }
}

function openCreateModal() {
  editing.value = false
  resetForm()
  showModal.value = true
}

function openEditModal(trek) {
  editing.value = true

  form.value = {
    id: trek.id,
    title: trek.title,
    location: trek.location,
    difficulty: trek.difficulty,
    duration: trek.duration,
    price: trek.price,
    description: trek.description || '',
    start_date: trek.start_date,
    end_date: trek.end_date,
    total_slots: trek.total_slots,
    available_slots: trek.available_slots,
    status: trek.status
  }

  showModal.value = true
}

function closeModal() {
  if (!saving.value) {
    showModal.value = false
  }
}

async function saveTrek() {
  saving.value = true
  error.value = ''

  try {
    const payload = {
      title: form.value.title,
      location: form.value.location,
      difficulty: form.value.difficulty,
      duration: Number(form.value.duration),
      price: Number(form.value.price),
      description: form.value.description,
      start_date: form.value.start_date,
      end_date: form.value.end_date,
      total_slots: Number(form.value.total_slots)
    }

    if (editing.value) {
      payload.available_slots = Number(form.value.available_slots)
      payload.status = form.value.status

      await api.put(
        `/admin/treks/${form.value.id}`,
        payload
      )
    } else {
      await api.post('/admin/treks', payload)
    }

    showModal.value = false

    await loadTreks()

  } catch (err) {
    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to save trek.'
  } finally {
    saving.value = false
  }
}

async function deleteTrek(id) {
  const confirmed = confirm(
    'Are you sure you want to delete this trek?'
  )

  if (!confirmed) return

  try {
    await api.delete(`/admin/treks/${id}`)
    await loadTreks()
  } catch (err) {
    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to delete trek.'
  }
}

function statusClass(status) {
  if (status === 'UPCOMING') {
    return 'bg-success-subtle text-success'
  }

  if (status === 'COMPLETED') {
    return 'bg-secondary-subtle text-secondary'
  }

  if (status === 'CANCELLED') {
    return 'bg-danger-subtle text-danger'
  }

  return 'bg-warning-subtle text-warning-emphasis'
}

onMounted(loadTreks)
</script>

<style scoped>

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

.modal-dialog-custom {
  width: 100%;
  max-width: 800px;

  max-height: 90vh;
  overflow-y: auto;
}

.form-label {
  font-weight: 600;
  font-size: 0.85rem;
}

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

.difficulty-badge {
  background-color: var(--tm-primary-light);
  color: var(--tm-primary-dark);
}

</style>