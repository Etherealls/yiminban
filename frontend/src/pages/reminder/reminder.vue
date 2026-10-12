<template>
  <view class="page">
    <view class="tip">🔒 提醒数据仅保存在本机，不会自动抓取证件信息，隐私优先。</view>

    <view v-if="!list.length" class="empty">
      <text class="empty-icon">⏰</text>
      <text class="empty-text">暂无提醒，点击下方按钮添加</text>
    </view>

    <view class="list">
      <view v-for="r in sortedList" :key="r.id" class="card reminder" :class="{ expired: isExpired(r) }">
        <view class="reminder-left">
          <text class="reminder-title">{{ r.title }}</text>
          <text class="reminder-date">到期：{{ formatDate(r.remind_date) }}</text>
          <text class="reminder-note" v-if="r.note">{{ r.note }}</text>
        </view>
        <view class="reminder-right">
          <text class="days" :class="daysClass(r)">{{ daysText(r) }}</text>
          <button class="del-btn" @click="remove(r)">删除</button>
        </view>
      </view>
    </view>

    <view class="footer">
      <button class="btn-primary" @click="goAdd">＋ 添加证件 / 事项提醒</button>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getStorage, setStorage, getDeviceId } from '../../utils/storage'
import { formatDate, daysUntil } from '../../utils/helper'

const list = ref([])

onShow(() => {
  list.value = getStorage('reminders', [])
})

const sortedList = computed(() => [...list.value].sort((a, b) => new Date(a.remind_date) - new Date(b.remind_date)))

function isExpired(r) { return daysUntil(r.remind_date) < 0 && !r.is_done }
function daysText(r) {
  if (r.is_done) return '已完成'
  const d = daysUntil(r.remind_date)
  if (d < 0) return '已过期'
  if (d === 0) return '今天到期'
  return `剩 ${d} 天`
}
function daysClass(r) {
  const d = daysUntil(r.remind_date)
  if (r.is_done) return 'done'
  if (d <= 0) return 'red'
  if (d <= 7) return 'orange'
  return 'green'
}
function remove(r) {
  uni.showModal({
    title: '删除提醒',
    content: `确定删除「${r.title}」吗？`,
    success: (res) => {
      if (res.confirm) {
        list.value = list.value.filter((x) => x.id !== r.id)
        setStorage('reminders', list.value)
      }
    },
  })
}
function goAdd() {
  uni.navigateTo({ url: '/pages/reminder-add/reminder-add' })
}
</script>

<style lang="scss" scoped>
.page { padding-bottom: 160rpx; }
.tip { margin: 20rpx 24rpx; font-size: 22rpx; color: #8a8f99; }
.empty { display: flex; flex-direction: column; align-items: center; padding: 100rpx 0; }
.empty-icon { font-size: 80rpx; }
.empty-text { font-size: 26rpx; color: #8a8f99; margin-top: 20rpx; }
.list { padding: 0 24rpx; }
.reminder { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20rpx; }
.reminder-left { flex: 1; display: flex; flex-direction: column; }
.reminder-title { font-size: 28rpx; font-weight: 600; color: #1f2329; }
.reminder-date { font-size: 24rpx; color: #646a73; margin-top: 8rpx; }
.reminder-note { font-size: 22rpx; color: #8a8f99; margin-top: 6rpx; }
.reminder-right { display: flex; flex-direction: column; align-items: flex-end; gap: 10rpx; }
.days { font-size: 26rpx; font-weight: 700; }
.days.green { color: #2eb872; }
.days.orange { color: #f5a623; }
.days.red { color: #ff4d4f; }
.days.done { color: #8a8f99; }
.del-btn { background: #fdecec; color: #ff4d4f; font-size: 22rpx; border-radius: 8rpx; line-height: 2; padding: 0 20rpx; }
.del-btn::after { border: none; }
.footer { position: fixed; bottom: 0; left: 0; right: 0; padding: 20rpx 24rpx 40rpx; background: #f7f8fa; }
.btn-primary { background: #4f7cff; color: #fff; border-radius: 12rpx; font-size: 30rpx; line-height: 2.6; }
.btn-primary::after { border: none; }
</style>
