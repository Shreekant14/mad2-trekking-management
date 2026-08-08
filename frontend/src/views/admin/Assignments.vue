<template>
  <div class="container-fluid p-4">

    <!-- Header -->
    <div class="d-flex flex-wrap justify-content-between align-items-center mb-4">
      <div>
        <h1 class="page-title mb-1">Staff Assignments</h1>
        <p class="text-muted mb-0">
          Assign staff members to trekking programs.
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

    <!-- Assignment Form -->
    <div class="card border-0 shadow-sm mb-4">

      <div class="card-header bg-white py-3">
        <h5 class="mb-0 fw-bold">
          Assign Staff
        </h5>
      </div>

      <form @submit.prevent="assignStaff">

        <div class="card-body">

          <div class="row g-3">

            <div class="col-md-5">
              <label class="form-label">
                Trek
              </label>

              <select
                v-model="form.trek_id"
                class="form-select"
                required
              >
                <option value="" disabled>
                  Select a trek
                </option>

                <option
                  v-for="trek in treks"
                  :key="trek.id"
                  :value="trek.id"
                >
                  {{ trek.title }} — {{ trek.location }}
                </option>
              </select>
            </div>

            <div class="col-md-5">
              <label class="form-label">
                Staff Member
              </label>

              <select
                v-model="form.staff_id"
                class="form-select"
                required
              >
                <option value="" disabled>
                  Select staff member
                </option>

                <option
                  v-for="member in staff"
                  :key="member.id"
                  :value="member.id"
                >
                  {{ member.full_name }}
                </option>
              </select>
            </div>

            <div class="col-md-2 d-flex align-items-end">

              <button
                type="submit"
                class="btn btn-success w-100"
                :disabled="saving"
              >
                <span
                  v-if="saving"
                  class="spinner-border spinner-border-sm me-2"
                ></span>

                <i
                  v-else
                  class="bi bi-person-plus me-2"
                ></i>

                {{ saving ? 'Assigning...' : 'Assign' }}
              </button>

            </div>

          </div>

        </div>

      </form>

    </div>

    <!-- Assignment List -->
    <div class="card border-0 shadow-sm">

      <div class="card-header bg-white py-3">

        <div class="d-flex justify-content-between align-items-center">

          <h5 class="mb-0 fw-bold">
            Current Assignments
          </h5>

          <span class="badge bg-success-subtle text-success">
            {{ assignments.length }} Assignments
          </span>

        </div>

      </div>

      <div
        v-if="loading"
        class="text-center py-5"
      >
        <div class="spinner-border text-success"></div>

        <p class="text-muted mt-3 mb-0">
          Loading assignments...
        </p>
      </div>

      <div
        v-else
        class="table-responsive"
      >

        <table class="table table-hover align-middle mb-0">

          <thead class="table-light">

            <tr>
              <th>Staff Member</th>
              <th>Trek</th>
              <th>Assigned On</th>
              <th class="text-end">Action</th>
            </tr>

          </thead>

          <tbody>

            <tr
              v-for="assignment in assignments"
              :key="assignment.id"
            >

              <td>

                <div class="d-flex align-items-center gap-2">

                  <div class="staff-avatar">
                    {{ initials(assignment.staff_name) }}
                  </div>

                  <div>
                    <div class="fw-semibold">
                      {{ assignment.staff_name }}
                    </div>

                    <small class="text-muted">
                      Staff #{{ assignment.staff_id }}
                    </small>
                  </div>

                </div>

              </td>

              <td>

                <div class="fw-semibold">
                  {{ assignment.trek_title }}
                </div>

                <small class="text-muted">
                  Trek #{{ assignment.trek_id }}
                </small>

              </td>

              <td>
                {{ formatDate(assignment.assigned_on) }}
              </td>

              <td class="text-end">

                <button
                  class="btn btn-sm btn-outline-danger"
                  @click="removeAssignment(assignment)"
                  :disabled="removingId === assignment.id"
                >

                  <span
                    v-if="removingId === assignment.id"
                    class="spinner-border spinner-border-sm"
                  ></span>

                  <i
                    v-else
                    class="bi bi-person-dash"
                  ></i>

                </button>

              </td>

            </tr>

            <tr v-if="assignments.length === 0">

              <td
                colspan="4"
                class="text-center py-5"
              >

                <i class="bi bi-diagram-3 fs-1 text-muted"></i>

                <h6 class="mt-3">
                  No staff assignments
                </h6>

                <p class="text-muted mb-0">
                  Assign a staff member to a trek above.
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
import api from '../../services/api'

const treks = ref([])
const staff = ref([])
const assignments = ref([])

const loading = ref(false)
const saving = ref(false)
const removingId = ref(null)

const error = ref('')

const form = ref({
  trek_id: '',
  staff_id: ''
})

async function loadTreks() {
  const response = await api.get('/admin/treks')
  treks.value = response.data
}

async function loadStaff() {
  const response = await api.get('/admin/staff')
  staff.value = response.data.filter(
    member => member.is_active
  )
}

async function loadAssignments() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/admin/assignments')
    assignments.value = response.data
  } catch (err) {
    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to load assignments.'
  } finally {
    loading.value = false
  }
}

async function loadPageData() {
  try {
    await Promise.all([
      loadTreks(),
      loadStaff(),
      loadAssignments()
    ])
  } catch (err) {
    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to load assignment data.'
  }
}

async function assignStaff() {
  saving.value = true
  error.value = ''

  try {

    await api.post('/admin/assignments', {
      staff_id: Number(form.value.staff_id),
      trek_id: Number(form.value.trek_id)
    })

    form.value = {
      trek_id: '',
      staff_id: ''
    }

    await loadAssignments()

  } catch (err) {

    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to assign staff member.'

  } finally {
    saving.value = false
  }
}

async function removeAssignment(assignment) {

  const confirmed = confirm(
    `Remove ${assignment.staff_name} from ${assignment.trek_title}?`
  )

  if (!confirmed) return

  removingId.value = assignment.id
  error.value = ''

  try {

    await api.delete(
      `/admin/assignments/${assignment.id}`
    )

    await loadAssignments()

  } catch (err) {

    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to remove assignment.'

  } finally {
    removingId.value = null
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

  return new Date(value).toLocaleString('en-IN')
}

onMounted(loadPageData)
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

.form-label {
  font-size: 0.85rem;
  font-weight: 600;
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

</style>