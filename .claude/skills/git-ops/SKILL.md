# Git 操作 Skill

版本: v1.0
作者: zjc
更新: 2026-03-04

---

## 用途

本 Skill 用于规范日常 Git 操作，特别是双仓库（GitHub + Gitee）的同步推送。

---

## 适用场景

- 日常代码提交
- 双仓库同步推送
- 提交信息规范化
- 分支管理

---

## 核心规则

### 1. 提交信息规范

必须遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type 类型

| 类型 | 说明 | 使用场景 |
|------|------|----------|
| `feat` | 新功能 | 新增功能、特性 |
| `fix` | 修复 | Bug 修复 |
| `docs` | 文档 | 仅文档变更 |
| `style` | 格式 | 代码格式调整（不影响功能） |
| `refactor` | 重构 | 代码重构（非 feat/fix） |
| `perf` | 性能 | 性能优化 |
| `test` | 测试 | 测试相关 |
| `chore` | 构建 | 构建/工具/依赖变更 |
| `ci` | CI | 持续集成配置 |
| `revert` | 回滚 | 代码回滚 |

#### Scope 范围（可选）

- `extractor` - 视频提取器
- `downloader` - 下载器
- `postprocessor` - 后处理器
- `utils` - 工具函数
- `config` - 配置
- `docs` - 文档
- `test` - 测试

#### Subject 主题

- 使用祈使句，现在时
- 首字母小写
- 结尾不加句号
- 不超过 50 个字符
- 使用中文

#### 示例

```
feat(extractor): 添加新视频平台支持

fix(downloader): 修复慢网络下的超时问题

docs: 更新 README 安装说明

refactor(utils): 简化 URL 解析逻辑

chore(deps): 升级 requests 从 2.28.0 到 2.31.0
```

### 2. 双仓库推送流程

#### 配置远程仓库

```bash
# 添加 GitHub 远程仓库
git remote add github https://github.com/<username>/<repo>.git

# 添加 Gitee 远程仓库
git remote add gitee https://gitee.com/<username>/<repo>.git

# 查看远程仓库
git remote -v
```

#### 日常推送命令

```bash
# 1. 添加更改
git add .

# 2. 提交（遵循规范）
git commit -m "feat(extractor): add new video source support"

# 3. 推送到 GitHub
git push github master

# 4. 推送到 Gitee
git push gitee master
```

#### 快捷推送脚本

```bash
# push-all.sh
#!/bin/bash
BRANCH=${1:-master}
echo "Pushing to GitHub..."
git push github $BRANCH
echo "Pushing to Gitee..."
git push gitee $BRANCH
echo "Done!"
```

### 3. 分支管理规范

#### 分支命名

- `master` / `main` - 主分支，稳定版本
- `develop` - 开发分支
- `feature/<name>` - 功能分支
- `fix/<name>` - 修复分支
- `hotfix/<name>` - 紧急修复
- `release/<version>` - 发布分支

#### 工作流程

```
master/main
    ↑
develop ←—— feature/new-extractor
    ↑
feature/login-page
```

### 4. 提交前检查清单

- [ ] 代码可以正常运行
- [ ] 无敏感信息泄露（密码、密钥等）
- [ ] 提交信息符合规范
- [ ] 已推送到两个远程仓库
- [ ] 无大文件（>100MB）提交

---

## 常用命令速查

### 基础操作

```bash
# 查看状态
git status

# 查看更改
git diff

# 查看提交历史
git log --oneline -10

# 查看分支
git branch -a
```

### 撤销操作

```bash
# 撤销工作区更改
git checkout -- <file>

# 撤销暂存区
git reset HEAD <file>

# 修改最后一次提交
git commit --amend

# 回滚到指定版本
git reset --hard <commit-id>
```

### 同步操作

```bash
# 从 GitHub 拉取
git pull github master

# 从 Gitee 拉取
git pull gitee master

# 获取所有远程更新
git fetch --all
```

---

## 参考资料

- [提交规范详解](references/commit-convention.md)
- [双仓库推送指南](references/dual-remote-push.md)
- [Git 工作流](references/git-workflow.md)

---

## 触发条件

当用户提到以下关键词时触发本 Skill：
- git 提交
- git push
- 双仓库推送
- 提交代码
- commit message
- 提交规范
