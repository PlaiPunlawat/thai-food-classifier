/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./pages/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        black: {
          ...require("daisyui/src/colors/themes")["[data-theme=dark]"],
          primary: "#987737",
          "primary-content": "#ffffff",
          "base-content": "#ffffff",
          accent: "#cd9637",
          neutral: "#e3e3e3",
          "base-100": "#111",
        },
      },
    ],
  },
};
