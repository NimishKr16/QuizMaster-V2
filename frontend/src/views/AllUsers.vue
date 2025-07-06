<template>
  <AdminNavbar @logout="handleLogoutClick" />

  <div class="container py-5">
    <h2 class="text-center fw-bold mb-4">User Management</h2>
    <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead class="table-dark">
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Qualification</th>
            <th>Date of Birth</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.full_name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.qualification }}</td>
            <td>{{ user.dob }}</td>
            <td>
              <button
                class="btn btn-sm btn-danger"
                @click="deleteUser(user.id)"
              >
                <i class="bi bi-trash"></i> Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useToast } from "vue-toastification";
import AdminNavbar from "@/components/AdminNavbar.vue";

const logoutModalVisible = ref(false);

const handleLogoutClick = () => {
  logoutModalVisible.value = true;
};
const users = ref([]);
const toast = useToast();

const fetchUsers = async () => {
  try {
    const token = localStorage.getItem("token");
    const res = await axios.get("http://127.0.0.1:5000/admin/users", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    users.value = res.data;
  } catch (err) {
    toast.error("Failed to fetch users");
    console.error(err);
  }
};

const deleteUser = async (userId) => {
  if (!confirm("Are you sure you want to delete this user?")) return;

  try {
    const token = localStorage.getItem("token");
    await axios.delete(`http://127.0.0.1:5000/admin/user/${userId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    users.value = users.value.filter((user) => user.id !== userId);
    toast.success("User deleted successfully");
  } catch (err) {
    toast.error("Failed to delete user");
    console.error(err);
  }
};

onMounted(fetchUsers);
</script>
