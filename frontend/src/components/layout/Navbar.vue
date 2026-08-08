<template>
  <nav class="navbar navbar-expand-lg bg-white border-bottom shadow-sm sticky-top px-3 py-2">
    <div class="container-fluid px-0">

      <!-- Mobile menu button -->
      <button
        class="btn btn-sm btn-outline-secondary d-lg-none me-2"
        type="button"
        @click="$emit('toggle-sidebar')"
        aria-label="Toggle navigation"
      >
        <i class="bi bi-list fs-5"></i>
      </button>

      <!-- Brand -->
      <div class="navbar-brand d-flex align-items-center gap-2">
        <div class="brand-icon">
          <i class="bi bi-tree-fill"></i>
        </div>

        <span class="brand-text fw-bold d-none d-sm-inline">
          {{ appName }}
        </span>

        <span class="brand-text fw-bold d-inline d-sm-none">
          TMS
        </span>
      </div>

      <!-- Role -->
      <div class="role-pill d-none d-md-flex align-items-center gap-2 ms-3">
        <span class="role-dot"></span>
        <span>{{ userRole }} MODE</span>
      </div>

      <!-- User -->
      <div class="dropdown ms-auto">

        <button
          class="btn user-button d-flex align-items-center gap-2"
          type="button"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          <div class="text-end d-none d-md-block">
            <div class="fw-semibold small">
              {{ userName }}
            </div>

            <div class="text-muted role-label">
              {{ userRole }}
            </div>
          </div>

          <div class="user-avatar">
            {{ userInitials }}
          </div>

          <i class="bi bi-chevron-down small"></i>
        </button>

        <ul class="dropdown-menu dropdown-menu-end shadow-sm">

          <li class="px-3 py-2 border-bottom">
            <div class="fw-semibold">
              {{ userName }}
            </div>

            <span class="badge bg-success-subtle text-success mt-1">
              {{ userRole }}
            </span>
          </li>

          <li>
            <button
              class="dropdown-item text-danger"
              type="button"
              @click="$emit('logout')"
            >
              <i class="bi bi-box-arrow-right me-2"></i>
              Sign Out
            </button>
          </li>

        </ul>

      </div>

    </div>
  </nav>
</template>

<script setup>
defineProps({
  appName: {
    type: String,
    default: 'Trekking Management System'
  },

  userName: {
    type: String,
    default: 'User'
  },

  userRole: {
    type: String,
    default: 'TREKKER'
  },

  userInitials: {
    type: String,
    default: 'US'
  }
})

defineEmits([
  'toggle-sidebar',
  'logout'
])
</script>

<style scoped>
.brand-icon {
  width: 38px;
  height: 38px;
  border-radius: 10px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: #fff;
  background-color: var(--tm-primary);

  font-size: 1.1rem;
}

.brand-text {
  color: var(--tm-primary-dark);
}

.role-pill {
  padding: 6px 14px;

  border: 1px solid #d9e7da;
  border-radius: 50px;

  background-color: var(--tm-primary-light);

  color: var(--tm-primary-dark);

  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.05em;
}

.role-dot {
  width: 8px;
  height: 8px;

  border-radius: 50%;
  background-color: var(--tm-accent);
}

.user-button {
  border: none;
  background: transparent;
  color: var(--tm-text);
}

.user-button:hover,
.user-button:focus {
  background-color: var(--tm-primary-light);
}

.user-avatar {
  width: 38px;
  height: 38px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background-color: var(--tm-primary-light);
  border: 1.5px solid var(--tm-primary);

  color: var(--tm-primary-dark);

  font-size: 0.8rem;
  font-weight: 700;
}

.role-label {
  font-size: 0.65rem;
  letter-spacing: 0.04em;
}
</style>