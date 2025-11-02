<template>
    <div class="app-container">
        <AppHeader />

        <main class="main-content">
            <ChatInterface />

            <div class="navigation">
                <NuxtLink to="/" class="nav-link">← Back to Home</NuxtLink>
            </div>
        </main>
    </div>
</template>

<script setup lang="ts">
// Chat page
</script>

<style scoped>
.app-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
}

.main-content {
    max-width: 800px;
    margin: 0 auto;
}

.navigation {
    margin-top: 2rem;
    text-align: center;
}

.nav-link {
    color: white;
    text-decoration: none;
    font-size: 1.1rem;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    background: rgba(255, 255, 255, 0.1);
    transition: background 0.3s;
    display: inline-block;
}

.nav-link:hover {
    background: rgba(255, 255, 255, 0.2);
}
</style>
