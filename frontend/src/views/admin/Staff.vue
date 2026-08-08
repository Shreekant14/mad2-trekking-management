<template>
  <div class="container-fluid p-4">

    <!-- Header -->
    <div class="d-flex flex-wrap justify-content-between align-items-center mb-4">
      <div>
        <h1 class="page-title mb-1">Staff Management</h1>
        <p class="text-muted mb-0">
          Manage staff members and their account status.
        </p>
      </div>

      <button
        class="btn btn-success mt-3 mt-md-0"
        @click="openCreateModal"
      >
        <i class="bi bi-person-plus me-2"></i>
        Add Staff
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

    <!-- Staff Table -->
    <div class="card border-0 shadow-sm">

      <div class="card-header bg-white py-3">
        <div class="d-flex justify-content-between align-items-center">
          <h5 class="mb-0 fw-bold">
            Staff Members
          </h5>

          <span class="badge bg-success-subtle text-success">
            {{ staff.length }} Staff
          </span>
        </div>
      </div>

      <div
        v-if="loading"
        class="text-center py-5"
      >
        <div class="spinner-border text-success"></div>
        <p class="text-muted mt-3 mb-0">
          Loading staff...
        </p>
      </div>

      <div
        v-else
        class="table-responsive"
      >
        <table class="table table-hover align-middle mb-0">

          <thead class="table-light">
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Status</th>
              <th>Created</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="member in staff"
              :key="member.id"
            >

              <td>
                <div class="d-flex align-items-center gap-2">

                  <div class="staff-avatar">
                    {{ initials(member.full_name) }}
                  </div>

                  <div>
                    <div class="fw-semibold">
                      {{ member.full_name }}
                    </div>

                    <small class="text-muted">
                      Staff #{{ member.id }}
                    </small>
                  </div>

                </div>
              </td>

              <td>{{ member.email }}</td>

              <td>
                {{ member.phone || '—' }}
              </td>

              <td>
                <span
                  class="badge"
                  :class="
                    member.is_active
                      ? 'bg-success-subtle text-success'
                      : 'bg-danger-subtle text-danger'
                  "
                >
                  {{ member.is_active ? 'ACTIVE' : 'INACTIVE' }}
                </span>
              </td>

              <td>
                <small>
                  {{ formatDate(member.created_at) }}
                </small>
              </td>

              <td class="text-end">

                <button
                  class="btn btn-sm btn-outline-success me-2"
                  @click="openEditModal(member)"
                  title="Edit staff"
                >
                  <i class="bi bi-pencil"></i>
                </button>

                <button
                  class="btn btn-sm"
                  :class="
                    member.is_active
                      ? 'btn-outline-danger'
                      : 'btn-outline-success'
                  "
                  @click="toggleStatus(member)"
                  :title="
                    member.is_active
                      ? 'Deactivate'
                      : 'Activate'
                  "
                >
                  <i
                    :class="
                      member.is_active
                        ? 'bi bi-person-dash'
                        : 'bi bi-person-check'
                    "
                  ></i>
                </button>

              </td>

            </tr>

            <tr v-if="staff.length === 0">
              <td
                colspan="6"
                class="text-center py-5"
              >
                <i class="bi bi-people fs-1 text-muted"></i>

                <h6 class="mt-3">
                  No staff members found
                </h6>

                <p class="text-muted mb-0">
                  Add a staff member to get started.
                </p>
              </td>
            </tr>

          </tbody>

        </table>
      </div>

    </div>

    <!-- Create / Edit Modal -->
    <div
      v-if="showModal"
      class="modal-backdrop-custom"
      @click.self="closeModal"
    >

      <div class="modal-dialog-custom">

        <div class="card border-0 shadow-lg">

          <div class="card-header bg-white d-flex justify-content-between align-items-center py-3">

            <h5 class="mb-0 fw-bold">
              {{ editing ? 'Edit Staff' : 'Add Staff Member' }}
            </h5>

            <button
              class="btn-close"
              type="button"
              @click="closeModal"
            ></button>

          </div>

          <form @submit.prevent="saveStaff">

            <div class="card-body">

              <div class="row g-3">

                <div class="col-12">
                  <label class="form-label">
                    Full Name
                  </label>

                  <input
                    v-model="form.full_name"
                    type="text"
                    class="form-control"
                    required
                  >
                </div>

                <div class="col-md-6">
                  <label class="form-label">
                    Email
                  </label>

                  <input
                    v-model="form.email"
                    type="email"
                    class="form-control"
                    required
                  >
                </div>

                <div class="col-md-6">
                  <label class="form-label">
                    Phone
                  </label>

                  <input
                    v-model="form.phone"
                    type="tel"
                    class="form-control"
                  >
                </div>

                <div
                  v-if="!editing"
                  class="col-12"
                >
                  <label class="form-label">
                    Password
                  </label>

                  <input
                    v-model="form.password"
                    type="password"
                    class="form-control"
                    minlength="6"
                    required
                  >
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

                {{ saving ? 'Saving...' : 'Save Staff' }}
              </button>

            </div>

          </form>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'

const staff = ref([])
const loading = ref(false)
const saving = ref(false)
const error = ref('')

const showModal = ref(false)
const editing = ref(false)

const form = ref({
  id: null,
  full_name: '',
  email: '',
  phone: '',
  password: ''
})

function resetForm() {
  form.value = {
    id: null,
    full_name: '',
    email: '',
    phone: '',
    password: ''
  }
}

async function loadStaff() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/admin/staff')
    staff.value = response.data
  } catch (err) {
    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to load staff members.'
  } finally {
    loading.value = false
  }
}

function openCreateModal() {
  editing.value = false
  resetForm()
  showModal.value = true
}

function openEditModal(member) {
  editing.value = true

  form.value = {
    id: member.id,
    full_name: member.full_name,
    email: member.email,
    phone: member.phone || '',
    password: ''
  }

  showModal.value = true
}

function closeModal() {
  if (!saving.value) {
    showModal.value = false
  }
}

async function saveStaff() {
  saving.value = true
  error.value = ''

  try {

    if (editing.value) {

      await api.put(
        `/admin/staff/${form.value.id}`,
        {
          full_name: form.value.full_name,
          email: form.value.email,
          phone: form.value.phone
        }
      )

    } else {

      await api.post(
        '/admin/staff',
        {
          full_name: form.value.full_name,
          email: form.value.email,
          phone: form.value.phone,
          password: form.value.password
        }
      )

    }

    showModal.value = false

    await loadStaff()

  } catch (err) {

    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to save staff member.'

  } finally {
    saving.value = false
  }
}

async function toggleStatus(member) {

  const action = member.is_active
    ? 'deactivate'
    : 'activate'

  if (!confirm(`Are you sure you want to ${action} this staff member?`)) {
    return
  }

  try {

    await api.put(
      `/admin/staff/${member.id}/status`,
      {
        is_active: !member.is_active
      }
    )

    await loadStaff()

  } catch (err) {

    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to update staff status.'
  }
}

function initials(name) {

  if (!name) return 'ST'

  const parts = name.trim().split(' ')

  if (parts.length >= 2) {
    return (
      parts[0][0] +
      parts[1][0]
    ).toUpperCase()
  }

  return name.substring(0, 2).toUpperCase()
}

function formatDate(value) {

  if (!value) return '—'

  return new Date(value).toLocaleDateString('en-IN')
}

onMounted(loadStaff)
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

.staff-avatar {
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
  max-width: 650px;
  max-height: 90vh;
  overflow-y: auto;
}

.form-label {
  font-size: 0.85rem;
  font-weight: 600;
}

</style>