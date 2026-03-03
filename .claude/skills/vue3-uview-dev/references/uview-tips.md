# uView Plus 组件库避坑指南 (uni-app)

## 1. 组件使用注意事项

### `up-input`
- **v-model**: 确保绑定的是 `ref` 或 `reactive` 属性。
- **border**: 小程序建议设为 `surround` 以符合视觉习惯。

### `up-button`
- **loading**: 请求数据时应显示加载状态。
- **customStyle**: 设置高度、圆角等优先使用此属性。

### `up-popup`
- **show**: 控制显示隐藏，需在父组件中管理。
- **mode**: `top`, `bottom`, `left`, `right`, `center` 的适配方案。

## 2. 布局与样式

- **Flex 布局**: 统一使用 Flex 布局。
- **rpx 单位**: 所有布局、间距、字体大小统一使用 `rpx`。
- **颜色系统**: 使用 uView Plus 预设的颜色类名或变量。

## 3. 全局配置

- 确保 `main.ts` 已正确引入 `uview-plus`：
```typescript
import uviewPlus from 'uview-plus'
app.use(uviewPlus)
```
- 配置全局属性（如 `navbar` 默认值）。
