<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->
<template>
  <div class="container py-5">
    <h2 class="text-center fw-bold mb-5">Add a new Subject</h2>

    <div class="card shadow-sm p-4 mx-auto" style="max-width: 800px">
      <form @submit.prevent="submitForm">
        <!-- Subject Name -->
        <div class="mb-4">
          <label class="form-label fw-semibold">Subject Name</label>
          <input
            v-model="subjectName"
            type="text"
            class="form-control"
            placeholder="Enter subject name"
            required
          />
        </div>

        <!-- Chapters Section -->
        <div v-for="(chapter, cIndex) in chapters" :key="cIndex" class="mb-5">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <label class="form-label fw-semibold"
              >Chapter {{ cIndex + 1 }}</label
            >
            <button
              type="button"
              class="btn btn-sm btn-outline-danger"
              @click="removeChapter(cIndex)"
            >
              <i class="bi bi-x-circle"></i> Remove
            </button>
          </div>
          <!-- Chapter Name -->
          <div class="mb-4">
            <label class="form-label fw-semibold">Chapter Name</label>
            <input
              v-model="chapter.chapterName"
              type="text"
              class="form-control"
              placeholder="Enter chapter name"
              required
            />
          </div>

          <!-- Quiz Info -->
          <div class="mb-4">
            <label class="form-label fw-semibold">Quiz Name</label>
            <input
              v-model="chapter.quizName"
              type="text"
              class="form-control"
              placeholder="Enter quiz name"
              required
            />
          </div>

          <div class="mb-4">
            <label class="form-label fw-semibold">Quiz Duration (hh:mm)</label>
            <input
              v-model="chapter.quizDuration"
              type="text"
              class="form-control"
              placeholder="e.g., 00:30"
              required
            />
          </div>

          <!-- Questions -->
          <div class="mb-4">
            <label class="form-label fw-semibold">Questions</label>
            <div
              v-for="(question, qIndex) in chapter.questions"
              :key="qIndex"
              class="mb-3 p-3 border rounded"
            >
              <label class="form-label">Question {{ qIndex + 1 }}</label>
              <input
                v-model="question.statement"
                type="text"
                class="form-control mb-2"
                placeholder="Question text"
                required
              />

              <div class="row">
                <div
                  class="col-6 mb-2"
                  v-for="opt in ['option1', 'option2', 'option3', 'option4']"
                  :key="opt"
                >
                  <input
                    v-model="question[opt]"
                    type="text"
                    class="form-control"
                    :placeholder="opt.toUpperCase()"
                    required
                  />
                </div>
              </div>

              <label class="form-label">Correct Answer</label>
              <select
                v-model="question.correct_option"
                class="form-select"
                required
              >
                <option value="option1">Option 1</option>
                <option value="option2">Option 2</option>
                <option value="option3">Option 3</option>
                <option value="option4">Option 4</option>
              </select>
            </div>

            <button
              type="button"
              class="btn btn-outline-primary w-100"
              @click="addQuestion(cIndex)"
            >
              <i class="bi bi-plus-circle me-2"></i>Add Question
            </button>
          </div>
        </div>

        <!-- Add Chapter Button -->
        <div class="text-center mb-4">
          <button
            type="button"
            class="btn btn-outline-secondary"
            @click="addChapter"
          >
            <i class="bi bi-plus-circle me-2"></i>Add Chapter
          </button>
        </div>

        <!-- Submit -->
        <div class="text-center">
          <button type="submit" class="btn btn-success px-5">Submit</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useToast } from "vue-toastification";
const toast = useToast();

const subjectName = ref("");

const chapters = ref([
  {
    chapterName: "",
    quizName: "",
    quizDuration: "",
    questions: [
      {
        statement: "",
        option1: "",
        option2: "",
        option3: "",
        option4: "",
        correct_option: "option1",
      },
    ],
  },
]);

const addQuestion = (chapterIndex) => {
  chapters.value[chapterIndex].questions.push({
    statement: "",
    option1: "",
    option2: "",
    option3: "",
    option4: "",
    correct_option: "option1",
  });
};

const addChapter = () => {
  chapters.value.push({
    chapterName: "",
    quizName: "",
    quizDuration: "",
    questions: [
      {
        statement: "",
        option1: "",
        option2: "",
        option3: "",
        option4: "",
        correct_option: "option1",
      },
    ],
  });
};

const removeChapter = (index) => {
  chapters.value.splice(index, 1);
};

import { useRouter } from "vue-router";
const router = useRouter();

const validateTime = (time) => {
  return /^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/.test(time);
};

const submitForm = async () => {
  try {
    // Validate quiz duration format
    for (const chapter of chapters.value) {
      if (!validateTime(chapter.quizDuration)) {
        toast.error("Invalid quiz duration format. Use hh:mm (e.g., 00:30).");
        return;
      }
    }

    const token = localStorage.getItem("token");
    // eslint-disable-next-line no-unused-vars
    const response = await axios.post(
      "http://127.0.0.1:5000/admin/add-subject",
      {
        subjectName: subjectName.value,
        chapters: chapters.value,
      },
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );
    toast.success("Subject added successfully!");

    // Clear form
    subjectName.value = "";
    chapters.value = [
      {
        chapterName: "",
        quizName: "",
        quizDuration: "",
        questions: [
          {
            statement: "",
            option1: "",
            option2: "",
            option3: "",
            option4: "",
            correct_option: "option1",
          },
        ],
      },
    ];

    // Redirect to admin dashboard after a short delay
    setTimeout(() => {
      router.push("/admin-dashboard");
    }, 1000);
  } catch (error) {
    toast.error("Failed to add subject. Please check your input.");
    console.error(error);
  }
};
</script>
