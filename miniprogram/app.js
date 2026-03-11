// app.js - 农产品溯源微信小程序
App({
  globalData: {
    // 后端API地址（生产环境替换为实际域名）
    baseUrl: 'https://your-domain.com',
    userInfo: null,
  },

  onLaunch() {
    console.log('[AgriTrace] 小程序启动')
  },
})
