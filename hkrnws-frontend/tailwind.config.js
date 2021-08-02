module.exports = {
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        'hkrnws': {
          DEFAULT: '#ED8936',
          '50': '#FFFFFF',
          '100': '#FEF7F1',
          '200': '#FADBC2',
          '300': '#F5C094',
          '400': '#F1A465',
          '500': '#ED8936',
          '600': '#DC6F14',
          '700': '#AD5710',
          '800': '#7F400B',
          '900': '#502807' },
      },
      fontSize: {
        'xxs': '.50rem'
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
