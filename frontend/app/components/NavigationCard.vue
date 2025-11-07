<template>
    <div class="nav-card">
        <h3>🚀 Explore</h3>
        <div class="nav-buttons">
            <NuxtLink to="/ask" class="nav-btn">
                ❓ Ask AI
            </NuxtLink>
            <NuxtLink to="/chat" class="nav-btn">
                💬 Go to Chat
            </NuxtLink>
        </div>
    </div>
</template>

<style scoped>
.nav-card {
    margin-top: 2rem;
    padding: 1.5rem;
    background: white;
    border-radius: 1rem;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    text-align: center;
}

.nav-card h3 {
    color: #333;
    margin-bottom: 1rem;
}

.nav-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

.nav-btn {
    display: inline-block;
    padding: 1rem 2rem;
    background: #667eea;
    color: white;
    text-decoration: none;
    border-radius: 0.5rem;
    font-size: 1rem;
    transition: background 0.3s, transform 0.2s;
}

.nav-btn:hover {
    background: #5568d3;
    transform: translateY(-2px);
}
</style>
