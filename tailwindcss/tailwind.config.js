/** @type {import('tailwindcss').Config} */
module.exports = {
  content: {
    files: [
      "../templates/**/*.html",
      "../static/**/*.js"
    ],
    extract: {
      html: (content) => {
        const result = content.match(/class="([^"]*)"/) || [];
        return result[1] ? result[1].split(" ") : [];
      }
    }
  },
  darkMode: 'class', // allows toggling with 'dark' class on <html>
  theme: {
    extend: {
      colors: {
        // Use CSS variables for dual themes
        bg: 'var(--bg)',
        'bg-soft': 'var(--bg-soft)',
        'bg-muted': 'var(--bg-muted)',

        text: 'var(--text)',
        'text-secondary': 'var(--text-secondary)',
        'text-muted': 'var(--text-muted)',

        primary: 'var(--primary)',
        'primary-glow': 'var(--primary-glow)',

        secondary: 'var(--secondary)',
        'secondary-glow': 'var(--secondary-glow)',

        border: 'var(--border)',
        'border-focus': 'var(--border-focus)',

        success: 'var(--success)',
        warning: 'var(--warning)',
        error: 'var(--error)',
      },

      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
      },

      boxShadow: {
        glow: '0 0 10px var(--primary-glow)',
        'glow-secondary': '0 0 12px var(--secondary-glow)',
        focus: '0 0 0 3px var(--border-focus)',
      },

      borderRadius: {
        xl: '1rem',
        '2xl': '1.5rem',
      },
    },
  },
  plugins: []
}
