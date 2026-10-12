// API 请求封装 —— 后端 FastAPI
// 后端地址：开发时指向本地，生产可替换
const BASE_URL = 'http://127.0.0.1:8000/api/v1'

export function request(url, options = {}) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + url,
      method: options.method || 'GET',
      data: options.data || {},
      header: { 'Content-Type': 'application/json' },
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else {
          reject(res)
        }
      },
      fail: reject,
    })
  })
}

export const api = {
  getCategories: () => request('/meta/categories'),
  getDistricts: () => request('/meta/districts'),
  getMatters: (params = {}) => request('/matters' + toQuery(params)),
  getMatter: (id, params = {}) => request(`/matters/${id}` + toQuery(params)),
  getTemplates: (params = {}) => request('/templates' + toQuery(params)),
  getTemplate: (id) => request(`/templates/${id}`),
  createFeedback: (data) => request('/feedbacks', { method: 'POST', data }),
  getReminders: (deviceId) => request('/reminders?device_id=' + deviceId),
  createReminder: (data) => request('/reminders', { method: 'POST', data }),
  deleteReminder: (id) => request(`/reminders/${id}`, { method: 'DELETE' }),
  getProgress: (deviceId) => request('/progress?device_id=' + deviceId),
  createProgress: (data) => request('/progress', { method: 'POST', data }),
  deleteProgress: (id) => request(`/progress/${id}`, { method: 'DELETE' }),
}

function toQuery(params) {
  const keys = Object.keys(params || {}).filter((k) => params[k] !== undefined && params[k] !== null && params[k] !== '')
  if (!keys.length) return ''
  return '?' + keys.map((k) => `${k}=${encodeURIComponent(params[k])}`).join('&')
}
