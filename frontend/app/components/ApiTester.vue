<template>
    <div class="api-test">
        <button @click="testBackend" class="btn" :disabled="loading">
            {{ loading ? 'Testing...' : 'Test Backend Connection' }}
        </button>
        <p v-if="apiStatus" :class="apiStatus.success ? 'success' : 'error'">
            {{ apiStatus.message }}
        </p>
    </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()
const apiStatus = ref<{ success: boolean; message: string } | null>(null)
const loading = ref(false)

const testBackend = async () => {
    loading.value = true
    apiStatus.value = null

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
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
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

.btn:hover:not(:disabled) {
    background: #5568d3;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
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
