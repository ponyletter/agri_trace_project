// pages/index/index.js
const { queryTrace } = require('../../utils/api')

Page({
  data: {
    inputCode: '',
    examples: [
      { name: '优质冰糖心苹果', code: 'BATCH-APPLE-20251025-001' },
    ],
  },

  onInputChange(e) {
    this.setData({ inputCode: e.detail.value })
  },

  // 扫描二维码
  scanQRCode() {
    wx.scanCode({
      onlyFromCamera: false,
      success: (res) => {
        const code = res.result
        this.doQuery(code)
      },
      fail() {
        wx.showToast({ title: '扫码失败', icon: 'none' })
      },
    })
  },

  // 手动查询
  queryTrace() {
    const code = this.data.inputCode.trim()
    if (!code) {
      wx.showToast({ title: '请输入溯源码', icon: 'none' })
      return
    }
    this.doQuery(code)
  },

  // 使用示例
  useExample(e) {
    const code = e.currentTarget.dataset.code
    this.setData({ inputCode: code })
    this.doQuery(code)
  },

  // 执行查询并跳转结果页
  async doQuery(code) {
    wx.showLoading({ title: '查询中...' })
    try {
      const data = await queryTrace(code)
      wx.hideLoading()
      // 将数据存入全局，结果页读取
      getApp().globalData.traceResult = data
      wx.navigateTo({ url: `/pages/result/result?code=${code}` })
    } catch {
      wx.hideLoading()
    }
  },
})
