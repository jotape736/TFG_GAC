/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {}
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: [
      'light',
      'dark',
      {
        ugr: {
          primary: "#cb2c30",
          "primary-content": "#ffffff",
          secondary: "#cb2c30",
          "secondary-content": "#cecdcd",
          accent: "#231f20",
          "accent-content": "#ffffff",
          neutral: "#231f20",
          "neutral-content": "#cecdcd",
          "base-100": "#ffffff",
          "base-200": "#dedede",
          "base-300": "#bebebe",
          "base-content": "#161616",
          info: "#007FC0",
          "info-content": "#00060e",
          success: "#009430",
          "success-content": "#000801",
          warning: "#ffd000",
          "warning-content": "#161000",
          error: "#cb2c30",
          "error-content": "#160709",
          "--rounded-box": "0.5rem", // border radius rounded-box utility class, used in card and other large boxes
          "--rounded-btn": "0.2rem", // border radius rounded-btn utility class, used in buttons and similar element
          "--rounded-badge": "0.5rem",
        },
      },
      'cupcake',
      'bumblebee',
      'emerald',
      'corporate',
      'synthwave',
      'retro',
      'cyberpunk',
      'valentine',
      'halloween',
      'garden',
      'forest',
      'aqua',
      'lofi',
      'pastel',
      'fantasy',
      'wireframe',
      'black',
      'luxury',
      'dracula',
      'cmyk',
      'autumn',
      'business',
      'acid',
      'lemonade',
      'night',
      'coffee',
      'winter',
      'dim',
      'nord',
      'sunset'
    ]
  }
}
