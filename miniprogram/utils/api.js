// utils/api.js - 封装网络请求
const app = getApp()

/**
 * 封装 wx.request，返回 Promise
 */
function request(method, path, data = {}) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: app.globalData.baseUrl + path,
      method,
      data,
      header: { 'Content-Type': 'application/json' },
      success(res) {
        if (res.data && res.data.code === 200) {
          resolve(res.data.data)
        } else {
          wx.showToast({ title: res.data?.msg || '请求失败', icon: 'none' })
          reject(res.data)
        }
      },
      fail(err) {
        wx.showToast({ title: '网络错误', icon: 'none' })
        reject(err)
      },
    })
  })
}

/**
 * 根据溯源批次号查询完整溯源链
 * @param {string} traceCode - 溯源批次号
 */
function queryTrace(traceCode) {
  return request('GET', `/api/v1/trace/${traceCode}`)
}

module.exports = { request, queryTrace }
