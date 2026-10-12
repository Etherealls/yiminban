<script>
export default {
  onLaunch() {
    console.log('易民办 App Launch')
  },
}
</script>

<style lang="scss">
/* 全局样式 —— 浅色系配色 */
page {
  background-color: #f7f8fa;
  color: #1f2329;
  font-size: 28rpx;
  line-height: 1.6;
}

/* 主题变量 */
:root {
  --primary: #4f7cff;
  --primary-light: #eef3ff;
  --success: #2eb872;
  --warning: #f5a623;
  --danger: #ff4d4f;
  --purple: #8b6fe8;
  --text-main: #1f2329;
  --text-sub: #646a73;
  --text-muted: #8a8f99;
  --bg-page: #f7f8fa;
  --bg-card: #ffffff;
  --border: #eef0f3;
  --radius: 16rpx;
}

.card {
  background: var(--bg-card);
  border-radius: var(--radius);
  padding: 28rpx;
  margin: 20rpx 24rpx;
  box-shadow: 0 2rpx 12rpx rgba(31, 35, 41, 0.04);
}

.btn-primary {
  background: var(--primary);
  color: #fff;
  border-radius: 12rpx;
  font-size: 30rpx;
  padding: 0 32rpx;
  line-height: 2.6;
  text-align: center;
  border: none;
}
.btn-primary::after { border: none; }

.tag {
  display: inline-block;
  font-size: 22rpx;
  padding: 4rpx 14rpx;
  border-radius: 8rpx;
  margin-right: 12rpx;
}
</style>
