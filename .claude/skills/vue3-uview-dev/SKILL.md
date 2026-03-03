---
name: vue3-uview-dev
description: 专门针对 Vue3 + uView Plus (uni-app) + Tailwind CSS 的前端开发规范。在处理 uni-app 项目、使用 uView 组件库、编写小程序或移动端 H5 页面时，必须使用此规范。
version: v1.1
paths:
  - "**/*.vue"
  - "**/*.ts"
  - "**/*.js"
  - "**/*.json"
  - "**/pages.json"
  - "**/manifest.json"
  - "**/tailwind.config.*"
---

# Vue3 + uView Plus + Tailwind 开发规范

本规范参考了通用前端开发规范并结合了 uni-app 移动端开发的特殊性，旨在指导开发者高效、标准地构建跨端应用。

## 0. UI 视觉风格约束

为了保证产品质量，严禁生成“AI 风格”或“炫酷科技风”的界面。

### 1.1 严格禁止（常见 AI 风格）
- ❌ 蓝紫色霓虹渐变、发光描边、玻璃拟态（glassmorphism）。
- ❌ 大面积渐变、过多装饰性几何图形、无意义的动效堆叠。
- ❌ UI 文案中使用 emoji（除非产品明确要求）。
- ❌ 赛博风、暗黑科技风。

### 1.2 移动端应用（默认风格）
- **目标**: “简约、清晰、易用”，符合原生 App 或成熟小程序的设计规范。
- **配色**: 白/浅灰背景为主 + 1 个主色点缀，文字层级分明。
- **单位**: 布局使用 `rpx`（在 Tailwind 中通过配置支持）。

---

## 1. 技术栈要求

- **框架**: Vue 3 (Composition API) + TypeScript
- **平台**: uni-app (支持微信小程序/H5/App)
- **UI 组件库**: uView Plus (统一前缀 `up-`)
- **样式工具**: Tailwind CSS (移动端适配版，如 `tailwindcss-rem2px-preset` 或 `weapp-tailwindcss`)

---

## 2. 编码规范

### 2.1 组件基础模板 (Setup + Tailwind)

```vue
<script setup lang="ts">
import { ref, reactive } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

// 1. Props & Emits
interface Props {
  title?: string
  loading?: boolean
}
const props = withDefaults(defineProps<Props>(), {
  title: '页面标题',
  loading: false
})

const emit = defineEmits<{
  (e: 'confirm', data: any): void
}>()

// 2. 状态管理
const formData = reactive({
  name: '',
  phone: ''
})

// 3. 生命周期
onLoad((options) => {
  console.log('Page Load:', options)
})

// 4. 方法
const handleSubmit = () => {
  emit('confirm', formData)
}
</script>

<template>
  <view class="min-h-screen bg-gray-50 flex flex-col">
    <up-navbar :title="props.title" autoBack placeholder border></up-navbar>
    
    <view class="p-4 flex-1">
      <!-- Tailwind CSS 布局 -->
      <view class="bg-white rounded-2xl p-6 shadow-sm">
        <up-form labelPosition="left" labelWidth="160rpx">
          <up-form-item label="姓名" borderBottom>
            <up-input v-model="formData.name" placeholder="请输入姓名" border="none"></up-input>
          </up-form-item>
          <up-form-item label="电话" borderBottom>
            <up-input v-model="formData.phone" placeholder="请输入电话" border="none"></up-input>
          </up-form-item>
        </up-form>
        
        <view class="mt-8">
          <up-button 
            type="primary" 
            text="提交" 
            :loading="props.loading"
            @click="handleSubmit"
          ></up-button>
        </view>
      </view>
    </view>
  </view>
</template>

<style lang="scss" scoped>
/* 仅存放无法通过 Tailwind 实现的复杂样式或第三方样式覆盖 */
</style>
```

### 2.2 Tailwind CSS 在 uni-app 中的使用要点
- **布局优先**: 优先使用 Tailwind 的 Utility Classes 进行布局（如 `flex`, `grid`, `p-4`, `m-2`）。
- **rpx 适配**: 确保 `tailwind.config.js` 已配置单位转换，使得 `p-4` 等类名能正确转换为 `rpx` 或相应的移动端单位。
- **原子化**: 减少 `<style>` 块中的代码量，提升样式复用性。

---

## 3. 详细指南

- [Vue3 组合式 API 最佳实践](./references/vue3-best-practices.md)
- [uView Plus & Tailwind 协作指南](./references/uview-tailwind-guide.md)
- [小程序性能优化指南](./references/performance.md)
