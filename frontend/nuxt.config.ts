// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({

  // Development tools
  devtools: { enabled: true },

  // Runtime config
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
    }
  },

  // Development server configuration for Docker
  devServer: {
    host: '0.0.0.0',
    port: 3000
  }
})
