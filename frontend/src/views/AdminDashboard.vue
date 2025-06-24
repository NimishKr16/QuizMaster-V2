<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable vue/no-parsing-error -->
<!-- eslint-disable vue/no-use-v-if-with-v-for -->
<!-- eslint-disable no-unused-vars -->
<template>
  <nav
    class="navbar navbar-expand-lg navbar-dark bg-primary px-4 fixed-top shadow"
  >
    <div class="container-fluid">
      <span class="navbar-brand fw-bold">Admin Dashboard</span>
      <div class="d-flex align-items-center ms-auto">
        <a class="nav-link text-white me-3" href="/admin-dashboard">
          <i class="bi bi-journal-text me-1"></i>Quizzes
        </a>
        <a class="nav-link text-white me-3" href="/admin-dashboard/users">
          <i class="bi bi-people-fill me-1"></i>Users
        </a>
        <button
          class="btn btn-danger btn-sm fw-bold"
          @click="logoutModalVisible = true"
        >
          <i class="bi bi-power"></i> Logout
        </button>
      </div>
    </div>
  </nav>
  <div style="height: 50px"></div>
  <div class="container">
    <h3 class="text-center mb-4 text-primary fw-bold">
      Quiz Management Dashboard
    </h3>
    <div class="text-center mb-4">
      <button
        class="btn fw-bold btn-success"
        @click="createQuizModalVisible = true"
      >
        <i class="bi bi-plus-lg me-1"></i> Add
      </button>
    </div>
    <h5 class="fw-bold text-dark mb-3 mt-2">Subjects</h5>
    <div class="accordion" id="subjectAccordion">
      <div
        class="accordion-item w-75 mx-auto mb-1"
        v-for="subject in subjects"
        :key="subject.id"
      >
        <h2 class="accordion-header" :id="`headingSubject${subject.id}`">
          <button
            class="accordion-button"
            :class="{ collapsed: !expandedSubjects.includes(subject.id) }"
            type="button"
            aria-expanded="expandedSubjects.includes(subject.id) ? 'true' : 'false'"
            :aria-controls="`collapseSubject${subject.id}`"
            @click="toggleSubject(subject.id)"
          >
            <span class="fw-bold">{{ subject.name }}</span>
          </button>
        </h2>
        <div
          :id="`collapseSubject${subject.id}`"
          class="accordion-collapse"
          :class="{
            collapse: true,
            show: expandedSubjects.includes(subject.id),
          }"
          :aria-labelledby="`headingSubject${subject.id}`"
          data-bs-parent="#subjectAccordion"
          v-show="expandedSubjects.includes(subject.id)"
        >
          <div class="accordion-body p-0">
            <div
              class="accordion accordion-flush"
              :id="`chapterAccordion${subject.id}`"
            >
              <div
                class="accordion-item"
                v-for="chapter in subject.chapters || []"
                :key="chapter.id"
              >
                <h2
                  class="accordion-header"
                  :id="`headingChapter${chapter.id}`"
                >
                  <button
                    class="accordion-button"
                    :class="{
                      collapsed: !expandedChapters.includes(chapter.id),
                      'bg-light text-dark': true,
                    }"
                    type="button"
                    aria-expanded="expandedChapters.includes(chapter.id) ? 'true' : 'false'"
                    :aria-controls="`collapseChapter${chapter.id}`"
                    @click="toggleChapter(chapter.id)"
                  >
                    {{ chapter.name }}
                  </button>
                </h2>
                <div
                  :id="`collapseChapter${chapter.id}`"
                  class="accordion-collapse"
                  :class="{
                    collapse: true,
                    show: expandedChapters.includes(chapter.id),
                  }"
                  :aria-labelledby="`headingChapter${chapter.id}`"
                  :data-bs-parent="`#chapterAccordion${subject.id}`"
                  v-show="expandedChapters.includes(chapter.id)"
                >
                  <div class="accordion-body p-3">
                    <div
                      v-for="quiz in chapter.quizzes || []"
                      :key="quiz.id"
                      class="mb-3 border rounded p-3 bg-white shadow-sm"
                    >
                      <div
                        class="d-flex justify-content-between align-items-center"
                      >
                        <div>
                          <strong class="text-primary">{{
                            quiz.remarks
                          }}</strong>
                          <span class="text-muted ms-2"
                            >({{ quiz.time_duration }})</span
                          >
                        </div>
                        <div>
                          <button
                            @click="openQuestionsModal(quiz)"
                            class="btn btn-sm btn-outline-info me-2"
                          >
                            Show Questions
                          </button>
                          <button
                            @click="confirmDeleteQuiz(quiz)"
                            class="btn btn-sm btn-danger"
                            title="Delete Quiz"
                          >
                            <i class="bi bi-trash-fill"></i>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="deleteModalVisible"
      class="modal d-block"
      tabindex="-1"
      style="
        background: rgba(0, 0, 0, 0.4);
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1055;
      "
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content text-center p-3">
          <div class="modal-body">
            <p class="mb-3">Do you want to delete this quiz?</p>
            <div class="d-flex justify-content-center gap-3">
              <button class="btn btn-danger" @click="deleteQuiz">Yes</button>
              <button class="btn btn-secondary" @click="closeModal">No</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="showQuestionsModalVisible"
      class="modal d-block"
      tabindex="-1"
      style="
        background: rgba(0, 0, 0, 0.4);
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1055;
      "
    >
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content p-3">
          <div class="modal-header">
            <h5 class="modal-title">Quiz Questions</h5>
            <button class="btn-close" @click="closeQuestionsModal"></button>
          </div>
          <div class="modal-body">
            <div
              v-for="(q, index) in selectedQuizQuestions"
              :key="q.id"
              class="mb-3"
            >
              <strong>Q{{ index + 1 }}: {{ q.question_statement }}</strong>
              <ul class="list-group mt-2">
                <li
                  class="list-group-item"
                  :class="{
                    'bg-success text-white': q.correct_option === 'option1',
                  }"
                >
                  {{ q.option1 }}
                </li>
                <li
                  class="list-group-item"
                  :class="{
                    'bg-success text-white': q.correct_option === 'option2',
                  }"
                >
                  {{ q.option2 }}
                </li>
                <li
                  class="list-group-item"
                  :class="{
                    'bg-success text-white': q.correct_option === 'option3',
                  }"
                >
                  {{ q.option3 }}
                </li>
                <li
                  class="list-group-item"
                  :class="{
                    'bg-success text-white': q.correct_option === 'option4',
                  }"
                >
                  {{ q.option4 }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="logoutModalVisible"
      class="modal d-block"
      tabindex="-1"
      style="
        background: rgba(0, 0, 0, 0.4);
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1055;
      "
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content text-center p-3">
          <div class="modal-body">
            <p class="mb-3">Do you want to logout?</p>
            <div class="d-flex justify-content-center gap-3">
              <button class="btn btn-danger" @click="logout">Yes</button>
              <button
                class="btn btn-secondary"
                @click="logoutModalVisible = false"
              >
                No
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useToast } from "vue-toastification";

const subjects = ref([]);
const expandedSubjects = ref([]);
const expandedChapters = ref([]);
// const expandedQuizzes = ref([]);

const token = localStorage.getItem("token");

const toast = useToast();
const deleteModalVisible = ref(false);
const quizToDelete = ref(null);

const showQuestionsModalVisible = ref(false);
const selectedQuizQuestions = ref([]);
const logoutModalVisible = ref(false);
const toggleSubject = async (id) => {
  if (!expandedSubjects.value.includes(id)) {
    const { data } = await axios.get(`/admin/chapters/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const subject = subjects.value.find((s) => s.id === id);
    subject.chapters = data;
    expandedSubjects.value.push(id);
  } else {
    expandedSubjects.value = expandedSubjects.value.filter((x) => x !== id);
  }
};

const toggleChapter = async (id) => {
  if (!expandedChapters.value.includes(id)) {
    const { data } = await axios.get(`/admin/quizzes/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const chapter = subjects.value
      .flatMap((s) => s.chapters || [])
      .find((c) => c.id === id);
    if (chapter) {
      chapter.quizzes = data;
      expandedChapters.value.push(id);
    }
  } else {
    expandedChapters.value = expandedChapters.value.filter((x) => x !== id);
  }
};

// const _toggleQuiz = async (id) => {
//   if (!expandedQuizzes.value.includes(id)) {
//     const { data } = await axios.get(`/admin/questions/${id}`, {
//       headers: { Authorization: `Bearer ${token}` },
//     });
//     const quiz = subjects.value
//       .flatMap((s) => s.chapters || [])
//       .flatMap((c) => c.quizzes || [])
//       .find((q) => q.id === id);
//     if (quiz) {
//       quiz.questions = data;
//       expandedQuizzes.value.push(id);
//     }
//   } else {
//     expandedQuizzes.value = expandedQuizzes.value.filter((x) => x !== id);
//   }
// };

const confirmDeleteQuiz = (quiz) => {
  quizToDelete.value = quiz;
  deleteModalVisible.value = true;
};

const closeModal = () => {
  deleteModalVisible.value = false;
  quizToDelete.value = null;
};

const deleteQuiz = async () => {
  if (!quizToDelete.value) return;

  try {
    await axios.delete(`/admin/quiz/${quizToDelete.value.id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    // Remove quiz from local state
    const chapter = subjects.value
      .flatMap((s) => s.chapters || [])
      .find((c) => c.quizzes?.some((q) => q.id === quizToDelete.value.id));

    if (chapter) {
      chapter.quizzes = chapter.quizzes.filter(
        (q) => q.id !== quizToDelete.value.id
      );
    }

    toast.success("Quiz deleted successfully");
  } catch (err) {
    toast.error("Failed to delete quiz");
  } finally {
    closeModal();
  }
};

const openQuestionsModal = async (quiz) => {
  try {
    const { data } = await axios.get(`/admin/questions/${quiz.id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    selectedQuizQuestions.value = data;
    showQuestionsModalVisible.value = true;
  } catch (error) {
    toast.error("Failed to load questions.");
  }
};

const closeQuestionsModal = () => {
  selectedQuizQuestions.value = [];
  showQuestionsModalVisible.value = false;
};

const logout = () => {
  localStorage.removeItem("token");
  window.location.href = "/";
};

onMounted(async () => {
  const { data } = await axios.get("/admin/subjects", {
    headers: { Authorization: `Bearer ${token}` },
  });
  subjects.value = data;
});
</script>

<style scoped></style>
