<template>
  <view class="page">
    <view class="tip">📝 以下模板仅供参考，实际以窗口最终要求为准。</view>

    <view class="list">
      <view v-for="t in templates" :key="t.id" class="card tpl" @click="goDetail(t)">
        <view class="tpl-left">
          <text class="tpl-icon">📄</text>
          <view class="tpl-body">
            <text class="tpl-name">{{ t.name }}</text>
            <text class="tpl-type">{{ t.template_type }}</text>
          </view>
        </view>
        <text class="tpl-arrow">›</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { onMounted } from 'vue'
import { api } from '../../utils/api'

const templates = ref([])

onMounted(async () => {
  try {
    templates.value = await api.getTemplates()
  } catch (e) {
    templates.value = []
  }
})

function goDetail(t) {
  uni.navigateTo({ url: `/pages/template-detail/template-detail?id=${t.id}` })
}
</script>

<style lang="scss" scoped>
.page { padding: 20rpx 0 40rpx; }
.tip { margin: 0 24rpx 20rpx; font-size: 22rpx; color: #f5a623; }
.list { padding: 0 24rpx; }
.tpl { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20rpx; }
.tpl-left { display: flex; align-items: center; }
.tpl-icon { font-size: 44rpx; margin-right: 20rpx; }
.tpl-body { display: flex; flex-direction: column; }
.tpl-name { font-size: 28rpx; font-weight: 600; color: #1f2329; }
.tpl-type { font-size: 22rpx; color: #8a8f99; margin-top: 6rpx; }
.tpl-arrow { font-size: 36rpx; color: #c0c4cc; }
</style>
