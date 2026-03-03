# Java 开发规范

作者：zjc
版本：v1.0
日期：2025-12-17
状态：草稿

> **部署位置**: `~/.claude/rules/java-style.md`
> **作用范围**: 所有 Java 项目
> **参考来源**: Google Java Style Guide、阿里巴巴 Java 开发手册

---
paths:
  - "**/*.java"
  - "**/pom.xml"
  - "**/build.gradle"
  - "**/build.gradle.kts"
---

## 工具链

<!-- [注释] 可根据项目调整，如使用 Checkstyle、SpotBugs 等 -->

- 格式化: IDE 内置格式化（遵循 Google Java Style 或团队规范）
- 静态检查: SpotBugs、PMD、Checkstyle
- 构建工具: Maven 或 Gradle
- 测试: JUnit 5 + Mockito

```bash
# Maven 常用命令
mvn clean compile                    # 编译
mvn test                             # 运行测试
mvn verify                           # 运行所有检查
mvn spotbugs:check                   # SpotBugs 检查

# Gradle 常用命令
./gradlew build                      # 构建
./gradlew test                       # 运行测试
./gradlew check                      # 运行所有检查
```

## 命名约定

<!-- [注释] 遵循 Java 社区通用规范 -->

### 包命名
- 全部小写，用域名反转: `com.example.project`
- 单词间不用分隔符

```java
// ✅ 好
package com.qiandao.service;
package org.example.util;

// ❌ 差
package com.qianDao.Service;    // 不要用大写
package com.qian_dao.service;   // 不要用下划线
```

### 类命名
- 大驼峰（PascalCase）: `UserService`、`HttpClient`
- 类名应是名词或名词短语
- 接口名可用形容词: `Runnable`、`Comparable`

```java
// ✅ 好
public class UserService { }
public class HttpRequestHandler { }
public interface Serializable { }

// ❌ 差
public class userService { }    // 应大写开头
public class Do_Something { }   // 不要用下划线
```

### 方法命名
- 小驼峰（camelCase）: `getUserById`、`isValid`
- 动词或动词短语开头
- 布尔返回值用 `is`/`has`/`can` 前缀

```java
// ✅ 好
public User findById(Long id) { }
public boolean isActive() { }
public boolean hasPermission(String role) { }

// ❌ 差
public User FindById(Long id) { }    // 应小写开头
public boolean active() { }          // 布尔值应用 is 前缀
```

### 变量命名
- 小驼峰: `userId`、`orderList`
- 常量全大写下划线分隔: `MAX_RETRY_COUNT`
- 避免单字符命名（循环变量除外）

```java
// ✅ 好
private Long userId;
private List<Order> orderList;
public static final int MAX_RETRY_COUNT = 3;

// ❌ 差
private Long UserId;              // 应小写开头
private List<Order> ol;           // 名称不清晰
public static final int maxRetry; // 常量应全大写
```

### 泛型类型参数
- 单个大写字母: `T`（类型）、`E`（元素）、`K`（键）、`V`（值）、`N`（数字）

```java
// ✅ 好
public class Box<T> { }
public interface Map<K, V> { }
public <E> List<E> filterList(List<E> list, Predicate<E> predicate) { }
```

## 代码组织

### 类成员顺序

<!-- [注释] 建议顺序，可根据团队习惯调整 -->

```java
public class Example {
    // 1. 静态常量
    public static final String CONSTANT = "value";

    // 2. 静态变量
    private static Logger logger = LoggerFactory.getLogger(Example.class);

    // 3. 实例变量（按访问级别：public → protected → package → private）
    private Long id;
    private String name;

    // 4. 构造函数
    public Example() { }
    public Example(Long id) { this.id = id; }

    // 5. 静态方法
    public static Example create() { return new Example(); }

    // 6. 实例方法（公共方法 → 私有方法）
    public void doSomething() { }
    private void helperMethod() { }

    // 7. getter/setter（放最后或使用 Lombok）
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
}
```

### import 规范
- 不使用通配符 `import *`（IDE 自动管理除外）
- 静态导入单独分组
- 按字母顺序排列

```java
// ✅ 好
import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

import com.qiandao.model.User;

import static org.junit.jupiter.api.Assertions.assertEquals;
```

### 项目结构（Maven 标准）

<!-- [注释] 遵循 Maven 约定优于配置 -->

```
project/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/project/
│   │   │       ├── controller/      # Web 层
│   │   │       ├── service/         # 业务层
│   │   │       │   └── impl/
│   │   │       ├── repository/      # 数据访问层
│   │   │       ├── model/           # 领域模型
│   │   │       │   ├── entity/      # JPA 实体
│   │   │       │   ├── dto/         # 数据传输对象
│   │   │       │   └── vo/          # 视图对象
│   │   │       ├── config/          # 配置类
│   │   │       └── util/            # 工具类
│   │   └── resources/
│   │       └── application.yml
│   └── test/
│       └── java/
└── pom.xml
```

## 异常处理

<!-- [注释] 异常处理是 Java 开发的重点 -->

### 基本原则
- 优先使用标准异常
- 不要捕获 `Exception` 或 `Throwable`（除非在最顶层）
- 不要忽略异常（空 catch 块）
- 异常信息要有意义

```java
// ✅ 好：捕获具体异常，添加上下文
try {
    user = userRepository.findById(id);
} catch (DataAccessException e) {
    throw new ServiceException("Failed to find user: " + id, e);
}

// ✅ 好：资源自动关闭
try (InputStream is = new FileInputStream(file)) {
    // 使用资源
}

// ❌ 差：捕获过宽
try {
    doSomething();
} catch (Exception e) {  // 太宽泛
    e.printStackTrace(); // 不要用 printStackTrace
}

// ❌ 差：忽略异常
try {
    doSomething();
} catch (IOException e) {
    // 空的 catch 块，异常被吞掉
}
```

### 自定义异常
- 业务异常继承 `RuntimeException`
- 必须提供有意义的消息

```java
public class BusinessException extends RuntimeException {
    private final String errorCode;

    public BusinessException(String errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }

    public BusinessException(String errorCode, String message, Throwable cause) {
        super(message, cause);
        this.errorCode = errorCode;
    }

    public String getErrorCode() {
        return errorCode;
    }
}
```

## 空值处理

<!-- [注释] NPE 是 Java 最常见的错误，需特别注意 -->

### 基本原则
- 优先使用 `Optional` 表示可能为空的返回值
- 参数校验放在方法开头
- 使用 `Objects.requireNonNull()` 快速失败

```java
// ✅ 好：使用 Optional
public Optional<User> findById(Long id) {
    return userRepository.findById(id);
}

// ✅ 好：参数校验
public void updateUser(User user) {
    Objects.requireNonNull(user, "user must not be null");
    Objects.requireNonNull(user.getId(), "user.id must not be null");
    // ...
}

// ✅ 好：安全的空值处理
String name = Optional.ofNullable(user)
    .map(User::getName)
    .orElse("Unknown");

// ❌ 差：返回 null 表示"没找到"
public User findById(Long id) {
    return userRepository.findById(id).orElse(null);  // 调用方容易忘记判空
}
```

## 注释规范

<!-- [注释] Javadoc 是 Java 文档的标准方式 -->

### Javadoc
- 所有公共 API 必须有 Javadoc
- 描述"做什么"而非"怎么做"

```java
/**
 * Finds a user by their unique identifier.
 *
 * @param id the user's unique identifier, must not be null
 * @return an Optional containing the user if found, empty otherwise
 * @throws IllegalArgumentException if id is null
 */
public Optional<User> findById(Long id) {
    // ...
}
```

### 行内注释
- 解释"为什么"而非"是什么"
- 避免废话注释

```java
// ✅ 好：解释原因
// 使用同步块而非 ConcurrentHashMap，因为需要原子地检查并更新多个字段
synchronized (lock) {
    // ...
}

// ❌ 差：废话注释
// 获取用户 ID
Long userId = user.getId();  // 代码已经很清楚了
```

## 并发编程

<!-- [注释] Java 并发是复杂话题，以下是基本原则 -->

### 基本原则
- 优先使用高层并发工具（`ExecutorService`、`CompletableFuture`）
- 避免直接使用 `Thread`、`wait/notify`
- 使用线程安全的集合（`ConcurrentHashMap`、`CopyOnWriteArrayList`）

```java
// ✅ 好：使用 ExecutorService
ExecutorService executor = Executors.newFixedThreadPool(10);
Future<Result> future = executor.submit(() -> doWork());

// ✅ 好：使用 CompletableFuture
CompletableFuture<User> future = CompletableFuture
    .supplyAsync(() -> findUser(id))
    .thenApply(user -> enrichUser(user));

// ❌ 差：直接创建线程
new Thread(() -> doWork()).start();  // 没有生命周期管理
```

### 线程安全
- 优先使用不可变对象
- 使用 `@ThreadSafe`、`@NotThreadSafe` 注解标记（如果项目引入了 JSR-305）

```java
// ✅ 不可变对象是线程安全的
public final class User {
    private final Long id;
    private final String name;

    public User(Long id, String name) {
        this.id = id;
        this.name = name;
    }

    // 只有 getter，没有 setter
}
```

## 测试规范

<!-- [注释] 使用 JUnit 5 + Mockito -->

### 测试方法命名
- 描述测试场景和预期结果
- 使用 `@DisplayName` 提供可读描述

```java
class UserServiceTest {

    @Test
    @DisplayName("根据 ID 查找用户 - 用户存在时返回用户")
    void findById_whenUserExists_returnsUser() {
        // given
        Long userId = 1L;
        User expected = new User(userId, "test");
        when(userRepository.findById(userId)).thenReturn(Optional.of(expected));

        // when
        Optional<User> result = userService.findById(userId);

        // then
        assertThat(result).isPresent();
        assertThat(result.get().getName()).isEqualTo("test");
    }

    @Test
    @DisplayName("根据 ID 查找用户 - 用户不存在时返回空")
    void findById_whenUserNotExists_returnsEmpty() {
        // given
        when(userRepository.findById(anyLong())).thenReturn(Optional.empty());

        // when
        Optional<User> result = userService.findById(999L);

        // then
        assertThat(result).isEmpty();
    }
}
```

### 测试结构
- 使用 Given-When-Then 或 Arrange-Act-Assert 模式
- 每个测试只验证一个行为

```java
@Test
void createOrder_withValidData_createsAndReturnsOrder() {
    // Given (Arrange)
    OrderRequest request = new OrderRequest(/* ... */);
    when(productService.checkStock(anyLong())).thenReturn(true);

    // When (Act)
    Order result = orderService.createOrder(request);

    // Then (Assert)
    assertThat(result).isNotNull();
    assertThat(result.getStatus()).isEqualTo(OrderStatus.CREATED);
    verify(orderRepository).save(any(Order.class));
}
```

## 日志规范

<!-- [注释] 使用 SLF4J + Logback/Log4j2 -->

### 基本原则
- 使用 SLF4J 作为日志门面
- 使用参数化日志，避免字符串拼接
- 选择合适的日志级别

```java
// ✅ 好：参数化日志
private static final Logger log = LoggerFactory.getLogger(UserService.class);

log.debug("Finding user by id: {}", userId);
log.info("User {} logged in successfully", username);
log.warn("Failed to send email to {}, will retry", email);
log.error("Failed to process order {}", orderId, exception);

// ❌ 差：字符串拼接（即使不输出也会执行拼接）
log.debug("Finding user by id: " + userId);
```

### 日志级别
- `ERROR`: 系统错误，需要立即关注
- `WARN`: 警告，可能的问题
- `INFO`: 重要业务事件
- `DEBUG`: 调试信息
- `TRACE`: 详细追踪信息

## Spring 相关规范

<!-- [注释] 如果项目使用 Spring，以下是补充规范 -->

### 依赖注入
- 优先使用构造函数注入
- 使用 Lombok 的 `@RequiredArgsConstructor` 简化

```java
// ✅ 好：构造函数注入
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;

    // 不需要 @Autowired，Spring 4.3+ 自动注入
}

// ❌ 差：字段注入
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;  // 不利于测试
}
```

### REST Controller
- 使用 `@RestController` 而非 `@Controller` + `@ResponseBody`
- 路径使用小写和连字符: `/api/user-profiles`

```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping("/{id}")
    public ResponseEntity<UserDto> findById(@PathVariable Long id) {
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<UserDto> create(@Valid @RequestBody CreateUserRequest request) {
        UserDto created = userService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
}
```

## 性能考虑

<!-- [注释] 先写正确的代码，再优化性能 -->

### 核心原则

| 原则 | 说明 |
|------|------|
| **先正确后优化** | 先确保功能正确，再考虑性能 |
| **先测量后优化** | 用 JProfiler/VisualVM 定位瓶颈 |
| **避免过早优化** | 可读性优先，除非有明确的性能需求 |

### 数据库查询优化

```java
// ❌ N+1 查询问题
List<User> users = userRepository.findAll();
for (User user : users) {
    List<Order> orders = orderRepository.findByUserId(user.getId());
}

// ✅ 使用 JOIN FETCH 或 @EntityGraph
@Query("SELECT u FROM User u LEFT JOIN FETCH u.orders")
List<User> findAllWithOrders();

// ✅ 或使用 @EntityGraph
@EntityGraph(attributePaths = {"orders"})
List<User> findAll();

// ✅ 批量查询
List<Long> userIds = users.stream().map(User::getId).toList();
List<Order> orders = orderRepository.findByUserIdIn(userIds);
Map<Long, List<Order>> orderMap = orders.stream()
    .collect(Collectors.groupingBy(Order::getUserId));
```

### 集合与 Stream 优化

```java
// ✅ 选择合适的集合类型
List<User> users = new ArrayList<>(expectedSize);  // 预分配容量
Set<String> unique = new HashSet<>(expectedSize);  // O(1) 查找
Map<Long, User> userMap = new HashMap<>(expectedSize);

// ❌ 差：多次遍历
long count = list.stream().filter(x -> x > 0).count();
List<Integer> filtered = list.stream().filter(x -> x > 0).toList();

// ✅ 好：单次遍历收集多个结果
record Stats(long count, List<Integer> filtered) {}
Stats stats = list.stream()
    .filter(x -> x > 0)
    .collect(Collectors.teeing(
        Collectors.counting(),
        Collectors.toList(),
        Stats::new
    ));

// ❌ 差：频繁装箱拆箱
List<Integer> numbers = ...;
int sum = numbers.stream().mapToInt(Integer::intValue).sum();

// ✅ 好：使用原始类型流
int[] numbers = ...;
int sum = Arrays.stream(numbers).sum();
```

### 字符串处理

```java
// ❌ 差：循环拼接字符串
String result = "";
for (String s : strings) {
    result += s;  // 每次创建新对象
}

// ✅ 好：使用 StringBuilder
StringBuilder sb = new StringBuilder(estimatedSize);
for (String s : strings) {
    sb.append(s);
}
String result = sb.toString();

// ✅ 好：使用 String.join 或 Collectors.joining
String result = String.join(",", strings);
String result = strings.stream().collect(Collectors.joining(","));
```

### 连接池配置

```yaml
# HikariCP 推荐配置
spring:
  datasource:
    hikari:
      maximum-pool-size: 10          # CPU 核心数 * 2
      minimum-idle: 5
      idle-timeout: 300000           # 5 分钟
      connection-timeout: 20000      # 20 秒
      max-lifetime: 1200000          # 20 分钟
```

### 避免常见陷阱

| 陷阱 | 解决方案 |
|------|---------|
| N+1 查询 | 使用 JOIN FETCH 或批量查询 |
| 循环中拼接字符串 | 使用 `StringBuilder` |
| 频繁装箱拆箱 | 使用原始类型或原始类型流 |
| 未指定集合初始容量 | `new ArrayList<>(size)` |
| 同步方法粒度过大 | 缩小同步块范围 |
| 未关闭资源 | 使用 try-with-resources |

### 性能分析工具

```bash
# JVM 参数（开发环境）
-XX:+PrintGCDetails -XX:+PrintGCTimeStamps

# 使用 VisualVM 或 JProfiler 进行分析
# 或使用 async-profiler
./profiler.sh -d 30 -f profile.html <pid>
```

## 规则溯源要求

当回复明确受到本规则约束时，在回复末尾声明：

```
> 📋 本回复遵循规则：`java-style.md` - [具体章节]
```

---

## 参考资料

- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- [阿里巴巴 Java 开发手册](https://github.com/alibaba/p3c)
- [Effective Java (3rd Edition)](https://www.oreilly.com/library/view/effective-java/9780134686097/)
- [Spring Boot Best Practices](https://docs.spring.io/spring-boot/docs/current/reference/html/)
