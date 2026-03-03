# Vue3 组合式 API 最佳实践 (uni-app)

## 1. 组件通讯

### Props & Emits
- **类型声明**: 统一使用 TypeScript 接口。
- **默认值**: 使用 `withDefaults`。

### Provide / Inject
- 跨层级通讯优先考虑，而非全局 Pinia。

## 2. 状态管理 (Pinia)

- **命名规范**: `use[StoreName]Store`。
- **模块化**: 不同业务逻辑拆分 store。

## 3. 工具类与 Hook (Composables)

- 封装常用功能（如扫码、位置、文件上传）为 `useScanCode`, `useLocation` 等。
- 保证逻辑复用性。

## 4. 响应式系统

- **ref vs reactive**:
  - `ref` 用于基本类型、数组、简单对象。
  - `reactive` 用于大型对象、表单数据、复杂状态。
- **解构响应式对象**: 必须使用 `toRefs`。
