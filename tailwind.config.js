module.exports = {
  content: ["./src/**/*.{html,js,jsx,ts,tsx,vue}"],
  mode: "jit",
  purge: ["./public/**/*.html", "./src/**/*.{js,jsx,ts,tsx,vue}"],
  theme: {
    fontFamily:{
      'font1': ['Inter Tight', 'Helvetica', 'Arial', 'sans-serif'],
    },
    extend: {

      screens:{
        'xsm' : '300px'
      },

      height:{
        'gap1':'92px',
      },
      
      fontWeight:{
        '200': 200,
      },

      colors : {
        bg: '#fafafa',
        text1: '#222',
        bg1: 'rgba(0, 0, 0, .03)',
        bgHover: 'rgba(0, 0, 0, .06)',
        text3: 'rgba(34, 34, 34, .45)',
        green: '#58a65d',
        text2: 'rgba(34, 34, 34, .7)',
        border: 'rgba(0, 0, 0, .05)',
        blue: '#4c95f7',
        blueHover: '#3f7bcc' 
      }
    },
  },
  plugins: [],
};

