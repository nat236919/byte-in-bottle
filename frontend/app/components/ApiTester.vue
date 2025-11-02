<template>
    <div class="api-test">
        <button @click="testBackend" class="btn" :disabled="loading">
            {{ loading ? 'Testing...' : 'Test Backend Connection' }}
        </button>

        <div v-if="apiStatus" :class="['status-card', apiStatus.success ? 'success' : 'error']">
            <h3>{{ apiStatus.success ? '✅ Connection Successful' : '❌ Connection Failed' }}</h3>

            <div v-if="apiStatus.success && healthData">
                <div class="overview-grid">
                    <div class="status-item">
                        <span class="label">Status</span>
                        <span :class="['badge', `badge-${healthData.status?.toLowerCase()}`]">
                            {{ healthData.status }}
                        </span>
                    </div>
                    <div class="status-item">
                        <span class="label">Ollama</span>
                        <span :class="['badge', `badge-${healthData.ollama?.toLowerCase()}`]">
                            {{ healthData.ollama }}
                        </span>
                    </div>
                    <div class="status-item">
                        <span class="label">Redis</span>
                        <span :class="['badge', `badge-${healthData.redis?.toLowerCase()}`]">
                            {{ healthData.redis }}
                        </span>
                    </div>
                </div>

                <div v-if="healthData.available_models?.length" class="models-section">
                    <h4>
                        <span>🤖 Available Models</span>
                        <span class="model-count">{{ healthData.available_models.length }}</span>
                    </h4>

                    <div v-for="model in healthData.available_models" :key="model.digest" class="model-card">
                        <div class="model-header">
                            <div>
                                <span class="model-icon">🦙</span>
                                <span class="model-name">{{ model.model }}</span>
                            </div>
                            <span class="model-size">{{ formatSize(model.size) }}</span>
                        </div>

                        <div class="model-details">
                            <div class="detail-row">
                                <span>Family</span>
                                <span>{{ model.details.family }}</span>
                            </div>
                            <div class="detail-row">
                                <span>Parameters</span>
                                <span>{{ model.details.parameter_size }}</span>
                            </div>
                            <div class="detail-row">
                                <span>Quantization</span>
                                <span>{{ model.details.quantization_level }}</span>
                            </div>
                            <div class="detail-row">
                                <span>Format</span>
                                <span>{{ model.details.format.toUpperCase() }}</span>
                            </div>
                            <div class="detail-row">
                                <span>Modified</span>
                                <span>{{ formatDate(model.modified_at) }}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-else-if="healthData.available_models?.length === 0" class="warning">
                    ⚠️ No models available. Ollama may be disconnected or no models are installed.
                </div>
            </div>

            <p v-else class="error">{{ apiStatus.message }}</p>
        </div>
    </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()
const apiStatus = ref<{ success: boolean; message: string } | null>(null)
const healthData = ref<any>(null)
const loading = ref(false)

const testBackend = async () => {
    loading.value = true
    apiStatus.value = null
    healthData.value = null

    try {
        healthData.value = await $fetch(`${config.public.apiBase}/v1/health`)
        apiStatus.value = { success: true, message: 'Backend is healthy!' }
    } catch (error) {
        apiStatus.value = { success: false, message: `Backend connection failed: ${error}` }
    } finally {
        loading.value = false
    }
}

const formatSize = (bytes: number): string => {
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    if (!bytes) return '0 Bytes'
    const i = Math.floor(Math.log(bytes) / Math.log(1024))
    return `${Math.round((bytes / Math.pow(1024, i)) * 100) / 100} ${sizes[i]}`
}

const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}
</script>

<style scoped>
.api-test {
    margin: 2rem auto;
    text-align: center;
    max-width: 900px;
}

.btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 1rem 2.5rem;
    border-radius: 0.75rem;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.status-card {
    margin-top: 2rem;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    text-align: left;
    animation: slideIn 0.4s;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
}

.status-card.success {
    background: linear-gradient(135deg, #f0fff4 0%, #e6fffa 100%);
    border: 2px solid #48bb78;
}

.status-card.error {
    background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
    border: 2px solid #e53e3e;
}

.status-card h3 {
    margin: 0;
    font-size: 1.5rem;
    color: #2d3748;
}

.overview-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
}

.status-item {
    background: white;
    padding: 1rem;
    border-radius: 0.75rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.label {
    font-size: 0.875rem;
    color: #718096;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.badge {
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    font-weight: 600;
    font-size: 0.875rem;
    text-align: center;
    text-transform: capitalize;
}

.badge-healthy,
.badge-connected {
    background: #c6f6d5;
    color: #22543d;
}

.badge-degraded,
.badge-unhealthy,
.badge-disconnected {
    background: #fed7d7;
    color: #742a2a;
}

.models-section {
    background: white;
    padding: 1.5rem;
    border-radius: 0.75rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.models-section h4 {
    margin: 0 0 1rem;
    font-size: 1.25rem;
    color: #2d3748;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.model-count {
    background: #667eea;
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.875rem;
}

.model-card {
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 0.75rem;
    padding: 1.25rem;
    margin-top: 1rem;
}

.model-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border-color: #667eea;
}

.model-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #e2e8f0;
}

.model-header>div {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.model-icon {
    font-size: 1.5rem;
}

.model-name {
    font-size: 1.125rem;
    font-weight: 700;
    color: #2d3748;
}

.model-size {
    background: #667eea;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    font-weight: 600;
    font-size: 0.875rem;
}

.model-details {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 0.75rem;
}

.detail-row {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem;
    background: white;
    border-radius: 0.5rem;
    font-size: 0.875rem;
}

.detail-row span:first-child {
    color: #718096;
    font-weight: 500;
}

.detail-row span:last-child {
    color: #2d3748;
    font-weight: 600;
}

.error {
    color: #e53e3e;
    margin: 0;
}

.warning {
    background: #fefcbf;
    border: 2px solid #d69e2e;
    border-radius: 0.75rem;
    padding: 1.25rem;
    color: #744210;
    font-weight: 500;
}

@media (max-width: 768px) {
    .api-test {
        padding: 0 1rem;
    }

    .overview-grid,
    .model-details {
        grid-template-columns: 1fr;
    }

    .model-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.75rem;
    }
}
</style>
