<template>
  <div class="app-container">
    <header class="header">
      <h1>🍾 Byte in Bottle</h1>
      <p>Nuxt 3 + FastAPI + Ollama</p>
    </header>

    <main class="main-content">
      <div class="card">
        <h2>Welcome to Your Full Stack App!</h2>
        <p>This is a Nuxt 3 frontend connected to your FastAPI backend.</p>

        <div class="info">
          <h3>Stack:</h3>
          <ul>
            <li>✅ Frontend: Nuxt 3 (Vue.js)</li>
            <li>✅ Backend: FastAPI (Python)</li>
            <li>✅ LLM: Ollama (llama3.2)</li>
            <li>✅ Docker Compose</li>
          </ul>
        </div>

        <div class="api-test">
          <button @click="testBackend" class="btn">Test Backend Connection</button>
          <p v-if="apiStatus" :class="apiStatus.success ? 'success' : 'error'">
            {{ apiStatus.message }}
          </p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()
const apiStatus = ref<{ success: boolean; message: string } | null>(null)

const testBackend = async () => {
  try {
    const response = await $fetch(`${config.public.apiBase}/v1/health`)
    apiStatus.value = {
      success: true,
      message: `✅ Backend is healthy! Response: ${JSON.stringify(response)}`
    }
  } catch (error) {
    apiStatus.value = {
      success: false,
      message: `❌ Backend connection failed: ${error}`
    }
  }
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.header {
  text-align: center;
  color: white;
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.main-content {
  max-width: 800px;
  margin: 0 auto;
}

.card {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.card h2 {
  color: #333;
  margin-bottom: 1rem;
}

.info {
  margin: 2rem 0;
  padding: 1rem;
  background: #f7fafc;
  border-radius: 0.5rem;
}

.info h3 {
  color: #667eea;
  margin-bottom: 0.5rem;
}

.info ul {
  list-style: none;
  padding: 0;
}

.info li {
  padding: 0.5rem 0;
  color: #4a5568;
}

.api-test {
  margin-top: 2rem;
  text-align: center;
}

.btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 0.5rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.btn:hover {
  background: #5568d3;
}

.success {
  color: #38a169;
  margin-top: 1rem;
  padding: 1rem;
  background: #f0fff4;
  border-radius: 0.5rem;
}

.error {
  color: #e53e3e;
  margin-top: 1rem;
  padding: 1rem;
  background: #fff5f5;
  border-radius: 0.5rem;
}
</style>
