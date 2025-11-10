<template>
    <div class="card">
        <h2>Welcome to Your Full Stack App!</h2>
        <p>This is a Nuxt 4 frontend connected to your FastAPI backend.</p>

        <StackInfo />
        <ApiTester />
    </div>
</template>

<style scoped>
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
</style>
