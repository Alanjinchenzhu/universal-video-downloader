/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1777FF',
          hover: '#4096FF',
          50: '#E6F4FF',
          100: '#BAE0FF',
          500: '#1777FF',
          600: '#0958D9',
        },
        surface: '#FFFFFF',
        background: '#F5F5F5',
      },
      boxShadow: {
        'card': '0 4px 20px -4px rgba(0, 0, 0, 0.05)',
        'card-hover': '0 8px 30px -4px rgba(0, 0, 0, 0.1)',
      },
      borderRadius: {
        'card': '12px',
        'button': '9999px',
      },
    },
  },
  plugins: [],
}
