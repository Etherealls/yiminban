<template>
  <view class="page">
    <!-- 搜索栏（当从搜索进入时展示） -->
    <view v-if="isSearch" class="search-bar">
      <input v-model="keyword" placeholder="搜索办事事项" confirm-type="search" @confirm="load" />
    </view>

    <view class="list">
      <view v-for="m in list" :key="m.id" class="matter-card" @click="goMatter(m)">
        <view class="matter-top">
          <text class="matter-name">{{ m.name }}</text>
          <text class="tag" :style="tagStyle(m.fee_type)">{{ feeLabel(m.fee_type) }}</text>
        </view>
        <text class="matter-summary">{{ m.summary }}</text>
        <view class="matter-bottom">
          <text class="meta">{{ m.time_limit }}</text>
          <text class="meta" v-if="m.is_online">🟢 可线上</text>
          <text class="meta" v-else>🏢 需线下</text>
        </view>
      </view>
    </view>

    <view v-if="!list.length && loaded" class="empty">暂无相关事项</view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { api } from '../../utils/api'

const list = ref([])
const loaded = ref(false)
const categoryCode = ref('')
const keyword = ref('')
const isSearch = ref(false)

onLoad((q) => {
  if (q.code) {
    categoryCode.value = q.code
    uni.setNavigationBarTitle({ title: q.name || '事项' })
  }
  if (q.keyword) {
    isSearch.value = true
    keyword.value = decodeURIComponent(q.keyword)
  }
  load()
})

async function load() {
  loaded.value = false
  const params = {}
  if (categoryCode.value) params.category_code = categoryCode.value
  if (keyword.value) params.keyword = keyword.value
  try {
    list.value = await api.getMatters(params)
  } catch (e) {
    list.value = []
  }
  loaded.value = true
}

function goMatter(m) {
  uni.navigateTo({ url: `/pages/matter/matter?id=${m.id}` })
}
function feeLabel(t) { return { free: '免费', charged: '收费', mixed: '部分收费' }[t] || '' }
function tagStyle(t) {
  return { free: 'background:#e6f7ee;color:#2eb872', charged: 'background:#fff3e0;color:#f5a623', mixed: 'background:#eef3ff;color:#4f7cff' }[t] || ''
}
</script>

<style lang="scss" scoped>
.page { padding: 20rpx 0 40rpx; }
.search-bar { padding: 0 24rpx 16rpx; }
.search-bar input { background: #fff; border-radius: 30rpx; padding: 12rpx 24rpx; font-size: 26rpx; }
.list { padding: 0 24rpx; }
.matter-card {
  background: #fff;
  border-radius: 16rpx;
  padding: 28rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 12rpx rgba(31, 35, 41, 0.04);
}
.matter-top { display: flex; justify-content: space-between; align-items: center; }
.matter-name { font-size: 30rpx; font-weight: 600; color: #1f2329; flex: 1; }
.matter-summary { font-size: 24rpx; color: #646a73; margin-top: 10rpx; display: block; }
.matter-bottom { display: flex; gap: 20rpx; margin-top: 14rpx; }
.meta { font-size: 22rpx; color: #8a8f99; }
.empty { text-align: center; color: #8a8f99; padding: 80rpx 0; }
</style>
