// 全局状态：分类、区县、适老模式、设置
import { defineStore } from 'pinia'
import { api } from '../utils/api'
import { getStorage, setStorage } from '../utils/storage'

export const useAppStore = defineStore('app', {
  state: () => ({
    categories: [],
    districts: [],
    selectedDistrict: null, // 当前选择的区县 {code,name}
    elderMode: getStorage('elder_mode', false), // 适老模式
    fontSize: getStorage('font_size', 1), // 字体缩放 1/1.2/1.4
    highContrast: getStorage('high_contrast', false), // 高对比度
  }),
  getters: {
    elderCategory() {
      // 适老模式只展示高频事项
      return this.categories
    },
  },
  actions: {
    async loadMeta() {
      try {
        const [cats, dists] = await Promise.all([api.getCategories(), api.getDistricts()])
        this.categories = cats || []
        this.districts = dists || []
      } catch (e) {
        console.error('加载元数据失败', e)
      }
    },
    setDistrict(d) {
      this.selectedDistrict = d
      setStorage('selected_district', d)
    },
    toggleElderMode() {
      this.elderMode = !this.elderMode
      setStorage('elder_mode', this.elderMode)
    },
    setFontSize(s) {
      this.fontSize = s
      setStorage('font_size', s)
    },
    toggleContrast() {
      this.highContrast = !this.highContrast
      setStorage('high_contrast', this.highContrast)
    },
    init() {
      this.selectedDistrict = getStorage('selected_district', null)
    },
  },
})
