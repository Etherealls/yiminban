<template>
  <view class="page" v-if="matter">
    <!-- 事项头部 -->
    <view class="hero">
      <text class="hero-name">{{ matter.name }}</text>
      <text class="hero-summary">{{ matter.summary }}</text>
      <view class="hero-tags">
        <text class="tag" :style="tagStyle(matter.fee_type)">{{ feeLabel(matter.fee_type) }}</text>
        <text class="tag" v-if="matter.is_online" style="background:#e6f7ee;color:#2eb872">支持线上办理</text>
        <text class="tag" v-if="matter.is_offline" style="background:#fff3e0;color:#f5a623">需线下窗口</text>
      </view>
      <view class="hero-meta">
        <text>办理时限：{{ matter.time_limit || '以窗口为准' }}</text>
      </view>
    </view>

    <!-- 本地化材料清单 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">📋 材料清单</text>
        <text class="district-hint" v-if="currentDistrict">适用于：{{ currentDistrict }}</text>
      </view>
      <view class="card">
        <view class="mat-group-title">必备材料</view>
        <view v-for="m in requiredMaterials" :key="m.id" class="mat-item">
          <view class="mat-check">✓</view>
          <view class="mat-body">
            <text class="mat-name">{{ m.name }}</text>
            <view class="mat-tags">
              <text class="mat-tag">{{ copyLabel(m.copy_requirement) }}</text>
              <text class="mat-tag" v-if="m.need_electronic" style="color:#4f7cff;border-color:#4f7cff">需电子版</text>
              <text class="mat-tag" v-if="m.quantity > 1">{{ m.quantity }} 份</text>
            </view>
            <text class="mat-note" v-if="m.note">{{ m.note }}</text>
          </view>
        </view>
        <template v-if="optionalMaterials.length">
          <view class="mat-group-title">可选材料</view>
          <view v-for="m in optionalMaterials" :key="m.id" class="mat-item">
            <view class="mat-check optional">○</view>
            <view class="mat-body">
              <text class="mat-name">{{ m.name }}</text>
              <view class="mat-tags">
                <text class="mat-tag">{{ copyLabel(m.copy_requirement) }}</text>
              </view>
              <text class="mat-note" v-if="m.note">{{ m.note }}</text>
            </view>
          </view>
        </template>
      </view>
      <text class="fee-note" v-if="matter.fee_desc">💰 收费说明：{{ matter.fee_desc }}</text>
    </view>

    <!-- 避坑提示 -->
    <view class="section" v-if="matter.pitfalls && matter.pitfalls.length">
      <view class="section-title">⚠️ 避坑提示</view>
      <view class="card">
        <view v-for="p in matter.pitfalls" :key="p.id" class="pitfall">
          <view class="pitfall-head">
            <text class="pitfall-tag" :style="pitTagStyle(p.tag)">{{ p.tag || '提示' }}</text>
            <text class="pitfall-title">{{ p.title }}</text>
          </view>
          <text class="pitfall-content">{{ p.content }}</text>
        </view>
      </view>
    </view>

    <!-- 官方原文溯源 -->
    <view class="section" v-if="matter.official_url">
      <view class="section-title">🔗 官方原文溯源</view>
      <view class="card link-card" @click="openOfficial">
        <view class="link-body">
          <text class="link-title">{{ matter.official_title || '查看官方原文' }}</text>
          <text class="link-source">{{ matter.official_source || '' }}</text>
        </view>
        <text class="link-arrow">›</text>
      </view>
    </view>

    <!-- 操作按钮 -->
    <view class="actions">
      <button class="btn-primary" @click="goAppointment">📅 预约与导航</button>
      <button class="btn-secondary" @click="addReminder">⏰ 添加提醒</button>
      <button class="btn-secondary" @click="goFeedback">💬 信息有误？反馈</button>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { api } from '../../utils/api'
import { useAppStore } from '../../utils/store'
import { getStorage } from '../../utils/storage'

const store = useAppStore()
const matter = ref(null)
const currentDistrict = computed(() => (store.selectedDistrict ? store.selectedDistrict.name : ''))

onLoad(async (q) => {
  store.init()
  const params = {}
  if (store.selectedDistrict) params.district_code = store.selectedDistrict.code
  try {
    matter.value = await api.getMatter(q.id, params)
    uni.setNavigationBarTitle({ title: matter.value.short_name || matter.value.name })
  } catch (e) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
})

const requiredMaterials = computed(() => (matter.value?.materials || []).filter((m) => m.material_type === 'required'))
const optionalMaterials = computed(() => (matter.value?.materials || []).filter((m) => m.material_type === 'optional'))

function feeLabel(t) { return { free: '免费', charged: '收费', mixed: '部分收费' }[t] || '' }
function tagStyle(t) {
  return { free: 'background:#e6f7ee;color:#2eb872', charged: 'background:#fff3e0;color:#f5a623', mixed: 'background:#eef3ff;color:#4f7cff' }[t] || ''
}
function copyLabel(c) {
  const map = { original: '原件', copy: '复印件', 'original+copy': '原件+复印件', electronic: '电子版' }
  return map[c] || c
}
function pitTagStyle(tag) {
  const map = { 照片: '#fff3e0;color:#f5a623', 预约: '#eef3ff;color:#4f7cff', 时间: '#fff3e0;color:#f5a623', 材料: '#e6f7ee;color:#2eb872', 费用: '#fdecec;color:#ff4d4f', 政策: '#f3edfb;color:#8b6fe8' }
  return map[tag] || '#f2f3f5;color:#646a73'
}
function openOfficial() {
  if (matter.value.official_url) {
    // #ifdef H5
    window.open(matter.value.official_url)
    // #endif
    // #ifdef MP-WEIXIN
    uni.setClipboardData({ data: matter.value.official_url, success: () => uni.showToast({ title: '链接已复制', icon: 'none' }) })
    // #endif
  }
}
function goAppointment() {
  uni.navigateTo({ url: `/pages/appointment/appointment?matterId=${matter.value.id}` })
}
function addReminder() {
  uni.navigateTo({ url: `/pages/reminder-add/reminder-add?title=${encodeURIComponent(matter.value.name)}` })
}
function goFeedback() {
  uni.navigateTo({ url: `/pages/feedback/feedback?matterId=${matter.value.id}` })
}
</script>

<style lang="scss" scoped>
.page { padding-bottom: 40rpx; }
.hero {
  background: linear-gradient(135deg, #4f7cff, #6a8dff);
  color: #fff;
  padding: 40rpx 32rpx;
}
.hero-name { font-size: 40rpx; font-weight: 700; display: block; }
.hero-summary { font-size: 26rpx; opacity: 0.9; margin-top: 10rpx; display: block; }
.hero-tags { display: flex; flex-wrap: wrap; gap: 12rpx; margin-top: 20rpx; }
.hero .tag { background: rgba(255, 255, 255, 0.2); color: #fff; }
.hero-meta { margin-top: 16rpx; font-size: 24rpx; opacity: 0.85; }
.section { margin-top: 28rpx; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin: 0 24rpx 14rpx; }
.section-title { font-size: 30rpx; font-weight: 600; color: #1f2329; margin: 0 24rpx 14rpx; }
.district-hint { font-size: 22rpx; color: #4f7cff; }
.card { background: #fff; border-radius: 16rpx; padding: 24rpx 28rpx; margin: 0 24rpx; box-shadow: 0 2rpx 12rpx rgba(31,35,41,0.04); }
.mat-group-title { font-size: 26rpx; font-weight: 600; color: #4f7cff; margin: 16rpx 0; }
.mat-item { display: flex; margin-bottom: 20rpx; }
.mat-check {
  width: 40rpx; height: 40rpx; border-radius: 50%;
  background: #e6f7ee; color: #2eb872;
  display: flex; align-items: center; justify-content: center;
  font-size: 24rpx; margin-right: 16rpx; flex-shrink: 0;
  &.optional { background: #f2f3f5; color: #8a8f99; }
}
.mat-body { flex: 1; display: flex; flex-direction: column; }
.mat-name { font-size: 28rpx; color: #1f2329; }
.mat-tags { display: flex; flex-wrap: wrap; gap: 8rpx; margin-top: 8rpx; }
.mat-tag {
  font-size: 20rpx; color: #646a73; border: 1rpx solid #e0e3e8;
  border-radius: 6rpx; padding: 2rpx 10rpx;
}
.mat-note { font-size: 22rpx; color: #8a8f99; margin-top: 6rpx; }
.fee-note { display: block; font-size: 24rpx; color: #646a73; margin: 16rpx 24rpx 0; }
.pitfall { margin-bottom: 20rpx; &:last-child { margin-bottom: 0; } }
.pitfall-head { display: flex; align-items: center; gap: 12rpx; }
.pitfall-tag { font-size: 20rpx; padding: 4rpx 12rpx; border-radius: 6rpx; }
.pitfall-title { font-size: 26rpx; font-weight: 600; color: #1f2329; }
.pitfall-content { font-size: 24rpx; color: #646a73; margin-top: 8rpx; display: block; line-height: 1.6; }
.link-card { display: flex; justify-content: space-between; align-items: center; }
.link-body { display: flex; flex-direction: column; }
.link-title { font-size: 28rpx; color: #4f7cff; }
.link-source { font-size: 22rpx; color: #8a8f99; margin-top: 6rpx; }
.link-arrow { font-size: 40rpx; color: #c0c4cc; }
.actions { padding: 30rpx 24rpx 0; display: flex; flex-direction: column; gap: 16rpx; }
.btn-primary { background: #4f7cff; color: #fff; border-radius: 12rpx; font-size: 30rpx; line-height: 2.6; }
.btn-primary::after { border: none; }
.btn-secondary { background: #fff; color: #4f7cff; border: 1rpx solid #4f7cff; border-radius: 12rpx; font-size: 28rpx; line-height: 2.5; }
.btn-secondary::after { border: none; }
</style>
