import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "mdb-vue-ui-kit/css/mdb.min.css";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

const app = createApp(App); // ✅ create a Vue app instance
app.use(router); // ✅ use the router
app.use(Toast); // ✅ use the toast plugin
app.mount("#app"); // ✅ mount the app
