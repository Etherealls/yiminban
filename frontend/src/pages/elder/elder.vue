<template>
  <view class="page" :class="{ 'high-contrast': highContrast }" :style="{ fontSize: fontPx }">
    <view class="elder-head">
      <text class="elder-title">关怀版 · 大字简易模式</text>
      <text class="elder-sub">只保留高频事项与电话联系，操作更简单</text>
    </view>

    <!-- 高频事项大按钮 -->
    <view class="section-title">常用事项</view>
    <view class="big-list">
      <view v-for="m in highFreq" :key="m.id" class="big-card" @click="goMatter(m)">
        <text class="big-name">{{ m.short_name || m.name }}</text>
        <view class="big-actions">
          <button class="big-btn" @click.stop="readGuide(m)">🔊 朗读</button>
          <button class="big-btn primary" @click.stop="callWindow(m)">📞 电话</button>
        </view>
      </view>
    </view>

    <!-- 语音朗读控制 -->
    <view class="section-title">语音朗读</view>
    <view class="card">
      <text class="read-hint">点击上方「朗读」可语音播报办事指南；点击「电话」可直接联系窗口。</text>
    </view>

    <!-- 快捷电话 -->
    <view class="section-title">常用服务电话</view>
    <view class="card">
      <view v-for="t in hotlines" :key="t.name" class="hotline" @click="call(t.phone)">
        <text class="hot-name">{{ t.name }}</text>
        <text class="hot-phone">{{ t.phone }}</text>
      </view>
    </view>

    <view class="footer-btn" @click="exitElder">
      <text>退出关怀版</text>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onMounted } from 'vue'
import { api } from '../../utils/api'
import { useAppStore } from '../../utils/store'
import { speak, stopSpeak } from '../../utils/helper'

const store = useAppStore()
const highFreq = ref([])
const hotlines = [
  { name: '政务服务热线', phone: '12345' },
  { name: '社保咨询', phone: '12333' },
  { name: '公积金热线', phone: '12329' },
  { name: '报警求助', phone: '110' },
  { name: '医疗急救', phone: '120' },
]

const highContrast = computed(() => store.highContrast)
const fontPx = computed(() => (16 * (store.fontSize || 1.4)).toFixed(0) + 'px')

onMounted(async () => {
  try {
    highFreq.value = await api.getMatters({ high_frequency: true })
  } catch (e) {
    highFreq.value = []
  }
})

function goMatter(m) {
  uni.navigateTo({ url: `/pages/matter/matter?id=${m.id}` })
}
function readGuide(m) {
  const text = `${m.name}。${m.summary || ''}。办理时限：${m.time_limit || '以窗口为准'}。${m.fee_desc || ''}。如需了解材料清单，请点击事项查看详情。`
  speak(text)
  uni.showToast({ title: '正在朗读', icon: 'none' })
}
function callWindow(m) {
  const phone = m.windows?.[0]?.phone
  if (phone) {
    uni.makePhoneCall({ phoneNumber: phone })
  } else {
    uni.makePhoneCall({ phoneNumber: '12345' })
  }
}
function call(phone) {
  uni.makePhoneCall({ phoneNumber: phone })
}
function exitElder() {
  store.toggleElderMode()
  uni.switchTab({ url: '/pages/index/index' })
}
</script>

<style lang="scss" scoped>
.page { padding: 0 0 60rpx; min-height: 100vh; }
.high-contrast { background: #000; color: #fff; }
.elder-head {
  background: linear-gradient(135deg, #4f7cff, #6a8dff);
  color: #fff; padding: 50rpx 40rpx;
}
.elder-title { font-size: 44rpx; font-weight: 700; display: block; }
.elder-sub { font-size: 28rpx; opacity: 0.9; margin-top: 12rpx; display: block; }
.section-title { font-size: 34rpx; font-weight: 600; margin: 30rpx 28rpx 16rpx; }
.big-list { padding: 0 28rpx; }
.big-card {
  background: #fff; border-radius: 16rpx; padding: 32rpx;
  margin-bottom: 24rpx; box-shadow: 0 2rpx 12rpx rgba(31,35,41,0.06);
}
.high-contrast .big-card { background: #222; }
.big-name { font-size: 36rpx; font-weight: 700; display: block; }
.big-actions { display: flex; gap: 20rpx; margin-top: 24rpx; }
.big-btn {
  flex: 1; background: #f2f3f5; color: #333; border-radius: 12rpx;
  font-size: 30rpx; line-height: 2.6;
}
.big-btn.primary { background: #eef3ff; color: #4f7cff; }
.big-btn::after { border: none; }
.card { background: #fff; border-radius: 16rpx; padding: 32rpx; margin: 0 28rpx; }
.high-contrast .card { background: #222; }
.read-hint { font-size: 30rpx; line-height: 1.7; }
.hotline { display: flex; justify-content: space-between; align-items: center; padding: 24rpx 0; border-bottom: 1rpx solid #eee; }
.hotline:last-child { border-bottom: none; }
.hot-name { font-size: 32rpx; }
.hot-phone { font-size: 32rpx; color: #4f7cff; font-weight: 700; }
.footer-btn { text-align: center; padding: 40rpx 0; color: #8a8f99; font-size: 28rpx; }
</style>
