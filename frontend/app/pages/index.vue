<template>
    <div class="app-container">
        <AppHeader />

        <main class="main-content">
            <WelcomeCard />
            <NavigationCard />
        </main>
    </div>
</template>

<script setup lang="ts">
// Index page - Home
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
</style>
