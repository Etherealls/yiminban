<template>
  <view class="page" v-if="tpl">
    <view class="card">
      <text class="tpl-name">{{ tpl.name }}</text>
      <text class="tpl-type">{{ tpl.template_type }}</text>
      <view class="divider"></view>
      <text class="tpl-content">{{ tpl.content }}</text>
      <view class="divider"></view>
      <text class="disclaimer">⚠️ {{ tpl.disclaimer || '本模板仅供参考，以窗口最终要求为准' }}</text>
      <text class="usage" v-if="tpl.usage_note">{{ tpl.usage_note }}</text>
    </view>

    <view class="actions">
      <button class="btn-primary" @click="exportPdf">📤 导出 PDF</button>
      <button class="btn-secondary" @click="copyContent">📋 复制内容</button>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { api } from '../../utils/api'

const tpl = ref(null)

onLoad(async (q) => {
  try {
    tpl.value = await api.getTemplate(q.id)
    uni.setNavigationBarTitle({ title: tpl.value.name })
  } catch (e) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
})

function copyContent() {
  uni.setClipboardData({ data: tpl.value.content, success: () => uni.showToast({ title: '已复制', icon: 'none' }) })
}

function exportPdf() {
  // H5 端：生成打印友好的 PDF
  // #ifdef H5
  const content = tpl.value.content.replace(/\n/g, '<br/>')
  const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>${tpl.value.name}</title>
    <style>body{font-family:'SimSun','宋体',serif;padding:40px;line-height:2;font-size:16px;}
    h1{font-size:24px;text-align:center;} .disc{color:#999;font-size:12px;text-align:center;margin-top:30px;}</style>
    </head><body><h1>${tpl.value.name}</h1><div>${content}</div><div class="disc">本模板仅供参考，以窗口最终要求为准</div></body></html>`
  const w = window.open('', '_blank')
  w.document.write(html)
  w.document.close()
  w.print()
  // #endif
  // #ifdef MP-WEIXIN
  uni.showToast({ title: '请在浏览器打开后打印为 PDF', icon: 'none' })
  // #endif
}
</script>

<style lang="scss" scoped>
.page { padding-bottom: 40rpx; }
.card { background: #fff; border-radius: 16rpx; padding: 36rpx; margin: 20rpx 24rpx; box-shadow: 0 2rpx 12rpx rgba(31,35,41,0.04); }
.tpl-name { font-size: 36rpx; font-weight: 700; color: #1f2329; display: block; text-align: center; }
.tpl-type { font-size: 24rpx; color: #8a8f99; display: block; text-align: center; margin-top: 8rpx; }
.divider { height: 1rpx; background: #eef0f3; margin: 30rpx 0; }
.tpl-content { font-size: 28rpx; color: #333; white-space: pre-wrap; line-height: 1.9; }
.disclaimer { display: block; font-size: 22rpx; color: #f5a623; }
.usage { display: block; font-size: 22rpx; color: #8a8f99; margin-top: 12rpx; }
.actions { padding: 20rpx 24rpx; display: flex; flex-direction: column; gap: 16rpx; }
.btn-primary { background: #4f7cff; color: #fff; border-radius: 12rpx; font-size: 30rpx; line-height: 2.6; }
.btn-primary::after { border: none; }
.btn-secondary { background: #fff; color: #4f7cff; border: 1rpx solid #4f7cff; border-radius: 12rpx; font-size: 28rpx; line-height: 2.5; }
.btn-secondary::after { border: none; }
</style>
