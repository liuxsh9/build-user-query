# SFT 训练数据标注能力分类体系评估报告 (v2)

> 版本: 2.0 | 日期: 2026-02-14
> 评估对象: 9 类别 ~252 标签的 Capability Taxonomy (v2)
> 前序版本: v1 — 7 类别 198 标签 (2026-02-13)
> 评估方法: 模拟标注 20 条 + 覆盖率分析 + 专家评审 + v1 对比

---

## 目录

1. [更新说明](#1-更新说明)
2. [新增 10 条模拟查询 (Q11-Q20)](#2-新增-10-条模拟查询-q11-q20)
3. [全部 20 条标注结果](#3-全部-20-条标注结果)
4. [分析（20 条样本）](#4-分析20-条样本)
5. [第三方专家评估 (v2)](#5-第三方专家评估-v2)

---

## 1. 更新说明

v2 相对 v1 的分类体系变更如下：

| 变更项 | v1 | v2 | 说明 |
|--------|----|----|------|
| 类别数 | 7 | 9 | 新增 2 个类别 |
| 标签总数 | ~198 | ~252 | 净增 ~54 个标签 |
| Library 类别 | 已移除 | **恢复 (Top 50)** | 直接回应 v1 评估 P0 建议 #1 |
| Difficulty 类别 | 不存在 | **新增 (4 级)** | 直接回应 v1 评估 P0 建议 #2 |

### 1.1 Library 类别恢复 (50 tags, multi-select)

v1 评估中明确指出 Library/Framework 维度缺失是"重大缺陷"——"用 React 写组件"和"用 Vue 写组件"虽然 Language 都是 JavaScript、Domain 都是 web-frontend，但所需知识和代码模式完全不同。v2 恢复了 Library 类别，精选 Top 50 高频框架/库，覆盖前端 (react, vue, angular, nextjs, svelte, tailwindcss)、后端 (express, nestjs, django, flask, fastapi, spring-boot, gin, laravel, rails, aspnet-core)、数据/ML (numpy, pandas, pytorch, tensorflow, scikit-learn, langchain, hugging-face-transformers)、数据库/ORM (prisma, sqlalchemy, hibernate, gorm, entity-framework)、测试 (jest, pytest, junit, selenium, playwright)、工具链 (webpack, vite, axios, requests, pydantic, serde, tokio, axum, boost, redis) 等。

### 1.2 Difficulty 类别新增 (4 tags, single-select)

v1 评估指出"难度/复杂度维度缺失"是关键能力缺口——Q1（算法优化）和 Q4（React 组件）的技术深度差异巨大，但无法通过标签体现。v2 新增 Difficulty 类别，4 级单选：

| 级别 | 定义 |
|------|------|
| `beginner` | 入门级，涉及语言基础语法、简单 API 调用、基本概念理解 |
| `intermediate` | 中级，涉及框架使用、常见设计模式、标准工程实践 |
| `advanced` | 高级，涉及性能优化、复杂架构设计、深层 debug、多系统集成 |
| `expert` | 专家级，涉及底层原理、前沿技术、大规模系统、需要深厚领域经验 |

### 1.3 未变更的类别

以下 7 个类别从 v1 原样保留，标签内容不变：

- Language (75 tags, multi-select)
- Concept (21 tags, multi-select)
- Domain (31 tags, multi-select)
- Agentic (24 tags, multi-select)
- Task (18 tags, multi-select)
- Constraint (19 tags, multi-select)
- Context (10 tags, single-select)

---

## 2. 新增 10 条模拟查询 (Q11-Q20)

### Q11 — 大学生学习编程（Python 入门）

> 老师好，我刚学 Python 两周，有个作业不太会做。题目是让我读一个 csv 文件，然后把里面成绩大于 90 分的同学名字打印出来。我试了下 open() 读文件但是不知道怎么按逗号分割每一行，而且 list comprehension 那个语法我看了半天没看懂... 能给我讲讲吗？最好给个简单的例子。
>
> 我的代码：
> ```python
> f = open('scores.csv')
> for line in f:
>     print(line)  # 这里不知道怎么处理了
> ```

**Response trajectory**: Read code → Explain list comprehension → Write csv parsing example → Suggest csv module → Explain with/as context manager

### Q12 — 全栈独立开发者（SaaS 产品）

> 我在做一个 SaaS 订阅制产品，技术栈 Next.js 14 (App Router) + Prisma + PostgreSQL，现在要接 Stripe 支付。需求：
> - 月付/年付两种 plan
> - Stripe Checkout Session 创建
> - Webhook 处理 subscription 状态变更
> - Prisma schema 里存 subscription 信息
> - 用户 dashboard 显示当前 plan 和账单历史
>
> 之前没接过 Stripe，能帮我把整个 flow 走通吗？从 schema 设计到 API route 到前端页面。

**Response trajectory**: Write Prisma schema → Write Stripe checkout API route → Write webhook handler → Write dashboard page → Write middleware for subscription check

### Q13 — 数据工程师（ETL Pipeline）

> 我们的 Airflow DAG 跑 Spark ETL job，最近上游数据源改了 schema（加了几个 nullable 字段，改了一个字段名），导致下游 Parquet 写入失败。现在的问题：
> 1. 没有 schema evolution 策略，每次上游改 schema 就炸
> 2. 数据质量检查只有 row count，没有 column-level validation
> 3. Spark job 的 error handling 太粗糙，失败了只知道 "Task failed" 没有具体原因
>
> 用的是 PySpark 3.5 + Airflow 2.8 + Delta Lake。帮我设计一个 robust 的 schema evolution + data quality 方案。

**Response trajectory**: Analyze schema evolution options → Write Delta Lake merge schema config → Write Great Expectations data quality suite → Write Airflow error handling callbacks → Write alerting integration

### Q14 — Rust 新手（从 C++ 迁移）

> 我是写了 5 年 C++ 的，最近在学 Rust，被 lifetime 搞疯了。这段代码编译不过，编译器报了一堆 lifetime 错误我看不懂：
>
> ```rust
> struct Parser<'a> {
>     input: &'a str,
> }
>
> impl<'a> Parser<'a> {
>     fn parse(&mut self) -> Vec<&str> {
>         let mut results = Vec::new();
>         for line in self.input.lines() {
>             let trimmed = line.trim();
>             if !trimmed.is_empty() {
>                 results.push(trimmed);
>             }
>         }
>         results
>     }
> }
>
> fn process(data: String) -> Vec<&str> {
>     let parser = Parser { input: &data };
>     parser.parse()
> }
> ```
>
> 编译器说 `lifetime may not live long enough` 还有 `cannot return value referencing local variable`。C++ 里这种写法完全没问题啊，Rust 的 ownership 到底怎么理解？

**Response trajectory**: Analyze lifetime errors → Explain ownership vs C++ references → Write fixed version with proper lifetimes → Explain alternative with owned String → Suggest Rust book chapters

### Q15 — QA 自动化工程师（E2E 测试）

> 我们团队要从 Cypress 迁移到 Playwright，我负责搭建整个 E2E 测试框架。主要需求：
> - 登录流程的 auth state 复用（不想每个 test 都重新登录）
> - Visual regression testing（截图对比）
> - 多浏览器并行测试 (Chromium + Firefox + WebKit)
> - CI/CD 集成 (GitHub Actions)
> - Page Object Model 组织代码
>
> 现在的 app 是 React SPA，有 OAuth2 登录（Google + GitHub），API 是 REST。能帮我搭一个 Playwright 项目的 scaffold 吗？包括 config、auth setup、和一个示例 test。

**Response trajectory**: Write playwright.config.ts → Write auth setup (global-setup.ts) → Write POM base class → Write example test with visual comparison → Write GitHub Actions workflow

### Q16 — 区块链开发者（智能合约）

> I'm building a DeFi lending protocol on Ethereum. The core contract handles deposits, borrows, and liquidations. Two issues:
>
> 1. Gas optimization — my `liquidate()` function costs 350k gas, need to get it under 200k
> 2. Reentrancy protection — I'm using a simple `locked` boolean but heard it's not enough for cross-function reentrancy
>
> ```solidity
> function liquidate(address borrower, address collateral) external {
>     require(!locked, "reentrancy");
>     locked = true;
>
>     uint256 debt = userDebts[borrower];
>     uint256 collateralAmount = userCollateral[borrower][collateral];
>     uint256 price = IOracle(oracle).getPrice(collateral);
>
>     require(collateralAmount * price / 1e18 < debt * liquidationThreshold / 100, "healthy");
>
>     // ... transfer logic with multiple external calls ...
>
>     locked = false;
> }
> ```
>
> Also want to add flash loan protection. What's the best practice pattern now?

**Response trajectory**: Analyze gas costs → Write optimized liquidate with packed storage → Write ReentrancyGuard with cross-function protection → Write flash loan guard → Suggest OpenZeppelin patterns

### Q17 — 运维老手（数据库性能）

> 线上 PostgreSQL 14 有个慢查询，EXPLAIN ANALYZE 结果如下：
>
> ```sql
> EXPLAIN ANALYZE
> SELECT o.id, o.created_at, u.name, SUM(oi.quantity * oi.price) as total
> FROM orders o
> JOIN users u ON o.user_id = u.id
> JOIN order_items oi ON oi.order_id = o.id
> WHERE o.created_at BETWEEN '2025-01-01' AND '2025-12-31'
>   AND o.status = 'completed'
> GROUP BY o.id, o.created_at, u.name
> ORDER BY total DESC
> LIMIT 100;
> ```
>
> ```
> Limit  (cost=89234.56..89234.81 rows=100) (actual time=12847.234..12847.312 rows=100 loops=1)
>   -> Sort  (cost=89234.56..89456.78 rows=88890) (actual time=12847.231..12847.289 rows=100 loops=1)
>         Sort Key: (sum((oi.quantity * oi.price))) DESC
>         Sort Method: top-N heapsort  Memory: 45kB
>         -> HashAggregate  (cost=78123.45..79012.35 rows=88890) (actual time=12534.123..12789.456 rows=88890 loops=1)
>               -> Hash Join  (cost=34567.89..72345.67 rows=577800) (actual time=2345.678..9876.543 rows=577800 loops=1)
>                     -> Seq Scan on order_items oi  (cost=0.00..28901.00 rows=1200000) (actual time=0.012..1234.567 rows=1200000 loops=1)
>                     -> Hash  (cost=31234.56..31234.56 rows=88890) (actual time=2345.123..2345.123 rows=88890 loops=1)
>                           -> Hash Join  (cost=1234.56..31234.56 rows=88890) (actual time=123.456..2234.567 rows=88890 loops=1)
>                                 -> Seq Scan on orders o  (cost=0.00..28901.23 rows=88890) (actual time=0.023..1987.654 rows=88890 loops=1)
>                                       Filter: (status = 'completed' AND created_at >= '2025-01-01' AND created_at <= '2025-12-31')
>                                       Rows Removed by Filter: 911110
>                                 -> Hash  (cost=1012.00..1012.00 rows=50000) (actual time=123.234..123.234 rows=50000 loops=1)
>                                       -> Seq Scan on users u  (cost=0.00..1012.00 rows=50000) (actual time=0.011..67.890 rows=50000 loops=1)
> Planning Time: 1.234 ms
> Execution Time: 12848.567 ms
> ```
>
> orders 表 100 万行，order_items 表 1200 万行，users 表 5 万行。现在跑了 12.8 秒，业务要求 < 500ms。帮我分析下瓶颈在哪，怎么加索引优化。

**Response trajectory**: Analyze EXPLAIN output → Identify missing indexes → Write CREATE INDEX statements → Suggest partial index → Write optimized query with CTE → Suggest materialized view for reporting

### Q18 — 科研人员（数值计算）

> 我在用 Julia 做 2D incompressible Navier-Stokes 方程的数值模拟（lid-driven cavity flow），用的是 finite difference method + fractional step method。网格 512×512，Re=10000。
>
> 两个问题：
> 1. 单线程跑太慢了，一个 timestep 要 2 秒，总共要跑 10 万步。想用 Julia 的多线程或者 GPU (CUDA.jl) 加速，但不确定 stencil computation 怎么并行化
> 2. 高 Re 数下数值不稳定，出现 checkerboard oscillation，我怀疑是 pressure-velocity coupling 的问题
>
> ```julia
> function pressure_poisson!(p, div_u, dx, dy, niter=1000)
>     for _ in 1:niter
>         for j in 2:ny-1, i in 2:nx-1
>             p[i,j] = ((p[i+1,j]+p[i-1,j])*dy^2 + (p[i,j+1]+p[i,j-1])*dx^2 - div_u[i,j]*dx^2*dy^2) / (2*(dx^2+dy^2))
>         end
>     end
> end
> ```

**Response trajectory**: Analyze numerical scheme → Write CUDA.jl kernel for pressure Poisson → Write threaded stencil with @threads → Suggest staggered grid for checkerboard fix → Write multigrid preconditioner → Benchmark comparison

### Q19 — 开源贡献者（PR Review）

> 我想给 fastapi 提一个 PR，解决 issue #12345（假设）：当 response_model 是一个有 Optional 字段的 Pydantic v2 model 时，OpenAPI schema 生成的 nullable 标注不正确。
>
> 我 fork 了 repo，看了下源码大概在 `fastapi/utils.py` 和 `fastapi/routing.py` 里面处理 response_model 的逻辑，但是代码量挺大的，不太确定改哪里。
>
> 能帮我：
> 1. 定位到具体需要改的函数
> 2. 理解现在的 schema generation flow
> 3. 写一个 fix + 对应的 test case
>
> 我本地已经 clone 了 repo，Python 3.11，装了 dev dependencies。

**Response trajectory**: Search codebase for schema generation → Read relevant functions → Trace OpenAPI nullable handling → Write fix in utils.py → Write test case → Run pytest → Write PR description

### Q20 — CTO/架构师（技术选型）

> 我们是一个 50 人的团队，要从零开始做一个 B2B SaaS 平台（多租户、复杂权限、审计日志、数据隔离）。预期 2 年内到 500 个企业客户，每个客户 50-500 用户。
>
> 现在在纠结几个技术选型：
> 1. **单体 vs 微服务**: 团队之前只做过单体，但担心后期扩展性
> 2. **数据库**: PostgreSQL (schema-per-tenant) vs CockroachDB (row-level isolation) vs 每个租户独立数据库
> 3. **后端语言**: Go vs Rust vs Java (Spring Boot) vs TypeScript (NestJS)
> 4. **前端**: Next.js vs Remix vs 纯 SPA (React + Vite)
> 5. **部署**: Kubernetes 从第一天就上，还是先 Docker Compose 后面再迁？
>
> 预算有限，不想过度工程化，但也不想半年后推倒重来。能给个综合建议吗？

**Response trajectory**: Analyze requirements → Compare architecture options → Compare database multi-tenancy strategies → Evaluate language/framework fit → Write deployment roadmap → Provide decision matrix with trade-offs

---

## 3. 全部 20 条标注结果

### 3.1 总览表

下表展示全部 20 条查询在 9 个类别上的标注结果。由于列数较多，分为两个子表。

#### 表 A: Language / Library / Concept / Domain / Difficulty

| ID | Persona | Language | Library | Concept | Domain | Difficulty |
|----|---------|----------|---------|---------|--------|------------|
| Q1 | 竞赛选手 | cpp | (none) | algorithms, data-structures, control-flow | (none) | advanced |
| Q2 | 资深后端 | go | redis | concurrency, error-handling, memory-management | web-backend, devops | expert |
| Q3 | 数据科学家 | python | pytorch, hugging-face-transformers | error-handling, type-system | machine-learning, data-science | advanced |
| Q4 | 前端初级 | javascript | react | data-structures, design-patterns | web-frontend | intermediate |
| Q5 | DevOps | yaml, hcl | (none) | architecture, caching | cloud-computing, devops | advanced |
| Q6 | 嵌入式工程师 | c | (none) | concurrency, memory-management, type-system | embedded-systems, real-time-systems | expert |
| Q7 | 安全研究员 | javascript | express | security, metaprogramming | cybersecurity, web-backend | advanced |
| Q8 | 移动开发者 | dart | flutter | architecture, concurrency, data-structures | mobile-development, iot | advanced |
| Q9 | 游戏开发者 | rust | tokio | concurrency, type-system, design-patterns, ownership | game-development, systems-programming | expert |
| Q10 | Tech Lead | java | spring-boot | architecture, design-patterns, concurrency | web-backend, e-commerce | expert |
| Q11 | 大学生 | python | (none) | control-flow, data-structures | (none) | beginner |
| Q12 | 独立开发者 | typescript | nextjs, prisma | architecture, api-protocols | web-backend, web-frontend, e-commerce, financial-technology | intermediate |
| Q13 | 数据工程师 | python | (none) | error-handling, data-structures, type-system | data-engineering, data-science | advanced |
| Q14 | Rust 新手 | rust | (none) | ownership, memory-management, type-system | systems-programming | intermediate |
| Q15 | QA 工程师 | typescript | playwright, react | testing, design-patterns | web-frontend, automation | intermediate |
| Q16 | 区块链开发者 | solidity | (none) | security, memory-management, design-patterns | blockchain, financial-technology | advanced |
| Q17 | 运维老手 | sql | (none) | data-structures, caching, algorithms | database-administration | advanced |
| Q18 | 科研人员 | julia | (none) | concurrency, algorithms, memory-management | scientific-computing | expert |
| Q19 | 开源贡献者 | python | fastapi, pydantic | type-system, testing, metaprogramming | api-development | advanced |
| Q20 | CTO/架构师 | (none) | (none) | architecture, design-patterns | cloud-computing, web-backend, e-commerce | intermediate |

#### 表 B: Agentic / Task / Constraint / Context

| ID | Persona | Agentic | Task | Constraint | Context |
|----|---------|---------|------|------------|---------|
| Q1 | 竞赛选手 | code-execution, iterative-refinement | optimization, code-refactoring | performance-optimized | single-function |
| Q2 | 资深后端 | web-search, bash-execution, static-analysis | bug-fixing, monitoring | fault-tolerant, observable | repository |
| Q3 | 数据科学家 | code-execution, iterative-refinement | bug-fixing, optimization | performance-optimized, deterministic | multi-file |
| Q4 | 前端初级 | code-execution, iterative-refinement | code-refactoring, optimization | performance-optimized, accessible | single-file |
| Q5 | DevOps | bash-execution, file-write, multi-file-coordination | configuration, deployment | scalable, fault-tolerant, portable | greenfield |
| Q6 | 嵌入式工程师 | code-execution, iterative-refinement | bug-fixing, optimization | performance-optimized, deterministic, no-dynamic-allocation | module |
| Q7 | 安全研究员 | code-execution, static-analysis | security-audit, bug-fixing | type-safe, thread-safe | single-file |
| Q8 | 移动开发者 | file-write, multi-file-coordination, planning | feature-implementation, schema-design | fault-tolerant, scalable | greenfield |
| Q9 | 游戏开发者 | code-execution, static-analysis, iterative-refinement | feature-implementation, api-design | thread-safe, performance-optimized | module |
| Q10 | Tech Lead | planning, multi-file-coordination, static-analysis | code-review-task, migration, schema-design | backward-compatible, scalable, fault-tolerant | monorepo |
| Q11 | 大学生 | (none) | code-explanation, code-completion | (none) | snippet |
| Q12 | 独立开发者 | file-write, multi-file-coordination, planning | feature-implementation, schema-design, api-design | scalable, stateless | greenfield |
| Q13 | 数据工程师 | file-write, multi-file-coordination, error-recovery | configuration, feature-implementation, monitoring | fault-tolerant, backward-compatible, observable | multi-file |
| Q14 | Rust 新手 | (none) | code-explanation, bug-fixing | type-safe | single-file |
| Q15 | QA 工程师 | file-write, multi-file-coordination, ui-automation | testing-task, configuration | portable | greenfield |
| Q16 | 区块链开发者 | code-execution, static-analysis | optimization, security-audit | performance-optimized, idempotent | single-file |
| Q17 | 运维老手 | database-query, bash-execution | optimization, schema-design | performance-optimized, scalable | repository |
| Q18 | 科研人员 | code-execution, iterative-refinement | optimization, feature-implementation | performance-optimized, deterministic | module |
| Q19 | 开源贡献者 | search, file-read, test-running, git-operations | bug-fixing, testing-task | backward-compatible, type-safe | repository |
| Q20 | CTO/架构师 | planning | code-explanation, configuration | scalable, fault-tolerant, portable | greenfield |

### 3.2 Q11-Q20 逐条详细标注

#### Q11 — 大学生学习编程（Python 入门）

| Category | Tags | 标注理由 |
|----------|------|----------|
| Language | `python` | 明确使用 Python |
| Library | (none) | 仅使用内置 open()，未涉及第三方库 |
| Concept | `control-flow`, `data-structures` | for 循环遍历 + list comprehension + CSV 行解析 |
| Domain | (none) | 纯学习场景，无特定应用领域 |
| Agentic | (none) | 简单问答，无需工具调用 |
| Task | `code-explanation`, `code-completion` | 需要解释语法 + 补全代码 |
| Constraint | (none) | 入门级无非功能性约束 |
| Context | `snippet` | 仅有几行代码片段 |
| Difficulty | `beginner` | Python 两周新手，基础文件 I/O 和 list comprehension |

#### Q12 — 全栈独立开发者（SaaS 产品）

| Category | Tags | 标注理由 |
|----------|------|----------|
| Language | `typescript` | Next.js 14 App Router 使用 TypeScript |
| Library | `nextjs`, `prisma` | 明确提到 Next.js 14 + Prisma ORM |
| Concept | `architecture`, `api-protocols` | 整体支付流程架构设计 + REST API / Webhook 协议 |
| Domain | `web-backend`, `web-frontend`, `e-commerce`, `financial-technology` | SaaS 订阅制产品涉及前后端 + 电商支付 + 金融科技 |
| Agentic | `file-write`, `multi-file-coordination`, `planning` | 需要生成多个文件（schema, API routes, pages）并协调 |
| Task | `feature-implementation`, `schema-design`, `api-design` | 从零实现支付功能 + 数据库 schema + API 设计 |
| Constraint | `scalable`, `stateless` | SaaS 产品需要可扩展，webhook 处理需要幂等/无状态 |
| Context | `greenfield` | 支付模块从零搭建 |
| Difficulty | `intermediate` | 标准 Stripe 集成，有成熟文档和模式，但涉及多组件协调 |

#### Q13 — 数据工程师（ETL Pipeline）

| Category | Tags | 标注理由 |
|----------|------|----------|
| Language | `python` | PySpark + Airflow 均为 Python 生态 |
| Library | (none) | PySpark/Airflow/Delta Lake 不在 Top 50 列表中 |
| Concept | `error-handling`, `data-structures`, `type-system` | 错误处理改进 + schema 结构 + 类型演进 |
| Domain | `data-engineering`, `data-science` | ETL pipeline 属于数据工程核心场景 |
| Agentic | `file-write`, `multi-file-coordination`, `error-recovery` | 需要写多个配置/代码文件 + 错误恢复策略 |
| Task | `configuration`, `feature-implementation`, `monitoring` | 配置 schema evolution + 实现 data quality + 监控告警 |
| Constraint | `fault-tolerant`, `backward-compatible`, `observable` | ETL 需要容错 + schema 向后兼容 + 可观测性 |
| Context | `multi-file` | 涉及 DAG 定义、Spark job、quality checks 多个文件 |
| Difficulty | `advanced` | 生产级 schema evolution + data quality 方案设计 |

**标注争议**: Library 类别为空是因为 PySpark、Airflow、Delta Lake 均不在 Top 50 列表中。这是 Library 类别的一个覆盖盲区——数据工程生态的核心工具完全缺失。

#### Q14 — Rust 新手（从 C++ 迁移）

| Category | Tags | 标注理由 |
|----------|------|----------|
| Language | `rust` | 明确使用 Rust，附有 Rust 代码 |
| Library | (none) | 纯标准库代码，无第三方依赖 |
| Concept | `ownership`, `memory-management`, `type-system` | Rust 核心概念：ownership/borrowing + 内存管理 + lifetime 类型系统 |
| Domain | `systems-programming` | Rust parser 属于系统编程范畴 |
| Agentic | (none) | 概念解释 + 代码修复，无需工具调用 |
| Task | `code-explanation`, `bug-fixing` | 解释 lifetime 概念 + 修复编译错误 |
| Constraint | `type-safe` | Rust 的类型安全是核心约束 |
| Context | `single-file` | 单文件代码示例 |
| Difficulty | `intermediate` | Lifetime 是 Rust 中级概念，对 C++ 老手来说是学习曲线的关键点 |

#### Q15 — QA 自动化工程师（E2E 测试）

| Category | Tags | 标注理由 |
|----------|------|----------|
| Language | `typescript` | Playwright 项目通常使用 TypeScript |
| Library | `playwright`, `react` | 明确使用 Playwright 测试框架，被测应用是 React SPA |
| Concept | `testing`, `design-patterns` | E2E 测试方法论 + Page Object Model 设计模式 |
| Domain | `web-frontend`, `automation` | Web 前端测试 + 自动化 |
| Agentic | `file-write`, `multi-file-coordination`, `ui-automation` | 生成项目脚手架多文件 + UI 自动化测试 |
| Task | `testing-task`, `configuration` | 搭建测试框架 + 配置 CI/CD |
| Constraint | `portable` | 多浏览器兼容（Chromium + Firefox + WebKit） |
| Context | `greenfield` | 从零搭建 Playwright 项目 |
| Difficulty | `intermediate` | 标准 Playwright 项目搭建，有成熟模式可循 |

#### Q16 — 区块链开发者（智能合约）

| Category | Tags | 标注理由 |
|----------|------|----------|
| Language | `solidity` | 明确使用 Solidity 编写智能合约 |
| Library | (none) | OpenZeppelin 不在 Top 50 列表中 |
| Concept | `security`, `memory-management`, `design-patterns` | 重入攻击防护 + gas/storage 优化 + Guard 模式 |
| Domain | `blockchain`, `financial-technology` | DeFi 借贷协议 = 区块链 + 金融科技 |
| Agentic | `code-execution`, `static-analysis` | 合约编译测试 + 静态分析 gas 消耗 |
| Task | `optimization`, `security-audit` | Gas 优化 + 安全审计（重入、闪电贷） |
| Constraint | `performance-optimized`, `idempotent` | Gas 优化 + 清算操作需要幂等性 |
| Context | `single-file` | 单个合约文件 |
| Difficulty | `advanced` | DeFi 协议安全 + gas 优化需要深厚领域知识 |

**标注争议**: OpenZeppelin 是 Solidity 生态最重要的库，但不在 Top 50 中。Solidity 生态的 Library 覆盖为零。

#### Q17 — 运维老手（数据库性能）

| Category | Tags | 标注理由 |
|----------|------|----------|
| Language | `sql` | 纯 SQL 查询优化 |
| Library | (none) | PostgreSQL 是数据库而非 Library |
| Concept | `data-structures`, `caching`, `algorithms` | 索引数据结构 (B-tree) + 查询缓存 + 查询计划算法 |
| Domain | `database-administration` | 数据库性能调优是 DBA 核心工作 |
| Agentic | `database-query`, `bash-execution` | 执行 EXPLAIN ANALYZE + 创建索引命令 |
| Task | `optimization`, `schema-design` | 查询优化 + 索引设计 |
| Constraint | `performance-optimized`, `scalable` | 从 12.8s 优化到 <500ms + 大表可扩展性 |
| Context | `repository` | 涉及多表关联的生产数据库 |
| Difficulty | `advanced` | 需要深入理解查询计划、索引策略、PostgreSQL 内部机制 |

#### Q18 — 科研人员（数值计算）

| Category | Tags | 标注理由 |
|----------|------|----------|
| Language | `julia` | 明确使用 Julia 语言 |
| Library | (none) | CUDA.jl 不在 Top 50 列表中 |
| Concept | `concurrency`, `algorithms`, `memory-management` | GPU/多线程并行 + 数值算法 (Navier-Stokes) + 内存布局优化 |
| Domain | `scientific-computing` | 计算流体力学 (CFD) 数值模拟 |
| Agentic | `code-execution`, `iterative-refinement` | 运行 benchmark + 迭代优化性能 |
| Task | `optimization`, `feature-implementation` | 性能优化 (并行化) + 实现 multigrid solver |
| Constraint | `performance-optimized`, `deterministic` | 计算性能是核心 + 数值稳定性要求确定性 |
| Context | `module` | 压力 Poisson 求解器是模拟系统的一个模块 |
| Difficulty | `expert` | 高 Re 数 CFD + GPU 并行化 + 数值稳定性，需要深厚的数值分析和 HPC 背景 |

**标注争议**: Julia 的科学计算生态（CUDA.jl, DifferentialEquations.jl 等）完全不在 Top 50 中。科学计算领域的 Library 覆盖为零。

#### Q19 — 开源贡献者（PR Review）

| Category | Tags | 标注理由 |
|----------|------|----------|
| Language | `python` | FastAPI 是 Python 框架 |
| Library | `fastapi`, `pydantic` | 明确涉及 FastAPI + Pydantic v2 的 schema 生成 |
| Concept | `type-system`, `testing`, `metaprogramming` | Pydantic 类型系统 + 测试用例 + OpenAPI schema 元编程 |
| Domain | `api-development` | FastAPI 的 OpenAPI schema 生成属于 API 开发 |
| Agentic | `search`, `file-read`, `test-running`, `git-operations` | 搜索代码库 + 读取源码 + 运行测试 + Git PR 操作 |
| Task | `bug-fixing`, `testing-task` | 修复 nullable 标注 bug + 编写测试用例 |
| Constraint | `backward-compatible`, `type-safe` | 开源项目修复需要向后兼容 + 类型安全 |
| Context | `repository` | 在完整的 FastAPI 仓库中工作 |
| Difficulty | `advanced` | 需要理解 FastAPI 内部 schema 生成机制 + Pydantic v2 变更 |

#### Q20 — CTO/架构师（技术选型）

| Category | Tags | 标注理由 |
|----------|------|----------|
| Language | (none) | 技术选型讨论，未涉及具体编码 |
| Library | (none) | 讨论层面，未使用具体库 |
| Concept | `architecture`, `design-patterns` | 系统架构设计 + 架构模式（单体 vs 微服务） |
| Domain | `cloud-computing`, `web-backend`, `e-commerce` | B2B SaaS 平台 = 云计算 + Web 后端 + 电商 |
| Agentic | `planning` | 纯规划和决策，无代码执行 |
| Task | `code-explanation`, `configuration` | 解释各技术方案优劣 + 部署配置建议 |
| Constraint | `scalable`, `fault-tolerant`, `portable` | 多租户可扩展 + 容错 + 多环境可移植 |
| Context | `greenfield` | 从零开始的新项目 |
| Difficulty | `intermediate` | 技术选型本身不需要 expert 级编码能力，但需要广泛的工程经验；标注为 intermediate 因为问题本身是"选择"而非"实现" |

**标注争议**: Q20 的 Difficulty 标注存在分歧。从"需要的知识广度"看应该是 advanced 甚至 expert，但从"编码难度"看是 intermediate。这暴露了 Difficulty 维度定义的模糊性——它衡量的是"编码难度"还是"综合决策难度"？

---

## 4. 分析（20 条样本）

### 4.1 标签覆盖率统计

#### 各类别标签命中情况

| Category | 总标签数 | 命中标签数 | 命中率 | 命中的标签 |
|----------|---------|-----------|--------|-----------|
| Language (75) | 75 | 12 | 16.0% | c, cpp, dart, go, java, javascript, julia, python, rust, solidity, sql, typescript |
| Library (50) | 50 | 13 | 26.0% | express, fastapi, flutter, hugging-face-transformers, nextjs, playwright, prisma, pydantic, pytorch, react, redis, spring-boot, tokio |
| Concept (21) | 21 | 15 | 71.4% | algorithms, api-protocols, architecture, caching, concurrency, control-flow, data-structures, design-patterns, error-handling, memory-management, metaprogramming, ownership, security, testing, type-system |
| Domain (31) | 31 | 21 | 67.7% | api-development, automation, blockchain, cloud-computing, cybersecurity, data-engineering, data-science, database-administration, devops, e-commerce, embedded-systems, financial-technology, game-development, iot, machine-learning, mobile-development, real-time-systems, scientific-computing, systems-programming, web-backend, web-frontend |
| Agentic (24) | 24 | 15 | 62.5% | bash-execution, code-execution, database-query, error-recovery, file-read, file-write, git-operations, iterative-refinement, multi-file-coordination, planning, search, static-analysis, test-running, ui-automation, web-search |
| Task (18) | 18 | 15 | 83.3% | api-design, bug-fixing, code-completion, code-explanation, code-refactoring, code-review-task, configuration, deployment, feature-implementation, migration, monitoring, optimization, schema-design, security-audit, testing-task |
| Constraint (19) | 19 | 13 | 68.4% | accessible, backward-compatible, deterministic, fault-tolerant, idempotent, observable, performance-optimized, portable, scalable, stateless, thread-safe, type-safe, no-dynamic-allocation |
| Context (10) | 10 | 7 | 70.0% | greenfield, module, monorepo, multi-file, repository, single-file, snippet |
| Difficulty (4) | 4 | 4 | 100.0% | beginner, intermediate, advanced, expert |

**总计**: 252 个标签中命中 115 个，总覆盖率 **45.6%**。

#### v1 vs v2 覆盖率对比

| 指标 | v1 (10 samples, 7 categories) | v2 (20 samples, 9 categories) | 变化 |
|------|-------------------------------|-------------------------------|------|
| 样本数 | 10 | 20 | +100% |
| 类别数 | 7 | 9 | +2 |
| 标签总数 | ~198 | ~252 | +54 |
| 命中标签数 | ~72 | ~115 | +60% |
| 总覆盖率 | ~36.4% | ~45.6% | +9.2pp |
| Concept 命中率 | 61.9% | 71.4% | +9.5pp |
| Domain 命中率 | 45.2% | 67.7% | +22.5pp |
| Task 命中率 | 66.7% | 83.3% | +16.6pp |

样本量翻倍后，覆盖率提升显著（+9.2pp），Domain 和 Task 类别的覆盖率提升尤为明显，说明新增的 10 条样本有效补充了 v1 的盲区。但 Language 和 Library 的长尾标签仍需更有针对性的样本设计才能覆盖。

### 4.2 Library 类别专项分析

Library 是 v2 新增的核心类别，50 个标签中命中 13 个，命中率 26.0%。

#### 命中的 Library 标签 (13/50)

| Library | 命中查询 | 生态 |
|---------|---------|------|
| react | Q4, Q15 | 前端 |
| nextjs | Q12 | 前端 |
| prisma | Q12 | ORM |
| express | Q7 | 后端 |
| fastapi | Q19 | 后端 |
| pydantic | Q19 | 数据验证 |
| pytorch | Q3 | ML |
| hugging-face-transformers | Q3 | ML |
| flutter | Q8 | 移动 |
| playwright | Q15 | 测试 |
| spring-boot | Q10 | 后端 |
| tokio | Q9 | Rust async |
| redis | Q2 | 缓存 |

#### 未命中的 Library 标签 (37/50)

| 未命中分组 | 标签 |
|-----------|------|
| 前端框架 | vue, angular, svelte, tailwindcss, electron |
| 后端框架 | nestjs, django, flask, gin, laravel, symfony, rails, aspnet-core, axum |
| 数据/ML | numpy, pandas, tensorflow, scikit-learn, matplotlib, sqlalchemy, langchain, keras, xgboost, opencv |
| 构建工具 | webpack, vite, axios |
| 测试 | jest, junit, selenium, pytest |
| Rust 生态 | serde |
| 其他 | hibernate, gorm, entity-framework, boost, requests |

**关键发现**:
1. **前端三大框架只命中 React**，Vue 和 Angular 完全缺失
2. **Python ML 生态严重偏科**: pytorch + transformers 命中，但 numpy/pandas/tensorflow/scikit-learn 全部缺失
3. **Python Web 框架**: fastapi 命中但 django/flask 缺失——这两个是 Python Web 最主流的框架
4. **Java 生态**: spring-boot 命中但 hibernate/junit 缺失
5. **Go 生态**: gin/gorm 均未命中
6. **构建工具全军覆没**: webpack/vite/axios 无一命中

Library 类别的 26% 命中率说明 20 条样本远不足以覆盖 Top 50 库。这不是分类体系的问题，而是样本设计的问题——需要有针对性地为未覆盖的库设计查询。

### 4.3 Difficulty 分布分析

| Difficulty | 查询数 | 占比 | 查询 ID |
|-----------|--------|------|---------|
| beginner | 1 | 5% | Q11 |
| intermediate | 5 | 25% | Q4, Q12, Q14, Q15, Q20 |
| advanced | 8 | 40% | Q1, Q3, Q5, Q7, Q8, Q13, Q16, Q17, Q19 |
| expert | 6 | 30% | Q2, Q6, Q9, Q10, Q18 |

**分布问题**:
- **beginner 严重不足** (仅 1 条, 5%)：真实用户查询中初学者占比远高于 5%。SFT 数据如果 beginner 样本不足，模型对初学者的回答质量会下降。
- **advanced 偏多** (40%)：样本设计偏向复杂场景，这在评估分类体系时是合理的（复杂场景更能暴露标签不足），但在实际 SFT 数据中需要平衡。
- **intermediate 和 expert 相对合理**。

### 4.4 未命中标签分析

#### Language 未命中 (63/75)

大量语言未被覆盖是预期内的——75 种语言不可能在 20 条样本中全部出现。但以下高频语言的缺失值得关注：

| 高频但未命中 | 说明 |
|-------------|------|
| php | Web 开发主流语言，全球使用量巨大 |
| ruby | Rails 生态仍然活跃 |
| swift | iOS 开发主力语言 |
| kotlin | Android 开发主力语言 |
| scala | 大数据生态 (Spark) 核心语言 |
| shell | DevOps/运维高频语言 |
| css, html | 前端基础语言 |

#### Domain 未命中 (10/31)

| 未命中 Domain | 说明 |
|--------------|------|
| cli-tool | 无 CLI 工具开发场景 |
| compiler-development | 无编译器开发场景 |
| computer-vision | Q3 涉及多模态但未直接涉及 CV |
| desktop-application | 无桌面应用场景 |
| graphics-and-xr | 无图形/XR 场景 |
| media-processing | 无音视频处理场景 |
| natural-language-processing | 无 NLP 专项场景 |
| network-programming | 无网络编程场景 |
| operating-systems | 无 OS 开发场景 |
| robotics | 无机器人场景 |

#### Concept 未命中 (6/21)

| 未命中 Concept | 说明 |
|---------------|------|
| functional-programming | 无纯函数式编程场景 |
| object-oriented-programming | 虽然多个查询隐含 OOP，但未作为核心概念标注 |
| recursion | 无递归专项场景 |
| iterators | 未作为核心概念出现 |
| database-concepts | Q17 涉及但标注为 data-structures |
| version-control | 仅 Q19 间接涉及 git |

### 4.5 跨类别关联模式

通过 20 条样本，可以观察到一些有意义的标签共现模式：

| 模式 | 出现频率 | 说明 |
|------|---------|------|
| `performance-optimized` + `optimization` | 6/20 | Constraint 和 Task 高度关联 |
| `concurrency` + `thread-safe` | 3/20 | 并发概念自然关联线程安全约束 |
| `architecture` + `planning` | 4/20 | 架构设计类查询需要规划能力 |
| `security` + `security-audit` | 2/20 | 安全概念关联安全审计任务 |
| `greenfield` + `multi-file-coordination` | 3/20 | 新项目通常需要多文件协调 |
| `bug-fixing` + `iterative-refinement` | 3/20 | 修 bug 通常需要迭代 |

这些共现模式可以用于：(1) 标注一致性校验——如果标注了 `security` 但没标注 `security-audit`，可能需要复查；(2) 自动标注建议——基于已标注的标签推荐可能遗漏的标签。

---

## 5. 第三方专家评估 (v2)

> 评估者: 资深 ML 工程师 / SFT 数据标注系统设计经验
> 评估基准: v1 评估报告 (评分 7.2/10)

### 5.1 v2 改进评估

#### 5.1.1 Library 类别恢复 — 评估

**正面评价**:
- 直接回应了 v1 评估中最严重的缺陷（P0 #1），执行力好
- Top 50 的选择策略合理——覆盖了主流生态的核心库
- multi-select 设计正确，一个查询可以涉及多个库（如 Q12: nextjs + prisma）
- 标签粒度适中：选择 `react` 而非 `react-hooks` / `react-router` 是正确的

**问题与不足**:
1. **Top 50 的选择偏向 Web/JS 生态**: 前端 6 个 + 后端 Node.js 3 个 + 构建工具 3 个 = 12/50 (24%) 给了 JavaScript 生态。相比之下，C/C++ 生态只有 boost 和 opencv (4%)，Go 生态只有 gin 和 gorm (4%)。
2. **数据工程生态完全缺失**: Spark, Airflow, dbt, Kafka, Flink 等数据工程核心工具无一入选。Q13 的标注直接暴露了这个问题。
3. **科学计算生态缺失**: CUDA.jl, DifferentialEquations.jl, SciPy 等均不在列表中。Q18 的标注暴露了这个问题。
4. **区块链生态缺失**: OpenZeppelin, Hardhat, Foundry 等 Solidity 生态核心工具不在列表中。Q16 的标注暴露了这个问题。
5. **"Top 50" 的选择标准不透明**: 按什么指标排名？GitHub stars? npm/pip downloads? Stack Overflow 问题数？不同指标会产生不同的 Top 50。建议明确选择标准并公开数据来源。
6. **版本问题未解决**: `react` 标签无法区分 React 18 (class components) 和 React 19 (server components)。对于 SFT 数据来说，版本差异可能导致训练数据冲突。

#### 5.1.2 Difficulty 类别新增 — 评估

**正面评价**:
- 直接回应了 v1 评估中的 P0 #2 建议
- 4 级分类 (beginner/intermediate/advanced/expert) 是业界常见的分级方式，标注者容易理解
- single-select 设计正确，一个查询只有一个难度级别

**问题与不足**:
1. **定义模糊，缺乏可操作的判定标准**: "涉及性能优化"就是 advanced？"涉及底层原理"就是 expert？这些描述过于主观。Q20 的标注争议直接证明了这一点——同一个查询，不同标注者可能给出 intermediate 到 expert 的不同判断。
2. **单维度难度无法捕捉多维复杂性**: 一个查询可能"编码难度低但架构决策难度高"（如 Q20），或"概念简单但工程复杂度高"（如 Q5）。单一 Difficulty 标签过度简化了复杂性。
3. **缺乏锚定样本 (anchor examples)**: 每个级别应该提供 3-5 个标准样本作为标注参考，否则标注者之间的一致性 (inter-annotator agreement) 会很低。
4. **与 Concept 类别的 difficulty 属性重叠**: taxonomy.yaml 中 Concept 标签已有 `difficulty: basic | intermediate | advanced` 属性。现在又新增了顶层 Difficulty 类别，两者的关系未明确。一个 `beginner` 难度的查询是否可以涉及 `advanced` 难度的 Concept？

### 5.2 遗留问题（v1 未解决）

以下 v1 评估中提出的问题在 v2 中仍未解决：

| v1 问题 | v2 状态 | 严重程度 |
|---------|---------|---------|
| 缺少 "用户意图" 维度 (learn vs build vs debug) | 未解决 | P1 |
| 缺少 "输出格式" 维度 (code vs explanation vs diagram) | 未解决 | P1 |
| Agentic 类别的 tool-level 和 behavioral 混在一起 | 未解决 | P2 |
| 缺少标注者一致性 (IAA) 评估机制 | 未解决 | P1 |
| 缺少标注指南文档 (annotation guidelines) | 未解决 | P1 |
| Language 类别 75 个标签中大量低频语言 | 未解决 | P2 |

### 5.3 v2 新引入的问题

| 新问题 | 说明 | 严重程度 |
|--------|------|---------|
| Library Top 50 选择标准不透明 | 无法验证选择的合理性，也无法系统性地更新 | P1 |
| Library 生态覆盖不均衡 | JS/Python 过度代表，数据工程/科学计算/区块链缺失 | P1 |
| Difficulty 定义缺乏可操作性 | 无锚定样本，标注一致性存疑 | P1 |
| Difficulty 与 Concept.difficulty 属性语义重叠 | 两个不同层面的 "difficulty" 可能造成混淆 | P2 |
| 标签总数膨胀至 252 | 标注成本增加，但 Library 和 Difficulty 的边际收益需要验证 | P2 |
| Library 标签的时效性维护 | Top 50 会随时间变化，需要定期更新机制 | P2 |

### 5.4 评分（v2）

| 维度 | v1 评分 | v2 评分 | 变化 | 评价 |
|------|--------|--------|------|------|
| 完备性 (Completeness) | 6.5 | 7.5 | +1.0 | Library 和 Difficulty 填补了两个最大的缺口，但 "用户意图" 和 "输出格式" 维度仍缺失 |
| 正交性 (Orthogonality) | 8.0 | 7.5 | -0.5 | Difficulty 与 Concept.difficulty 属性存在语义重叠；Library 与 Language 的边界在某些场景下模糊（如 SQL 是 Language 还是 Library？） |
| 可操作性 (Operability) | 7.0 | 6.5 | -0.5 | 标签总数从 198 增至 252，标注负担增加；Difficulty 缺乏明确判定标准，降低了可操作性 |
| 可扩展性 (Extensibility) | 7.5 | 7.5 | 0 | Library Top 50 的扩展机制不明确；其他类别扩展性不变 |
| 工程实用性 (Engineering Utility) | 7.0 | 7.5 | +0.5 | Library 维度对 SFT 数据的实际价值很高（可以按框架筛选训练数据）；Difficulty 对数据平衡有直接帮助 |

**综合评分: 7.3 / 10** (v1: 7.2)

评分仅微幅提升 (+0.1)，原因是：
- Library 和 Difficulty 的新增确实解决了 v1 的两个最大痛点 (+1.0 完备性, +0.5 工程实用性)
- 但同时引入了新问题：正交性下降 (-0.5)、可操作性下降 (-0.5)
- v1 的多个 P1 问题仍未解决

### 5.5 与 v1 评估的对比总结

```
v1 评估核心建议 (P0):
  #1 恢复 Library 维度          → ✅ 已解决（但实现有偏差）
  #2 增加 Difficulty 维度       → ✅ 已解决（但定义不够清晰）

v1 评估核心建议 (P1):
  #3 增加用户意图维度           → ❌ 未解决
  #4 增加输出格式维度           → ❌ 未解决
  #5 建立标注一致性评估机制     → ❌ 未解决
  #6 编写标注指南文档           → ❌ 未解决

结论: v2 解决了 v1 的 P0 问题，但 P1 问题全部遗留。
```

### 5.6 生产就绪度评估

| 维度 | 就绪度 | 阻塞项 |
|------|--------|--------|
| 分类体系设计 | 🟡 基本就绪 | Difficulty 定义需要细化 |
| 标签覆盖度 | 🟡 基本就绪 | Library 生态覆盖不均需要补充 |
| 标注指南 | 🔴 未就绪 | 无标注指南文档 |
| 标注一致性 | 🔴 未就绪 | 无 IAA 评估，Difficulty 一致性存疑 |
| 工具支持 | 🟡 基本就绪 | 有 taxonomy.yaml + validate 脚本 |
| 样本验证 | 🟡 基本就绪 | 20 条样本覆盖率 45.6%，需要更多样本 |

### 5.7 最终建议（v2 → v3 路线图）

#### P0 — 必须在生产标注前完成

1. **编写 Difficulty 标注指南**: 为每个级别提供 5+ 个锚定样本，明确判定标准。特别要解决"编码难度 vs 综合难度"的歧义。建议定义为"回答该查询所需的编码能力水平"，而非"问题本身的复杂度"。

2. **编写完整标注指南 (Annotation Guidelines)**: 覆盖所有 9 个类别的标注规则、边界案例处理、常见争议的裁决标准。这是生产标注的前提条件。

3. **进行标注一致性测试 (IAA Pilot)**: 选取 50 条样本，由 3+ 名标注者独立标注，计算 Cohen's Kappa 或 Fleiss' Kappa。目标: 所有类别 κ > 0.7。

#### P1 — 应在第一批标注数据完成后迭代

4. **补充 Library 覆盖盲区**: 增加数据工程 (spark, airflow, kafka, flink)、科学计算 (scipy, cuda)、区块链 (openzeppelin, hardhat) 等生态的核心库。建议将 Top 50 扩展为 Top 80，或按生态配额分配。

5. **明确 Library Top 50 选择标准**: 公开选择方法论（如 "GitHub stars > 10k + npm/pip weekly downloads > 100k + 出现在 Stack Overflow 年度调查 Top 50"），并建立年度更新机制。

6. **考虑增加 Intent 维度**: `learn` / `build` / `debug` / `review` / `decide` — 这对 SFT 数据的回答风格调控至关重要。Q11 (learn) 和 Q12 (build) 需要完全不同的回答策略。

#### P2 — 长期优化

7. **解决 Difficulty 与 Concept.difficulty 的语义重叠**: 建议移除 Concept 标签上的 difficulty 属性，统一使用顶层 Difficulty 类别。

8. **建立标签使用频率监控**: 在实际标注过程中统计每个标签的使用频率，识别"僵尸标签"（从未被使用的标签）和"过载标签"（使用频率异常高的标签），据此调整分类体系。

9. **考虑 Agentic 类别的子类别拆分**: 将 tool-level actions (18) 和 behavioral patterns (6) 正式拆分为两个子类别，提高标注清晰度。

---

## 附录 A: 标签命中热力图

```
Category        ████████████████████ 命中率
─────────────────────────────────────────
Difficulty      ████████████████████ 100.0%  (4/4)
Task            ████████████████░░░░  83.3%  (15/18)
Concept         ██████████████░░░░░░  71.4%  (15/21)
Context         ██████████████░░░░░░  70.0%  (7/10)
Constraint      █████████████░░░░░░░  68.4%  (13/19)
Domain          █████████████░░░░░░░  67.7%  (21/31)
Agentic         ████████████░░░░░░░░  62.5%  (15/24)
Library         █████░░░░░░░░░░░░░░░  26.0%  (13/50)
Language        ███░░░░░░░░░░░░░░░░░  16.0%  (12/75)
─────────────────────────────────────────
Overall         █████████░░░░░░░░░░░  45.6%  (115/252)
```

## 附录 B: Difficulty 分布可视化

```
beginner     █░░░░░░░░░░░░░░░░░░░  5%   (1)
intermediate █████░░░░░░░░░░░░░░░░ 25%  (5)
advanced     ████████░░░░░░░░░░░░░ 40%  (8)
expert       ██████░░░░░░░░░░░░░░░ 30%  (6)
```

## 附录 C: 20 条样本的 Persona-Difficulty 矩阵

| Persona 类型 | beginner | intermediate | advanced | expert |
|-------------|----------|-------------|----------|--------|
| 学生/初学者 | Q11 | Q14 | | |
| 中级工程师 | | Q4, Q12, Q15 | | |
| 高级工程师 | | | Q1, Q3, Q5, Q7, Q8, Q13, Q16, Q17, Q19 | Q2, Q6, Q9, Q10, Q18 |
| 管理/架构 | | Q20 | | |

**观察**: 高级工程师 persona 过度集中在 advanced/expert 区间，缺少"高级工程师问简单问题"的场景（现实中很常见，如资深工程师学习新语言/框架时会问 intermediate 甚至 beginner 级别的问题）。

---

> **报告结论**: v2 分类体系通过恢复 Library 类别和新增 Difficulty 类别，解决了 v1 的两个最关键缺陷。综合评分从 7.2 微升至 7.3，反映了"解决旧问题的同时引入了新问题"的现实。在投入生产标注前，最紧迫的任务是编写标注指南和进行标注一致性测试——分类体系的设计已经"基本够用"，但标注的可操作性和一致性仍是最大风险。

