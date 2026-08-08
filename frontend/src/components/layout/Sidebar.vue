<template>
  <aside
    class="tm-sidebar"
    :class="{ 'mobile-open': mobileOpen }"
  >

    <div class="sidebar-inner">

      <div class="sidebar-heading">
        MAIN MENU
      </div>

      <!-- ADMIN -->
      <template v-if="role === 'ADMIN'">

        <RouterLink
          to="/admin"
          class="sidebar-link"
        >
          <i class="bi bi-grid-1x2"></i>
          <span>Dashboard</span>
        </RouterLink>

        <RouterLink
          to="/admin/treks"
          class="sidebar-link"
        >
          <i class="bi bi-map"></i>
          <span>Treks</span>
        </RouterLink>

        <RouterLink
          to="/admin/users"
          class="sidebar-link"
        >
          <i class="bi bi-people"></i>
          <span>Users</span>
        </RouterLink>

        <RouterLink
          to="/admin/staff"
          class="sidebar-link"
        >
          <i class="bi bi-person-badge"></i>
          <span>Staff</span>
        </RouterLink>

        <RouterLink
          to="/admin/assignments"
          class="sidebar-link"
        >
          <i class="bi bi-person-check"></i>
          <span>Assignments</span>
        </RouterLink>

        <RouterLink
          to="/admin/bookings"
          class="sidebar-link"
        >
          <i class="bi bi-calendar-check"></i>
          <span>Bookings</span>
        </RouterLink>

      </template>

      <!-- STAFF -->
      <template v-if="role === 'STAFF'">

        <RouterLink
          to="/staff"
          class="sidebar-link"
        >
          <i class="bi bi-grid-1x2"></i>
          <span>Dashboard</span>
        </RouterLink>

        <RouterLink
          to="/staff/my-treks"
          class="sidebar-link"
        >
          <i class="bi bi-map"></i>
          <span>My Treks</span>
        </RouterLink>

        <RouterLink
          to="/staff/participants"
          class="sidebar-link"
        >
          <i class="bi bi-people"></i>
          <span>Participants</span>
        </RouterLink>

      </template>

      <!-- TREKKER -->
      <template v-if="role === 'TREKKER'">

        <RouterLink
          to="/trekker"
          class="sidebar-link"
        >
          <i class="bi bi-grid-1x2"></i>
          <span>Dashboard</span>
        </RouterLink>

        <RouterLink
          to="/trekker/treks"
          class="sidebar-link"
        >
          <i class="bi bi-map"></i>
          <span>Explore Treks</span>
        </RouterLink>

        <RouterLink
          to="/trekker/bookings"
          class="sidebar-link"
        >
          <i class="bi bi-calendar-check"></i>
          <span>My Bookings</span>
        </RouterLink>

      </template>

      <div class="sidebar-footer">
        <button
          class="logout-button"
          type="button"
          @click="$emit('logout')"
        >
          <i class="bi bi-box-arrow-left"></i>
          <span>Sign Out</span>
        </button>
      </div>

    </div>

  </aside>
</template>

<script setup>
defineProps({
  role: {
    type: String,
    default: 'TREKKER'
  },

  mobileOpen: {
    type: Boolean,
    default: false
  }
})

defineEmits(['logout'])
</script>

<style scoped>
.tm-sidebar {
  width: 240px;
  min-width: 240px;

  min-height: calc(100vh - 58px);

  background-color: var(--tm-primary-dark);

  transition: transform 0.2s ease;
}

.sidebar-inner {
  display: flex;
  flex-direction: column;

  height: calc(100vh - 58px);

  padding: 22px 14px;
}

.sidebar-heading {
  padding: 0 12px 10px;

  color: #a9c8ac;

  font-size: 0.7rem;
  font-weight: 700;

  letter-spacing: 0.12em;
}

.sidebar-link {
  position: relative;

  display: flex;
  align-items: center;
  gap: 12px;

  padding: 11px 13px;
  margin-bottom: 5px;

  border-radius: 9px;

  color: #e8f5e9;

  font-size: 0.9rem;
  font-weight: 500;

  transition: all 0.15s ease;
}

.sidebar-link i {
  width: 20px;

  font-size: 1rem;
}

.sidebar-link:hover {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.1);
}

.sidebar-link.router-link-active {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.13);
}

.sidebar-link.router-link-active::before {
  content: '';

  position: absolute;
  left: 0;
  top: 8px;
  bottom: 8px;

  width: 4px;

  border-radius: 0 4px 4px 0;

  background-color: var(--tm-accent);
}

.sidebar-footer {
  margin-top: auto;
  padding-top: 15px;
}

.logout-button {
  width: 100%;

  display: flex;
  align-items: center;
  gap: 12px;

  padding: 10px 13px;

  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 9px;

  background: transparent;

  color: #e8f5e9;

  font-size: 0.9rem;
}

.logout-button:hover {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.1);
}

@media (max-width: 991.98px) {
  .tm-sidebar {
    position: fixed;
    top: 58px;
    left: 0;
    bottom: 0;

    z-index: 1040;

    transform: translateX(-100%);
  }

  .tm-sidebar.mobile-open {
    transform: translateX(0);
  }
}
</style>