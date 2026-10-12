// 日期格式化工具
export function formatDate(date) {
  if (!date) return ''
  const d = new Date(date)
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

// 计算剩余天数
export function daysUntil(date) {
  const now = new Date()
  now.setHours(0, 0, 0, 0)
  const target = new Date(date)
  target.setHours(0, 0, 0, 0)
  return Math.ceil((target - now) / (1000 * 60 * 60 * 24))
}

// 语音朗读（适老模式用）
export function speak(text) {
  // #ifdef H5
  if (window.speechSynthesis) {
    window.speechSynthesis.cancel()
    const u = new SpeechSynthesisUtterance(text)
    u.lang = 'zh-CN'
    u.rate = 0.9
    window.speechSynthesis.speak(u)
    return true
  }
  // #endif
  // #ifdef MP-WEIXIN
  // 小程序端可用插件，此处留空，由宿主实现
  // #endif
  return false
}

export function stopSpeak() {
  // #ifdef H5
  if (window.speechSynthesis) window.speechSynthesis.cancel()
  // #endif
}
