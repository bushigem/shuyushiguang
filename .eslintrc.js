module.exports = {
  root: true,
  env: {
    node: true,
    'vue/setup-compiler-macros': true // 添加这个环境来识别 defineProps/defineEmits 等
  },
  extends: [
    'plugin:vue/vue3-essential', // 或者 vue3-recommended
    'eslint:recommended',
    // 其他你可能使用的扩展，比如 typescript, prettier
  ],
  parserOptions: {
    parser: '@babel/eslint-parser', // 或者 '@typescript-eslint/parser' 如果使用 TS
    ecmaVersion: 2020, // 或更高
    sourceType: 'module'
  },
  rules: {
    // 你的其他规则
    'vue/no-mutating-props': 'error', // 确保这条规则是开启的
    // ...
  }
}