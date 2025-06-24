<template>
  <div
    class="container-fluid d-flex justify-content-center align-items-center min-vh-100 bg-light"
  >
    <div class="card p-4 shadow rounded-5" style="width: 420px">
      <h3 class="text-center text-primary mb-4">Create Your Account</h3>
      <form @submit.prevent="register">
        <div class="form-outline mb-3">
          <input
            v-model="full_name"
            class="form-control"
            placeholder=" "
            required
          />
          <label class="form-label">Full Name</label>
        </div>

        <div class="form-outline mb-3">
          <input
            v-model="email"
            type="email"
            class="form-control"
            placeholder=" "
            required
          />
          <label class="form-label">Email</label>
        </div>

        <div class="form-outline mb-3">
          <input
            v-model="password"
            type="password"
            autocomplete="current-password"
            class="form-control"
            placeholder=" "
            required
          />
          <label class="form-label">Password</label>
        </div>

        <div class="form-outline mb-3">
          <input
            v-model="qualification"
            class="form-control"
            placeholder=" "
            required
          />
          <label class="form-label">Qualification</label>
        </div>

        <div class="form-outline mb-3">
          <input
            v-model="dob"
            type="date"
            class="form-control"
            placeholder=" "
            required
          />
          <label class="form-label">Date of Birth</label>
        </div>

        <button type="submit" class="btn btn-success w-100 mt-2">
          Register
        </button>

        <p class="text-center mt-3">
          Already have an account?
          <router-link to="/login">Log in</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useToast } from "vue-toastification";
import { useRouter } from "vue-router";

const toast = useToast();
const router = useRouter();

const email = ref("");
const password = ref("");
const full_name = ref("");
const qualification = ref("");
const dob = ref("");

const register = async () => {
  try {
    await axios.post("http://127.0.0.1:5000/auth/register", {
      email: email.value,
      password: password.value,
      full_name: full_name.value,
      qualification: qualification.value,
      dob: dob.value,
    });
    toast.success("Registration successful! Please log in.");
    router.push("/login");
  } catch (error) {
    toast.error(error.response?.data?.msg || "Registration failed.");
  }
};
</script>
