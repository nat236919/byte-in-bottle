<template>
    <div class="card">
        <h2>❓ Ask AI</h2>
        <p>Ask questions and get responses from Ollama LLM</p>

        <div class="mode-selector">
            <label for="mode-select">Response Mode:</label>
            <select id="mode-select" v-model="selectedMode" :disabled="loading">
                <option value="concise">💼 Concise</option>
                <option value="professional">👔 Professional</option>
                <option value="sarcastic">😏 Sarcastic</option>
                <option value="creative">🎨 Creative</option>
                <option value="friendly">😊 Friendly</option>
            </select>
        </div>

        <div class="input-container">
            <textarea v-model="userInput" @keydown.enter.prevent="handleSend" placeholder="Type your question here..."
                rows="3" :disabled="loading" />
            <button @click="handleSend" class="btn" :disabled="loading || !userInput.trim()">
                {{ loading ? 'Asking...' : 'Ask' }}
            </button>
        </div>

        <div v-if="response" class="response-container">
            <strong>🤖 Response:</strong>
            <p>{{ response }}</p>
        </div>

        <div v-if="loading" class="response-container loading">
            <strong>🤖 Response:</strong>
            <p class="typing">Thinking...</p>
        </div>

        <p v-if="error" class="error">{{ error }}</p>
    </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()
const userInput = ref('')
const response = ref('')
const loading = ref(false)
const error = ref('')
const selectedMode = ref('concise')

const handleSend = async () => {
    const question = userInput.value.trim()
    if (!question || loading.value) return

    error.value = ''
    response.value = ''
    loading.value = true

    try {
        const { response: apiResponse } = await $fetch<{ response: string }>(`${config.public.apiBase}/v1/chats/ask`, {
            method: 'POST',
            body: { model: 'llama3.2', prompt: question, mode: selectedMode.value }
        })
        response.value = apiResponse
        userInput.value = ''
    } catch (err: any) {
        error.value = `Failed to get response: ${err.message || 'Unknown error'}`
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.card {
    background: white;
    border-radius: 1rem;
    padding: 2rem;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.card h2 {
    color: #333;
    margin-bottom: 0.5rem;
}

.card>p {
    color: #666;
    margin-bottom: 1.5rem;
}

.mode-selector {
    margin-bottom: 1.5rem;
    padding: 1rem;
    background: #f7fafc;
    border-radius: 0.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.mode-selector label {
    font-weight: 600;
    color: #333;
}

.mode-selector select {
    flex: 1;
    padding: 0.5rem 1rem;
    border: 2px solid #e2e8f0;
    border-radius: 0.5rem;
    font: inherit;
    background: white;
    cursor: pointer;
}

.mode-selector select:focus {
    outline: none;
    border-color: #667eea;
}

.input-container {
    display: flex;
    gap: 1rem;
    align-items: flex-end;
    margin-bottom: 1.5rem;
}

.response-container {
    padding: 1.5rem;
    background: #f0f9ff;
    border-left: 4px solid #38a169;
    border-radius: 0.5rem;
    animation: fadeIn 0.3s;
}

.response-container.loading {
    background: #f7fafc;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
}

.response-container strong {
    display: block;
    margin-bottom: 0.5rem;
    color: #333;
}

.response-container p {
    margin: 0;
    color: #4a5568;
    white-space: pre-wrap;
    word-wrap: break-word;
}

.typing {
    font-style: italic;
    opacity: 0.7;
}

textarea {
    flex: 1;
    padding: 0.75rem;
    border: 2px solid #e2e8f0;
    border-radius: 0.5rem;
    font: inherit;
    resize: vertical;
}

textarea:focus {
    outline: none;
    border-color: #667eea;
}

textarea:disabled {
    background: #f7fafc;
    cursor: not-allowed;
}

button {
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font: inherit;
    cursor: pointer;
    white-space: nowrap;
}

button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn {
    background: #667eea;
    color: white;
}

.btn:hover:not(:disabled) {
    background: #5568d3;
}

.error {
    color: #e53e3e;
    margin-top: 1rem;
    padding: 1rem;
    background: #fff5f5;
    border-radius: 0.5rem;
}
</style>
