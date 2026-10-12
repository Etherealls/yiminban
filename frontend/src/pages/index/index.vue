<template>
  <view class="page">
    <!-- 顶部搜索 + 区县选择 -->
    <view class="header">
      <view class="district" @click="showDistrict">
        <text class="icon">📍</text>
        <text class="name">{{ currentDistrict || '选择区县' }}</text>
        <text class="arrow">▾</text>
      </view>
      <view class="search">
        <input
          v-model="keyword"
          placeholder="搜索办事事项，如：身份证、社保"
          confirm-type="search"
          @confirm="onSearch"
        />
      </view>
    </view>

    <!-- 适老模式开关提示 -->
    <view v-if="elderMode" class="elder-banner" @click="goElder">
      <text>🔊 已开启关怀版 · 点击进入大字简易模式</text>
    </view>

    <!-- 分类宫格 -->
    <view class="section-title">办事事项分类</view>
    <view class="grid">
      <view
        v-for="c in categories"
        :key="c.code"
        class="grid-item"
        @click="goCategory(c)"
      >
        <view class="grid-icon" :style="{ background: c.color + '1a', color: c.color }">
          {{ iconOf(c.icon) }}
        </view>
        <text class="grid-name">{{ c.name }}</text>
      </view>
    </view>

    <!-- 高频事项（快速入口） -->
    <view class="section-title">高频事项 · 快速办理</view>
    <view class="card">
      <view
        v-for="m in highFreq"
        :key="m.id"
        class="freq-item"
        @click="goMatter(m)"
      >
        <view class="freq-left">
          <text class="freq-name">{{ m.name }}</text>
          <text class="freq-sub">{{ m.summary }}</text>
        </view>
        <view class="freq-tags">
          <text class="tag" :style="tagStyle(m.fee_type)">{{ feeLabel(m.fee_type) }}</text>
          <text class="tag" v-if="m.is_online" style="background:#e6f7ee;color:#2eb872">可线上</text>
        </view>
      </view>
    </view>

    <!-- 功能入口 -->
    <view class="section-title">实用工具</view>
    <view class="tools">
      <view class="tool" @click="go('templates')">
        <text class="tool-icon">📄</text>
        <text class="tool-name">材料模板</text>
      </view>
      <view class="tool" @click="go('reminder')">
        <text class="tool-icon">⏰</text>
        <text class="tool-name">事项提醒</text>
      </view>
      <view class="tool" @click="go('progress')">
        <text class="tool-icon">📊</text>
        <text class="tool-name">进度聚合</text>
      </view>
      <view class="tool" @click="go('feedback')">
        <text class="tool-icon">💬</text>
        <text class="tool-name">反馈纠错</text>
      </view>
      <view class="tool" @click="go('elder')">
        <text class="tool-icon">👵</text>
        <text class="tool-name">关怀版</text>
      </view>
      <view class="tool" @click="go('settings')">
        <text class="tool-icon">⚙️</text>
        <text class="tool-name">设置</text>
      </view>
    </view>

    <view class="disclaimer">本工具仅提供办事指引，不替代政务系统、不直接办理业务，具体以窗口最终要求为准。</view>

    <!-- 区县选择弹窗 -->
    <view v-if="showPicker" class="mask" @click="showPicker = false">
      <view class="picker" @click.stop>
        <view class="picker-title">选择所在区县</view>
        <view
          v-for="d in districts"
          :key="d.code"
          class="picker-item"
          :class="{ active: currentDistrict === d.name }"
          @click="selectDistrict(d)"
        >
          {{ d.province }} · {{ d.city }} · {{ d.name }}
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../../utils/api'
import { useAppStore } from '../../utils/store'

const store = useAppStore()
const keyword = ref('')
const highFreq = ref([])
const showPicker = ref(false)

const categories = computed(() => store.categories)
const districts = computed(() => store.districts)
const currentDistrict = computed(() => (store.selectedDistrict ? store.selectedDistrict.name : ''))
const elderMode = computed(() => store.elderMode)

onMounted(async () => {
  store.init()
  if (!store.categories.length) await store.loadMeta()
  loadHighFreq()
})

async function loadHighFreq() {
  try {
    highFreq.value = await api.getMatters({ high_frequency: true })
  } catch (e) {
    highFreq.value = []
  }
}

function iconOf(icon) {
  const map = { hukou: '👨‍👩‍👧', shebao: '🛡️', gongjijin: '🏠', budongchan: '🏢', hunyin: '💍', ruxue: '🎒', yanglao: '🌻', zhengjian: '🪪' }
  return map[icon] || '📋'
}

function feeLabel(t) {
  return { free: '免费', charged: '收费', mixed: '部分收费' }[t] || ''
}
function tagStyle(t) {
  return { free: 'background:#e6f7ee;color:#2eb872', charged: 'background:#fff3e0;color:#f5a623', mixed: 'background:#eef3ff;color:#4f7cff' }[t] || ''
}

function showDistrict() { showPicker.value = true }
function selectDistrict(d) {
  store.setDistrict(d)
  showPicker.value = false
}

function onSearch() {
  if (!keyword.value.trim()) return
  uni.navigateTo({ url: `/pages/category/category?keyword=${encodeURIComponent(keyword.value.trim())}` })
}

function goCategory(c) {
  uni.navigateTo({ url: `/pages/category/category?code=${c.code}&name=${c.name}` })
}
function goMatter(m) {
  uni.navigateTo({ url: `/pages/matter/matter?id=${m.id}` })
}
function go(page) {
  const map = {
    templates: '/pages/templates/templates',
    reminder: '/pages/reminder/reminder',
    progress: '/pages/progress/progress',
    feedback: '/pages/feedback/feedback',
    elder: '/pages/elder/elder',
    settings: '/pages/settings/settings',
  }
  uni.navigateTo({ url: map[page] })
}
function goElder() {
  uni.navigateTo({ url: '/pages/elder/elder' })
}
</script>

<style lang="scss" scoped>
.page { padding-bottom: 40rpx; }
.header {
  background: #fff;
  padding: 20rpx 24rpx;
  display: flex;
  align-items: center;
  gap: 16rpx;
}
.district {
  display: flex;
  align-items: center;
  white-space: nowrap;
  .icon { font-size: 28rpx; }
  .name { font-size: 28rpx; color: #1f2329; margin: 0 4rpx; max-width: 160rpx; overflow: hidden; }
  .arrow { font-size: 22rpx; color: #8a8f99; }
}
.search {
  flex: 1;
  background: #f2f3f5;
  border-radius: 30rpx;
  padding: 8rpx 24rpx;
  input { font-size: 26rpx; height: 56rpx; }
}
.elder-banner {
  margin: 20rpx 24rpx 0;
  background: #fff8e6;
  color: #b37b00;
  border-radius: 12rpx;
  padding: 20rpx 24rpx;
  font-size: 26rpx;
}
.section-title {
  margin: 28rpx 24rpx 16rpx;
  font-size: 30rpx;
  font-weight: 600;
  color: #1f2329;
}
.grid {
  display: flex;
  flex-wrap: wrap;
  margin: 0 12rpx;
}
.grid-item {
  width: 25%;
  padding: 12rpx 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.grid-icon {
  width: 88rpx;
  height: 88rpx;
  border-radius: 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
}
.grid-name { font-size: 24rpx; color: #1f2329; margin-top: 8rpx; }
.freq-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #f2f3f5;
  &:last-child { border-bottom: none; }
}
.freq-left { flex: 1; display: flex; flex-direction: column; }
.freq-name { font-size: 28rpx; color: #1f2329; }
.freq-sub { font-size: 22rpx; color: #8a8f99; margin-top: 6rpx; }
.freq-tags { display: flex; flex-direction: column; gap: 6rpx; align-items: flex-end; }
.tools {
  display: flex;
  flex-wrap: wrap;
  margin: 0 12rpx;
}
.tool {
  width: 33.33%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20rpx 0;
}
.tool-icon { font-size: 48rpx; }
.tool-name { font-size: 24rpx; color: #1f2329; margin-top: 8rpx; }
.disclaimer {
  margin: 30rpx 40rpx;
  font-size: 22rpx;
  color: #b0b5bd;
  text-align: center;
  line-height: 1.5;
}
.mask {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 100;
  display: flex;
  align-items: flex-end;
}
.picker {
  width: 100%;
  background: #fff;
  border-radius: 24rpx 24rpx 0 0;
  padding: 30rpx 24rpx 60rpx;
  max-height: 70vh;
  overflow-y: auto;
}
.picker-title { font-size: 30rpx; font-weight: 600; text-align: center; margin-bottom: 20rpx; }
.picker-item {
  padding: 24rpx;
  font-size: 28rpx;
  border-bottom: 1rpx solid #f2f3f5;
  &.active { color: #4f7cff; font-weight: 600; }
}
</style>
