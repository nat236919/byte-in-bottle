<template>
    <div class="api-test">
        <button @click="testBackend" class="btn" :disabled="loading">
            {{ loading ? 'Testing...' : 'Test Backend Connection' }}
        </button>

        <div v-if="apiStatus" :class="['status-card', apiStatus.success ? 'success' : 'error']">
            <h3 class="status-title">
                {{ apiStatus.success ? '✅ Connection Successful' : '❌ Connection Failed' }}
            </h3>

            <div v-if="apiStatus.success && healthData" class="health-details">
                <!-- Status Overview -->
                <div class="overview-grid">
                    <div class="status-item">
                        <span class="label">Status</span>
                        <span :class="['badge', getStatusBadgeClass(healthData.status)]">
                            {{ healthData.status }}
                        </span>
                    </div>

                    <div class="status-item">
                        <span class="label">Ollama</span>
                        <span :class="['badge', getServiceBadgeClass(healthData.ollama)]">
                            {{ healthData.ollama }}
                        </span>
                    </div>

                    <div class="status-item">
                        <span class="label">Redis</span>
                        <span :class="['badge', getServiceBadgeClass(healthData.redis)]">
                            {{ healthData.redis }}
                        </span>
                    </div>
                </div>

                <!-- Available Models -->
                <div v-if="healthData.available_models?.length" class="models-section">
                    <h4 class="section-title">
                        <span>🤖 Available Models</span>
                        <span class="model-count">{{ healthData.available_models.length }}</span>
                    </h4>

                    <div v-for="model in healthData.available_models" :key="model.digest" class="model-card">
                        <div class="model-header">
                            <div class="model-name-wrapper">
                                <span class="model-icon">🦙</span>
                                <span class="model-name">{{ model.model }}</span>
                            </div>
                            <span class="model-size">{{ formatSize(model.size) }}</span>
                        </div>

                        <div class="model-details">
                            <div class="detail-row">
                                <span class="detail-label">Family</span>
                                <span class="detail-value">{{ model.details.family }}</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Parameters</span>
                                <span class="detail-value">{{ model.details.parameter_size }}</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Quantization</span>
                                <span class="detail-value">{{ model.details.quantization_level }}</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Format</span>
                                <span class="detail-value">{{ model.details.format.toUpperCase() }}</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Modified</span>
                                <span class="detail-value">{{ formatDate(model.modified_at) }}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- No Models Warning -->
                <div v-else-if="healthData.available_models && healthData.available_models.length === 0"
                    class="warning-message">
                    <span class="warning-icon">⚠️</span>
                    <span>No models available. Ollama may be disconnected or no models are installed.</span>
                </div>
            </div>

            <p v-else class="error-message">{{ apiStatus.message }}</p>
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
        const response = await $fetch(`${config.public.apiBase}/v1/health`)
        apiStatus.value = {
            success: true,
            message: 'Backend is healthy!'
        }
        healthData.value = response
    } catch (error) {
        apiStatus.value = {
            success: false,
            message: `Backend connection failed: ${error}`
        }
    } finally {
        loading.value = false
    }
}

const formatSize = (bytes: number): string => {
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    if (bytes === 0) return '0 Bytes'
    const i = Math.floor(Math.log(bytes) / Math.log(1024))
    return Math.round((bytes / Math.pow(1024, i)) * 100) / 100 + ' ' + sizes[i]
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

const getStatusBadgeClass = (status: string): string => {
    switch (status?.toLowerCase()) {
        case 'healthy':
            return 'badge-healthy'
        case 'degraded':
            return 'badge-degraded'
        case 'unhealthy':
            return 'badge-unhealthy'
        default:
            return 'badge-unknown'
    }
}

const getServiceBadgeClass = (serviceStatus: string): string => {
    switch (serviceStatus?.toLowerCase()) {
        case 'connected':
            return 'badge-connected'
        case 'disconnected':
            return 'badge-disconnected'
        default:
            return 'badge-unknown'
    }
}
</script>

<style scoped>
.api-test {
    margin-top: 2rem;
    text-align: center;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
}

.btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 1rem 2.5rem;
    border-radius: 0.75rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}

.status-card {
    margin-top: 2rem;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    text-align: left;
    animation: slideIn 0.4s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
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

.status-title {
    margin: 0 0 1.5rem 0;
    font-size: 1.5rem;
    font-weight: 700;
    color: #2d3748;
}

.health-details {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
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

.badge-healthy {
    background: #c6f6d5;
    color: #22543d;
}

.badge-degraded {
    background: #fed7d7;
    color: #742a2a;
}

.badge-unhealthy {
    background: #fed7d7;
    color: #742a2a;
}

.badge-connected {
    background: #bee3f8;
    color: #2c5282;
}

.badge-disconnected {
    background: #fed7d7;
    color: #742a2a;
}

.badge-unknown {
    background: #e2e8f0;
    color: #4a5568;
}

.models-section {
    background: white;
    padding: 1.5rem;
    border-radius: 0.75rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.section-title {
    margin: 0 0 1rem 0;
    font-size: 1.25rem;
    font-weight: 700;
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
    transition: all 0.3s ease;
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

.model-name-wrapper {
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
    align-items: center;
    padding: 0.5rem;
    background: white;
    border-radius: 0.5rem;
}

.detail-label {
    font-size: 0.875rem;
    color: #718096;
    font-weight: 500;
}

.detail-value {
    font-size: 0.875rem;
    color: #2d3748;
    font-weight: 600;
}

.error-message {
    color: #e53e3e;
    margin: 0;
    font-size: 1rem;
}

.warning-message {
    background: #fefcbf;
    border: 2px solid #d69e2e;
    border-radius: 0.75rem;
    padding: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #744210;
    font-weight: 500;
}

.warning-icon {
    font-size: 1.5rem;
}

@media (max-width: 768px) {
    .api-test {
        padding: 0 1rem;
    }

    .overview-grid {
        grid-template-columns: 1fr;
    }

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
