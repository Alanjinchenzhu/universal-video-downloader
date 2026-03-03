# Vue3 + Vite + Ant Design + Tailwind + FastAPI 技术栈规则

版本: v1.1
作者: zjc
更新: 2026-03-04

---

## 技术栈概述

| 层级 | 技术 | 版本 | 用途 |
|------|------|------|------|
| 前端框架 | Vue 3 | ^3.4.x | 渐进式 JavaScript 框架 |
| 构建工具 | Vite | ^5.x | 下一代前端构建工具 |
| UI 组件库 | Ant Design Vue | ^4.x | 企业级 UI 组件库 |
| CSS 框架 | Tailwind CSS | ^3.4.x | 原子化 CSS 框架 |
| 后端框架 | FastAPI | ^0.110.x | 高性能 Python Web 框架 |
| 类型系统 | TypeScript | ^5.x | 静态类型检查 |

---

## 项目结构

```
project/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── api/             # API 接口封装
│   │   ├── assets/          # 静态资源
│   │   ├── components/      # 公共组件
│   │   ├── composables/     # 组合式函数
│   │   ├── layouts/         # 布局组件
│   │   ├── router/          # 路由配置
│   │   ├── stores/          # Pinia 状态管理
│   │   ├── styles/          # 全局样式
│   │   ├── utils/           # 工具函数
│   │   ├── views/           # 页面视图
│   │   ├── App.vue
│   │   └── main.ts
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── .env
├── backend/                  # 后端项目
│   ├── app/
│   │   ├── api/             # API 路由
│   │   │   └── v1/
│   │   ├── core/            # 核心配置
│   │   ├── db/              # 数据库模型
│   │   ├── models/          # Pydantic 模型
│   │   ├── schemas/         # 数据校验模型
│   │   ├── services/        # 业务逻辑
│   │   └── main.py
│   ├── tests/
│   ├── alembic/             # 数据库迁移
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 前端规范

### Vue 3 组合式 API

```typescript
<!-- 推荐：使用 <script setup> 语法 -->
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

// 类型定义
interface User {
  id: number
  name: string
  email: string
}

// 响应式数据
const userList = ref<User[]>([])
const loading = ref(false)
const searchKeyword = ref('')

// 计算属性
const filteredUsers = computed(() => {
  if (!searchKeyword.value) return userList.value
  return userList.value.filter(user => 
    user.name.includes(searchKeyword.value)
  )
})

// 方法
const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await getUserList()
    userList.value = res.data
  } finally {
    loading.value = false
  }
}

// 生命周期
onMounted(() => {
  fetchUsers()
})
</script>
```

### Ant Design Vue 使用规范

```typescript
<!-- 组件引入 -->
<script setup lang="ts">
import { Button, Table, Form, Input, message } from 'ant-design-vue'

// 消息提示
const handleSuccess = () => {
  message.success('操作成功')
}

const handleError = (err: Error) => {
  message.error(err.message || '操作失败')
}
</script>

<template>
  <!-- 表格使用 -->
  <a-table
    :columns="columns"
    :data-source="dataSource"
    :loading="loading"
    :pagination="pagination"
    row-key="id"
    @change="handleTableChange"
  />
  
  <!-- 表单使用 -->
  <a-form
    :model="formState"
    :rules="rules"
    @finish="handleSubmit"
  >
    <a-form-item label="用户名" name="username">
      <a-input v-model:value="formState.username" />
    </a-form-item>
    <a-form-item>
      <a-button type="primary" html-type="submit">提交</a-button>
    </a-form-item>
  </a-form>
</template>
```

### 类型定义规范

```typescript
// types/user.ts
export interface User {
  id: number
  username: string
  email: string
  avatar?: string
  created_at: string
  updated_at: string
}

export interface UserCreateRequest {
  username: string
  email: string
  password: string
}

export interface UserUpdateRequest {
  username?: string
  email?: string
  avatar?: string
}

// 通用响应类型
export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

export interface PaginatedData<T> {
  list: T[]
  total: number
  page: number
  page_size: number
}
```

### API 封装规范

```typescript
// utils/request.ts
import axios, { AxiosError, AxiosInstance, AxiosRequestConfig } from 'axios'
import { message } from 'ant-design-vue'
import { useUserStore } from '@/stores/user'

const request: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器
request.interceptors.response.use(
  (response) => response.data,
  (error: AxiosError) => {
    const { response } = error
    if (response?.status === 401) {
      const userStore = useUserStore()
      userStore.logout()
      window.location.href = '/login'
    } else {
      message.error(response?.data?.message || '请求失败')
    }
    return Promise.reject(error)
  }
)

export default request
```

```typescript
// api/user.ts
import request from '@/utils/request'
import type { ApiResponse, PaginatedData, User, UserCreateRequest } from '@/types'

export const getUserList = (params?: { page?: number; page_size?: number }) => {
  return request.get<ApiResponse<PaginatedData<User>>>('/api/v1/users', { params })
}

export const getUserById = (id: number) => {
  return request.get<ApiResponse<User>>(`/api/v1/users/${id}`)
}

export const createUser = (data: UserCreateRequest) => {
  return request.post<ApiResponse<User>>('/api/v1/users', data)
}

export const updateUser = (id: number, data: Partial<UserCreateRequest>) => {
  return request.put<ApiResponse<User>>(`/api/v1/users/${id}`, data)
}

export const deleteUser = (id: number) => {
  return request.delete<ApiResponse<null>>(`/api/v1/users/${id}`)
}
```

### Pinia Store 规范

```typescript
// stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'

export const useUserStore = defineStore('user', () => {
  // State
  const token = ref<string>(localStorage.getItem('token') || '')
  const userInfo = ref<User | null>(null)
  
  // Getters
  const isLoggedIn = computed(() => !!token.value)
  
  // Actions
  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }
  
  const setUserInfo = (info: User) => {
    userInfo.value = info
  }
  
  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }
  
  return {
    token,
    userInfo,
    isLoggedIn,
    setToken,
    setUserInfo,
    logout
  }
})
```

### 路由配置

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { public: true }
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue')
      },
      {
        path: '/users',
        name: 'UserList',
        component: () => import('@/views/user/list.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  if (!to.meta.public && !userStore.isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
```

### Tailwind CSS 配置

```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
        }
      }
    },
  },
  plugins: [],
}
```

```css
/* src/styles/tailwind.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* 自定义工具类 */
@layer components {
  .btn-primary {
    @apply bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors;
  }
  
  .card {
    @apply bg-white rounded-xl shadow-md p-6;
  }
}
```

```typescript
// main.ts
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// Tailwind CSS
import './styles/tailwind.css'

// Ant Design Vue
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Antd)

app.mount('#app')
```

### Tailwind + Ant Design 混合使用

```vue
<template>
  <!-- 使用 Tailwind 进行布局，Ant Design 提供组件 -->
  <div class="min-h-screen bg-gray-50">
    <!-- 头部导航 -->
    <header class="bg-white shadow-sm sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <h1 class="text-xl font-bold text-gray-900">管理系统</h1>
          <a-button type="primary" @click="handleAdd">新增</a-button>
        </div>
      </div>
    </header>
    
    <!-- 主内容区 -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 统计卡片 - 使用 Tailwind 样式 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="card">
          <p class="text-sm text-gray-500">总用户数</p>
          <p class="text-2xl font-bold text-gray-900">1,234</p>
        </div>
        <div class="card">
          <p class="text-sm text-gray-500">今日订单</p>
          <p class="text-2xl font-bold text-gray-900">56</p>
        </div>
        <div class="card">
          <p class="text-sm text-gray-500">收入</p>
          <p class="text-2xl font-bold text-gray-900">¥12,345</p>
        </div>
      </div>
      
      <!-- 数据表格 - 使用 Ant Design -->
      <div class="card">
        <a-table
          :columns="columns"
          :data-source="dataSource"
          :loading="loading"
          :pagination="pagination"
          row-key="id"
        />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const loading = ref(false)
const dataSource = ref([])
const columns = [
  { title: '用户名', dataIndex: 'username' },
  { title: '邮箱', dataIndex: 'email' },
  { title: '状态', dataIndex: 'status' },
  { title: '操作', key: 'action' }
]
const pagination = { pageSize: 10 }

const handleAdd = () => {
  console.log('新增')
}
</script>
```

### 常用 Tailwind 工具类组合

```vue
<template>
  <!-- 表单布局 -->
  <div class="space-y-4">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <a-form-item label="用户名">
        <a-input 
          v-model:value="form.username" 
          class="w-full"
          placeholder="请输入用户名"
        />
      </a-form-item>
      <a-form-item label="邮箱">
        <a-input 
          v-model:value="form.email" 
          class="w-full"
          placeholder="请输入邮箱"
        />
      </a-form-item>
    </div>
  </div>
  
  <!-- 按钮组 -->
  <div class="flex justify-end gap-3 mt-6">
    <a-button>取消</a-button>
    <a-button type="primary" class="bg-primary-600 hover:bg-primary-700">
      保存
    </a-button>
  </div>
  
  <!-- 响应式侧边栏 -->
  <aside class="hidden lg:block w-64 bg-white border-r border-gray-200 min-h-screen">
    <nav class="p-4 space-y-2">
      <a 
        v-for="item in menuItems" 
        :key="item.key"
        :class="[
          'flex items-center gap-3 px-4 py-2 rounded-lg transition-colors',
          activeKey === item.key 
            ? 'bg-primary-50 text-primary-600' 
            : 'text-gray-600 hover:bg-gray-50'
        ]"
      >
        <component :is="item.icon" class="w-5 h-5" />
        <span>{{ item.label }}</span>
      </a>
    </nav>
  </aside>
</template>
```

---

## 后端规范

### FastAPI 项目结构

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.v1 import api_router
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动事件
    await init_db()
    yield
    # 关闭事件
    await close_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
```

### 配置管理

```python
# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Project"
    VERSION: str = "1.0.0"
    
    # 数据库
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["http://localhost:5173"]
    
    # JWT
    SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 数据模型

```python
# app/db/models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
```

### API 路由

```python
# app/api/v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user import UserService
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取用户列表"""
    service = UserService(db)
    return await service.get_users(skip=skip, limit=limit)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建用户"""
    service = UserService(db)
    return await service.create_user(user_in)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取用户详情"""
    service = UserService(db)
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新用户"""
    service = UserService(db)
    return await service.update_user(user_id, user_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """删除用户"""
    service = UserService(db)
    await service.delete_user(user_id)
```

### 业务服务层

```python
# app/services/user.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_users(self, skip: int = 0, limit: int = 100):
        result = await self.db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def get_user_by_id(self, user_id: int):
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str):
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def create_user(self, user_in: UserCreate):
        # 检查邮箱是否已存在
        existing = await self.get_user_by_email(user_in.email)
        if existing:
            raise ValueError("邮箱已存在")
        
        # 创建用户
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password)
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user
    
    async def update_user(self, user_id: int, user_in: UserUpdate):
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")
        
        update_data = user_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def delete_user(self, user_id: int):
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")
        
        await self.db.delete(user)
        await self.db.commit()
```

---

## 开发命令

### 前端

```bash
# 安装依赖
cd frontend && npm install

# 安装 Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# 开发服务器
npm run dev

# 构建
npm run build

# 类型检查
npm run type-check

# 代码检查
npm run lint
```

### 后端

```bash
# 安装依赖
cd backend && pip install -r requirements.txt

# 开发服务器
uvicorn app.main:app --reload

# 数据库迁移
alembic revision --autogenerate -m "migration message"
alembic upgrade head

# 运行测试
pytest
```

---

## 环境变量

### 前端 (.env)

```
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=Vue3 FastAPI App
```

### 后端 (.env)

```
PROJECT_NAME="Vue3 FastAPI Project"
DATABASE_URL=sqlite:///./app.db
# DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
ALLOWED_HOSTS=["http://localhost:5173"]
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Docker 部署

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/app
    depends_on:
      - db
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --reload

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_BASE_URL=http://localhost:8000/api/v1
    command: npm run dev -- --host

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

---

## 最佳实践

### 前端

1. **组件设计**
   - 单一职责原则
   - Props 向下传递，Events 向上传递
   - 使用 TypeScript 定义 Props 类型

2. **状态管理**
   - 组件级状态使用 ref/reactive
   - 跨组件状态使用 Pinia
   - 避免直接修改 props

3. **性能优化**
   - 使用 v-once 和 v-memo
   - 懒加载路由组件
   - 使用 computed 缓存计算结果

### 后端

1. **API 设计**
   - RESTful 规范
   - 统一响应格式
   - 完善的错误处理

2. **数据库**
   - 使用异步 ORM
   - 数据库迁移管理
   - 连接池配置

3. **安全**
   - JWT 认证
   - 密码哈希存储
   - CORS 配置
   - 输入验证

---

## 开发阶段与工具使用

### 阶段 1: 需求分析与设计

**适用场景：** 项目启动、功能规划、UI 设计

| 工具 | 路径/命令 | 用途 |
|------|----------|------|
| **UI/UX Pro Max Skill** | `.claude/skills/ui-ux-pro-max` | 生成设计系统、配色方案、字体搭配 |
| **搜索设计资源** | `python .claude/skills/ui-ux-pro-max/scripts/search.py` | 查询样式、颜色、UX 指南 |

**使用示例：**
```bash
# 生成项目设计系统
python .claude/skills/ui-ux-pro-max/scripts/search.py "saas dashboard" --design-system -p "MyProject"

# 搜索配色方案
python .claude/skills/ui-ux-pro-max/scripts/search.py "modern blue" --domain color

# 搜索字体搭配
python .claude/skills/ui-ux-pro-max/scripts/search.py "professional clean" --domain typography
```

---

### 阶段 2: 代码开发

**适用场景：** 编写前端/后端代码、组件开发、API 实现

| 工具 | 路径 | 用途 |
|------|------|------|
| **Vue Skill** | 内置 Skill | Vue 3 Composition API 模式、组件最佳实践 |
| **Vite Skill** | 内置 Skill | Vite 配置、插件、构建优化 |
| **前端设计 Skill** | 内置 Skill | 创建高质量 UI 组件和页面 |

**开发流程：**
1. 使用 UI/UX Pro Max 获取设计规范
2. 使用 Vue Skill 编写组件代码
3. 使用 Vite Skill 优化构建配置

---

### 阶段 3: Git 版本控制

**适用场景：** 代码提交、分支管理、双仓库推送

| 工具 | 路径 | 用途 |
|------|------|------|
| **Git-Ops Skill** | `.claude/skills/git-ops` | 提交规范、双仓库推送、工作流 |

**使用示例：**
```bash
# 查看 Git 操作指南
cat .claude/skills/git-ops/SKILL.md

# 提交代码（遵循 Conventional Commits）
git add .
git commit -m "feat(user): 添加用户登录功能

- 实现 JWT 认证
- 添加登录表单验证
- 集成 Pinia 状态管理"

# 推送到双仓库
git push github master
git push gitee master
```

**提交规范：**
```
<type>(<scope>): <subject>

<body>

<footer>
```

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修复 Bug |
| `docs` | 文档更新 |
| `style` | 代码格式 |
| `refactor` | 重构 |
| `test` | 测试 |
| `chore` | 构建/工具 |

---

### 阶段 4: 代码审查与优化

**适用场景：** 代码 Review、性能优化、Bug 修复

| 工具 | 路径 | 用途 |
|------|------|------|
| **UI/UX Pro Max Skill** | `.claude/skills/ui-ux-pro-max` | 审查 UI 代码、检查 UX 问题 |
| **Vitest Skill** | 内置 Skill | 单元测试、集成测试 |

**审查检查项：**
```bash
# 搜索 UX 最佳实践
python .claude/skills/ui-ux-pro-max/scripts/search.py "accessibility" --domain ux

# 搜索性能优化
python .claude/skills/ui-ux-pro-max/scripts/search.py "performance" --domain ux
```

---

### 阶段 5: 部署与运维

**适用场景：** 构建、部署、监控

| 工具 | 命令/路径 | 用途 |
|------|----------|------|
| **Docker** | `docker-compose up` | 容器化部署 |
| **GitHub/Gitee MCP** | MCP 工具 | 创建 PR、Issue、查看仓库状态 |

**部署命令：**
```bash
# 本地 Docker 部署
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

---

### 工具使用速查表

| 开发阶段 | 主要工具 | 辅助工具 |
|----------|----------|----------|
| 需求设计 | UI/UX Pro Max Skill | - |
| 前端开发 | Vue Skill + 前端设计 Skill | UI/UX Pro Max Skill |
| 后端开发 | FastAPI (规则文档) | - |
| Git 操作 | Git-Ops Skill | GitHub/Gitee MCP |
| 代码审查 | UI/UX Pro Max Skill | Vitest Skill |
| 测试 | Vitest Skill | - |
| 部署 | Docker | GitHub/Gitee MCP |

---

### 快速启动工作流

```bash
# 1. 初始化项目（使用本规则创建项目结构）

# 2. 生成设计系统
python .claude/skills/ui-ux-pro-max/scripts/search.py "project type" --design-system -p "ProjectName"

# 3. 开发代码（遵循本规则的前后端规范）

# 4. 提交代码（遵循 Git-Ops Skill 规范）
git add .
git commit -m "feat(scope): description"
git push github master && git push gitee master

# 5. 创建 PR（使用 MCP 工具）
# 通过 MCP GitHub 工具创建 Pull Request
```
