// nuxt.config.ts
export default defineNuxtConfig({
  // Enable SPA mode for client-side routing
  ssr: false,
  
  // Configure for static generation
  nitro: {
    preset: 'static'
  },
  
  // Disable payload extraction for SPA mode
  experimental: {
    payloadExtraction: false
  },
  // Configure the app for SPA deployment
  app: {
    // Base URL if serving from a subdirectory
    // baseURL: '/app/',
    
    // Configure the router for SPA mode
    head: {
      title: 'My Media Player',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ]
    }
  },
  
  // CSS framework (if using Tailwind)
  css: ['~/assets/css/tailwind.css'],
  
  // Modules
  modules: ['@nuxtjs/tailwindcss', '@nuxt/image'],
  
  // Development server configuration
  devtools: { enabled: true },
  
  // Runtime configuration
  runtimeConfig: {
    // 這些變數只在伺服器端可用
    // privateRuntimeConfig: {}, 
    
    // public 中的變數在客戶端和伺服器端都可用
    public: {
      apiBase: process.env.NODE_ENV === 'production' 
        ? 'https://music.j205025.org'  // Production: Use HTTPS with your Cloudflare tunnel domain
        : process.env.NUXT_PUBLIC_API_BASE || 'http://192.168.2.118:8001'  // Development: Use env var or fallback
    }
  }
  
  // Note: router.mode is deprecated in Nuxt 3
  // SPA routing is handled by ssr: false
})
