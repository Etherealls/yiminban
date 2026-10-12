// 本地存储工具 —— 隐私优先，证件提醒、进度、设置默认存本地
const PREFIX = 'ymf_'

export function getStorage(key, def = null) {
  try {
    const v = uni.getStorageSync(PREFIX + key)
    return v === '' || v === undefined || v === null ? def : v
  } catch (e) {
    return def
  }
}

export function setStorage(key, value) {
  try {
    uni.setStorageSync(PREFIX + key, value)
  } catch (e) {
    console.error('存储失败', e)
  }
}

export function removeStorage(key) {
  try {
    uni.removeStorageSync(PREFIX + key)
  } catch (e) {}
}

// 清除所有本地数据（保留设备 ID）
export function clearAll() {
  try {
    const deviceId = getDeviceId()
    uni.clearStorageSync()
    setStorage('device_id', deviceId)
  } catch (e) {
    console.error('清除失败', e)
  }
}

// 生成本地设备 ID（不采集任何个人信息）
export function getDeviceId() {
  let id = getStorage('device_id')
  if (!id) {
    id = 'dev_' + Date.now().toString(36) + Math.random().toString(36).slice(2, 8)
    setStorage('device_id', id)
  }
  return id
}
