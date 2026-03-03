---
name: frontend-dev
description: 大厂级前端开发规范体系，包含代码注释规范、ESLint检查流程、变动记录机制、Vue 3 编码规范、UI 风格约束、TypeScript 规范等。适用于所有前端代码编写、修改、审查场景。当用户要求编写或修改前端代码时，必须使用此skill。
version: v4.0
paths:
  - "**/*.vue"
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/*.ts"
  - "**/*.js"
  - "**/*.css"
  - "**/*.scss"
  - "**/*.less"
  - "**/package.json"
  - "**/vite.config.*"
---

# 大厂级前端开发规范体系

> 版本: v4.0 | 参考来源: 阿里前端规范、腾讯前端规范、Vue 官方风格指南、Element Plus 最佳实践

---

## 核心工作流程（必须遵循）

```
┌─────────────────────────────────────────────────────────────────┐
│  1. 编写代码 → 2. 添加注释 → 3. ESLint检查 → 4. 记录变动 → 5. 提交  │
└─────────────────────────────────────────────────────────────────┘
```

**每次代码编写完成后必须执行**：
1. ✅ 添加详细的中文注释
2. ✅ 运行 ESLint 检查并修复
3. ✅ 在 `CHANGELOG.md` 中记录变动

---

## 一、代码注释规范

### 1.1 注释原则

| 原则 | 说明 |
|------|------|
| 必须性 | 所有函数、组件、复杂逻辑必须有注释 |
| 语言 | 使用简体中文注释 |
| 位置 | 注释位于代码上方或右侧，保持对齐 |
| 更新 | 代码修改时同步更新注释 |

### 1.2 文件头注释

```typescript
/**
 * @file 文件名称
 * @description 文件功能描述
 * @author 作者名
 * @date 创建日期
 * @lastModified 最后修改日期
 * @modifiedBy 最后修改人
 */
```

### 1.3 函数注释

```typescript
/**
 * 获取用户列表数据
 * @description 根据筛选条件分页查询用户列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 当前页码
 * @param {number} params.pageSize - 每页条数
 * @param {string} params.keyword - 搜索关键词
 * @returns {Promise<PageResult<User>>} 用户列表分页数据
 * @throws {Error} 当网络请求失败时抛出异常
 * @example
 * const result = await getUserList({ page: 1, pageSize: 10 })
 * console.log(result.total) // 总条数
 */
async function getUserList(params: QueryParams): Promise<PageResult<User>> {
  // 函数实现...
}
```

### 1.4 组件注释

```vue
<script setup lang="ts">
/**
 * UserCard 组件
 * @description 用户信息卡片组件，用于展示用户基本信息和操作按钮
 * @props {number} userId - 用户ID，必填
 * @props {boolean} editable - 是否可编辑，默认false
 * @emits update - 用户信息更新时触发，参数为更新后的用户对象
 * @emits delete - 删除用户时触发，参数为用户ID
 * @example
 * <UserCard :user-id="123" :editable="true" @update="handleUpdate" />
 */
</script>
```

### 1.5 复杂逻辑注释

```typescript
// ========== 数据处理逻辑 ==========
// 1. 过滤掉无效数据（status为null或undefined）
// 2. 按创建时间倒序排列
// 3. 取前10条作为推荐数据
const recommendedList = computed(() => {
  return list.value
    .filter(item => item.status != null)  // 过滤无效状态
    .sort((a, b) => b.createdAt.localeCompare(a.createdAt))  // 时间倒序
    .slice(0, 10)  // 取前10条
})

// ========== 权限校验逻辑 ==========
// 管理员：拥有所有权限
// 编辑：可编辑、可查看
// 访客：仅可查看
const canEdit = computed(() => {
  const role = userStore.role
  if (role === 'admin') return true   // 管理员全权限
  if (role === 'editor') return true  // 编辑有写权限
  return false  // 其他角色无写权限
})
```

### 1.6 变量注释

```typescript
// 用户列表数据
const userList = ref<User[]>([])

// 当前选中的用户ID，用于编辑和删除操作
const selectedUserId = ref<number | null>(null)

// 加载状态：true-加载中，false-加载完成
const loading = ref(false)

// 表单验证规则配置
const formRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ]
}
```

### 1.7 TODO 注释

```typescript
// TODO: 待实现分页功能 - @zjc 2024-01-15
// FIXME: 修复大列表渲染性能问题 - @zjc 2024-01-16
// HACK: 临时解决方案，后续需要优化 - @zjc 2024-01-17
// NOTE: 此处逻辑较复杂，修改时需谨慎 - @zjc 2024-01-18
```

---

## 二、ESLint 检查流程

### 2.1 检查时机

| 时机 | 操作 |
|------|------|
| 代码编写完成 | 立即运行 `npm run lint` |
| 提交代码前 | 运行 `npm run lint:fix` 自动修复 |
| CI/CD 流水线 | 自动运行 lint 检查 |

### 2.2 执行命令

```bash
# 检查所有文件
npm run lint

# 检查并自动修复
npm run lint:fix

# 检查指定文件
npx eslint src/views/User.vue

# 检查指定目录
npx eslint src/components/
```

### 2.3 ESLint 配置规范

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
  rules: {
    // Vue 规则
    'vue/multi-word-component-names': 'off',
    'vue/no-v-html': 'warn',
    'vue/require-default-prop': 'warn',
    'vue/require-explicit-emits': 'error',
    
    // TypeScript 规则
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    
    // 通用规则
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'prefer-const': 'error',
    'no-var': 'error'
  }
}
```

### 2.4 常见问题修复

| 问题 | 修复方案 |
|------|---------|
| 未使用的变量 | 删除或添加 `_` 前缀 |
| 缺少 prop 默认值 | 使用 `withDefaults` |
| 使用 `any` 类型 | 定义具体类型 |
| 使用 `var` | 改为 `const` 或 `let` |
| 缺少 emit 声明 | 在 `defineEmits` 中声明 |

---

## 三、变动记录规范

### 3.1 变动记录文件

所有代码变动必须记录在项目根目录的 `CHANGELOG.md` 文件中。

### 3.2 记录格式

```markdown
# 变动记录 (CHANGELOG)

## [日期] - 版本号

### 新增 (Added)
- 新增用户管理模块，支持增删改查功能
- 新增权限控制中间件

### 修改 (Changed)
- 优化列表页加载性能，添加虚拟滚动
- 重构 API 请求封装，统一错误处理

### 修复 (Fixed)
- 修复表单验证规则失效问题
- 修复分页组件页码显示错误

### 删除 (Removed)
- 移除废弃的旧版登录组件

### 详细记录

#### 2024-01-20 用户管理模块
- **文件**: `src/views/user/index.vue`
- **变更**: 新增用户列表页面
- **影响范围**: 用户管理模块
- **测试**: 已通过功能测试

#### 2024-01-19 API封装优化
- **文件**: `src/utils/request.ts`
- **变更**: 添加请求重试机制
- **影响范围**: 所有 API 请求
- **测试**: 需要进行回归测试
```

### 3.3 记录时机

| 场景 | 记录要求 |
|------|---------|
| 新功能开发 | 记录新增内容和影响范围 |
| Bug 修复 | 记录问题描述和修复方案 |
| 代码重构 | 记录重构原因和影响范围 |
| 性能优化 | 记录优化前后对比数据 |
| 配置变更 | 记录变更原因和影响 |

---

## 四、大厂编码规范细节

### 4.1 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件名 | PascalCase | `UserCard.vue` |
| 页面组件 | PascalCase + 目录 | `views/user/Index.vue` |
| Composables | useXxx | `useAuth.ts` |
| Store | useXxxStore | `useUserStore.ts` |
| 类型文件 | camelCase | `user.ts` |
| 常量 | UPPER_SNAKE_CASE | `API_BASE_URL` |
| 变量/函数 | camelCase | `getUserInfo` |
| CSS 类名 | kebab-case | `user-card` |
| 私有变量 | _前缀 | `_privateData` |

### 4.2 文件组织规范

```typescript
// Vue 组件内部顺序
<script setup lang="ts">
// 1. 导入语句（按顺序分组）
//    - Vue 核心
//    - 第三方库
//    - 组件
//    - 工具函数
//    - 类型定义
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import UserCard from '@/components/UserCard.vue'
import { formatDate } from '@/utils/format'
import type { User } from '@/types'

// 2. Props 定义
const props = defineProps<{
  userId: number
}>()

// 3. Emits 定义
const emit = defineEmits<{
  (e: 'update', user: User): void
}>()

// 4. 响应式状态
const loading = ref(false)
const user = ref<User | null>(null)

// 5. 计算属性
const displayName = computed(() => user.value?.name ?? '未知')

// 6. 方法
async function fetchUser() {
  // ...
}

// 7. 生命周期钩子
onMounted(() => {
  fetchUser()
})
</script>
```

### 4.3 代码行数限制

| 类型 | 限制 | 说明 |
|------|------|------|
| 单个 Vue 文件 | < 500 行 | 超出需拆分组件 |
| 单个函数 | < 50 行 | 超出需拆分逻辑 |
| 单个文件导入 | < 20 个 | 超出需考虑重构 |
| style 块 | < 20 行 | 超出抽到单独文件 |

### 4.4 错误处理规范

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
      // 业务错误：显示后端返回的错误信息
      ElMessage.error(res.message || '保存失败')
    }
  } catch (error) {
    // 网络错误：显示友好提示
    ElMessage.error('网络异常，请稍后重试')
    console.error('保存用户失败:', error)
  } finally {
    submitting.value = false
  }
}

// ❌ 错误：静默忽略错误
async function handleSubmit() {
  const res = await api.saveUser(formData)
  if (res.code === 200) {
    emit('success', res.data)
  }
}
```

### 4.5 异步处理规范

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

// ❌ 错误：回调地狱
function fetchData() {
  api.getData().then(res => {
    api.getDetail(res.id).then(detail => {
      api.getExtra(detail.code).then(extra => {
        // 嵌套太深
      })
    })
  })
}
```

### 4.6 类型定义规范

```typescript
// ✅ 正确：完整的类型定义
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

// ✅ 正确：API 响应类型
export interface ApiResponse<T> {
  /** 状态码：200-成功，其他-失败 */
  code: number
  /** 提示信息 */
  message: string
  /** 响应数据 */
  data: T
}

// ✅ 正确：分页参数类型
export interface PageParams {
  /** 当前页码，从1开始 */
  page: number
  /** 每页条数 */
  pageSize: number
  /** 搜索关键词 */
  keyword?: string
}

// ❌ 错误：使用 any
function processData(data: any) {
  return data.value
}
```

### 4.7 Git 提交规范

```bash
# 提交格式
<type>(<scope>): <subject>

<body>

<footer>

# 类型说明
feat:     新功能
fix:      修复bug
docs:     文档变更
style:    代码格式（不影响功能）
refactor: 重构（既不是新功能也不是bug修复）
perf:     性能优化
test:     增加测试
chore:    构建过程或辅助工具变动
revert:   回滚

# 示例
feat(user): 新增用户管理模块

- 新增用户列表页面
- 新增用户增删改查功能
- 新增用户权限控制

Closes #123
```

---

## 五、UI 风格约束

### 5.1 严格禁止（常见 AI 风格）

- ❌ 蓝紫色霓虹渐变、发光描边、玻璃拟态
- ❌ 大面积渐变、过多装饰性几何图形
- ❌ 赛博风、暗黑科技风、AI 风格 UI
- ❌ UI 文案中使用 emoji

### 5.2 后台系统（默认风格）

| 要素 | 要求 |
|------|------|
| 主题 | 使用组件库默认主题 |
| 配色 | 黑白灰为主 + 1 个主色点缀 |
| 动效 | 克制，仅保留必要交互反馈 |

---

## 六、交互状态处理

**必须处理的状态**: loading、empty、error、disabled、submitting

```vue
<template>
  <el-skeleton v-if="loading" :rows="5" animated />
  <el-result v-else-if="error" icon="error" :title="error">
    <template #extra>
      <el-button @click="fetchData">重试</el-button>
    </template>
  </el-result>
  <el-empty v-else-if="list.length === 0" description="暂无数据" />
  <template v-else>
    <!-- 正常内容 -->
  </template>
</template>
```

---

## 七、目录结构

```
src/
├── api/                 # API 请求
├── assets/
│   └── styles/          # 全局/共享样式
├── components/          # 通用组件
├── composables/         # 组合式函数
├── router/              # 路由配置
├── stores/              # Pinia stores
├── types/               # TypeScript 类型
├── utils/               # 工具函数
├── views/               # 页面组件
├── App.vue
└── main.ts
```

---

## 详细参考

完整规范见 `references/frontend-style.md`，包含：
- 完整 UI 风格约束
- Vue 3 编码规范详解
- Pinia 状态管理
- API 请求封装
- 性能优化详解

---

> 📋 本回复遵循：`frontend-dev` - [具体章节]
