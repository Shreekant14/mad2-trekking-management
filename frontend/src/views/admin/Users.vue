<template>
  <div class="container-fluid py-4">

    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h1 class="fw-bold mb-1">Users & Staff</h1>
        <p class="text-muted mb-0">
          Manage registered users and staff members.
        </p>
      </div>

      <button
        class="btn btn-success"
        @click="loadUsers"
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
      <p class="text-muted mt-2">Loading users...</p>
    </div>

    <div v-else class="card border-0 shadow-sm">
      <div class="card-body">

        <div v-if="users.length === 0" class="text-center py-5">
          <i class="bi bi-people fs-1 text-muted"></i>
          <h5 class="mt-3">No users found</h5>
          <p class="text-muted mb-0">
            There are currently no users to display.
          </p>
        </div>

        <div v-else class="table-responsive">
          <table class="table table-hover align-middle mb-0">

            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Role</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="user in users" :key="user.id">

                <td>#{{ user.id }}</td>

                <td class="fw-semibold">
                  {{ user.full_name }}
                </td>

                <td>
                  {{ user.email }}
                </td>

                <td>
                  {{ user.phone || '-' }}
                </td>

                <td>
                  <span class="badge bg-success-subtle text-success">
                    {{ user.role }}
                  </span>
                </td>

                <td>
                  <span
                    class="badge"
                    :class="user.is_active !== false
                      ? 'bg-success'
                      : 'bg-secondary'"
                  >
                    {{ user.is_active !== false ? 'ACTIVE' : 'INACTIVE' }}
                  </span>
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

const users = ref([])
const loading = ref(false)
const error = ref('')

async function loadUsers() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/admin/users')

    users.value = Array.isArray(response.data)
      ? response.data
      : response.data.users || []

  } catch (err) {
    console.error(err)

    error.value =
      err.response?.data?.message ||
      'Unable to load users.'
  } finally {
    loading.value = false
  }
}

onMounted(loadUsers)
</script>