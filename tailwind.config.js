/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',    // Adjust to your actual HTML template paths
    './static/**/*.css',        // Assuming your CSS files are here
    './static/**/*.js',         // Adjust to your actual JS paths
    '!./node_modules/**/*',
  ],
  theme: {
    extend: {
      keyframes: {
        fadeInRight: {
          '0%': { opacity: '0', transform: 'translateX(20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
      },
      animation: {
        fadeInRight: 'fadeInRight 1.2s ease-out',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),          // Forms plugin
    require('@tailwindcss/typography'),     // Typography plugin
    require('@tailwindcss/aspect-ratio'),   // Aspect Ratio plugin
  ],
};
