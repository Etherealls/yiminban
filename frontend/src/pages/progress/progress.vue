<template>
  <view class="page">
    <view class="tip">📊 聚合多个办事事项进度，点击跳转对应官方平台查看，不对接政务 API。</view>

    <view v-if="!list.length" class="empty">
      <text class="empty-icon">📭</text>
      <text class="empty-text">暂无进行中的事项，点击下方添加</text>
    </view>

    <view class="list">
      <view v-for="p in list" :key="p.id" class="card prog">
        <view class="prog-head">
          <text class="prog-title">{{ p.title }}</text>
          <text class="status" :style="statusStyle(p.status)">{{ statusLabel(p.status) }}</text>
        </view>
        <text class="prog-platform" v-if="p.platform">{{ p.platform }}</text>
        <text class="prog-note" v-if="p.note">{{ p.note }}</text>
        <view class="prog-actions">
          <button class="mini-btn primary" @click="goPlatform(p)">查看进度</button>
          <button class="mini-btn" @click="remove(p)">删除</button>
        </view>
      </view>
    </view>

    <view class="footer">
      <button class="btn-primary" @click="showAdd = true">＋ 添加办事事项</button>
    </view>

    <!-- 添加弹窗 -->
    <view v-if="showAdd" class="mask" @click="showAdd = false">
      <view class="sheet" @click.stop>
        <view class="sheet-title">添加办事事项</view>
        <view class="form-item">
          <input v-model="form.title" placeholder="事项名称，如：公积金提取" />
        </view>
        <view class="form-item">
          <input v-model="form.platform" placeholder="对应平台，如：XX公积金" />
        </view>
        <view class="form-item">
          <input v-model="form.platform_url" placeholder="平台链接（选填）" />
        </view>
        <view class="form-item">
          <input v-model="form.note" placeholder="备注（选填）" />
        </view>
        <button class="btn-primary" @click="save">保存</button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getStorage, setStorage } from '../../utils/storage'

const list = ref([])
const showAdd = ref(false)
const form = reactive({ title: '', platform: '', platform_url: '', note: '' })

onShow(() => {
  list.value = getStorage('progress', [])
})

function statusLabel(s) { return { processing: '办理中', done: '已办结', failed: '需补正' }[s] || s }
function statusStyle(s) {
  return { processing: 'color:#4f7cff', done: 'color:#2eb872', failed: 'color:#ff4d4f' }[s] || 'color:#8a8f99'
}
function goPlatform(p) {
  if (p.platform_url) {
    // #ifdef H5
    window.open(p.platform_url)
    // #endif
    // #ifdef MP-WEIXIN
    uni.setClipboardData({ data: p.platform_url, success: () => uni.showToast({ title: '已复制平台链接', icon: 'none' }) })
    // #endif
  } else {
    uni.showToast({ title: '请补充平台链接', icon: 'none' })
  }
}
function remove(p) {
  uni.showModal({
    title: '删除',
    content: `确定删除「${p.title}」吗？`,
    success: (res) => {
      if (res.confirm) {
        list.value = list.value.filter((x) => x.id !== p.id)
        setStorage('progress', list.value)
      }
    },
  })
}
function save() {
  if (!form.title.trim()) {
    uni.showToast({ title: '请填写事项名称', icon: 'none' })
    return
  }
  list.value.push({
    id: Date.now(),
    title: form.title.trim(),
    platform: form.platform,
    platform_url: form.platform_url,
    status: 'processing',
    note: form.note,
    created_at: new Date().toISOString(),
  })
  setStorage('progress', list.value)
  showAdd.value = false
  form.title = form.platform = form.platform_url = form.note = ''
  uni.showToast({ title: '已添加', icon: 'success' })
}
</script>

<style lang="scss" scoped>
.page { padding-bottom: 160rpx; }
.tip { margin: 20rpx 24rpx; font-size: 22rpx; color: #8a8f99; }
.empty { display: flex; flex-direction: column; align-items: center; padding: 100rpx 0; }
.empty-icon { font-size: 80rpx; }
.empty-text { font-size: 26rpx; color: #8a8f99; margin-top: 20rpx; }
.list { padding: 0 24rpx; }
.prog { margin-bottom: 20rpx; }
.prog-head { display: flex; justify-content: space-between; align-items: center; }
.prog-title { font-size: 30rpx; font-weight: 600; color: #1f2329; }
.status { font-size: 24rpx; font-weight: 600; }
.prog-platform { display: block; font-size: 24rpx; color: #646a73; margin-top: 10rpx; }
.prog-note { display: block; font-size: 22rpx; color: #8a8f99; margin-top: 6rpx; }
.prog-actions { display: flex; gap: 16rpx; margin-top: 20rpx; }
.mini-btn { flex: 1; background: #f2f3f5; color: #646a73; border-radius: 10rpx; font-size: 26rpx; line-height: 2.4; }
.mini-btn.primary { background: #eef3ff; color: #4f7cff; }
.mini-btn::after { border: none; }
.footer { position: fixed; bottom: 0; left: 0; right: 0; padding: 20rpx 24rpx 40rpx; background: #f7f8fa; }
.btn-primary { background: #4f7cff; color: #fff; border-radius: 12rpx; font-size: 30rpx; line-height: 2.6; }
.btn-primary::after { border: none; }
.mask { position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 100; display: flex; align-items: flex-end; }
.sheet { width: 100%; background: #fff; border-radius: 24rpx 24rpx 0 0; padding: 30rpx 24rpx 60rpx; }
.sheet-title { font-size: 30rpx; font-weight: 600; text-align: center; margin-bottom: 24rpx; }
.form-item { margin-bottom: 20rpx; }
.form-item input { background: #f7f8fa; border-radius: 12rpx; padding: 20rpx; font-size: 28rpx; width: 100%; box-sizing: border-box; }
</style>
