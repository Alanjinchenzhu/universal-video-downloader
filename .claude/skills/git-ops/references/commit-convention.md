# Git 提交信息规范

版本: v1.0
作者: zjc
更新: 2026-03-04

---

## 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

---

## Type 类型详解

### feat - 新功能

用于新增功能或特性。

```
feat(extractor): add bilibili live stream support

Add support for downloading Bilibili live streams with real-time
chat replay functionality.

Closes #123
```

### fix - 修复

用于 Bug 修复。

```
fix(downloader): resolve download timeout on slow networks

Increase default timeout from 30s to 120s for large files.
Add retry logic for network interruptions.

Fixes #456
```

### docs - 文档

仅文档变更，不涉及代码。

```
docs: update README with Windows installation guide

Add detailed steps for Windows users including Python
installation and PATH configuration.
```

### style - 格式

代码格式调整，不影响功能。

```
style: format code with black and isort

Apply consistent code formatting across all Python files.
No functional changes.
```

### refactor - 重构

代码重构，既不是新增功能也不是修复 Bug。

```
refactor(utils): simplify URL parsing logic

Extract common URL parsing patterns into reusable functions.
Reduce code duplication by 40%.
```

### perf - 性能优化

性能提升相关。

```
perf(extractor): cache regex patterns for 10x speedup

Compile and cache frequently used regex patterns to avoid
recompilation on each call.

Benchmark: 150ms → 15ms per extraction
```

### test - 测试

测试相关变更。

```
test(extractor): add unit tests for youtube extractor

Achieve 95% code coverage for YouTube extractor module.
Add mock tests for API responses.
```

### chore - 构建/工具

构建过程或辅助工具的变更。

```
chore(deps): bump requests from 2.28.0 to 2.31.0

Update requests library to fix security vulnerability
CVE-2023-32681.
```

### ci - 持续集成

CI/CD 配置变更。

```
ci: add GitHub Actions workflow for automated testing

Run tests on Python 3.8, 3.9, 3.10, 3.11 on every PR.
```

### revert - 回滚

撤销之前的提交。

```
revert: feat(extractor): add experimental feature

This reverts commit abc1234.

The feature caused memory leaks in production.
```

---

## Scope 范围定义

### 本项目专用 Scope

| Scope | 说明 | 示例 |
|-------|------|------|
| `extractor` | 视频提取器 | `feat(extractor): add new source` |
| `downloader` | 下载器 | `fix(downloader): handle retry` |
| `postprocessor` | 后处理器 | `feat(postprocessor): add metadata` |
| `utils` | 工具函数 | `refactor(utils): optimize helper` |
| `config` | 配置相关 | `chore(config): update defaults` |
| `cli` | 命令行接口 | `feat(cli): add progress bar` |
| `api` | API 接口 | `fix(api): handle auth error` |
| `deps` | 依赖管理 | `chore(deps): update packages` |
| `build` | 构建系统 | `chore(build): update setup.py` |
| `test` | 测试相关 | `test: add integration tests` |
| `docs` | 文档 | `docs: update API reference` |

---

## Subject 主题规范

### 要求

1. **祈使句，现在时**
   - ✅ `add feature`
   - ❌ `added feature`
   - ❌ `adds feature`

2. **首字母小写**
   - ✅ `add support`
   - ❌ `Add support`

3. **结尾不加句号**
   - ✅ `fix bug`
   - ❌ `fix bug.`

4. **不超过 50 个字符**
   - 保持简洁明了

### 常用动词

- `add` - 添加
- `fix` - 修复
- `update` - 更新
- `remove` - 移除
- `refactor` - 重构
- `optimize` - 优化
- `implement` - 实现
- `support` - 支持
- `disable` - 禁用
- `enable` - 启用

---

## Body 正文规范

### 何时需要

- 提交需要解释背景
- 有 breaking changes
- 需要说明实现细节

### 格式

- 使用祈使句
- 每行不超过 72 字符
- 解释 **what** 和 **why**，而非 **how**

### 示例

```
feat(extractor): add support for new video platform

Implement extractor for example.com video platform.
This platform uses dynamic loading requiring JavaScript
execution for metadata extraction.

- Add ExampleExtractor class
- Handle encrypted video URLs
- Support playlist extraction
```

---

## Footer 页脚规范

### Breaking Changes

```
BREAKING CHANGE: remove deprecated API endpoints

The old API v1 endpoints are no longer supported.
Migrate to API v2 before upgrading.
```

### Issue 关联

```
Closes #123
Fixes #456
Resolves #789

Related to #100
```

### Co-authors

```
Co-authored-by: Name <email@example.com>
```

---

## 完整示例

```
feat(extractor): add TikTok video download support

Implement full support for TikTok video extraction including:
- Single video download
- User profile video batch download
- Without watermark option

Technical details:
- Use mobile API endpoint for better reliability
- Handle rate limiting with exponential backoff
- Support both short and long URLs

BREAKING CHANGE: TikTok extractor now requires
additional cookie configuration for some regions.

Closes #234
Co-authored-by: Contributor <contrib@example.com>
```

---

## 提交信息模板

```bash
# 配置 Git 使用模板
git config commit.template ~/.gitmessage
```

模板内容：

```
# <type>(<scope>): <subject>
#
# <body>
#
# <footer>
#
# Type: feat|fix|docs|style|refactor|perf|test|chore|ci|revert
# Scope: extractor|downloader|postprocessor|utils|config|cli|api|deps|build|test|docs
#
# Subject rules:
# - Use imperative mood (add, not added)
# - First letter lowercase
# - No period at end
# - Max 50 characters
#
# Body rules:
# - Explain what and why, not how
# - Wrap at 72 characters
#
# Footer rules:
# - Reference issues: Closes #123, Fixes #456
# - Breaking changes: BREAKING CHANGE: description
# - Co-authors: Co-authored-by: Name <email>
```
