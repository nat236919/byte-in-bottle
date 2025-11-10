<script setup lang="ts">
useHead({
  title: 'Byte in Bottle',
  meta: [
    { name: 'description', content: 'A modern chat application built with Nuxt 4 and FastAPI' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    { charset: 'utf-8' },
    { name: 'keywords', content: 'chat, AI, Nuxt, FastAPI, Vue' },
    { name: 'author', content: 'Byte in Bottle' },
    { property: 'og:title', content: 'Byte in Bottle' },
    { property: 'og:description', content: 'A modern chat application built with Nuxt 4 and FastAPI' },
    { property: 'og:type', content: 'website' },
    { name: 'twitter:card', content: 'summary_large_image' },
    { name: 'twitter:title', content: 'Byte in Bottle' },
    { name: 'twitter:description', content: 'A modern chat application built with Nuxt 4 and FastAPI' },
  ],
  htmlAttrs: {
    lang: 'en'
  }
})
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Scrollbar styling */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>