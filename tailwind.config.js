/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html',
    '../static/**/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        body: ['var(--font-body)', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        heading: ['var(--font-heading)', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      },
      colors: {
        steel: 'var(--color-steel)',
      },
    },
  },
  plugins: [],
}
