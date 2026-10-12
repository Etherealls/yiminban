<template>
  <view class="page">
    <!-- 预约说明 -->
    <view class="section-title">📅 预约说明</view>
    <view class="card">
      <view class="appoint-row">
        <text class="label">是否需要预约</text>
        <text class="value" :style="{ color: needAppoint ? '#f5a623' : '#2eb872' }">
          {{ needAppoint ? '需提前预约' : '无需预约，可现场取号' }}
        </text>
      </view>
      <text class="note" v-if="appointmentNote">{{ appointmentNote }}</text>
      <button class="btn-primary" @click="goAppoint">直达官方预约入口</button>
    </view>

    <!-- 窗口信息 -->
    <view class="section-title">🏢 办理窗口</view>
    <view v-if="windows.length">
      <view v-for="w in windows" :key="w.id" class="card window-card">
        <text class="win-name">{{ w.name }}</text>
        <view class="win-row"><text class="win-icon">📍</text><text class="win-text">{{ w.address }}</text></view>
        <view class="win-row" v-if="w.office_time"><text class="win-icon">🕐</text><text class="win-text">{{ w.office_time }}</text></view>
        <view class="win-row" v-if="w.phone"><text class="win-icon">📞</text><text class="win-text phone" @click="callPhone(w.phone)">{{ w.phone }}</text></view>
        <view class="win-row" v-if="w.parking"><text class="win-icon">🅿️</text><text class="win-text">{{ w.parking }}</text></view>
        <view class="win-row" v-if="w.bus"><text class="win-icon">🚌</text><text class="win-text">{{ w.bus }}</text></view>
        <view class="win-row" v-if="w.queue_note"><text class="win-icon">🎫</text><text class="win-text">{{ w.queue_note }}</text></view>
        <view class="win-actions">
          <button class="mini-btn" @click="callPhone(w.phone)" v-if="w.phone">拨打电话</button>
          <button class="mini-btn" @click="openMap(w.address)">地图导航</button>
        </view>
      </view>
    </view>
    <view v-else class="card empty">暂无窗口信息，请查看官方平台</view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { api } from '../../utils/api'
import { useAppStore } from '../../utils/store'

const store = useAppStore()
const matter = ref(null)
const windows = computed(() => matter.value?.windows || [])
const needAppoint = computed(() => matter.value?.need_appointment || false)
const appointmentNote = computed(() => matter.value?.appointment_note || '')

onLoad(async (q) => {
  store.init()
  const params = {}
  if (store.selectedDistrict) params.district_code = store.selectedDistrict.code
  try {
    matter.value = await api.getMatter(q.matterId, params)
  } catch (e) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
})

function goAppoint() {
  const url = matter.value?.windows?.[0]?.appointment_url
  if (url) {
    // #ifdef H5
    window.open(url)
    // #endif
    // #ifdef MP-WEIXIN
    uni.setClipboardData({ data: url, success: () => uni.showToast({ title: '已复制入口链接', icon: 'none' }) })
    // #endif
  } else {
    uni.showToast({ title: '请通过政务小程序预约', icon: 'none' })
  }
}
function callPhone(phone) {
  if (!phone) return
  uni.makePhoneCall({ phoneNumber: phone })
}
function openMap(address) {
  // #ifdef MP-WEIXIN
  uni.openLocation({ name: address, address, latitude: 39.9, longitude: 116.4 })
  // #endif
  // #ifdef H5
  uni.showToast({ title: '请在手机地图搜索：' + address, icon: 'none' })
  // #endif
}
</script>

<style lang="scss" scoped>
.page { padding-bottom: 40rpx; }
.section-title { font-size: 30rpx; font-weight: 600; color: #1f2329; margin: 28rpx 24rpx 14rpx; }
.card { background: #fff; border-radius: 16rpx; padding: 28rpx; margin: 0 24rpx; box-shadow: 0 2rpx 12rpx rgba(31,35,41,0.04); }
.appoint-row { display: flex; justify-content: space-between; align-items: center; }
.label { font-size: 26rpx; color: #646a73; }
.value { font-size: 28rpx; font-weight: 600; }
.note { font-size: 24rpx; color: #8a8f99; margin: 12rpx 0 20rpx; display: block; }
.btn-primary { background: #4f7cff; color: #fff; border-radius: 12rpx; font-size: 30rpx; line-height: 2.6; }
.btn-primary::after { border: none; }
.window-card { margin-bottom: 20rpx; }
.win-name { font-size: 30rpx; font-weight: 600; color: #1f2329; display: block; margin-bottom: 16rpx; }
.win-row { display: flex; margin-bottom: 12rpx; }
.win-icon { margin-right: 12rpx; font-size: 26rpx; }
.win-text { font-size: 26rpx; color: #646a73; flex: 1; line-height: 1.5; }
.phone { color: #4f7cff; }
.win-actions { display: flex; gap: 16rpx; margin-top: 20rpx; }
.mini-btn { flex: 1; background: #eef3ff; color: #4f7cff; border-radius: 10rpx; font-size: 26rpx; line-height: 2.4; }
.mini-btn::after { border: none; }
.empty { text-align: center; color: #8a8f99; padding: 60rpx 0; }
</style>
