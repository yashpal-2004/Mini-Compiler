/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        custom: {
          bg:     '#EBEBEB',   // main app background
          panel:  '#F5F5F5',   // panel / card surfaces
          border: '#CCCCCC',   // borders and dividers
          text:   '#111111',   // primary text
          sub:    '#555555',   // secondary text
          muted:  '#999999',   // placeholder / muted labels
          cta:    '#111111',   // CTA button background
        }
      }
    },
  },
  plugins: [],
}
