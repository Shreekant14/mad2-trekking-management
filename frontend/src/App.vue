<template>
  <div class="tm-app">

    <template v-if="authenticated">

      <Navbar
        :app-name="appName"
        :user-name="userName"
        :user-role="userRole"
        :user-initials="userInitials"
        @toggle-sidebar="mobileSidebar = !mobileSidebar"
        @logout="handleLogout"
      />

      <div class="d-flex">

        <Sidebar
          :role="userRole"
          :mobile-open="mobileSidebar"
          @logout="handleLogout"
        />

        <main class="flex-grow-1 tm-main">
          <RouterView />
        </main>

      </div>

    </template>

    <template v-else>
      <RouterView />
    </template>

  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import Navbar from './components/layout/Navbar.vue'
import Sidebar from './components/layout/Sidebar.vue'

import {
  getCurrentUser,
  isAuthenticated,
  logout
} from './services/auth'

const router = useRouter()

const mobileSidebar = ref(false)

const appName = 'Trekking Management System'

const authenticated = computed(() => isAuthenticated())

const user = computed(() => getCurrentUser())

const userName = computed(() => {
  return user.value?.full_name || 'User'
})

const userRole = computed(() => {
  return user.value?.role || 'TREKKER'
})

const userInitials = computed(() => {
  const name = userName.value.trim()

  if (!name) {
    return 'U'
  }

  const parts = name.split(/\s+/)

  if (parts.length >= 2) {
    return `${parts[0][0]}${parts[1][0]}`.toUpperCase()
  }

  return name.substring(0, 2).toUpperCase()
})

function handleLogout() {
  logout()
  router.push('/login')
}
</script>

<style>
.tm-app {
  min-height: 100vh;
}

.tm-main {
  min-width: 0;
  min-height: calc(100vh - 58px);
  background-color: var(--tm-background);
}
</style>
