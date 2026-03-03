# Git 工作流指南

版本: v1.0
作者: zjc
更新: 2026-03-04

---

## 概述

本文档定义本项目的 Git 分支管理策略和工作流程。

---

## 分支模型

采用简化版 Git Flow 模型：

```
master (稳定版本)
  ↑
develop (开发分支)
  ↑
feature/* (功能分支)
fix/* (修复分支)
```

---

## 分支说明

### master 分支

- **用途**: 生产环境代码
- **保护**: 禁止直接推送，需通过 PR/MR 合并
- **标签**: 每个发布版本打标签 `v1.0.0`

### develop 分支

- **用途**: 开发集成
- **来源**: 从 master 检出
- **合并**: 功能分支完成后合并至此

### feature/* 分支

- **命名**: `feature/功能描述`，如 `feature/bilibili-extractor`
- **来源**: 从 develop 检出
- **合并**: 完成后合并回 develop

### fix/* 分支

- **命名**: `fix/问题描述`，如 `fix/download-timeout`
- **来源**: 从 develop 检出
- **合并**: 完成后合并回 develop

### hotfix/* 分支

- **命名**: `hotfix/紧急修复描述`
- **来源**: 从 master 检出
- **合并**: 完成后同时合并到 master 和 develop

---

## 工作流程

### 1. 开始新功能

```bash
# 切换到 develop 分支
git checkout develop

# 拉取最新代码
git pull github develop

# 创建功能分支
git checkout -b feature/new-video-source

# 开发完成后提交
git add .
git commit -m "feat(extractor): add support for new video platform"

# 推送到远程
git push github feature/new-video-source
git push gitee feature/new-video-source
```

### 2. 修复 Bug

```bash
# 创建修复分支
git checkout -b fix/timeout-issue

# 修复完成后提交
git add .
git commit -m "fix(downloader): resolve timeout on slow networks"

# 推送
git push github fix/timeout-issue
git push gitee fix/timeout-issue
```

### 3. 紧急修复

```bash
# 从 master 创建热修复分支
git checkout master
git checkout -b hotfix/critical-bug

# 修复并提交
git add .
git commit -m "fix: resolve critical security issue"

# 合并到 master
git checkout master
git merge hotfix/critical-bug
git push github master
git push gitee master

# 合并到 develop
git checkout develop
git merge hotfix/critical-bug
git push github develop
git push gitee develop
```

---

## 提交规范

### 提交信息格式

```
类型(范围): 主题

正文

页脚
```

### 类型说明

| 类型 | 用途 |
|------|------|
| feat | 新功能 |
| fix | 修复 |
| docs | 文档 |
| style | 格式 |
| refactor | 重构 |
| test | 测试 |
| chore | 构建/工具 |

### 示例

```bash
# 功能提交
git commit -m "feat(extractor): add TikTok support"

# 修复提交
git commit -m "fix(downloader): handle network retry"

# 文档提交
git commit -m "docs: update API documentation"
```

---

## 版本发布

### 版本号规则

采用语义化版本 `主版本.次版本.修订号`：

- **主版本**: 不兼容的 API 修改
- **次版本**: 向下兼容的功能新增
- **修订号**: 向下兼容的问题修复

### 发布流程

```bash
# 1. 确保代码在 master 分支
git checkout master

# 2. 打版本标签
git tag -a v1.2.0 -m "Release version 1.2.0"

# 3. 推送标签
git push github v1.2.0
git push gitee v1.2.0

# 4. 推送所有分支
git push github master
git push gitee master
```

---

## 日常操作

### 开始工作

```bash
# 获取最新代码
git fetch --all

# 切换到工作分支
git checkout develop

# 拉取更新
git pull github develop
```

### 提交更改

```bash
# 查看更改
git status
git diff

# 添加文件
git add .

# 提交
git commit -m "类型(范围): 描述"

# 推送
git push github 分支名
git push gitee 分支名
```

### 同步分支

```bash
# 切换到目标分支
git checkout develop

# 合并功能分支
git merge feature/xxx

# 推送
git push github develop
git push gitee develop
```

---

## 冲突解决

### 拉取时冲突

```bash
# 拉取代码
git pull github develop

# 出现冲突时，编辑冲突文件
# 冲突标记：
# <<<<<<< HEAD
# 本地代码
# =======
# 远程代码
# >>>>>>> branch-name

# 解决后标记为已解决
git add 冲突文件

# 继续合并
git commit -m "merge: resolve conflicts"
```

### 合并时冲突

```bash
# 合并分支
git merge feature/xxx

# 解决冲突...

# 提交合并
git add .
git commit -m "merge: integrate feature branch"
```

---

## 最佳实践

1. **频繁提交**: 小步快跑，多次小提交优于一次大提交
2. **清晰信息**: 提交信息要清晰描述做了什么
3. **先拉后推**: 推送前先拉取最新代码
4. **功能隔离**: 每个功能独立分支，不要混用
5. **及时合并**: 功能完成后及时合并，避免长期分支
6. **双库同步**: 始终推送到 GitHub 和 Gitee 两个仓库

---

## 命令速查

| 操作 | 命令 |
|------|------|
| 查看分支 | `git branch` |
| 切换分支 | `git checkout 分支名` |
| 创建并切换 | `git checkout -b 分支名` |
| 合并分支 | `git merge 分支名` |
| 删除本地分支 | `git branch -d 分支名` |
| 删除远程分支 | `git push 远程名 --delete 分支名` |
| 查看标签 | `git tag` |
| 创建标签 | `git tag -a v1.0 -m "描述"` |
| 推送标签 | `git push 远程名 标签名` |
| 推送所有标签 | `git push 远程名 --tags` |
