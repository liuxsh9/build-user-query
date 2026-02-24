# SFT 数据标注指南 (Annotation Guidelines)

> Version: 1.1 | 适用于 Taxonomy v3.1 (9 类别, 221 标签)

---

## 1. 总则

### 1.1 标注目标

为每条用户查询 (query) 分配一组标签，描述该查询涉及的编程语言、领域、概念、任务类型、约束条件、Agent 能力需求、代码上下文、难度级别和用户意图。标注结果用于 SFT 训练数据的筛选、平衡和质量控制。

### 1.2 标注原则

1. **只标注明确信号**：标签必须有查询文本中的直接证据支持。不要推测隐含信息。
2. **宁缺勿滥**：不确定时不标注。少标一个正确标签的损害远小于多标一个错误标签。
3. **独立维度**：每个类别回答不同的问题（见下表）。标注一个类别时，不要受其他类别标注的影响。
4. **以回答所需能力为准**：标注的是"回答这个查询需要什么"，而非"查询本身是什么"。

### 1.3 类别维度定义

| 类别 | 回答的问题 | 选择方式 |
|------|-----------|---------|
| Language | 涉及哪些编程语言？ | multi-select |
| Domain | 属于什么应用领域？ | multi-select |
| Concept | 需要掌握哪些编程概念？ | multi-select |
| Task | 在执行什么类型的工作？ | multi-select |
| Constraint | 有哪些非功能性约束？ | multi-select |
| Agentic | Agent 需要什么能力？ | multi-select |
| Context | 代码范围/项目上下文是什么？ | single-select |
| Difficulty | 回答所需的编码能力水平？ | single-select |
| Intent | 用户的主要目标是什么？ | single-select |

---

## 2. 各类别标注规则

### 2.1 Language (多选)

**标注什么**: 查询中明确使用或要求使用的编程语言。

**规则**:
- 看代码片段中实际使用的语言
- 看用户明确提到的语言
- 如果用户提到框架但未提到语言，根据框架推断语言（如 Django → Python, Spring Boot → Java）
- 配置文件格式也算语言（YAML, JSON, Dockerfile 等）
- 如果查询纯粹是架构/选型讨论，不涉及具体编码，Language 可以为空

**边界案例**:
- "用 Next.js 做一个网站" → `typescript`（Next.js 默认 TypeScript）
- "帮我写个 Docker Compose 文件" → `yaml`, `dockerfile`
- "单体 vs 微服务怎么选？" → 空（纯讨论）
- "这段代码有什么问题？" + Python 代码 → `python`

### 2.2 Domain (多选)

**标注什么**: 查询涉及的应用领域或行业场景。

**规则**:
- 标注查询所在的应用场景，而非涉及的技术领域
- 一个查询可以跨多个领域（如"SaaS 支付系统" → `web-backend`, `e-commerce`, `financial-technology`）
- 纯学习/练习场景无明确领域时，Domain 可以为空
- 优先选择最具体的领域标签

**边界案例**:
- "帮我写个排序算法" → 空（纯算法练习，无应用领域）
- "优化这个 SQL 查询" → `database-administration`
- "做一个 IoT 设备的固件" → `embedded-systems`, `iot`

### 2.3 Concept (多选)

**标注什么**: 回答该查询需要掌握的编程概念和知识领域。

**规则**:
- 标注回答所需的**核心**概念，不需要标注所有沾边的概念
- 一般标注 1-4 个概念，极少超过 5 个
- 选择伞形概念（如 `concurrency`），不需要分解到子概念（如线程、互斥锁）
- 如果查询仅涉及框架使用而无深层概念，可以只标注 1 个

**边界案例**:
- "Rust lifetime 报错" → `ownership`, `type-system`（不需要拆分为 borrow-checker + lifetimes）
- "写一个 REST API" → `api-protocols`（简单场景只需 1 个概念）
- "设计一个高并发消息队列" → `concurrency`, `architecture`, `data-structures`

### 2.4 Task (多选)

**标注什么**: 用户要求执行的工作类型。

**规则**:
- 标注查询中明确或隐含的任务类型
- 一般标注 1-3 个任务
- `feature-implementation` 是最常见的"兜底"任务 — 如果用户要写新代码且不属于其他特定任务，用这个
- `code-explanation` 和 `code-review-task` 不产生新代码，只产生分析/反馈

**边界案例**:
- "帮我把这个 class 拆成更小的模块" → `code-refactoring`
- "这段代码为什么报错？" → `bug-fixing`（即使用户没说"修复"）
- "帮我设计数据库表结构" → `schema-design`
- "帮我接 Stripe 支付" → `feature-implementation`, `api-design`

### 2.5 Constraint (多选)

**标注什么**: 查询中明确提到或强烈暗示的非功能性约束。

**规则**:
- **只标注明确提到的约束**，不要推测
- "性能要好" → `performance-optimized`；没提性能就不标
- 合规类约束（GDPR, HIPAA, PCI-DSS）必须有明确提及
- 如果查询没有非功能性要求，Constraint 为空是正常的

**边界案例**:
- "要求 < 500ms 响应" → `performance-optimized`
- "不要用第三方库" → `no-external-dependencies`
- "做一个 HIPAA 合规的系统" → `hipaa-compliant`
- "帮我写个排序函数" → 空（未提到约束）

### 2.6 Agentic (多选)

**标注什么**: 一个 AI Agent 在回答此查询时需要使用的工具和行为模式。

**规则**:
- Tool Actions：Agent 需要调用的具体工具（文件操作、shell、搜索等）
- Behavioral Patterns：Agent 需要的认知策略（规划、迭代、多文件协调等）
- 如果查询是简单问答，不需要工具调用，Agentic 可以为空
- 区分"回答需要什么"和"查询讨论什么"：用户问"如何使用 Git"不代表 Agent 需要 `git-operations`

**边界案例**:
- "解释 Rust 的 ownership" → 空（纯知识问答）
- "帮我从零搭建项目" → `file-operations`, `multi-file-coordination`, `planning`
- "帮我修复这个 bug" → `file-operations`, `iterative-refinement`
- "运行一下这段代码看看结果" → `code-execution`

### 2.7 Context (单选)

**标注什么**: 查询涉及的代码范围和项目上下文。

**规则**:
- 按代码范围从小到大选择最匹配的一个
- `snippet` < `single-function` < `single-file` < `multi-file` < `module` < `repository` < `monorepo`
- `greenfield` = 从零开始的新项目
- `legacy-code` = 维护/重构已有代码

**选择优先级**:
1. 如果用户明确说"新项目" → `greenfield`
2. 如果用户明确说"维护/重构旧代码" → `legacy-code`
3. 否则按代码范围选择

### 2.8 Difficulty (单选)

**标注什么**: 产出高质量回答所需的**编码能力**水平。

**关键定义**: Difficulty 衡量的是**编码难度**，不是**问题复杂度**或**知识广度**。

| 级别 | 判定标准 | 典型场景 |
|------|---------|---------|
| `beginner` | 只需基础语法和标准库 | 读 CSV, 写 for 循环, 基础 API 调用 |
| `intermediate` | 需要框架知识和标准工程实践 | React 组件, REST API, 基础 CI/CD |
| `advanced` | 需要深入的技术知识和非平凡的设计 | SQL 优化, 并发 bug 修复, 复杂架构设计 |
| `expert` | 需要多年深厚领域经验 | GPU 并行化, 分布式一致性协议, 编译器开发 |

**边界案例**:
- "单体 vs 微服务怎么选？" → `intermediate`（决策不需要 expert 编码能力，虽然需要广泛经验）
- "帮我优化这个 12 秒的 SQL" → `advanced`（需要深入理解查询计划和索引）
- "用 CUDA 并行化 Navier-Stokes 求解器" → `expert`（需要 HPC + 数值分析经验）

### 2.9 Intent (单选)

**标注什么**: 用户的主要目标或动机。

| Intent | 判定信号 | 回答风格 |
|--------|---------|---------|
| `learn` | "怎么理解""讲讲""区别是什么" | 教学式：解释原理，给例子 |
| `build` | "帮我做""实现""搭建" | 实现式：给可运行的代码 |
| `debug` | "报错了""不工作""为什么失败" | 诊断式：定位原因，给修复 |
| `review` | "帮我看看""有什么问题""改进建议" | 评审式：指出问题，建议改进 |
| `decide` | "选哪个""A vs B""怎么选" | 分析式：比较方案，给建议 |

**边界案例**:
- "这段代码为什么报错？帮我修一下" → `debug`（主要目标是修复，不是学习）
- "帮我做一个支付模块，顺便解释下 Stripe API" → `build`（主要目标是实现）
- "React 和 Vue 我该学哪个？" → `decide`

---

## 3. 跨类别一致性检查

标注完所有类别后，进行以下一致性检查：

| 检查规则 | 说明 |
|---------|------|
| Language 非空时，Domain 通常非空 | 如果涉及具体编程，通常有应用领域 |
| Intent=learn 时，Agentic 通常较少 | 学习类查询很少需要工具调用 |
| Intent=build 时，Task 通常包含 feature-implementation | 构建类查询核心是实现功能 |
| Difficulty=beginner 时，Concept 通常 ≤ 2 | 简单查询不会涉及太多概念 |
| Constraint 非空时，Difficulty 通常 ≥ intermediate | 有明确约束的查询通常不是入门级 |
| Context=greenfield + Agentic=multi-file-coordination | 新项目通常需要多文件协调 |

这些是**软规则**（启发式检查），不是硬约束。如果违反了，请复查标注是否正确。

---

## 4. 常见争议裁决

### 4.1 一个概念 vs 多个概念

**原则**: 标注最具代表性的伞形概念。

- ❌ `authentication`, `encryption`, `xss` → 太细
- ✅ `security` → 足够

### 4.2 Task 和 Agentic 边界

**原则**: Task = 用户要什么 (output)，Agentic = Agent 怎么做 (process)。

- "帮我写测试" → Task: `testing-task`, Agentic: `file-operations`
- "运行测试看看通不通过" → Task: `testing-task`, Agentic: `test-running`

### 4.3 Domain 和 Concept 边界

**原则**: Domain = 应用场景 (where)，Concept = 知识需求 (what knowledge)。

- 查询关于"数据库慢查询优化" → Domain: `database-administration`, Concept: `database-concepts`, `profiling`
- 查询关于"做一个安全审计工具" → Domain: `cybersecurity`, Concept: `security`

### 4.4 Difficulty 的"编码难度 vs 综合难度"

**裁决**: 始终按编码难度标注。

- CTO 做技术选型讨论 → `intermediate`（不需要高级编码能力）
- 初学者写简单 CRUD → `beginner`（即使对初学者来说很难）
- 资深工程师问简单问题 → `beginner`（不管提问者水平）

---

## 5. 标注流程

1. **通读查询**：完整阅读用户查询，理解整体需求
2. **标注 Intent**：先确定用户目标（这会影响对其他类别的理解）
3. **标注 Language + Domain**：确定技术栈和应用领域
4. **标注 Concept + Task**：确定知识需求和任务类型
5. **标注 Constraint**：检查是否有明确的非功能性约束
6. **标注 Agentic**：判断 Agent 需要什么能力来回答
7. **标注 Context + Difficulty**：确定代码范围和难度
8. **一致性检查**：按第 3 节的规则进行交叉验证
