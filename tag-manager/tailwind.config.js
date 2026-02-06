/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        // Category colors
        category: {
          concept: '#8b5cf6',    // purple
          library: '#3b82f6',    // blue
          language: '#ec4899',   // pink
          domain: '#14b8a6',     // teal
          constraint: '#f97316', // orange
          task: '#84cc16',       // lime
          agentic: '#06b6d4',    // cyan
          context: '#a855f7',    // violet
        },
        // Difficulty colors
        difficulty: {
          basic: '#10b981',       // green
          intermediate: '#f59e0b', // amber
          advanced: '#ef4444',    // red
        },
      },
    },
  },
  plugins: [],
};
