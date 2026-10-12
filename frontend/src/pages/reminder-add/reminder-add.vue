<template>
  <view class="page">
    <view class="card form">
      <view class="form-item">
        <text class="label">提醒标题</text>
        <input v-model="form.title" placeholder="如：身份证到期换领、居住证续签" />
      </view>
      <view class="form-item">
        <text class="label">类型</text>
        <view class="type-group">
          <view
            v-for="t in types"
            :key="t.value"
            class="type-chip"
            :class="{ active: form.reminder_type === t.value }"
            @click="form.reminder_type = t.value"
          >{{ t.label }}</view>
        </view>
      </view>
      <view class="form-item">
        <text class="label">到期日期</text>
        <picker mode="date" :value="form.remind_date" @change="onDate">
          <view class="date-picker">{{ form.remind_date || '请选择日期' }}</view>
        </picker>
      </view>
      <view class="form-item">
        <text class="label">提前提醒</text>
        <view class="advance-group">
          <view
            v-for="d in [3, 7, 15, 30]"
            :key="d"
            class="advance-chip"
            :class="{ active: form.advance_days === d }"
            @click="form.advance_days = d"
          >提前 {{ d }} 天</view>
        </view>
      </view>
      <view class="form-item">
        <text class="label">备注（可选）</text>
        <textarea v-model="form.note" placeholder="补充说明" />
      </view>
    </view>

    <view class="footer">
      <button class="btn-primary" @click="save">保存提醒</button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getStorage, setStorage } from '../../utils/storage'

const types = [
  { value: 'matter', label: '办事事项' },
  { value: 'cert', label: '证件到期' },
  { value: 'other', label: '其他' },
]

const form = reactive({
  title: '',
  reminder_type: 'matter',
  remind_date: '',
  advance_days: 7,
  note: '',
})

onLoad((q) => {
  if (q.title) form.title = decodeURIComponent(q.title)
  // 默认日期：一年后
  const d = new Date()
  d.setFullYear(d.getFullYear() + 1)
  form.remind_date = d.toISOString().slice(0, 10)
})

function onDate(e) {
  form.remind_date = e.detail.value
}

function save() {
  if (!form.title.trim()) {
    uni.showToast({ title: '请填写提醒标题', icon: 'none' })
    return
  }
  if (!form.remind_date) {
    uni.showToast({ title: '请选择到期日期', icon: 'none' })
    return
  }
  const list = getStorage('reminders', [])
  list.push({
    id: Date.now(),
    title: form.title.trim(),
    reminder_type: form.reminder_type,
    remind_date: form.remind_date,
    advance_days: form.advance_days,
    note: form.note,
    is_done: false,
    created_at: new Date().toISOString(),
  })
  setStorage('reminders', list)
  uni.showToast({ title: '已保存', icon: 'success' })
  setTimeout(() => uni.navigateBack(), 500)
}
</script>

<style lang="scss" scoped>
.page { padding: 20rpx 0 160rpx; }
.form { padding: 30rpx; }
.form-item { margin-bottom: 32rpx; }
.label { display: block; font-size: 26rpx; color: #646a73; margin-bottom: 14rpx; }
.form-item input, .form-item textarea {
  background: #f7f8fa; border-radius: 12rpx; padding: 20rpx;
  font-size: 28rpx; width: 100%; box-sizing: border-box;
}
.form-item textarea { height: 160rpx; }
.type-group, .advance-group { display: flex; flex-wrap: wrap; gap: 16rpx; }
.type-chip, .advance-chip {
  padding: 12rpx 28rpx; border-radius: 30rpx; font-size: 26rpx;
  background: #f2f3f5; color: #646a73;
  &.active { background: #eef3ff; color: #4f7cff; font-weight: 600; }
}
.date-picker { background: #f7f8fa; border-radius: 12rpx; padding: 20rpx; font-size: 28rpx; color: #1f2329; }
.footer { position: fixed; bottom: 0; left: 0; right: 0; padding: 20rpx 24rpx 40rpx; background: #f7f8fa; }
.btn-primary { background: #4f7cff; color: #fff; border-radius: 12rpx; font-size: 30rpx; line-height: 2.6; }
.btn-primary::after { border: none; }
</style>
