<template>
  <div
    class="container min-vh-100 d-flex flex-column justify-content-center align-items-center"
  >
    <h2 class="text-center fw-bold mb-4">Welcome Back to QuizMaster</h2>
    <div class="card p-4 shadow-4" style="width: 400px">
      <h4 class="text-center mb-4">Login</h4>
      <form @submit.prevent="login">
        <div class="form-outline mb-4">
          <input
            v-model="email"
            type="email"
            id="loginEmail"
            class="form-control"
            required
          />
          <label class="form-label" for="loginEmail">Email address</label>
        </div>

        <div class="form-outline mb-4">
          <input
            v-model="password"
            type="password"
            id="loginPassword"
            class="form-control"
            required
          />
          <label class="form-label" for="loginPassword">Password</label>
        </div>

        <button type="submit" class="btn btn-primary btn-block w-100 mb-3">
          Login
        </button>

        <p class="text-center">
          Don't have an account?
          <router-link to="/register">Register here</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { useToast } from "vue-toastification";

const email = ref("");
const password = ref("");
const router = useRouter();
const toast = useToast();

const login = async () => {
  try {
    const res = await axios.post("/auth/login", {
      email: email.value,
      password: password.value,
    });

    const token = res.data.access_token;
    localStorage.setItem("token", token);
    toast.success("Login successful!");

    // Decode JWT to get role
    const payload = JSON.parse(atob(token.split(".")[1]));
    const role = payload.sub?.role;

    if (role === "admin") {
      router.push("/admin-dashboard");
    } else {
      router.push("/user-dashboard");
    }
  } catch (err) {
    console.log("Login error:", err);
    toast.error(err.response?.data?.msg || "Login failed");
  }
};
</script>
