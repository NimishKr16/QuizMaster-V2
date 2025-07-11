import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import AdminDashboard from "../views/AdminDashboard.vue";
import RegisterView from "../views/RegisterView.vue";
import UserDashboard from "../views/UserDashboard.vue";
import AddSubject from "@/views/AddSubject.vue";
import AllUsers from "@/views/AllUsers.vue";
const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: LoginView },
  { path: "/register", component: RegisterView },
  { path: "/admin-dashboard", component: AdminDashboard },
  { path: "/user-dashboard", component: UserDashboard },
  { path: "/admin-dashboard/addSubject", component: AddSubject },
  { path: "/admin-dashboard/users", component: AllUsers },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
