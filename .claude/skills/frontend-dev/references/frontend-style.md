# 前端开发与 UI 风格规范（完整版）

作者：zjc
版本：v2.0
日期：2024-01-20
状态：正式版

> **部署位置**: `~/.claude/skills/frontend-dev/references/frontend-style.md`
> **作用范围**: 前端/界面相关代码
> **参考来源**: 阿里前端规范、腾讯前端规范、Vue 官方风格指南、Element Plus 最佳实践

---

## 目录

1. [适用原则](#1-适用原则)
2. [代码注释规范](#2-代码注释规范)
3. [ESLint 检查流程](#3-eslint-检查流程)
4. [变动记录规范](#4-变动记录规范)
5. [UI 视觉风格](#5-ui-视觉风格)
6. [技术栈默认选择](#6-技术栈默认选择)
7. [Vue 编码规范](#7-vue-编码规范)
8. [状态管理（Pinia）](#8-状态管理pinia)
9. [API 请求规范](#9-api-请求规范)
10. [交互状态规范](#10-交互状态规范)
11. [TypeScript 规范](#11-typescript-规范)
12. [目录结构](#12-目录结构)
13. [代码检查工具](#13-代码检查工具)
14. [性能优化](#14-性能优化)
15. [大厂编码规范细节](#15-大厂编码规范细节)
16. [Git 提交规范](#16-git-提交规范)

---

## 1. 适用原则

- **仅在涉及前端/界面开发时遵循**本规则
- **默认使用框架/组件库的脚手架风格**: 不做"AI 设计稿"，不做大改主题色
- **技术栈优先级**: Vue > React；默认使用 TypeScript

---

## 2. 代码注释规范

### 2.1 注释原则

| 原则 | 说明 |
|------|------|
| 必须性 | 所有函数、组件、复杂逻辑必须有注释 |
| 语言 | 使用简体中文注释 |
| 位置 | 注释位于代码上方或右侧，保持对齐 |
| 更新 | 代码修改时同步更新注释 |

### 2.2 文件头注释模板

```typescript
/**
 * @file 用户管理页面
 * @description 用户列表展示、搜索、新增、编辑、删除功能
 * @author zjc
 */
```

### 2.3 函数注释模板

```typescript
/**
 * 获取用户列表数据
 * @description 根据筛选条件分页查询用户列表，支持关键词搜索
 * @param {Object} params - 查询参数对象
 * @param {number} params.page - 当前页码，从1开始
 * @param {number} params.pageSize - 每页条数，默认10
 * @param {string} params.keyword - 搜索关键词，可选
 * @param {string} params.status - 用户状态筛选，可选
 * @returns {Promise<PageResult<User>>} 用户列表分页数据
 * @throws {Error} 当网络请求失败时抛出异常
 * @example
 * // 基础用法
 * const result = await getUserList({ page: 1, pageSize: 10 })
 * console.log(result.total) // 总条数
 * 
 * // 带搜索条件
 * const result = await getUserList({ 
 *   page: 1, 
 *   pageSize: 10, 
 *   keyword: '张三' 
 * })
 */
async function getUserList(params: QueryParams): Promise<PageResult<User>> {
  // 函数实现...
}
```

### 2.4 组件注释模板

```vue
<script setup lang="ts">
/**
 * UserCard 组件
 * @description 用户信息卡片组件，用于展示用户基本信息和操作按钮
 * @author zjc
 * @date 2024-01-20
 * 
 * @props {number} userId - 用户ID，必填
 * @props {boolean} editable - 是否可编辑，默认false
 * @props {boolean} showActions - 是否显示操作按钮，默认true
 * 
 * @emits update - 用户信息更新时触发，参数为更新后的用户对象
 * @emits delete - 删除用户时触发，参数为用户ID
 * @emits cancel - 取消编辑时触发
 * 
 * @example
 * <UserCard 
 *   :user-id="123" 
 *   :editable="true" 
 *   @update="handleUpdate" 
 *   @delete="handleDelete" 
 * />
 */
</script>
```

### 2.5 复杂逻辑注释

```typescript
// ========== 数据处理逻辑 ==========
// 处理流程：
// 1. 过滤掉无效数据（status为null或undefined）
// 2. 按创建时间倒序排列
// 3. 取前10条作为推荐数据
// 4. 补充用户头像信息
const recommendedList = computed(() => {
  return list.value
    .filter(item => item.status != null)  // 过滤无效状态
    .sort((a, b) => b.createdAt.localeCompare(a.createdAt))  // 时间倒序
    .slice(0, 10)  // 取前10条
    .map(item => ({
      ...item,
      avatar: item.avatar || defaultAvatar  // 补充默认头像
    }))
})

// ========== 权限校验逻辑 ==========
// 权限层级说明：
// - admin: 管理员，拥有所有权限
// - editor: 编辑，可编辑、可查看
// - viewer: 访客，仅可查看
const canEdit = computed(() => {
  const role = userStore.role
  if (role === 'admin') return true   // 管理员全权限
  if (role === 'editor') return true  // 编辑有写权限
  return false  // 其他角色无写权限
})
```

### 2.6 变量注释

```typescript
// ========== 响应式状态 ==========

// 用户列表数据
const userList = ref<User[]>([])

// 当前选中的用户ID，用于编辑和删除操作
const selectedUserId = ref<number | null>(null)

// 加载状态：true-加载中，false-加载完成
const loading = ref(false)

// 表单提交状态：防止重复提交
const submitting = ref(false)

// ========== 表单配置 ==========

// 表单验证规则配置
const formRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}
```

### 2.7 TODO 注释规范

```typescript
// TODO: 待实现分页功能 - @zjc 2024-01-15
// FIXME: 修复大列表渲染性能问题 - @zjc 2024-01-16
// HACK: 临时解决方案，后续需要优化 - @zjc 2024-01-17
// NOTE: 此处逻辑较复杂，修改时需谨慎 - @zjc 2024-01-18
// XXX: 此处代码有潜在问题，需要重构 - @zjc 2024-01-19
```

---

## 3. ESLint 检查流程

### 3.1 检查时机

| 时机 | 操作 | 说明 |
|------|------|------|
| 代码编写完成 | 立即运行 `npm run lint` | 发现问题及时修复 |
| 提交代码前 | 运行 `npm run lint:fix` | 自动修复可修复的问题 |
| CI/CD 流水线 | 自动运行 lint 检查 | 阻止不合规代码合并 |

### 3.2 执行命令

```bash
# 检查所有文件
npm run lint

# 检查并自动修复
npm run lint:fix

# 检查指定文件
npx eslint src/views/User.vue

# 检查指定目录
npx eslint src/components/

# 检查并输出详细报告
npx eslint src/ --format html --output-file eslint-report.html
```

### 3.3 ESLint 配置规范

```javascript
// .eslintrc.cjs
module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended',
    'plugin:@typescript-eslint/recommended',
    '@vue/eslint-config-typescript',
    '@vue/eslint-config-prettier/skip'
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  rules: {
    // ========== Vue 规则 ==========
    'vue/multi-word-component-names': 'off',
    'vue/no-v-html': 'warn',
    'vue/require-default-prop': 'warn',
    'vue/require-explicit-emits': 'error',
    'vue/component-definition-name-casing': ['error', 'PascalCase'],
    'vue/component-name-in-template-casing': ['error', 'PascalCase'],
    'vue/custom-event-name-casing': ['error', 'kebab-case'],
    
    // ========== TypeScript 规则 ==========
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/no-unused-vars': ['error', { 
      argsIgnorePattern: '^_',
      varsIgnorePattern: '^_' 
    }],
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    
    // ========== 通用规则 ==========
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'prefer-const': 'error',
    'no-var': 'error',
    'eqeqeq': ['error', 'always'],
    'curly': ['error', 'multi-line'],
    'no-multiple-empty-lines': ['error', { max: 2 }],
    'no-trailing-spaces': 'error',
    'comma-dangle': ['error', 'never'],
    'semi': ['error', 'never'],
    'quotes': ['error', 'single']
  }
}
```

### 3.4 常见问题修复指南

| 问题 | 修复方案 | 示例 |
|------|---------|------|
| 未使用的变量 | 删除或添加 `_` 前缀 | `const _unused = 1` |
| 缺少 prop 默认值 | 使用 `withDefaults` | `withDefaults(defineProps<{}>(), {})` |
| 使用 `any` 类型 | 定义具体类型 | `interface User { id: number }` |
| 使用 `var` | 改为 `const` 或 `let` | `const name = 'test'` |
| 缺少 emit 声明 | 在 `defineEmits` 中声明 | `defineEmits<{...}>()` |
| 使用 `==` | 改为 `===` | `if (a === b)` |
| 缺少分号 | 根据配置添加或删除 | 配置为不需要分号 |

---

## 4. 变动记录规范

### 4.1 变动记录文件

所有代码变动必须记录在项目根目录的 `CHANGELOG.md` 文件中。

### 4.2 记录格式模板

```markdown
# 变动记录 (CHANGELOG)

本文档记录项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)

---

## [Unreleased]

### 新增 (Added)
- 待发布的新功能

---

## [1.2.0] - 2024-01-20

### 新增 (Added)
- 新增用户管理模块，支持增删改查功能
- 新增权限控制中间件
- 新增操作日志记录功能

### 修改 (Changed)
- 优化列表页加载性能，添加虚拟滚动
- 重构 API 请求封装，统一错误处理
- 优化表格组件，支持列配置持久化

### 修复 (Fixed)
- 修复表单验证规则失效问题 (#123)
- 修复分页组件页码显示错误 (#124)
- 修复深色模式下样式异常问题

### 删除 (Removed)
- 移除废弃的旧版登录组件
- 移除未使用的工具函数

### 安全 (Security)
- 修复 XSS 漏洞，对用户输入进行转义

---

## [1.1.0] - 2024-01-15

### 详细记录

#### 2024-01-20 用户管理模块
- **文件**: `src/views/user/index.vue`
- **变更**: 新增用户列表页面
- **影响范围**: 用户管理模块
- **测试**: 已通过功能测试
- **审核人**: zjc

#### 2024-01-19 API封装优化
- **文件**: `src/utils/request.ts`
- **变更**: 添加请求重试机制
- **影响范围**: 所有 API 请求
- **测试**: 需要进行回归测试
- **审核人**: zjc

#### 2024-01-18 表格性能优化
- **文件**: `src/components/Table/index.vue`
- **变更**: 添加虚拟滚动支持
- **影响范围**: 所有使用表格的页面
- **测试**: 已通过性能测试
- **审核人**: zjc
```

### 4.3 记录时机和要求

| 场景 | 记录要求 | 详细程度 |
|------|---------|---------|
| 新功能开发 | 记录新增内容和影响范围 | 详细 |
| Bug 修复 | 记录问题描述和修复方案 | 详细 |
| 代码重构 | 记录重构原因和影响范围 | 详细 |
| 性能优化 | 记录优化前后对比数据 | 详细 |
| 配置变更 | 记录变更原因和影响 | 简要 |
| 样式调整 | 记录调整内容 | 简要 |

---

## 5. UI 视觉风格

### 5.1 严格禁止（常见 AI 风格）

- ❌ 蓝紫色霓虹渐变背景、发光描边、玻璃拟态（glassmorphism）
- ❌ 大面积渐变、过多装饰性几何图形、无意义的动效堆叠
- ❌ 随机生成的"科技感"插画/图标，或多套图标混用
- ❌ UI 文案中使用 emoji（除非产品明确要求）
- ❌ 赛博风、暗黑科技风、AI 风格 UI

### 5.2 后台/管理系统（默认风格）

**目标**: "像一个成熟企业后台"，而不是宣传页

| 要素 | 要求 |
|------|------|
| 主题 | 使用组件库默认主题 + 默认布局 |
| 配色 | 黑白灰为主 + 1 个主色点缀，避免渐变 |
| 信息密度 | 适中，表格、筛选、分页、表单用标准组件 |
| 动效 | 克制，仅保留必要的交互反馈（hover/focus/loading） |

**可选风格**（保持一致，不要混搭）：
- Element Plus 默认风格（推荐）
- Ant Design Vue 风格
- Naive UI 风格

### 5.3 前台宣传/官网（如需要）

**目标**: "简约、大气、留白足、排版高级"

- ✅ 大留白 + 清晰栅格 + 强排版层级
- ✅ 颜色克制: 白/浅灰背景 + 深色文字 + 少量强调色
- ✅ 轻量动效: 小范围的渐显/滚动过渡即可

### 5.4 不确定时先问

如果需求不明确，必须先问清楚：
1. 这是 **后台管理** 还是 **前台宣传**？
2. 期望风格是 **默认脚手架/企业后台/Apple 官网** 哪一种？
3. 是否已有品牌色/组件库/参考站点/设计稿？

---

## 6. 技术栈默认选择

### 6.1 Vue 技术栈（首选）

| 层级 | 选择 |
|------|------|
| 框架 | Vue 3 + TypeScript |
| 构建 | Vite |
| 路由 | Vue Router 4 |
| 状态管理 | Pinia |
| UI 组件库 | Element Plus |
| HTTP | Axios |
| 工具库 | VueUse |

### 6.2 React 技术栈（备选）

| 层级 | 选择 |
|------|------|
| 框架 | React 18 + TypeScript |
| 构建 | Vite |
| 路由 | React Router 6 |
| 状态管理 | Zustand |
| UI 组件库 | Ant Design |
| 数据请求 | TanStack Query |

---

## 7. Vue 编码规范

### 7.1 组件基础

**必须使用 Composition API + `<script setup>`**：

```vue
<script setup lang="ts">
/**
 * UserCard 组件
 * @description 用户信息卡片组件
 */
import { ref, computed, onMounted } from 'vue'
import type { User } from '@/types'

// ========== Props 定义 ==========
const props = defineProps<{
  userId: number
  title?: string
}>()

// ========== Emits 定义 ==========
const emit = defineEmits<{
  (e: 'update', value: string): void
  (e: 'delete', id: number): void
}>()

// ========== 响应式状态 ==========
const loading = ref(false)
const user = ref<User | null>(null)

// ========== 计算属性 ==========
const displayName = computed(() => user.value?.name ?? '未知用户')

// ========== 生命周期 ==========
onMounted(async () => {
  await fetchUser()
})

// ========== 方法 ==========
async function fetchUser() {
  loading.value = true
  try {
    user.value = await api.getUser(props.userId)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="user-card">
    <h3>{{ displayName }}</h3>
    <el-button @click="emit('delete', props.userId)">删除</el-button>
  </div>
</template>

<style scoped>
.user-card {
  padding: 16px;
}
</style>
```

### 7.2 命名约定

| 类型 | 约定 | 示例 |
|------|------|------|
| 组件文件 | PascalCase.vue | `UserCard.vue` |
| 组件目录 | 可复用放 `components/`，页面放 `views/` | |
| Composables | useXxx.ts | `useAuth.ts` |
| Store | useXxxStore.ts | `useUserStore.ts` |
| 类型文件 | xxx.d.ts 或 types/ 目录 | `user.d.ts` |
| 常量 | UPPER_SNAKE_CASE | `API_BASE_URL` |
| 变量/函数 | camelCase | `getUserInfo` |
| CSS 类名 | kebab-case | `user-card` |
| 私有变量 | _前缀 | `_privateData` |

### 7.3 组件组织顺序

```vue
<script setup lang="ts">
// 1. 导入（按顺序：vue → 第三方 → 项目内部）
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

// 2. Props & Emits
const props = defineProps<{...}>()
const emit = defineEmits<{...}>()

// 3. Store & Composables
const userStore = useUserStore()

// 4. 响应式状态
const loading = ref(false)

// 5. 计算属性
const isAdmin = computed(() => userStore.role === 'admin')

// 6. 生命周期钩子
onMounted(() => {...})

// 7. 方法
function handleSubmit() {...}
</script>
```

### 7.4 Props 规范

```typescript
// ✅ 好：使用 TypeScript 类型定义
const props = defineProps<{
  id: number
  title: string
  disabled?: boolean
}>()

// ✅ 好：需要默认值时使用 withDefaults
const props = withDefaults(defineProps<{
  title: string
  size?: 'small' | 'medium' | 'large'
}>(), {
  size: 'medium'
})

// ❌ 差：使用运行时声明（除非需要复杂验证）
const props = defineProps({
  id: {
    type: Number,
    required: true
  }
})
```

### 7.5 样式规范

```vue
<!-- ✅ 好：使用 scoped 防止样式污染 -->
<style scoped>
.container {
  padding: 16px;
}
</style>

<!-- ✅ 好：需要穿透组件库样式时 -->
<style scoped>
.container :deep(.el-input__inner) {
  border-radius: 8px;
}
</style>

<!-- ❌ 差：全局样式（除非确实需要） -->
<style>
.container {
  padding: 16px;
}
</style>
```

---

## 8. 状态管理（Pinia）

### 8.1 Store 定义

```typescript
/**
 * 用户状态管理
 * @description 管理用户登录状态、用户信息、权限等
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'

export const useUserStore = defineStore('user', () => {
  // ========== State ==========
  
  /** 当前登录用户信息 */
  const user = ref<User | null>(null)
  
  /** 用户令牌 */
  const token = ref<string>('')

  // ========== Getters ==========
  
  /** 是否已登录 */
  const isLoggedIn = computed(() => !!token.value)
  
  /** 用户名 */
  const userName = computed(() => user.value?.name ?? '')
  
  /** 用户角色 */
  const userRole = computed(() => user.value?.role ?? 'guest')

  // ========== Actions ==========
  
  /**
   * 用户登录
   * @param username 用户名
   * @param password 密码
   */
  async function login(username: string, password: string) {
    const res = await api.login(username, password)
    token.value = res.token
    user.value = res.user
  }

  /**
   * 用户登出
   */
  function logout() {
    token.value = ''
    user.value = null
  }

  return {
    user,
    token,
    isLoggedIn,
    userName,
    userRole,
    login,
    logout
  }
})
```

### 8.2 在组件中使用

```vue
<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'

const userStore = useUserStore()

// ✅ 好：使用 storeToRefs 保持响应性
const { user, isLoggedIn } = storeToRefs(userStore)

// ✅ 好：actions 直接解构
const { login, logout } = userStore
</script>
```

---

## 9. API 请求规范

### 9.1 API 模块组织

```typescript
// api/index.ts - 统一导出
export * from './user'
export * from './site'

// api/user.ts - 用户相关 API
import request from '@/utils/request'
import type { User, LoginParams, LoginResult } from '@/types'

/**
 * 用户登录
 * @param params 登录参数
 * @returns 登录结果
 */
export function login(params: LoginParams): Promise<LoginResult> {
  return request.post('/api/v1/login', params)
}

/**
 * 获取用户信息
 * @returns 用户信息
 */
export function getUserInfo(): Promise<User> {
  return request.get('/api/v1/user/info')
}

/**
 * 更新用户信息
 * @param id 用户ID
 * @param data 更新数据
 * @returns 更新后的用户信息
 */
export function updateUser(id: number, data: Partial<User>): Promise<User> {
  return request.put(`/api/v1/users/${id}`, data)
}
```

### 9.2 请求封装

```typescript
/**
 * Axios 请求封装
 * @description 统一处理请求拦截、响应拦截、错误处理
 */
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(config => {
  const userStore = useUserStore()
  if (userStore.token) {
    config.headers.Authorization = `Bearer ${userStore.token}`
  }
  return config
})

// 响应拦截器
request.interceptors.response.use(
  response => {
    const { code, message, data } = response.data
    if (code === 0) {
      return data
    }
    ElMessage.error(message || '请求失败')
    return Promise.reject(new Error(message))
  },
  error => {
    ElMessage.error(error.message || '网络错误')
    return Promise.reject(error)
  }
)

export default request
```

---

## 10. 交互状态规范

### 10.1 必须处理的状态

| 状态 | 说明 | 示例 |
|------|------|------|
| loading | 加载中 | 骨架屏、加载动画 |
| empty | 空数据 | "暂无数据" 提示 |
| error | 错误 | 错误信息 + 重试按钮 |
| disabled | 禁用 | 按钮置灰 |
| submitting | 提交中 | 按钮 loading + 防重复点击 |

### 10.2 示例实现

```vue
<template>
  <div class="list-container">
    <!-- 加载状态 -->
    <el-skeleton v-if="loading" :rows="5" animated />

    <!-- 错误状态 -->
    <el-result v-else-if="error" icon="error" :title="error">
      <template #extra>
        <el-button @click="fetchData">重试</el-button>
      </template>
    </el-result>

    <!-- 空状态 -->
    <el-empty v-else-if="list.length === 0" description="暂无数据" />

    <!-- 正常内容 -->
    <template v-else>
      <div v-for="item in list" :key="item.id">
        {{ item.name }}
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
const loading = ref(false)
const error = ref('')
const list = ref<Item[]>([])

async function fetchData() {
  loading.value = true
  error.value = ''
  try {
    list.value = await api.getList()
  } catch (e) {
    error.value = e.message || '加载失败'
  } finally {
    loading.value = false
  }
}
</script>
```

---

## 11. TypeScript 规范

### 11.1 基本要求

- 默认使用 TypeScript，禁止大范围 `any`
- 必须为 API 响应定义类型
- 组件 Props 和 Emits 必须有类型定义

### 11.2 类型定义位置

```
src/
├── types/
│   ├── index.ts        # 统一导出
│   ├── user.ts         # 用户相关类型
│   ├── site.ts         # 站点相关类型
│   └── api.ts          # API 通用类型
```

### 11.3 类型定义示例

```typescript
/**
 * 用户信息类型
 */
export interface User {
  /** 用户ID */
  id: number
  /** 用户名 */
  username: string
  /** 邮箱 */
  email: string
  /** 用户角色 */
  role: 'admin' | 'editor' | 'viewer'
  /** 创建时间 */
  createdAt: string
  /** 更新时间 */
  updatedAt: string
}

/**
 * 登录参数类型
 */
export interface LoginParams {
  username: string
  password: string
}

/**
 * 登录结果类型
 */
export interface LoginResult {
  token: string
  user: User
}

/**
 * API 通用响应类型
 */
export interface ApiResponse<T = unknown> {
  /** 状态码 */
  code: number
  /** 提示信息 */
  message: string
  /** 响应数据 */
  data: T
}

/**
 * 分页参数类型
 */
export interface PageParams {
  /** 当前页码 */
  page: number
  /** 每页条数 */
  pageSize: number
}

/**
 * 分页结果类型
 */
export interface PageResult<T> {
  /** 数据列表 */
  list: T[]
  /** 总条数 */
  total: number
}
```

---

## 12. 目录结构

```
web/
├── src/
│   ├── api/                 # API 请求模块
│   │   ├── index.ts
│   │   ├── user.ts
│   │   └── site.ts
│   ├── assets/              # 静态资源
│   │   ├── images/
│   │   └── styles/
│   ├── components/          # 通用组件
│   │   ├── common/         # 基础通用组件
│   │   └── business/       # 业务通用组件
│   ├── composables/         # 组合式函数
│   │   ├── useAuth.ts
│   │   └── useTable.ts
│   ├── layouts/             # 布局组件
│   │   └── DefaultLayout.vue
│   ├── router/              # 路由配置
│   │   └── index.ts
│   ├── stores/              # Pinia stores
│   │   ├── index.ts
│   │   └── user.ts
│   ├── types/               # TypeScript 类型
│   │   └── index.ts
│   ├── utils/               # 工具函数
│   │   ├── request.ts
│   │   └── format.ts
│   ├── views/               # 页面组件
│   │   ├── home/
│   │   └── user/
│   ├── App.vue
│   └── main.ts
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

---

## 13. 代码检查工具

### 13.1 推荐配置

```bash
# 安装依赖
npm install -D eslint prettier eslint-plugin-vue @typescript-eslint/parser
```

### 13.2 常用命令

```bash
npm run lint          # 代码检查
npm run lint:fix      # 自动修复
npm run format        # 格式化
npm run type-check    # 类型检查
```

---

## 14. 性能优化

### 14.1 核心原则

| 原则 | 说明 |
|------|------|
| **先正确后优化** | 先确保功能正确，再考虑性能 |
| **先测量后优化** | 用 DevTools 定位瓶颈 |
| **用户感知优先** | 优化用户能感知到的性能问题 |

### 14.2 组件渲染优化

```vue
<script setup lang="ts">
import { computed, shallowRef } from 'vue'

// ✅ 使用 computed 缓存计算结果
const filteredList = computed(() =>
  list.value.filter(item => item.active)
)

// ✅ 大列表使用 shallowRef
const largeList = shallowRef<Item[]>([])

// ✅ 使用 v-once 标记静态内容
// <div v-once>{{ staticContent }}</div>

// ✅ 使用 v-memo 缓存列表项（Vue 3.2+）
// <div v-for="item in list" :key="item.id" v-memo="[item.id, item.selected]">
</script>
```

### 14.3 列表渲染优化

```vue
<template>
  <!-- ✅ 大列表使用虚拟滚动 -->
  <el-table-v2
    :columns="columns"
    :data="data"
    :height="400"
    :row-height="50"
  />
</template>
```

### 14.4 懒加载

```typescript
// ✅ 路由懒加载
const routes = [
  {
    path: '/dashboard',
    component: () => import('@/views/Dashboard.vue')
  }
]

// ✅ 组件懒加载
const HeavyComponent = defineAsyncComponent(() =>
  import('@/components/HeavyComponent.vue')
)
```

---

## 15. 大厂编码规范细节

### 15.1 代码行数限制

| 类型 | 限制 | 说明 |
|------|------|------|
| 单个 Vue 文件 | < 500 行 | 超出需拆分组件 |
| 单个函数 | < 50 行 | 超出需拆分逻辑 |
| 单个文件导入 | < 20 个 | 超出需考虑重构 |
| style 块 | < 20 行 | 超出抽到单独文件 |

### 15.2 错误处理规范

```typescript
// ✅ 正确：完整的错误处理
async function handleSubmit() {
  submitting.value = true
  try {
    const res = await api.saveUser(formData)
    if (res.code === 200) {
      ElMessage.success('保存成功')
      emit('success', res.data)
    } else {
      ElMessage.error(res.message || '保存失败')
    }
  } catch (error) {
    ElMessage.error('网络异常，请稍后重试')
    console.error('保存用户失败:', error)
  } finally {
    submitting.value = false
  }
}
```

### 15.3 异步处理规范

```typescript
// ✅ 正确：使用 async/await
async function fetchData() {
  loading.value = true
  try {
    const data = await api.getData()
    list.value = data
  } finally {
    loading.value = false
  }
}

// ✅ 正确：并行请求
async function fetchAllData() {
  const [users, roles, permissions] = await Promise.all([
    api.getUsers(),
    api.getRoles(),
    api.getPermissions()
  ])
  return { users, roles, permissions }
}
```

---

## 16. Git 提交规范

### 16.1 提交格式

```bash
<type>(<scope>): <subject>

<body>

<footer>
```

### 16.2 类型说明

| 类型 | 说明 | 示例 |
|------|------|------|
| feat | 新功能 | feat(user): 新增用户管理模块 |
| fix | 修复bug | fix(login): 修复登录验证失败问题 |
| docs | 文档变更 | docs: 更新README文档 |
| style | 代码格式 | style: 格式化代码 |
| refactor | 重构 | refactor(api): 重构请求封装 |
| perf | 性能优化 | perf(list): 优化列表渲染性能 |
| test | 增加测试 | test(user): 添加用户模块单元测试 |
| chore | 构建/工具 | chore: 更新依赖版本 |
| revert | 回滚 | revert: 回滚上一次提交 |

### 16.3 提交示例

```bash
feat(user): 新增用户管理模块

- 新增用户列表页面
- 新增用户增删改查功能
- 新增用户权限控制

Closes #123
```

---

## 规则溯源要求

当回复明确受到本规则约束时，在回复末尾声明：

```
> 📋 本回复遵循规则：`frontend-style.md` - [具体章节]
```

---

## 参考资料

- [Vue 3 官方文档](https://vuejs.org/)
- [Vue 风格指南](https://vuejs.org/style-guide/)
- [Element Plus](https://element-plus.org/)
- [Pinia 官方文档](https://pinia.vuejs.org/)
- [TypeScript 官方文档](https://www.typescriptlang.org/)
- [阿里前端规范](https://github.com/alibaba/f2e-spec)
- [腾讯前端规范](https://tgideas.qq.com/doc/index.html)
