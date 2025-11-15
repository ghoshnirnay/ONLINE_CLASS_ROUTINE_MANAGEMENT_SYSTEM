export default {
  head: {
    title: 'ClassSync | Smart Class Routine Management',
    htmlAttrs: { lang: 'en' },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content: 'ClassSync — A smart and efficient Class Routine Management System for Admins, Faculty, and Students.'
      },
      { name: 'theme-color', content: '#2563eb' } // blue accent color
    ],
    link: [
      { rel: 'icon', type: 'image/png', href: '/favicon.png' } // use favicon.png instead of .ico
    ]
  },

  // Global CSS
  css: [
    '@/assets/css/main.css'
  ],

  // Plugins (your Flask backend API connector)
  plugins: [
    '~/plugins/api.js'
  ],

  // Auto import components
  components: true,

  // Modules
  modules: [
    '@nuxtjs/dotenv'
  ],

  // Public runtime config (Backend Flask API base URL)
  publicRuntimeConfig: {
    API_BASE: process.env.API_BASE || 'http://127.0.0.1:5000/api'
  },

  // Build configuration
  build: {
    transpile: [],
    extractCSS: true,
  }
}
