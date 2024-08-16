/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/**/*.js',
  ],
  theme: {
    extend: {
      fontFamily: {
        'mulish': ['Mulish', 'sans-serif'],
        'merriweather': ['Merriweather', 'serif'],
      },
    },
  },
  plugins: [],
};


tailwind.config = {
  darkMode: 'class',
  theme: {
    extend: {}
  }
}