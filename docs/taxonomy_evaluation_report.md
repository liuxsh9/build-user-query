# SFT 训练数据标注能力分类体系评估报告

> 版本: 1.0 | 日期: 2026-02-13
> 评估对象: 7 类别 198 标签的 Capability Taxonomy
> 评估方法: 模拟标注 + 覆盖率分析 + 专家评审

---

## 目录

1. [模拟查询（10 条）](#1-模拟查询)
2. [模拟 Claude Code 响应轨迹](#2-模拟-claude-code-响应轨迹)
3. [标注结果](#3-标注结果)
4. [分析](#4-分析)
5. [专家评估](#5-专家评估)

---

## 1. 模拟查询

### Query 1 — 竞赛选手（算法题）

> 这道题要求在一个 n×n 的网格上找最短路径，但有些格子有传送门可以瞬移到另一个格子。我写了个 BFS 但是 TLE 了，n 最大 1000。能帮我看看怎么优化吗？附上我的代码：
>
> ```cpp
> #include <bits/stdc++.h>
> using namespace std;
> int bfs(vector<vector<int>>& grid, map<pair<int,int>, pair<int,int>>& portals) {
>     // ... 标准 BFS 实现，但对传送门处理有冗余 ...
> }
> ```

### Query 2 — 资深后端工程师（生产系统问题）

> 线上 Go 服务出现间歇性 goroutine 泄漏，pprof 显示 goroutine 数量在 24h 内从 200 涨到 50000+。初步排查发现是 gRPC streaming 相关的，但具体哪个 stream 没 close 还没定位到。服务用了 go-micro 框架，有 Redis pub/sub 和 Kafka consumer。麻烦帮我分析下可能的泄漏点，给个排查方案。

### Query 3 — 数据科学家（ML Pipeline）

> 我在用 PyTorch 训练一个多模态模型（文本+图像），训练到第 3 个 epoch 的时候 loss 突然变成 NaN。用的是 mixed precision training (fp16)，batch size 64，lr 1e-4 with cosine scheduler。数据预处理用的 HuggingFace datasets。能帮我排查下 NaN 的常见原因吗？另外我想加 gradient clipping，应该加在哪里？

### Query 4 — 前端初级开发者（UI 组件）

> 大佬求助！我在写一个 React 的无限滚动列表组件，但是滚动的时候特别卡，而且有时候会重复加载数据。我用的是 useEffect + IntersectionObserver，状态管理用的 useState。代码大概长这样：
>
> ```jsx
> function InfiniteList() {
>   const [items, setItems] = useState([]);
>   const [page, setPage] = useState(1);
>   const observerRef = useRef();
>
>   useEffect(() => {
>     const observer = new IntersectionObserver((entries) => {
>       if (entries[0].isIntersecting) {
>         setPage(p => p + 1);
>       }
>     });
>     observer.observe(observerRef.current);
>     return () => observer.disconnect();
>   }, []);
>
>   useEffect(() => {
>     fetch(`/api/items?page=${page}`).then(r => r.json()).then(data => {
>       setItems(prev => [...prev, ...data]);
>     });
>   }, [page]);
>
>   return <div>{items.map(i => <Item key={i.id} {...i} />)}{<div ref={observerRef} />}</div>;
> }
> ```
>
> 怎么优化啊？虚拟滚动要不要上？

### Query 5 — DevOps 工程师（基础设施）

> Need to set up a multi-region Kubernetes deployment with the following requirements:
> - 3 regions (us-east-1, eu-west-1, ap-southeast-1)
> - Global load balancing with failover
> - Shared PostgreSQL with read replicas per region
> - GitOps workflow using ArgoCD
> - Terraform for infrastructure provisioning
>
> Can you generate the base Terraform modules and ArgoCD ApplicationSet manifests? We're on AWS EKS.

### Query 6 — 嵌入式工程师（固件开发）

> 我在 STM32F407 上用 FreeRTOS 写一个电机控制器，需要实现 FOC（磁场定向控制）算法。现在 ADC 采样和 PWM 输出的时序对不上，导致电流环控制不稳定。ADC 用的 DMA 双缓冲模式，PWM 是 TIM1 的互补输出。中断优先级我设的 ADC > TIM > UART。
>
> 另外 Clarke/Park 变换的定点数实现精度不够，用的 Q15 格式。能帮我看看时序问题怎么解决，以及定点数精度怎么提升到 Q31 吗？

### Query 7 — 安全研究员（漏洞分析）

> I'm auditing a Node.js Express application and found a potential prototype pollution vulnerability in the deep merge utility:
>
> ```javascript
> function deepMerge(target, source) {
>   for (let key in source) {
>     if (typeof source[key] === 'object' && source[key] !== null) {
>       if (!target[key]) target[key] = {};
>       deepMerge(target[key], source[key]);
>     } else {
>       target[key] = source[key];
>     }
>   }
>   return target;
> }
> ```
>
> This is used to merge user-supplied JSON config with defaults. I need:
> 1. A PoC demonstrating the exploit
> 2. Impact analysis — can this escalate to RCE?
> 3. A secure fix that maintains functionality

### Query 8 — 移动开发者（跨平台应用）

> 我们团队要用 Flutter 开发一个健康管理 App，需要接入以下硬件：
> - 蓝牙心率带（BLE）
> - Apple HealthKit / Google Fit
> - 手机陀螺仪和加速度计
>
> 架构上想用 Riverpod 做状态管理，数据本地存储用 Drift (SQLite)，后端 API 用 Dio。
> 请帮我设计一下整体架构，特别是 BLE 连接管理和传感器数据的实时处理 pipeline。需要考虑后台运行和电量优化。

### Query 9 — 游戏开发者（引擎功能）

> 在用 Rust + wgpu 写一个 2D 游戏引擎，现在要实现一个 ECS (Entity Component System)。基本的 World、Entity、Component 存储已经有了，用的是 SparseSet。现在需要加 System 调度器，要求：
>
> 1. 支持 system 之间的依赖声明
> 2. 自动并行执行无冲突的 system（基于 component 读写分析）
> 3. 支持 exclusive system（独占 World 访问）
>
> 参考了 bevy_ecs 的设计但想简化。能帮我设计 System trait 和 Scheduler 的核心数据结构吗？

### Query 10 — Tech Lead（代码审查 / 架构评审）

> 团队提交了一个 PR，把我们的单体 Java Spring Boot 应用拆成微服务。PR 改了 200+ 个文件，主要变更：
>
> 1. 把 `OrderService`, `PaymentService`, `InventoryService` 拆成独立的 Spring Boot 应用
> 2. 服务间通信从方法调用改成了 REST + Kafka 事件
> 3. 数据库从共享 MySQL 拆成每个服务独立的库
> 4. 加了 Spring Cloud Gateway 做 API 网关
>
> 我需要你帮我 review 这个架构变更，重点关注：
> - 分布式事务一致性（原来用的 @Transactional 现在怎么保证？）
> - 服务拆分粒度是否合理
> - 数据迁移方案是否有数据丢失风险
> - 性能影响评估（网络延迟、序列化开销）

---

## 2. 模拟 Claude Code 响应轨迹

### Response 1 — 竞赛算法优化

1. **Read** 用户提供的 BFS 代码
2. **分析** 时间复杂度：标准 BFS O(n²) 但传送门处理导致重复入队
3. **File Write** 优化后的代码：使用 0-1 BFS (deque)，传送门边权为 0，普通移动边权为 1
4. **代码解释** 说明 0-1 BFS 的原理和为什么适合这个场景
5. **补充** 提供复杂度分析 O(n²) 和边界情况处理

### Response 2 — Goroutine 泄漏排查

1. **Web Search** 搜索 go-micro gRPC stream goroutine leak 已知问题
2. **分析** 列出 3 个常见泄漏点：未关闭的 stream、context 未传播、Kafka consumer group rebalance
3. **Code Write** 提供排查脚本：runtime.NumGoroutine() 监控 + pprof goroutine dump 分析
4. **Code Write** 提供修复模板：确保 stream.Close() 在 defer 中、context 超时设置、Kafka consumer 优雅关闭
5. **Bash** 建议运行 `go tool pprof -http=:8080 http://localhost:6060/debug/pprof/goroutine`

### Response 3 — PyTorch NaN 排查

1. **分析** 列出 mixed precision 下 NaN 的常见原因：loss scaling overflow、数据中有 inf/nan、学习率过大
2. **Code Write** 提供诊断代码片段：`torch.autograd.detect_anomaly()` 启用、gradient norm 监控
3. **Code Write** 提供 gradient clipping 的正确位置（在 `scaler.unscale_()` 之后、`scaler.step()` 之前）
4. **Code Write** 提供数据验证脚本检查 dataset 中的异常值
5. **补充** 建议降低 lr 到 5e-5 并使用 warmup

### Response 4 — React 无限滚动优化

1. **Read** 用户代码，识别问题：缺少 loading 状态防重复、未做 cleanup、无虚拟化
2. **File Write** 重写组件：添加 `isLoading` ref 防重复请求、`useCallback` 优化
3. **Code Write** 提供 `react-window` 虚拟滚动集成方案
4. **代码解释** 解释为什么 `useState` 的 page 变化会触发重复 fetch
5. **补充** 建议使用 `useSWRInfinite` 或 `@tanstack/react-query` 的 `useInfiniteQuery`

### Response 5 — 多区域 K8s 部署

1. **File Write** `modules/eks-cluster/main.tf` — EKS 集群 Terraform 模块
2. **File Write** `modules/rds-postgres/main.tf` — RDS + 跨区域只读副本
3. **File Write** `modules/global-lb/main.tf` — Route53 + Global Accelerator
4. **File Write** `argocd/applicationset.yaml` — ArgoCD ApplicationSet 多集群配置
5. **File Write** `environments/us-east-1/terraform.tfvars` 等环境变量文件
6. **Bash** 提供 `terraform init && terraform plan` 验证命令

### Response 6 — STM32 FOC 控制

1. **分析** ADC-PWM 时序问题：DMA 双缓冲的半传输/全传输中断与 PWM 周期的同步
2. **Code Write** 修改 TIM1 配置：使用 ADC 注入通道由 TIM1 TRGO 触发，确保采样在 PWM 中心对齐
3. **Code Write** Q15 → Q31 的 Clarke/Park 变换实现，使用 CMSIS-DSP 库的 `arm_park_q31()`
4. **Code Write** 中断优先级调整建议：ADC 和 TIM 同优先级，用 DMA 减少 CPU 中断负载
5. **补充** 提供时序图说明采样点与 PWM 周期的关系

### Response 7 — Prototype Pollution 分析

1. **Read** 分析 deepMerge 函数的漏洞
2. **Code Write** PoC：`deepMerge({}, JSON.parse('{"__proto__":{"isAdmin":true}}'))`
3. **分析** RCE 可能性：如果配合 `child_process` 或模板引擎（如 EJS），可以实现 RCE
4. **Code Write** 安全修复：添加 `__proto__`, `constructor`, `prototype` 键过滤 + 使用 `Object.create(null)`
5. **补充** 建议使用成熟库如 `lodash.merge`（但注意其历史 CVE）或 `structuredClone`

### Response 8 — Flutter 健康 App 架构

1. **File Write** `lib/core/architecture.dart` — 分层架构图和目录结构
2. **File Write** `lib/services/ble_manager.dart` — BLE 连接管理器骨架（使用 `flutter_blue_plus`）
3. **File Write** `lib/services/sensor_pipeline.dart` — 传感器数据 Stream 处理 pipeline
4. **File Write** `lib/providers/health_providers.dart` — Riverpod provider 定义
5. **Code Write** 后台运行方案：`flutter_background_service` + `WorkManager` 配置
6. **补充** 电量优化策略：BLE 扫描间隔动态调整、传感器采样率降级

### Response 9 — Rust ECS System 调度器

1. **分析** 设计 System trait 和 access 声明机制
2. **File Write** `src/system.rs` — `System` trait 定义 + `SystemMeta`（component 读写声明）
3. **File Write** `src/scheduler.rs` — 基于拓扑排序的依赖解析 + 基于 access 冲突检测的并行分组
4. **Code Write** `ExclusiveSystem` trait 和调度器中的 barrier 机制
5. **Bash** `cargo check` 验证编译
6. **补充** 与 bevy_ecs 的设计对比和简化取舍说明

### Response 10 — 微服务架构 Review

1. **分析** 分布式事务：建议 Saga 模式替代 @Transactional，给出 Order→Payment→Inventory 的补偿流程
2. **分析** 拆分粒度评估：Order 和 Payment 耦合度高，建议考虑是否合并
3. **分析** 数据迁移风险：双写期间的一致性、外键约束丢失后的数据完整性
4. **Code Write** 提供 Saga 编排器的伪代码框架
5. **分析** 性能影响：估算 REST 调用增加的 p99 延迟（~5-20ms per hop）、JSON 序列化开销
6. **补充** 建议分阶段迁移：先拆 Inventory（耦合最低），验证后再拆 Payment

---

## 3. 标注结果

### 总览表

| # | Language | Concept | Domain | Agentic | Constraint | Task | Context |
|---|----------|---------|--------|---------|------------|------|---------|
| Q1 | cpp | algorithms, data-structures, control-flow | — | file-read, file-write, code-execution | performance-optimized, no-recursion | code-refactoring, optimization | single-function |
| Q2 | go | concurrency, error-handling, memory-management | cloud-computing, web-backend | web-search, file-write, bash-execution, code-execution | fault-tolerant, observable | bug-fixing, monitoring | repository |
| Q3 | python | algorithms, type-system, error-handling | machine-learning, data-science | web-search, file-write, code-execution | performance-optimized, type-safe | bug-fixing, configuration | multi-file |
| Q4 | javascript, typescript | control-flow, design-patterns, iterators | web-frontend | file-read, file-write | performance-optimized, accessible | code-refactoring, feature-implementation | single-file |
| Q5 | hcl, yaml | architecture | cloud-computing, devops | file-write, bash-execution, multi-file-coordination, planning | scalable, fault-tolerant, portable | configuration, deployment, feature-implementation | greenfield |
| Q6 | c | concurrency, memory-management, type-system | embedded-systems, real-time-systems | file-write, code-execution | performance-optimized, no-dynamic-allocation, deterministic, thread-safe | bug-fixing, optimization | module |
| Q7 | javascript | security, metaprogramming | cybersecurity, web-backend | file-read, file-write, web-search | type-safe | security-audit, bug-fixing | single-function |
| Q8 | dart | architecture, design-patterns, concurrency, data-structures | mobile-development, iot | file-write, planning, multi-file-coordination | performance-optimized, portable, fault-tolerant | feature-implementation, api-design, schema-design | greenfield |
| Q9 | rust | concurrency, data-structures, design-patterns, type-system, ownership, iterators | game-development, systems-programming | file-write, bash-execution, planning | thread-safe, performance-optimized, type-safe | feature-implementation, api-design | module |
| Q10 | java | architecture, design-patterns, concurrency, error-handling, database-concepts | web-backend, e-commerce | file-read, planning, multi-file-coordination | scalable, fault-tolerant, backward-compatible | code-review-task, migration | repository |

### 详细标注

#### Q1: 竞赛选手 — BFS 优化

| Category | Tags |
|----------|------|
| Language | `cpp` |
| Concept | `algorithms`, `data-structures`, `control-flow` |
| Domain | _(无)_ |
| Agentic | `file-read`, `file-write`, `code-execution` |
| Constraint | `performance-optimized`, `no-recursion` |
| Task | `code-refactoring`, `optimization` |
| Context | `single-function` |

#### Q2: 后端工程师 — Goroutine 泄漏

| Category | Tags |
|----------|------|
| Language | `go` |
| Concept | `concurrency`, `error-handling`, `memory-management` |
| Domain | `cloud-computing`, `web-backend` |
| Agentic | `web-search`, `file-write`, `bash-execution`, `code-execution` |
| Constraint | `fault-tolerant`, `observable` |
| Task | `bug-fixing`, `monitoring` |
| Context | `repository` |

#### Q3: 数据科学家 — NaN Loss

| Category | Tags |
|----------|------|
| Language | `python` |
| Concept | `algorithms`, `type-system`, `error-handling` |
| Domain | `machine-learning`, `data-science` |
| Agentic | `web-search`, `file-write`, `code-execution` |
| Constraint | `performance-optimized`, `type-safe` |
| Task | `bug-fixing`, `configuration` |
| Context | `multi-file` |

#### Q4: 前端初级开发者 — 无限滚动

| Category | Tags |
|----------|------|
| Language | `javascript`, `typescript` |
| Concept | `control-flow`, `design-patterns`, `iterators` |
| Domain | `web-frontend` |
| Agentic | `file-read`, `file-write` |
| Constraint | `performance-optimized`, `accessible` |
| Task | `code-refactoring`, `feature-implementation` |
| Context | `single-file` |

#### Q5: DevOps 工程师 — 多区域 K8s

| Category | Tags |
|----------|------|
| Language | `hcl`, `yaml` |
| Concept | `architecture` |
| Domain | `cloud-computing`, `devops` |
| Agentic | `file-write`, `bash-execution`, `multi-file-coordination`, `planning` |
| Constraint | `scalable`, `fault-tolerant`, `portable` |
| Task | `configuration`, `deployment`, `feature-implementation` |
| Context | `greenfield` |

#### Q6: 嵌入式工程师 — FOC 控制

| Category | Tags |
|----------|------|
| Language | `c` |
| Concept | `concurrency`, `memory-management`, `type-system` |
| Domain | `embedded-systems`, `real-time-systems` |
| Agentic | `file-write`, `code-execution` |
| Constraint | `performance-optimized`, `no-dynamic-allocation`, `deterministic`, `thread-safe` |
| Task | `bug-fixing`, `optimization` |
| Context | `module` |

#### Q7: 安全研究员 — Prototype Pollution

| Category | Tags |
|----------|------|
| Language | `javascript` |
| Concept | `security`, `metaprogramming` |
| Domain | `cybersecurity`, `web-backend` |
| Agentic | `file-read`, `file-write`, `web-search` |
| Constraint | `type-safe` |
| Task | `security-audit`, `bug-fixing` |
| Context | `single-function` |

#### Q8: 移动开发者 — Flutter 健康 App

| Category | Tags |
|----------|------|
| Language | `dart` |
| Concept | `architecture`, `design-patterns`, `concurrency`, `data-structures` |
| Domain | `mobile-development`, `iot` |
| Agentic | `file-write`, `planning`, `multi-file-coordination` |
| Constraint | `performance-optimized`, `portable`, `fault-tolerant` |
| Task | `feature-implementation`, `api-design`, `schema-design` |
| Context | `greenfield` |

#### Q9: 游戏开发者 — ECS 调度器

| Category | Tags |
|----------|------|
| Language | `rust` |
| Concept | `concurrency`, `data-structures`, `design-patterns`, `type-system`, `ownership`, `iterators` |
| Domain | `game-development`, `systems-programming` |
| Agentic | `file-write`, `bash-execution`, `planning` |
| Constraint | `thread-safe`, `performance-optimized`, `type-safe` |
| Task | `feature-implementation`, `api-design` |
| Context | `module` |

#### Q10: Tech Lead — 微服务架构 Review

| Category | Tags |
|----------|------|
| Language | `java` |
| Concept | `architecture`, `design-patterns`, `concurrency`, `error-handling`, `database-concepts` |
| Domain | `web-backend`, `e-commerce` |
| Agentic | `file-read`, `planning`, `multi-file-coordination` |
| Constraint | `scalable`, `fault-tolerant`, `backward-compatible` |
| Task | `code-review-task`, `migration` |
| Context | `repository` |

---

## 4. 分析

### 4.1 标签覆盖率

10 条样本共命中的去重标签统计：

| Category | 总标签数 | 命中数 | 覆盖率 | 命中的标签 |
|----------|---------|--------|--------|-----------|
| Language (75) | 75 | 10 | 13.3% | cpp, go, python, javascript, typescript, hcl, yaml, c, dart, rust, java |
| Concept (21) | 21 | 13 | 61.9% | algorithms, data-structures, control-flow, concurrency, error-handling, memory-management, type-system, design-patterns, iterators, architecture, security, metaprogramming, database-concepts, ownership |
| Domain (31) | 31 | 13 | 41.9% | cloud-computing, web-backend, machine-learning, data-science, web-frontend, devops, embedded-systems, real-time-systems, cybersecurity, mobile-development, iot, game-development, systems-programming, e-commerce |
| Agentic (24) | 24 | 9 | 37.5% | file-read, file-write, code-execution, web-search, bash-execution, multi-file-coordination, planning, tool-selection (隐含), iterative-refinement (隐含) |
| Constraint (19) | 19 | 10 | 52.6% | performance-optimized, no-recursion, fault-tolerant, observable, type-safe, accessible, scalable, portable, no-dynamic-allocation, deterministic, thread-safe, backward-compatible |
| Task (18) | 18 | 12 | 66.7% | code-refactoring, optimization, bug-fixing, monitoring, configuration, feature-implementation, deployment, security-audit, api-design, schema-design, code-review-task, migration |
| Context (10) | 10 | 6 | 60.0% | single-function, repository, multi-file, single-file, greenfield, module |

**总计：198 个标签中命中约 73 个，总覆盖率约 36.9%。**

### 4.2 类别密度分析

#### 高密度类别（标注时经常被选中，每条样本平均命中多个标签）

- **Concept**: 平均每条样本命中 3.4 个标签，是最"密集"的类别。这符合预期——任何编程任务都涉及多个概念。21 个标签的规模恰当，既不过于细碎也不过于笼统。
- **Constraint**: 平均每条样本命中 2.4 个标签。约束条件天然具有叠加性（一个系统可以同时要求高性能、线程安全、可扩展）。
- **Task**: 平均每条样本命中 2.0 个标签。多数查询涉及复合任务（如 bug-fixing + optimization）。

#### 低密度类别（标注时选择较少）

- **Language**: 平均每条样本命中 1.2 个标签。这是正常的——大多数查询聚焦于 1-2 种语言。但 75 个标签中仅命中 10 个（13.3%），说明长尾语言（如 ada, apl, cobol, fortran 等）在日常查询中极少出现。
- **Context**: 单选类别，每条样本恰好 1 个标签。6/10 的覆盖率说明分类粒度合理。

#### 中等密度类别

- **Domain**: 平均每条样本命中 1.6 个标签。跨领域查询（如 Q8 的 mobile + IoT）自然产生多标签。
- **Agentic**: 平均每条样本命中 2.8 个标签，但集中在少数高频标签（file-write 出现 10/10，planning 出现 4/10）。

### 4.3 分类体系不足之处

#### 场景 1: 竞赛编程（Q1）缺少 Domain 标签

竞赛编程（competitive programming）是一个明确的场景，但在 31 个 Domain 标签中没有对应项。最接近的是 `scientific-computing`，但语义不匹配。类似地，**教育/教学**（educational）场景也缺失。

#### 场景 2: 硬件交互（Q6）概念覆盖不足

嵌入式开发中的核心概念如**中断处理（interrupt handling）**、**DMA**、**定点数运算（fixed-point arithmetic）**、**实时调度（real-time scheduling）**在 Concept 类别中没有对应标签。现有的 `concurrency` 过于笼统，无法区分 OS 级并发和硬件中断级并发。

#### 场景 3: 架构评审（Q10）Task 粒度不足

`code-review-task` 无法区分"代码级 review"和"架构级 review"。后者涉及系统设计决策、服务拆分策略、数据一致性模型等，与逐行代码审查有本质区别。

#### 场景 4: 数据处理管道（Q3）缺少 Concept

`data-pipeline`、`feature-engineering`、`model-training` 等 ML 工作流概念在 Concept 中缺失。现有标签只能用 `algorithms` 笼统覆盖。

### 4.4 冗余标签分析

即使在 10 条高度多样化的样本中，以下标签仍显得冗余或区分度不足：

| 标签对 | 问题 |
|--------|------|
| `optimization` (Task) vs `performance-optimized` (Constraint) | 语义高度重叠。前者是"做优化这件事"，后者是"要求高性能"。在实际标注中几乎总是同时出现或容易混淆。建议明确：Task 描述"做什么"，Constraint 描述"满足什么要求"。 |
| `code-refactoring` (Task) vs Agentic 中的 `refactoring` 行为 | 实际 YAML 中 Agentic 有 `refactoring` 标签，与 Task 的 `code-refactoring` 语义重叠。跨类别冗余。 |
| `search` (Agentic) vs `web-search` (Agentic) vs `code-search` (Agentic) | 实际 YAML 中存在三个搜索相关标签。`search` 过于笼统，与另外两个形成包含关系而非并列关系。 |
| `scalable` (Constraint) vs `performance-optimized` (Constraint) | 在分布式系统场景中经常同时出现，但语义确实不同（水平扩展 vs 单机性能）。保留但需要更清晰的标注指南。 |

### 4.5 能力缺口

通过 10 条样本暴露的分类体系能力缺口：

1. **难度/复杂度维度缺失**: 分类体系没有表达查询难度的维度。Q1（算法优化）和 Q4（React 组件）的技术深度差异巨大，但无法通过标签体现。建议增加 `Difficulty` 类别（如 beginner / intermediate / advanced / expert）。

2. **用户意图维度缺失**: 用户是要"学习理解"还是"解决生产问题"？Q1 的学生和 Q2 的工程师有本质不同的意图，但标签体系无法区分。可考虑增加 `Intent` 类别（如 learning, debugging, building, reviewing, exploring）。

3. **交互模式维度缺失**: 有些查询期望一次性完整回答（Q1），有些期望多轮迭代（Q10 的架构 review）。分类体系没有捕捉这种交互模式差异。

4. **Library/Framework 维度在用户指定版本中被移除**: 用户给出的 198 标签版本不包含 Library 类别，但实际 YAML 中存在。Q3 涉及 PyTorch、HuggingFace，Q4 涉及 React，Q8 涉及 Flutter/Riverpod/Drift——这些框架信息对 SFT 训练极其重要，缺失会导致严重的信息损失。

5. **输出格式维度缺失**: 有些查询期望代码（Q9），有些期望分析报告（Q10），有些期望诊断步骤（Q2）。输出格式对训练数据的质量评估很重要。

---

## 5. 专家评估

### 5.1 评估背景

本评估从 SFT（Supervised Fine-Tuning）训练数据标注的实际需求出发，对该 7 类别 198 标签的能力分类体系进行独立评审。评估标准包括：完备性、正交性、可操作性、可扩展性和实际标注效率。

### 5.2 优势

#### (1) 正交性设计合理

7 个类别之间的正交性总体良好。Language 描述"用什么语言"，Concept 描述"涉及什么知识"，Domain 描述"在什么领域"，Task 描述"做什么事"，Constraint 描述"满足什么约束"，Agentic 描述"Agent 做了什么"，Context 描述"代码规模"。这种多维正交设计使得同一条数据可以从多个独立角度被检索和分析，是分类体系设计的最佳实践。

#### (2) Agentic 类别具有前瞻性

将 Agent 行为（tool-level actions）和行为模式（behavioral patterns）纳入分类体系，是该体系最具创新性的部分。在 LLM Agent 成为主流开发范式的背景下，这一类别为训练数据提供了独特的行为标注维度，可以直接用于分析和优化 Agent 的工具调用策略。

#### (3) Context 类别的单选设计务实

Context 作为唯一的单选类别，从 snippet 到 monorepo 形成了清晰的代码规模梯度。这种设计避免了多选带来的标注歧义，同时提供了足够的区分度。

#### (4) Constraint 类别贴近工程实际

`no-dynamic-allocation`、`lock-free`、`idempotent` 等标签直接对应真实的工程约束，而非学术概念。这使得标注结果可以直接用于筛选特定约束场景下的训练数据。

### 5.3 弱点与盲区

#### (1) Language 类别的长尾问题严重

75 个语言标签中，预计在真实数据分布中，前 10 种语言（Python, JavaScript, TypeScript, Java, Go, Rust, C, C++, C#, Ruby）将占据 85%+ 的样本。剩余 65 个标签的实际使用频率极低，会导致：
- 标注者对冷门语言的判断不确定性增加
- 训练数据中冷门语言样本严重不足，标签形同虚设
- 维护成本高但收益低

**建议**: 将低频语言合并为 `other-compiled`、`other-interpreted`、`other-functional` 等聚合标签，或设置最低样本阈值，低于阈值的语言自动归入 `other`。

#### (2) 缺少 Library/Framework 维度是重大缺陷

在用户指定的 198 标签版本中，Library 类别被移除。这是一个严重的信息损失。在实际开发中，"用 React 写组件"和"用 Vue 写组件"虽然 Language 都是 JavaScript、Domain 都是 web-frontend，但所需的知识和代码模式完全不同。Library/Framework 是区分训练数据最有效的维度之一。

**建议**: 恢复 Library 类别，至少保留 Top 50 高频框架（React, Vue, Angular, Django, Flask, Spring Boot, Express, Next.js, PyTorch, TensorFlow 等）。

#### (3) Concept 类别粒度不均匀

- `algorithms` 一个标签覆盖了从排序到图论到动态规划的所有算法，粒度过粗
- `ownership` 是 Rust 特有概念，粒度过细（仅适用于 1/75 的语言）
- `functional-programming` 和 `object-oriented-programming` 是范式级概念，与 `recursion`、`caching` 等技术级概念不在同一抽象层次

**建议**: 为 `algorithms` 增加子标签（sorting, graph, dynamic-programming, string-algorithms 等），或将 `ownership` 提升为更通用的 `resource-management` 概念。

#### (4) Agentic 类别的 tool-level 和 behavioral 边界模糊

`planning` 既是一个 behavioral pattern，也可以被视为一个 tool-level action（如 Claude Code 的 TaskCreate）。`error-recovery` 和 `iterative-refinement` 在实际标注中难以区分——修复一个编译错误后重试，算 error-recovery 还是 iterative-refinement？

**建议**: 为 Agentic 类别增加明确的子类别标识（tool-action vs behavior-pattern），并提供判断边界的标注指南和示例。

#### (5) 缺少难度和意图维度

如第 4 节分析所述，难度和用户意图是 SFT 训练数据最重要的元信息之一。缺少这两个维度意味着：
- 无法按难度梯度构建课程式训练数据
- 无法区分"教学型"和"生产型"数据的不同训练价值
- 无法评估模型在不同难度级别上的能力分布

### 5.4 与行业标准的对比

目前业界没有公开的、被广泛采用的 SFT 代码训练数据标注分类标准。最接近的参考包括：

| 参考体系 | 对比 |
|----------|------|
| **HumanEval / MBPP 的任务分类** | 仅覆盖 Task 维度，且粒度远粗于本体系。本体系在多维度标注上显著领先。 |
| **SWE-bench 的标注方式** | 按 repository + issue 组织，隐含了 Context 和 Task 信息，但没有显式的 Concept、Constraint、Agentic 维度。本体系更系统化。 |
| **BigCode / StarCoder 的数据标注** | 主要按语言和许可证分类，维度远少于本体系。 |
| **LMSYS Chatbot Arena 的分类** | 按对话类型分类（coding, math, reasoning 等），粒度远粗于本体系。 |

**结论**: 本体系在维度丰富度和工程实用性上优于现有公开标准，尤其是 Agentic 和 Constraint 类别具有独创性。但在标注一致性保障（inter-annotator agreement）方面缺少配套的标注指南和质量控制机制。

### 5.5 具体改进建议

#### 优先级 P0（必须改进）

1. **恢复 Library/Framework 类别**: 至少包含 Top 50 高频框架，这是区分训练数据最有效的维度。
2. **增加 Difficulty 维度**: 建议 4 级：`beginner` / `intermediate` / `advanced` / `expert`，单选。
3. **编写标注指南**: 为每个类别提供 3-5 个标注示例，明确边界情况的判断规则。

#### 优先级 P1（强烈建议）

4. **增加 Intent 维度**: `learning` / `debugging` / `building` / `reviewing` / `exploring` / `migrating`，单选。
5. **细化 algorithms 标签**: 拆分为 `sorting-searching`、`graph-algorithms`、`dynamic-programming`、`string-algorithms`、`numerical-algorithms` 等子标签。
6. **处理 Language 长尾**: 设置样本阈值，低频语言归入聚合标签。

#### 优先级 P2（建议改进）

7. **增加 competitive-programming 和 education Domain 标签**。
8. **为 Agentic 类别增加子类别标识**（tool-action vs behavior-pattern）。
9. **增加输出格式标签**: `code-output` / `analysis-output` / `tutorial-output` / `mixed-output`。
10. **增加 multi-language 标签**: 用于标注涉及多语言交互的场景（如 Python 调用 C 扩展、TypeScript + Rust WASM）。

### 5.6 总体评分

| 维度 | 评分 (1-10) | 说明 |
|------|-------------|------|
| 完备性 | 7/10 | 核心维度覆盖良好，但缺少 Library、Difficulty、Intent 维度 |
| 正交性 | 8/10 | 类别间正交性好，但 Agentic 内部和跨类别存在少量冗余 |
| 可操作性 | 6/10 | 缺少标注指南，部分标签边界模糊，标注一致性难以保证 |
| 可扩展性 | 8/10 | YAML 结构清晰，新增标签和类别的成本低 |
| 工程实用性 | 7/10 | Agentic 和 Constraint 类别实用性强，但 Language 长尾和 Library 缺失降低了实际价值 |
| **综合评分** | **7.2/10** | **一个有良好设计基础的分类体系，但在投入生产标注前需要补充 Library 维度、标注指南和难度分级。** |

### 5.7 结论

该分类体系展现了对 SFT 代码训练数据标注需求的深入理解，尤其是 Agentic 类别的引入体现了对 LLM Agent 时代训练数据需求的前瞻性思考。7 个类别的正交设计为多维度数据分析提供了坚实基础。

然而，体系在投入实际标注生产前仍有关键缺陷需要解决：Library/Framework 维度的缺失会导致严重的信息损失；缺少难度和意图维度会限制训练数据的精细化利用；标注指南的缺失会导致标注一致性问题。

建议按 P0 → P1 → P2 的优先级逐步完善，在完成 P0 改进后即可进入小规模试标注阶段，通过实际标注反馈进一步迭代优化分类体系。

---

> 报告完成于 2026-02-13。本报告基于 10 条模拟查询的标注实验和分类体系结构分析，不代表大规模标注场景下的统计结论。建议在 100+ 真实样本上进行正式的标注一致性测试（inter-annotator agreement study）后再做最终评估。
