# 双仓库推送指南

版本: v1.0
作者: zjc
更新: 2026-03-04

---

## 概述

本项目同时维护 GitHub 和 Gitee 两个远程仓库，实现代码双备份和国内外访问优化。

---

## 仓库地址

| 平台 | 地址 | 用途 |
|------|------|------|
| GitHub | https://github.com/Alanjinchenzhu/universal-video-downloader | 国际访问、主要仓库 |
| Gitee | https://gitee.com/z-jinchen/universal-video-downloader | 国内访问、加速下载 |

---

## 初始配置

### 1. 添加远程仓库

```bash
# 添加 GitHub 远程仓库（命名为 github）
git remote add github https://github.com/Alanjinchenzhu/universal-video-downloader.git

# 添加 Gitee 远程仓库（命名为 gitee）
git remote add gitee https://gitee.com/z-jinchen/universal-video-downloader.git

# 验证配置
git remote -v
```

预期输出：
```
gitee   https://gitee.com/z-jinchen/universal-video-downloader.git (fetch)
gitee   https://gitee.com/z-jinchen/universal-video-downloader.git (push)
github  https://github.com/Alanjinchenzhu/universal-video-downloader.git (fetch)
github  https://github.com/Alanjinchenzhu/universal-video-downloader.git (push)
```

### 2. 更新远程仓库地址

如果地址变更：

```bash
# 更新 GitHub 地址
git remote set-url github https://github.com/<new-path>.git

# 更新 Gitee 地址
git remote set-url gitee https://gitee.com/<new-path>.git
```

---

## 日常推送流程

### 标准流程

```bash
# 1. 检查当前状态
git status

# 2. 添加更改到暂存区
git add .
# 或添加特定文件
git add <file1> <file2>

# 3. 提交更改（遵循提交规范）
git commit -m "feat(extractor): add new video source support"

# 4. 推送到 GitHub
git push github master

# 5. 推送到 Gitee
git push gitee master
```

### 快捷脚本

创建 `push-all.sh`：

```bash
#!/bin/bash

# 双仓库推送脚本
# 用法: ./push-all.sh [分支名]

BRANCH=${1:-master}

echo "================================"
echo "双仓库推送脚本"
echo "分支: $BRANCH"
echo "================================"
echo ""

# 检查是否有未提交的更改
if ! git diff-index --quiet HEAD --; then
    echo "❌ 有未提交的更改，请先提交"
    exit 1
fi

echo "📤 推送到 GitHub..."
if git push github $BRANCH; then
    echo "✅ GitHub 推送成功"
else
    echo "❌ GitHub 推送失败"
    exit 1
fi

echo ""
echo "📤 推送到 Gitee..."
if git push gitee $BRANCH; then
    echo "✅ Gitee 推送成功"
else
    echo "❌ Gitee 推送失败"
    exit 1
fi

echo ""
echo "================================"
echo "🎉 双仓库推送完成！"
echo "================================"
```

使用方法：

```bash
# 添加执行权限
chmod +x push-all.sh

# 推送到默认分支（master）
./push-all.sh

# 推送到指定分支
./push-all.sh develop
```

---

## 拉取同步

### 从 GitHub 拉取

```bash
# 拉取最新代码
git pull github master

# 获取但不合并
git fetch github
```

### 从 Gitee 拉取

```bash
# 拉取最新代码
git pull gitee master

# 获取但不合并
git fetch gitee
```

### 同步所有远程

```bash
# 获取所有远程仓库的更新
git fetch --all

# 查看所有分支
git branch -a
```

---

## 分支管理

### 创建新分支并推送

```bash
# 创建并切换到新分支
git checkout -b feature/new-extractor

# 开发完成后提交
git add .
git commit -m "feat(extractor): implement new video source"

# 推送到两个远程
git push github feature/new-extractor
git push gitee feature/new-extractor
```

### 删除远程分支

```bash
# 删除 GitHub 分支
git push github --delete feature/new-extractor

# 删除 Gitee 分支
git push gitee --delete feature/new-extractor
```

---

## 常见问题

### 问题 1: 推送被拒绝（非快进）

**现象：**
```
! [rejected]        master -> master (non-fast-forward)
```

**解决：**
```bash
# 先拉取合并
git pull github master
# 解决冲突后重新推送
git push github master
git push gitee master
```

### 问题 2: 认证失败

**现象：**
```
fatal: Authentication failed
```

**解决：**
- GitHub: 使用 Personal Access Token 或 SSH
- Gitee: 使用密码或 SSH

配置 SSH：
```bash
# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "your@email.com"

# 添加到 GitHub/Gitee
# 然后修改远程地址为 SSH
git remote set-url github git@github.com:Alanjinchenzhu/universal-video-downloader.git
git remote set-url gitee git@gitee.com:z-jinchen/universal-video-downloader.git
```

### 问题 3: 仓库不存在

**现象：**
```
fatal: repository '...' not found
```

**解决：**
1. 检查仓库地址是否正确
2. 确认仓库已创建
3. 检查访问权限

### 问题 4: GitHub Secret Scanning 阻止推送

**现象：**
```
remote: error: GH013: Repository rule violations found
remote: Push cannot contain secrets
```

**解决：**
1. 如果是有意的测试密钥，在 GitHub 上允许：
   - 访问仓库 Settings → Security → Secret scanning
   - 找到被阻止的 secret，点击 Resolve
   - 选择 "It's used in tests" 或 "I'll fix it later"

2. 如果是误报，修改代码后重新提交

---

## 最佳实践

### 1. 推送前检查

```bash
# 检查代码质量
make lint
make test

# 检查敏感信息
git-secrets --scan

# 检查大文件
find . -type f -size +10M
```

### 2. 定期同步

```bash
# 每天开始工作前
git fetch --all
git status
```

### 3. 保持两个仓库同步

始终确保两个仓库的代码一致：
- 推送时同时推送到两个仓库
- 拉取时优先从 GitHub 拉取
- 发现不一致时及时同步

### 4. 使用 Git 别名

```bash
# 添加到 ~/.gitconfig
[alias]
    pushall = !git push github $(git branch --show-current) && git push gitee $(git branch --show-current)
    pullgh = pull github
    pullge = pull gitee
```

使用：
```bash
git pushall
git pullgh master
git pullge master
```

---

## 命令速查表

| 操作 | 命令 |
|------|------|
| 查看远程 | `git remote -v` |
| 添加远程 | `git remote add <name> <url>` |
| 修改远程 | `git remote set-url <name> <url>` |
| 删除远程 | `git remote remove <name>` |
| 推送到 GitHub | `git push github <branch>` |
| 推送到 Gitee | `git push gitee <branch>` |
| 从 GitHub 拉取 | `git pull github <branch>` |
| 从 Gitee 拉取 | `git pull gitee <branch>` |
| 获取所有更新 | `git fetch --all` |
