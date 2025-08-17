<template>
  <div class="container">
    <h1 class="title">Notas + Feedback IA</h1>

    <div class="controls">
      <button @click="addStudent" class="btn-add">+ Agregar</button>
      <select v-model="filter" class="select-filter">
        <option>Todos</option>
        <option>Aprobado</option>
        <option>Suspenso</option>
      </select>
    </div>

    <table class="students-table">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Email</th>
          <th>N1</th>
          <th>N2</th>
          <th>N3</th>
          <th>Promedio</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="s in filtered" :key="s.id">
          <td>{{ s.name }}</td>
          <td>{{ s.email }}</td>
          <td v-for="k in ['n1','n2','n3']" :key="k">
            <input type="number" min="0" max="20" step="0.5" v-model.number="s[k]" @input="updateScore(s)" class="input-score"/>
          </td>
          <td>{{ s.average }}</td>
          <td>
            <span :class="s.status === 'Aprobado' ? 'status-approved' : 'status-failed'">
              {{ s.status === 'Aprobado' ? '✔ ' : '✘ '}}{{ s.status }}
            </span>
          </td>
          <td>
            <button @click="getFeedback(s)" :disabled="loadingId === s.id" class="btn-feedback">
              <span v-if="loadingId === s.id" class="spinner">⏳</span>
              <span v-else>✨</span>
            </button>
            <button @click="showModal(s.last_feedback_text || 'Sin feedback')" class="btn-view">📄</button>
          </td>
        </tr>
        <tr v-if="filtered.length === 0">
          <td colspan="8" class="no-students">No hay estudiantes para mostrar.</td>
        </tr>
      </tbody>
    </table>
    <div v-if="modal.open" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>Recomendaciones IA</h3>
          <button @click="modal.open = false" class="modal-close">❌</button>
        </div>
        <div class="modal-content">
          <p v-for="line in modal.content.split('\n')" :key="line">{{ line }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'

function computeAverage(n1, n2, n3) { return Math.round(((n1||0)+(n2||0)+(n3||0))/3 * 10) / 10 }
function computeStatus(avg) { return avg >= 11 ? 'Aprobado' : 'Suspenso' }

const students = reactive([
  { id: '1', name: 'Ana Pérez', email: 'ana@demo.com', n1: 9, n2: 12, n3: 14 },
  { id: '2', name: 'Luis Rojas', email: 'luis@demo.com', n1: 7, n2: 8, n3: 10 },
  { id: '3', name: 'María Díaz', email: 'maria@demo.com', n1: 15, n2: 14, n3: 16 }
].map(s => ({ ...s, average: computeAverage(s.n1,s.n2,s.n3), status: computeStatus(computeAverage(s.n1,s.n2,s.n3)) })))

const filter = ref('Todos')
const loadingId = ref(null)
const modal = reactive({ open: false, content: null })
const filtered = computed(() => students.filter(s => filter.value === 'Todos' || s.status === filter.value))

function updateScore(s) {
  s.average = computeAverage(s.n1, s.n2, s.n3)
  s.status = computeStatus(s.average)
}

function addStudent() {
  const id = Date.now().toString()
  students.unshift({ id, name: 'Nuevo', email: `nuevo${id}@demo.com`, n1: 0, n2: 0, n3: 0, average: 0, status: 'Suspenso' })
}

async function getFeedback(s) {
  loadingId.value = s.id
  try {
    const res = await fetch("http://127.0.0.1:8000/api/feedback/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: s.name, email: s.email, n1: s.n1, n2: s.n2, n3: s.n3, average: s.average, status: s.status }),
    })
    const data = await res.json()
    s.last_feedback_text = data.feedback || "Sin feedback"
    showModal(s.last_feedback_text)
  } catch (err) {
    s.last_feedback_text = "Error al obtener feedback: " + err.message
    showModal(s.last_feedback_text)
  } finally {
    loadingId.value = null
  }
}

function showModal(content) {
  modal.content = content
  modal.open = true
}
</script>

<style scoped>
.container { padding: 1.5rem; font-family: sans-serif; }
.title { font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem; }
.controls { display: flex; gap: 0.5rem; margin-bottom: 1rem; align-items: center; }
.btn-add { background: black; color: white; padding: 0.5rem 1rem; border-radius: 0.25rem; cursor: pointer; }
.select-filter { border: 1px solid #ccc; padding: 0.5rem; border-radius: 0.25rem; }
.students-table { width: 100%; border-collapse: collapse; }
.students-table th, .students-table td { border: 1px solid #ccc; padding: 0.5rem; text-align: center; }
.students-table th { background-color: #f3f3f3; }
.input-score { width: 4rem; padding: 0.25rem; border: 1px solid #ccc; border-radius: 0.25rem; }
.status-approved { color: green; font-weight: bold; }
.status-failed { color: red; font-weight: bold; }
.btn-feedback, .btn-view { border: 1px solid #ccc; padding: 0.25rem 0.5rem; border-radius: 0.25rem; cursor: pointer; margin-left: 0.25rem; }
.spinner { display: inline-block; animation: spin 1s linear infinite; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.no-students { text-align: center; padding: 1rem; color: #666; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 50; }
.modal { background: white; border-radius: 1rem; box-shadow: 0 0 10px rgba(0,0,0,0.3); max-width: 50rem; width: 90%; padding: 1.5rem; position: relative; max-height: 24rem; overflow-y: auto; }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid #ccc; padding-bottom: 0.5rem; }
.modal-close { background: none; border: none; cursor: pointer; font-size: 1.25rem; color: #555; }
.modal-content p { margin-bottom: 0.5rem; color: #333; }
</style>