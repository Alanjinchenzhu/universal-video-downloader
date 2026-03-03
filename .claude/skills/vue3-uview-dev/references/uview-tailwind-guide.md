# uView Plus & Tailwind CSS 协作指南

在 uni-app 开发中，uView Plus 提供组件功能，而 Tailwind CSS 则负责快速构建布局和细粒度样式。

## 1. 为什么结合使用？

- **uView Plus**: 解决复杂的交互组件（Picker, Calendar, Form, Navbar 等）。
- **Tailwind CSS**: 解决样式编写繁琐、命名困难的问题，提供强大的原子化能力。

## 2. 协作模式

### 2.1 容器与布局
外层容器、间距、对齐方式优先使用 Tailwind。
```vue
<view class="flex justify-between items-center p-4 bg-white border-b border-gray-100">
  <text class="text-lg font-bold">标题</text>
  <up-icon name="arrow-right"></up-icon>
</view>
```

### 2.2 组件样式覆盖
uView 组件通常带有 `customStyle` 属性，建议通过此属性配合内联对象，或在 Tailwind 中定义 `utility classes`。
> 注意：在小程序中，Tailwind 类名直接作用于自定义组件可能因作用域限制失效，建议包裹一层 `view`。

## 3. Tailwind 配置 (uni-app)

为了在 uni-app 中正常使用，建议使用 `weapp-tailwindcss` 插件。

### 示例配置 (`tailwind.config.js`)
```javascript
module.exports = {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      // 这里的配置应与 uni-app 的 rpx 转换逻辑对应
      spacing: {
        'safe-area': 'env(safe-area-inset-bottom)',
      }
    },
  },
  // 禁用某些在小程序中不支持的选择器
  corePlugins: {
    preflight: false,
  }
}
```

## 4. 最佳实践

1. **避免类名冲突**: uView 的类名通常以 `u-` 开头，Tailwind 默认不带前缀，一般不会冲突。
2. **状态控制**: 依然使用 Vue 的 `:class` 绑定。
   ```vue
   <view :class="['p-2', isActive ? 'bg-blue-500' : 'bg-gray-100']"></view>
   ```
3. **颜色一致性**: 尽量在 `tailwind.config.js` 中定义与 uView 主题色一致的颜色变量。
