<template>
  <view class="page">
    <view class="card">
      <view class="setting-item" @click="store.toggleElderMode()">
        <view class="setting-left">
          <text class="setting-name">关怀模式</text>
          <text class="setting-desc">开启大字、高对比、语音朗读的简易模式</text>
        </view>
        <switch :checked="store.elderMode" color="#4f7cff" @change="store.toggleElderMode()" />
      </view>

      <view class="setting-item">
        <view class="setting-left">
          <text class="setting-name">高对比度</text>
          <text class="setting-desc">增强文字与背景对比，方便阅读</text>
        </view>
        <switch :checked="store.highContrast" color="#4f7cff" @change="store.toggleContrast()" />
      </view>

      <view class="setting-item">
        <view class="setting-left">
          <text class="setting-name">字体大小</text>
          <text class="setting-desc">调整关怀版字号</text>
        </view>
        <view class="font-options">
          <text
            v-for="o in fontOptions"
            :key="o.value"
            class="font-opt"
            :class="{ active: store.fontSize === o.value }"
            @click="store.setFontSize(o.value)"
          >{{ o.label }}</text>
        </view>
      </view>
    </view>

    <view class="card">
      <view class="setting-item" @click="clearCache">
        <view class="setting-left">
          <text class="setting-name">清除本地数据</text>
          <text class="setting-desc">清除提醒、进度等本机存储</text>
        </view>
        <text class="arrow">›</text>
      </view>
    </view>

    <view class="card about">
      <text class="about-title">关于易民办</text>
      <text class="about-text">版本 1.0.0</text>
      <text class="about-text">本工具仅提供办事指引，不替代政务系统、不直接办理业务。</text>
      <text class="about-text">数据以官方发布为准，如有出入欢迎反馈纠错。</text>
    </view>
  </view>
</template>

<script setup>
import { useAppStore } from '../../utils/store'
import { clearAll } from '../../utils/storage'

const store = useAppStore()
const fontOptions = [
  { value: 1, label: '标准' },
  { value: 1.2, label: '较大' },
  { value: 1.4, label: '特大' },
]

function clearCache() {
  uni.showModal({
    title: '清除本地数据',
    content: '将清除本机保存的提醒、进度等数据，确定继续？',
    success: (res) => {
      if (res.confirm) {
        clearAll()
        uni.showToast({ title: '已清除', icon: 'success' })
      }
    },
  })
}
</script>

<style lang="scss" scoped>
.page { padding: 20rpx 0; }
.card { background: #fff; border-radius: 16rpx; margin: 0 24rpx 20rpx; box-shadow: 0 2rpx 12rpx rgba(31,35,41,0.04); }
.setting-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: 28rpx; border-bottom: 1rpx solid #f2f3f5;
}
.setting-item:last-child { border-bottom: none; }
.setting-left { flex: 1; display: flex; flex-direction: column; }
.setting-name { font-size: 28rpx; color: #1f2329; }
.setting-desc { font-size: 22rpx; color: #8a8f99; margin-top: 6rpx; }
.arrow { font-size: 36rpx; color: #c0c4cc; }
.font-options { display: flex; gap: 12rpx; }
.font-opt {
  padding: 8rpx 20rpx; border-radius: 8rpx; background: #f2f3f5;
  color: #646a73; font-size: 24rpx;
  &.active { background: #eef3ff; color: #4f7cff; font-weight: 600; }
}
.about { padding: 30rpx; display: flex; flex-direction: column; }
.about-title { font-size: 28rpx; font-weight: 600; color: #1f2329; margin-bottom: 14rpx; }
.about-text { font-size: 22rpx; color: #8a8f99; margin-top: 8rpx; line-height: 1.6; }
</style>
