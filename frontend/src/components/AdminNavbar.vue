<template>
  <nav
    class="navbar navbar-expand-lg navbar-dark bg-primary px-4 fixed-top shadow"
  >
    <div class="container-fluid">
      <span class="navbar-brand fw-bold">Admin Dashboard</span>
      <div class="d-flex align-items-center ms-auto">
        <RouterLink class="nav-link text-white me-3" to="/admin-dashboard">
          <i class="bi bi-journal-text me-1"></i>Quizzes
        </RouterLink>
        <RouterLink
          class="nav-link text-white me-3"
          to="/admin-dashboard/users"
        >
          <i class="bi bi-people-fill me-1"></i>Users
        </RouterLink>
        <button class="btn btn-danger btn-sm fw-bold" @click="$emit('logout')">
          <i class="bi bi-power"></i> Logout
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
// No internal script logic needed here
</script>
