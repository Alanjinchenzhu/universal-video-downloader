# Go 开发规范

作者：zjc
版本：v1.0
日期：2025-12-17
状态：草稿

> **部署位置**: `~/.claude/rules/go-style.md`
> **作用范围**: 所有 Go 项目
> **参考来源**: Effective Go、Go Code Review Comments、uber-go/guide

---
paths:
  - "**/*.go"
  - "**/go.mod"
  - "**/go.sum"
---

## 工具链

<!-- [注释] 可根据项目调整，如使用 golangci-lint 替代单独工具 -->

- 格式化: `gofmt` 或 `goimports`（推荐，自动管理 import）
- 静态检查: `go vet`、`staticcheck`
- 综合检查: `golangci-lint`（集成多种 linter）
- 测试: `go test -v -race ./...`

```bash
# 常用命令
goimports -w .                    # 格式化并整理 import
go vet ./...                      # 静态分析
golangci-lint run                 # 综合检查
go test -v -race -cover ./...     # 测试（含竞态检测和覆盖率）
```

## 命名约定

<!-- [注释] 遵循 Effective Go，可按团队习惯微调 -->

### 包命名
- 小写单词，不用下划线或驼峰: `strconv`、`httputil`
- 简短、清晰、有意义
- 避免 `common`、`util`、`base` 等无意义名称

```go
// ✅ 好
package user
package orderservice

// ❌ 差
package common
package utils
package myPackage
```

### 变量和函数命名
- 使用驼峰命名: `userID`、`parseRequest`
- 缩写词保持一致大小写: `userID`（非 `userId`）、`HTTPServer`（非 `HttpServer`）
- 短变量名用于小作用域: `i`、`n`、`err`
- 长变量名用于大作用域或导出标识符

```go
// ✅ 好
var userID int64
var httpClient *http.Client
func parseJSON(data []byte) error

// ❌ 差
var UserId int64        // 应为 userID 或 UserID
var HttpClient          // 应为 HTTPClient
```

### 常量命名
- 导出常量用驼峰: `MaxRetryCount`
- 私有常量可用驼峰或全大写: `maxRetryCount` 或 `maxRetryCount`

<!-- [注释] Go 社区不强制要求常量全大写，与 Java 不同 -->

```go
// ✅ 两种都可接受
const MaxRetryCount = 3
const maxRetryCount = 3

// ❌ 不推荐（Go 风格）
const MAX_RETRY_COUNT = 3
```

### 接口命名
- 单方法接口用方法名 + `er`: `Reader`、`Writer`、`Formatter`
- 多方法接口描述行为: `ReadWriter`、`FileSystem`

```go
// ✅ 好
type Reader interface {
    Read(p []byte) (n int, err error)
}

type UserRepository interface {
    FindByID(id int64) (*User, error)
    Save(user *User) error
}
```

## 代码组织

<!-- [注释] 可根据项目规模调整 -->

### 文件组织
- 每个包一个目录
- 测试文件与源文件同目录: `user.go` + `user_test.go`
- 相关类型放同一文件，文件不宜过大（建议 < 500 行）

### import 顺序
- 标准库 → 第三方库 → 项目内部包
- 各组之间空行分隔

```go
import (
    "context"
    "fmt"
    "net/http"

    "github.com/gin-gonic/gin"
    "gorm.io/gorm"

    "qiandao/internal/model"
    "qiandao/internal/service"
)
```

### 项目结构（参考）

<!-- [注释] 这是常见布局，可根据项目实际情况调整 -->

```
project/
├── cmd/                    # 可执行文件入口
│   └── server/
│       └── main.go
├── internal/               # 私有代码（不可被外部导入）
│   ├── handler/           # HTTP 处理器
│   ├── service/           # 业务逻辑
│   ├── repository/        # 数据访问
│   └── model/             # 数据模型
├── pkg/                    # 可被外部导入的公共代码
├── api/                    # API 定义（OpenAPI/protobuf）
├── configs/                # 配置文件
├── scripts/                # 脚本
├── go.mod
└── go.sum
```

## 错误处理

<!-- [注释] Go 错误处理的核心原则，必须遵循 -->

### 基本原则
- **必须处理错误**，不能忽略
- 错误应该只处理一次（要么返回，要么记录日志）
- 添加上下文信息便于排查

```go
// ✅ 好：添加上下文
if err != nil {
    return fmt.Errorf("failed to query user %d: %w", userID, err)
}

// ✅ 好：记录日志后返回
if err != nil {
    log.Printf("failed to send email to %s: %v", email, err)
    return err
}

// ❌ 差：忽略错误
result, _ := doSomething()

// ❌ 差：重复处理（既记录又包装）
if err != nil {
    log.Printf("error: %v", err)
    return fmt.Errorf("failed: %w", err)  // 日志和返回都有，上层可能再次记录
}
```

### 错误包装
- 使用 `%w` 包装错误，保留错误链
- 使用 `errors.Is()` 和 `errors.As()` 检查错误

```go
// 包装错误
if err != nil {
    return fmt.Errorf("parse config: %w", err)
}

// 检查错误类型
if errors.Is(err, os.ErrNotExist) {
    // 文件不存在的处理
}

var pathErr *os.PathError
if errors.As(err, &pathErr) {
    // 处理路径错误
}
```

### 自定义错误
- 简单场景用 `errors.New()` 或 `fmt.Errorf()`
- 需要携带信息时定义错误类型

```go
// 简单错误
var ErrUserNotFound = errors.New("user not found")

// 携带信息的错误
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed on %s: %s", e.Field, e.Message)
}
```

## 并发编程

<!-- [注释] Go 并发是强项也是易错点，需谨慎 -->

### 基本原则
- 优先使用 channel 通信，而非共享内存
- 启动 goroutine 前考虑：谁来等待它？怎么停止它？
- 使用 `context.Context` 控制生命周期

```go
// ✅ 好：使用 context 控制 goroutine
func process(ctx context.Context) error {
    done := make(chan error, 1)

    go func() {
        done <- doWork()
    }()

    select {
    case err := <-done:
        return err
    case <-ctx.Done():
        return ctx.Err()
    }
}

// ❌ 差：无法停止的 goroutine
go func() {
    for {
        doWork()  // 永远无法停止
    }
}()
```

### 数据竞争
- 使用 `go test -race` 检测竞态
- 保护共享数据：channel、sync.Mutex、sync/atomic

```go
// ✅ 使用 mutex 保护
type Counter struct {
    mu    sync.Mutex
    count int
}

func (c *Counter) Inc() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

// ✅ 使用 atomic
var count int64
atomic.AddInt64(&count, 1)
```

## 注释规范

<!-- [注释] 导出标识符必须有注释，私有代码按需 -->

### 导出标识符
- 所有导出的类型、函数、常量、变量必须有注释
- 注释以标识符名称开头

```go
// User represents a registered user in the system.
type User struct {
    ID    int64
    Name  string
    Email string
}

// FindByID retrieves a user by their unique identifier.
// Returns ErrUserNotFound if the user does not exist.
func FindByID(id int64) (*User, error) {
    // ...
}
```

### 包注释
- 每个包应有包注释，放在任意一个源文件的 package 声明前
- 简短描述包的用途

```go
// Package user provides user management functionality including
// registration, authentication, and profile management.
package user
```

## 测试规范

<!-- [注释] 测试是质量保证的关键 -->

### 测试函数命名
- 测试函数: `TestXxx`
- 基准测试: `BenchmarkXxx`
- 示例函数: `ExampleXxx`

```go
func TestFindByID(t *testing.T) {
    // ...
}

func TestFindByID_NotFound(t *testing.T) {
    // ...
}

func BenchmarkFindByID(b *testing.B) {
    for i := 0; i < b.N; i++ {
        FindByID(1)
    }
}
```

### 表驱动测试

<!-- [注释] Go 推荐的测试模式 -->

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 1, 2, 3},
        {"negative", -1, -2, -3},
        {"zero", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := Add(tt.a, tt.b)
            if got != tt.expected {
                t.Errorf("Add(%d, %d) = %d, want %d", tt.a, tt.b, got, tt.expected)
            }
        })
    }
}
```

### 测试辅助
- 使用 `t.Helper()` 标记辅助函数
- 使用 `t.Cleanup()` 注册清理函数

```go
func setupTestDB(t *testing.T) *gorm.DB {
    t.Helper()
    db := createTestDB()
    t.Cleanup(func() {
        closeDB(db)
    })
    return db
}
```

## 性能考虑

<!-- [注释] 先写正确的代码，再优化性能 -->

### 核心原则

| 原则 | 说明 |
|------|------|
| **先正确后优化** | 先确保功能正确，再考虑性能 |
| **先测量后优化** | 用 pprof 定位瓶颈，不要猜 |
| **80/20 原则** | 优化 20% 的热点代码，获得 80% 的收益 |

### 数据库查询优化

```go
// ❌ N+1 查询问题
for _, user := range users {
    orders := db.Where("user_id = ?", user.ID).Find(&orders)
}

// ✅ 批量查询 + 预加载
db.Preload("Orders").Find(&users)

// ✅ 或手动批量查询
userIDs := extractIDs(users)
var orders []Order
db.Where("user_id IN ?", userIDs).Find(&orders)
orderMap := groupByUserID(orders)
```

### 内存优化

```go
// ✅ 预分配 slice 容量
users := make([]User, 0, len(ids))
for _, id := range ids {
    users = append(users, findUser(id))
}

// ✅ 使用 strings.Builder
var b strings.Builder
b.Grow(estimatedSize)
for _, s := range strs {
    b.WriteString(s)
}
result := b.String()

// ❌ 差：循环拼接字符串
var result string
for _, s := range strs {
    result += s  // 每次都分配新内存
}

// ✅ 使用 sync.Pool 复用对象（高频场景）
var bufPool = sync.Pool{
    New: func() interface{} {
        return new(bytes.Buffer)
    },
}

func process() {
    buf := bufPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        bufPool.Put(buf)
    }()
    // 使用 buf
}
```

### 并发控制

```go
// ✅ 使用 semaphore 限制并发数
sem := make(chan struct{}, maxConcurrency)
var wg sync.WaitGroup

for _, item := range items {
    wg.Add(1)
    sem <- struct{}{}
    go func(item Item) {
        defer func() {
            <-sem
            wg.Done()
        }()
        process(item)
    }(item)
}
wg.Wait()

// ✅ 使用 errgroup 处理并发错误
g, ctx := errgroup.WithContext(ctx)
g.SetLimit(maxConcurrency)

for _, item := range items {
    item := item
    g.Go(func() error {
        return process(ctx, item)
    })
}
if err := g.Wait(); err != nil {
    return err
}
```

### 避免常见陷阱

| 陷阱 | 解决方案 |
|------|---------|
| 循环中拼接字符串 | 使用 `strings.Builder` |
| 未预分配 slice | `make([]T, 0, cap)` |
| defer 在热路径 | 热路径避免 defer，或提取到单独函数 |
| 频繁创建临时对象 | 使用 `sync.Pool` |
| 锁粒度过大 | 缩小临界区，考虑读写锁 |
| 无限制并发 | 使用 semaphore 或 worker pool |

### 性能分析工具

```bash
# CPU 分析
go test -cpuprofile=cpu.prof -bench=.
go tool pprof cpu.prof

# 内存分析
go test -memprofile=mem.prof -bench=.
go tool pprof mem.prof

# 实时分析（需要导入 net/http/pprof）
go tool pprof http://localhost:6060/debug/pprof/profile
```

## 规则溯源要求

当回复明确受到本规则约束时，在回复末尾声明：

```
> 📋 本回复遵循规则：`go-style.md` - [具体章节]
```

---

## 参考资料

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md)
- [Standard Go Project Layout](https://github.com/golang-standards/project-layout)
