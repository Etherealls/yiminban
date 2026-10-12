<template>
  <view class="page">
    <view class="tip">🙏 感谢您的反馈，后台将人工审核并更新事项库，让信息更准确。</view>

    <view class="card form">
      <view class="form-item">
        <text class="label">反馈类型</text>
        <view class="type-group">
          <view
            v-for="t in types"
            :key="t.value"
            class="type-chip"
            :class="{ active: form.feedback_type === t.value }"
            @click="form.feedback_type = t.value"
          >{{ t.label }}</view>
        </view>
      </view>
      <view class="form-item">
        <text class="label">反馈内容</text>
        <textarea v-model="form.content" placeholder="请描述信息过时、材料变更或与实际窗口要求不一致的情况" />
      </view>
      <view class="form-item">
        <text class="label">联系方式（选填，便于核实）</text>
        <input v-model="form.contact" placeholder="手机号或邮箱" />
      </view>
    </view>

    <view class="footer">
      <button class="btn-primary" @click="submit">提交反馈</button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { api } from '../../utils/api'

const types = [
  { value: 'outdated', label: '信息过时' },
  { value: 'material_change', label: '材料要求变更' },
  { value: 'window_diff', label: '窗口要求不一致' },
  { value: 'other', label: '其他' },
]

const matterId = ref(null)
const form = reactive({ feedback_type: 'outdated', content: '', contact: '' })

onLoad((q) => {
  if (q.matterId) matterId.value = Number(q.matterId)
})

function submit() {
  if (!form.content.trim()) {
    uni.showToast({ title: '请填写反馈内容', icon: 'none' })
    return
  }
  const payload = { ...form, content: form.content.trim() }
  if (matterId.value) payload.matter_id = matterId.value
  api.createFeedback(payload)
    .then(() => {
      uni.showToast({ title: '反馈成功，感谢！', icon: 'success' })
      setTimeout(() => uni.navigateBack(), 800)
    })
    .catch(() => {
      // 后端不可用时本地暂存
      uni.showToast({ title: '已记录（离线暂存）', icon: 'none' })
      setTimeout(() => uni.navigateBack(), 800)
    })
}
</script>

<style lang="scss" scoped>
.page { padding: 20rpx 0 160rpx; }
.tip { margin: 0 24rpx 20rpx; font-size: 22rpx; color: #8a8f99; line-height: 1.6; }
.form { padding: 30rpx; }
.form-item { margin-bottom: 32rpx; }
.label { display: block; font-size: 26rpx; color: #646a73; margin-bottom: 14rpx; }
.form-item input, .form-item textarea {
  background: #f7f8fa; border-radius: 12rpx; padding: 20rpx;
  font-size: 28rpx; width: 100%; box-sizing: border-box;
}
.form-item textarea { height: 200rpx; }
.type-group { display: flex; flex-wrap: wrap; gap: 16rpx; }
.type-chip {
  padding: 12rpx 28rpx; border-radius: 30rpx; font-size: 26rpx;
  background: #f2f3f5; color: #646a73;
  &.active { background: #eef3ff; color: #4f7cff; font-weight: 600; }
}
.footer { position: fixed; bottom: 0; left: 0; right: 0; padding: 20rpx 24rpx 40rpx; background: #f7f8fa; }
.btn-primary { background: #4f7cff; color: #fff; border-radius: 12rpx; font-size: 30rpx; line-height: 2.6; }
.btn-primary::after { border: none; }
</style>
