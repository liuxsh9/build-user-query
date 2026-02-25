# Model Comparison Report: Labeling Pipeline Evaluation

> Generated: 2026-02-25 13:02:50
> Dataset: 108 samples
> Models: **deepseek-v3-prompt-v3** vs **deepseek-v3-prompt-v4**

## 1. Pipeline Metrics Overview

| Metric | deepseek-v3-prompt-v3 | deepseek-v3-prompt-v4 |
|--------|---------------------------------------------------------------|---------------------------------------------------------------|
| Success rate | 100.0% | 100.0% |
| Avg calls/sample | 2.0 | 2.0 |
| Total tokens | 1,262,396 | 1,302,588 |
| Arbitration rate | 0.0% | 0.0% |
| Elapsed | 764s | 522s |
| Unmapped tags | 3 | 3 |

## 2. Confidence Comparison (mean)

| Dimension | deepseek-v3-prompt-v3 | deepseek-v3-prompt-v4 | Delta |
|-----------|---------------------------------------------------------------|---------------------------------------------------------------|-------|
| intent | 0.979 █████████ | 0.973 █████████ | -0.006 |
| language | 0.969 █████████ | 0.963 █████████ | -0.006 |
| domain | 0.917 █████████ | 0.911 █████████ | -0.006 |
| task | 0.930 █████████ | 0.929 █████████ | -0.001 |
| difficulty | 0.855 ████████ | 0.849 ████████ | -0.006 |
| concept | 0.900 █████████ | 0.910 █████████ | +0.010 |
| agentic | 0.977 █████████ | 0.979 █████████ | +0.002 |
| constraint | 0.970 █████████ | 0.971 █████████ | +0.001 |
| context | 0.904 █████████ | 0.914 █████████ | +0.010 |

## 3. Inter-Model Agreement

| Dimension | Select | Exact Match | Partial Match | Jaccard |
|-----------|--------|-------------|---------------|---------|
| intent | single | 100.0% ██████████ | 100.0% | 1.000 |
| language | multi | 84.3% ████████ | 97.2% | 0.916 |
| domain | multi | 82.4% ████████ | 96.3% | 0.890 |
| task | multi | 75.9% ███████ | 100.0% | 0.891 |
| difficulty | single | 95.4% █████████ | 95.4% | 0.954 |
| concept | multi | 50.0% █████ | 88.9% | 0.701 |
| agentic | multi | 94.4% █████████ | 99.1% | 0.979 |
| constraint | multi | 94.4% █████████ | 96.3% | 0.954 |
| context | single | 87.0% ████████ | 87.0% | 0.870 |

## 4. Tag Distribution Comparison

### Intent

| Tag | deepseek-v3-prompt-v3 | deepseek-v3-prompt-v4 | Diff |
|-----|---------------------------------------------------------------|---------------------------------------------------------------|------|
| build | 57 | 57 | 0 |
| debug | 14 | 14 | 0 |
| decide | 9 | 9 | 0 |
| learn | 22 | 22 | 0 |
| review | 6 | 6 | 0 |

### Difficulty

| Tag | deepseek-v3-prompt-v3 | deepseek-v3-prompt-v4 | Diff |
|-----|---------------------------------------------------------------|---------------------------------------------------------------|------|
| advanced | 21 | 18 | -3 |
| beginner | 12 | 14 | +2 |
| expert | 6 | 6 | 0 |
| intermediate | 69 | 70 | +1 |

### Domain

| Tag | deepseek-v3-prompt-v3 | deepseek-v3-prompt-v4 | Diff |
|-----|---------------------------------------------------------------|---------------------------------------------------------------|------|
| api-development | 14 | 11 | -3 |
| automation | 1 | 1 | 0 |
| blockchain | 1 | 1 | 0 |
| cli-tool | 2 | 2 | 0 |
| cloud-computing | 1 | 3 | +2 |
| compiler-development | 3 | 3 | 0 |
| compliance | 1 | 0 | -1 |
| computer-vision | 1 | 0 | -1 |
| cybersecurity | 3 | 3 | 0 |
| data-engineering | 3 | 4 | +1 |
| data-science | 3 | 2 | -1 |
| database-administration | 11 | 12 | +1 |
| devops | 20 | 18 | -2 |
| e-commerce | 1 | 1 | 0 |
| financial-technology | 2 | 2 | 0 |

### Concept

| Tag | deepseek-v3-prompt-v3 | deepseek-v3-prompt-v4 | Diff |
|-----|---------------------------------------------------------------|---------------------------------------------------------------|------|
| algorithms | 18 | 16 | -2 |
| api-protocols | 14 | 12 | -2 |
| architecture | 14 | 8 | -6 |
| caching | 1 | 3 | +2 |
| ci-cd | 11 | 6 | -5 |
| concurrency | 23 | 22 | -1 |
| control-flow | 2 | 2 | 0 |
| data-structures | 27 | 17 | -10 |
| database-concepts | 20 | 17 | -3 |
| design-patterns | 2 | 2 | 0 |
| error-handling | 14 | 9 | -5 |
| functions | 9 | 3 | -6 |
| iterators | 1 | 0 | -1 |
| memory-management | 11 | 10 | -1 |
| metaprogramming | 0 | 2 | +2 |

### Task

| Tag | deepseek-v3-prompt-v3 | deepseek-v3-prompt-v4 | Diff |
|-----|---------------------------------------------------------------|---------------------------------------------------------------|------|
| api-design | 15 | 14 | -1 |
| bug-fixing | 12 | 12 | 0 |
| code-explanation | 35 | 33 | -2 |
| code-optimization | 11 | 8 | -3 |
| code-refactoring | 1 | 1 | 0 |
| code-review-task | 6 | 6 | 0 |
| code-translation | 2 | 2 | 0 |
| configuration | 21 | 22 | +1 |
| dependency-management | 5 | 4 | -1 |
| deployment | 6 | 6 | 0 |
| error-handling-task | 9 | 7 | -2 |
| feature-implementation | 48 | 47 | -1 |
| logging | 1 | 0 | -1 |
| migration | 1 | 1 | 0 |
| monitoring | 2 | 3 | +1 |

## 5. Key Disagreements

### Difficulty disagreements

**gen-0004**: _Git 的 merge 和 rebase 有什么区别？_
- deepseek-v3-prompt-v3: `intermediate` (conf: 0.8)
- deepseek-v3-prompt-v4: `beginner` (conf: 0.95)

**gen-0022**: _Write a simple HTML page with a form that validates email and password on submit using JavaScript_
- deepseek-v3-prompt-v3: `intermediate` (conf: 0.8)
- deepseek-v3-prompt-v4: `beginner` (conf: 0.85)

**gen-0058**: _Go 程序偶现 panic: concurrent map writes，但我已经用了 sync.Mutex，代码：
```go
type Cache struct {
    mu    sync.Mutex
    items map[..._
- deepseek-v3-prompt-v3: `advanced` (conf: 0.85)
- deepseek-v3-prompt-v4: `intermediate` (conf: 0.8)

### Concept disagreements

**gen-0000**: _Python 列表推导式和生成器表达式的区别是什么？给个例子_
- deepseek-v3-prompt-v3: `functions, iterators` (conf: 0.88)
- deepseek-v3-prompt-v4: `` (conf: 0.98)

**gen-0008**: _Rust 的 ownership 和 borrowing 是什么意思？为什么要这样设计？_
- deepseek-v3-prompt-v3: `ownership, memory-management` (conf: 0.95)
- deepseek-v3-prompt-v4: `ownership` (conf: 0.95)

**gen-0011**: _请解释动态规划的背包问题，0/1 背包和完全背包有什么区别？用 Python 代码举例_
- deepseek-v3-prompt-v3: `algorithms, data-structures` (conf: 0.95)
- deepseek-v3-prompt-v4: `algorithms` (conf: 0.95)

### Agentic disagreements

**gen-0028**: _帮我用 Flask 写一个 REST API，支持对用户的 CRUD 操作，用 SQLite 存储_
- deepseek-v3-prompt-v3: `planning` (conf: 0.75)
- deepseek-v3-prompt-v4: `` (conf: 0.98)

**gen-0077**: _我的 FastAPI 应用在生产环境偶现 500 错误，日志显示 sqlalchemy.exc.TimeoutError。能帮我诊断一下吗？_
- deepseek-v3-prompt-v3: `file-operations, bash-execution, multi-file-coordination, planning, multi-step-reasoning, iterative-refinement` (conf: 0.92)
- deepseek-v3-prompt-v4: `file-operations, bash-execution, multi-step-reasoning, planning, iterative-refinement` (conf: 0.95)

**gen-0078**: _帮我把这个 2000 行的 Express.js 单文件 API 重构成模块化结构_
- deepseek-v3-prompt-v3: `file-operations, bash-execution, multi-file-coordination, planning, iterative-refinement` (conf: 0.94)
- deepseek-v3-prompt-v4: `bash-execution, file-operations, multi-file-coordination, planning` (conf: 0.95)

### Context disagreements

**gen-0019**: _什么是 CRDT (Conflict-free Replicated Data Type)？和 OT 算法比有什么优劣？_
- deepseek-v3-prompt-v3: `single-file` (conf: 0.85)
- deepseek-v3-prompt-v4: `snippet` (conf: 0.9)

**gen-0032**: _帮我写一个 Docker Compose 文件，包含 Nginx + Node.js app + PostgreSQL + Redis_
- deepseek-v3-prompt-v3: `multi-file` (conf: 0.9)
- deepseek-v3-prompt-v4: `greenfield` (conf: 0.95)

**gen-0037**: _Implement a rate limiter middleware in Express.js using the sliding window algorithm with Redis_
- deepseek-v3-prompt-v3: `multi-file` (conf: 0.92)
- deepseek-v3-prompt-v4: `single-file` (conf: 0.92)

## 6. Unmapped Tags

| Tag | deepseek-v3-prompt-v3 | deepseek-v3-prompt-v4 |
|-----|---------------------------------------------------------------|---------------------------------------------------------------|
| concept:performance-optimized | 1 | 1 |
| concept:portable | 1 | 0 |
| language:cuda | 1 | 1 |
| task:automation | 0 | 1 |

## 7. Model Selection Recommendation

**Overall inter-model agreement: 84.9%**

- Token usage ratio (deepseek-v3-prompt-v4/deepseek-v3-prompt-v3): 1.03x
- Time ratio (deepseek-v3-prompt-v4/deepseek-v3-prompt-v3): 0.68x

High agreement (>80%) suggests both models produce consistent labels. The cheaper model (deepseek-v3-prompt-v3) may be sufficient for production use.

---
_Report generated by `scripts/compare_models.py` at 2026-02-25T13:02:50.568418_