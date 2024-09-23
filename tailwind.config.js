module.exports = {
  content: [
    './templates/**/*.html',   
    './staticfiles/**/*.css',  
    './static/**/*.js',        
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
  plugins: [],
}

