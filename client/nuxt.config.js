module.exports = {

  //Headers of the page
  head: {
    title: 'kemsu-documents',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'Diploma project for internal document flow in the university' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ],
  },

  // Customize the progress bar color
  loading: { color: '#4A5CFF' },

  // Build configuration
  build: {
    // Run ESLint on save
    extend (config, { isDev, isClient }) {
      if (isDev && isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        })
      }
    }
  },

  // Modules configuration
  modules: [
    '@nuxtjs/style-resources',
  ],

  // Style resources configuration
  styleResources: {
    less: ['./styles/index.less'],
  },

  // CSS configuration
  css: [
    {src: '~/styles/index.less', lang: 'less'}
  ],

  // Plugins configuration
  plugins: [
    '~/plugins/Vuelidate',
  ],

  // Router configuration
  router: {

  },

  // Server configuration
  server: {
    port: 3000,
    host: '0.0.0.0',
  },

  // Target configuration
  target: 'static',
}

