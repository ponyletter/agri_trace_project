// pages/result/result.js
Page({
  data: {
    traceData: null,
    code: '',
  },

  onLoad(options) {
    const code = options.code || ''
    this.setData({ code })
    const traceResult = getApp().globalData.traceResult
    if (traceResult) {
      this.processData(traceResult)
    }
  },

  // 处理数据，转换为小程序可渲染的格式
  processData(data) {
    if (!data) return
    // 处理时间轴节点
    const timeline = (data.timeline || []).map(node => {
      // 将 env_data 对象转为数组（小程序 wx:for 需要数组）
      const envDataList = []
      if (node.env_data) {
        Object.keys(node.env_data).forEach(key => {
          envDataList.push({ key, val: node.env_data[key] })
        })
      }
      return {
        ...node,
        env_data_list: envDataList,
        tx_hash_short: node.tx_hash ? node.tx_hash.slice(0, 22) + '...' : '',
      }
    })
    this.setData({
      traceData: { ...data, timeline },
    })
  },

  // 分享溯源结果
  onShareAppMessage() {
    return {
      title: `${this.data.traceData?.product_name || '农产品'} 溯源查询结果`,
      path: `/pages/result/result?code=${this.data.code}`,
    }
  },
})
