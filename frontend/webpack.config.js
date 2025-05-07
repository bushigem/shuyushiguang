const { DefinePlugin } = require('webpack');

module.exports = {
  // ... 其他配置 ...
  plugins: [
    new DefinePlugin({
      __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(false),
      // 其他需要的功能标志
    }),
  ],
};