<template>
    <div class="card">
        <h2>💬 Chat with AI</h2>
        <p>Ask questions and get responses from Ollama LLM</p>

        <div class="mode-selector">
            <label for="mode-select">Response Mode:</label>
            <select id="mode-select" v-model="selectedMode" :disabled="loading">
                <option value="concise">💼 Concise - Brief and to the point</option>
                <option value="professional">👔 Professional - Formal and structured</option>
                <option value="sarcastic">😏 Sarcastic - Witty and humorous</option>
                <option value="creative">🎨 Creative - Imaginative and expressive</option>
                <option value="friendly">😊 Friendly - Casual and warm</option>
            </select>
        </div>

        <div class="chat-container">
            <div class="messages" ref="messagesContainer" v-show="messages.length > 0">
                <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
                    <div class="message-content">
                        <strong>{{ message.role === 'user' ? '👤 You' : '🤖 AI' }}:</strong>
                        <p>{{ message.content }}</p>
                    </div>
                </div>
                <div v-if="loading" class="message assistant">
                    <div class="message-content">
                        <strong>🤖 AI:</strong>
                        <p class="typing">Thinking...</p>
                    </div>
                </div>
            </div>

            <div class="input-container">
                <textarea v-model="userInput" @keydown.enter.prevent="handleSend"
                    placeholder="Type your message here..." rows="3" :disabled="loading"></textarea>
                <div class="button-group">
                    <button @click="handleClear" class="btn btn-secondary" :disabled="loading || messages.length === 0">
                        Clear
                    </button>
                    <button @click="handleSend" class="btn" :disabled="isSendDisabled">
                        {{ loading ? 'Sending...' : 'Send' }}
                    </button>
                </div>
            </div>

            <p v-if="error" class="error">{{ error }}</p>
        </div>
    </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()
const userInput = ref('')
const messages = ref<Array<{ role: 'user' | 'assistant'; content: string }>>([])
const loading = ref(false)
const error = ref('')
const messagesContainer = ref<HTMLElement | null>(null)
const selectedMode = ref<'concise' | 'professional' | 'sarcastic' | 'creative' | 'friendly'>('concise')

const isSendDisabled = computed(() => loading.value || !userInput.value.trim())

const scrollToBottom = () => {
    nextTick(() => {
        if (messagesContainer.value) {
            messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
    })
}

const handleClear = () => {
    messages.value = []
    error.value = ''
    userInput.value = ''
}

const handleSend = async () => {
    if (!userInput.value.trim() || loading.value) return

    const question = userInput.value.trim()
    userInput.value = ''
    error.value = ''

    // Add user message
    messages.value.push({ role: 'user', content: question })
    scrollToBottom()

    loading.value = true

    try {
        const response = await $fetch<{ response: string }>(`${config.public.apiBase}/v1/chats/ask`, {
            method: 'POST',
            body: {
                model: 'llama3.2',
                prompt: question,
                mode: selectedMode.value
            }
        })

        // Add AI response
        messages.value.push({ role: 'assistant', content: response.response })
        scrollToBottom()
    } catch (err: any) {
        error.value = `Failed to get response: ${err.message || 'Unknown error'}`
        console.error('Chat error:', err)
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
    white-space: nowrap;
}

.mode-selector select {
    flex: 1;
    padding: 0.5rem 1rem;
    border: 2px solid #e2e8f0;
    border-radius: 0.5rem;
    font-size: 1rem;
    font-family: inherit;
    background: white;
    cursor: pointer;
    transition: border-color 0.3s;
}

.mode-selector select:focus {
    outline: none;
    border-color: #667eea;
}

.mode-selector select:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.chat-container {
    margin-top: 1rem;
}

.messages {
    max-height: 400px;
    overflow-y: auto;
    margin-bottom: 1rem;
    padding: 1rem;
    background: #f7fafc;
    border-radius: 0.5rem;
}

.message {
    margin-bottom: 1rem;
    animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.message-content {
    padding: 1rem;
    border-radius: 0.5rem;
}

.message.user .message-content {
    background: #e6f2ff;
    border-left: 4px solid #667eea;
}

.message.assistant .message-content {
    background: #f0f9ff;
    border-left: 4px solid #38a169;
}

.message-content strong {
    display: block;
    margin-bottom: 0.5rem;
    color: #333;
}

.message-content p {
    margin: 0;
    color: #4a5568;
    white-space: pre-wrap;
    word-wrap: break-word;
}

.typing {
    font-style: italic;
    opacity: 0.7;
}

.input-container {
    display: flex;
    gap: 1rem;
    align-items: flex-end;
}

.button-group {
    display: flex;
    gap: 0.5rem;
}

textarea {
    flex: 1;
    padding: 0.75rem;
    border: 2px solid #e2e8f0;
    border-radius: 0.5rem;
    font-size: 1rem;
    font-family: inherit;
    resize: vertical;
    transition: border-color 0.3s;
}

textarea:focus {
    outline: none;
    border-color: #667eea;
}

textarea:disabled {
    background: #f7fafc;
    cursor: not-allowed;
}

.btn {
    background: #667eea;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.3s;
    white-space: nowrap;
}

.btn:hover:not(:disabled) {
    background: #5568d3;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-secondary {
    background: #718096;
}

.btn-secondary:hover:not(:disabled) {
    background: #4a5568;
}

.error {
    color: #e53e3e;
    margin-top: 1rem;
    padding: 1rem;
    background: #fff5f5;
    border-radius: 0.5rem;
}
</style>
