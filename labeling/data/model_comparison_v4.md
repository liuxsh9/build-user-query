# Model Comparison Report: Labeling Pipeline Evaluation

> Generated: 2026-02-25 12:20:03
> Dataset: 108 samples
> Models: **deepseek-v3.2** vs **claude-sonnet-4-6**

## 1. Pipeline Metrics Overview

| Metric | deepseek-v3.2 | claude-sonnet-4-6 |
|--------|---------------------------------------|---------------------------------------------------|
| Success rate | 100.0% | 100.0% |
| Avg calls/sample | 2.0 | 2.0 |
| Total tokens | 1,302,588 | 1,544,645 |
| Arbitration rate | 0.0% | 2.8% |
| Elapsed | 522s | 357s |
| Unmapped tags | 3 | 33 |

## 2. Confidence Comparison (mean)

| Dimension | deepseek-v3.2 | claude-sonnet-4-6 | Delta |
|-----------|---------------------------------------|---------------------------------------------------|-------|
| intent | 0.973 █████████ | 0.974 █████████ | +0.001 |
| language | 0.963 █████████ | 0.945 █████████ | -0.018 |
| domain | 0.911 █████████ | 0.905 █████████ | -0.006 |
| task | 0.929 █████████ | 0.907 █████████ | -0.022 |
| difficulty | 0.849 ████████ | 0.846 ████████ | -0.003 |
| concept | 0.910 █████████ | 0.872 ████████ | -0.038 |
| agentic | 0.979 █████████ | 0.968 █████████ | -0.011 |
| constraint | 0.971 █████████ | 0.918 █████████ | -0.053 |
| context | 0.914 █████████ | 0.879 ████████ | -0.035 |

## 3. Inter-Model Agreement

| Dimension | Select | Exact Match | Partial Match | Jaccard |
|-----------|--------|-------------|---------------|---------|
| intent | single | 99.1% █████████ | 99.1% | 0.991 |
| language | multi | 69.4% ██████ | 100.0% | 0.868 |
| domain | multi | 63.0% ██████ | 88.9% | 0.767 |
| task | multi | 60.2% ██████ | 98.2% | 0.792 |
| difficulty | single | 84.3% ████████ | 84.3% | 0.843 |
| concept | multi | 50.9% █████ | 90.7% | 0.706 |
| agentic | multi | 88.0% ████████ | 97.2% | 0.949 |
| constraint | multi | 68.5% ██████ | 80.6% | 0.736 |
| context | single | 71.3% ███████ | 71.3% | 0.713 |

## 4. Tag Distribution Comparison

### Intent

| Tag | deepseek-v3.2 | claude-sonnet-4-6 | Diff |
|-----|---------------------------------------|---------------------------------------------------|------|
| build | 57 | 57 | 0 |
| debug | 14 | 15 | +1 |
| decide | 9 | 9 | 0 |
| learn | 22 | 21 | -1 |
| review | 6 | 6 | 0 |

### Difficulty

| Tag | deepseek-v3.2 | claude-sonnet-4-6 | Diff |
|-----|---------------------------------------|---------------------------------------------------|------|
| advanced | 18 | 22 | +4 |
| beginner | 14 | 13 | -1 |
| expert | 6 | 12 | +6 |
| intermediate | 70 | 61 | -9 |

### Domain

| Tag | deepseek-v3.2 | claude-sonnet-4-6 | Diff |
|-----|---------------------------------------|---------------------------------------------------|------|
| api-development | 11 | 15 | +4 |
| automation | 1 | 3 | +2 |
| blockchain | 1 | 1 | 0 |
| cli-tool | 2 | 8 | +6 |
| cloud-computing | 3 | 5 | +2 |
| compiler-development | 3 | 2 | -1 |
| compliance | 0 | 1 | +1 |
| computer-vision | 0 | 1 | +1 |
| cybersecurity | 3 | 4 | +1 |
| data-engineering | 4 | 3 | -1 |
| data-science | 2 | 2 | 0 |
| database-administration | 12 | 18 | +6 |
| devops | 18 | 20 | +2 |
| e-commerce | 1 | 2 | +1 |
| financial-technology | 2 | 2 | 0 |

### Concept

| Tag | deepseek-v3.2 | claude-sonnet-4-6 | Diff |
|-----|---------------------------------------|---------------------------------------------------|------|
| algorithms | 16 | 14 | -2 |
| api-protocols | 12 | 10 | -2 |
| architecture | 8 | 8 | 0 |
| caching | 3 | 5 | +2 |
| ci-cd | 6 | 8 | +2 |
| concurrency | 22 | 28 | +6 |
| control-flow | 2 | 2 | 0 |
| data-structures | 17 | 12 | -5 |
| database-concepts | 17 | 20 | +3 |
| design-patterns | 2 | 6 | +4 |
| error-handling | 9 | 14 | +5 |
| functions | 3 | 1 | -2 |
| iterators | 0 | 1 | +1 |
| memory-management | 10 | 12 | +2 |
| metaprogramming | 2 | 2 | 0 |

### Task

| Tag | deepseek-v3.2 | claude-sonnet-4-6 | Diff |
|-----|---------------------------------------|---------------------------------------------------|------|
| api-design | 14 | 8 | -6 |
| bug-fixing | 12 | 16 | +4 |
| code-explanation | 33 | 36 | +3 |
| code-optimization | 8 | 5 | -3 |
| code-refactoring | 1 | 2 | +1 |
| code-review-task | 6 | 6 | 0 |
| code-translation | 2 | 2 | 0 |
| configuration | 22 | 18 | -4 |
| dependency-management | 4 | 4 | 0 |
| deployment | 6 | 4 | -2 |
| error-handling-task | 7 | 11 | +4 |
| feature-implementation | 47 | 59 | +12 |
| logging | 0 | 1 | +1 |
| migration | 1 | 1 | 0 |
| monitoring | 3 | 3 | 0 |

## 5. Key Disagreements

### Intent disagreements

**gen-0053**: _Python pandas merge 两个 DataFrame 后行数比两个原始表都多，为什么？
```python
df1 = pd.DataFrame({'key': ['a','a','b'], 'val1': [1,2,3]})
..._
- deepseek-v3.2: `learn` (conf: 0.95)
- claude-sonnet-4-6: `debug` (conf: 0.92)

### Difficulty disagreements

**gen-0004**: _Git 的 merge 和 rebase 有什么区别？_
- deepseek-v3.2: `beginner` (conf: 0.95)
- claude-sonnet-4-6: `intermediate` (conf: 0.8)

**gen-0015**: _讲讲 Python 的 GIL（全局解释器锁），为什么多线程在 CPU 密集型任务上没用？_
- deepseek-v3.2: `intermediate` (conf: 0.8)
- claude-sonnet-4-6: `advanced` (conf: 0.8)

**gen-0017**: _什么是 CAP 定理？在实际分布式系统设计中怎么做取舍？_
- deepseek-v3.2: `intermediate` (conf: 0.8)
- claude-sonnet-4-6: `advanced` (conf: 0.82)

### Concept disagreements

**gen-0000**: _Python 列表推导式和生成器表达式的区别是什么？给个例子_
- deepseek-v3.2: `` (conf: 0.98)
- claude-sonnet-4-6: `iterators` (conf: 0.92)

**gen-0008**: _Rust 的 ownership 和 borrowing 是什么意思？为什么要这样设计？_
- deepseek-v3.2: `ownership` (conf: 0.95)
- claude-sonnet-4-6: `ownership, memory-management` (conf: 0.95)

**gen-0012**: _TypeScript 的泛型 (Generics) 是什么？什么时候该用？给几个实际的使用场景_
- deepseek-v3.2: `type-system` (conf: 0.95)
- claude-sonnet-4-6: `type-system, object-oriented-programming` (conf: 0.92)

### Agentic disagreements

**gen-0041**: _帮我设计一个分布式限流器，要求支持滑动窗口算法，用 Redis + Lua 脚本实现_
- deepseek-v3.2: `` (conf: 0.98)
- claude-sonnet-4-6: `planning, multi-step-reasoning` (conf: 0.72)

**gen-0045**: _帮我写一个 Kubernetes Operator (用 Go + controller-runtime)，管理自定义资源 MyApp 的生命周期_
- deepseek-v3.2: `` (conf: 0.98)
- claude-sonnet-4-6: `planning, multi-file-coordination` (conf: 0.85)

**gen-0077**: _我的 FastAPI 应用在生产环境偶现 500 错误，日志显示 sqlalchemy.exc.TimeoutError。能帮我诊断一下吗？_
- deepseek-v3.2: `file-operations, bash-execution, multi-step-reasoning, planning, iterative-refinement` (conf: 0.95)
- claude-sonnet-4-6: `bash-execution, file-operations, multi-file-coordination, multi-step-reasoning, planning` (conf: 0.92)

### Context disagreements

**gen-0011**: _请解释动态规划的背包问题，0/1 背包和完全背包有什么区别？用 Python 代码举例_
- deepseek-v3.2: `snippet` (conf: 0.9)
- claude-sonnet-4-6: `single-file` (conf: 0.82)

**gen-0014**: _Docker 的 multi-stage build 是什么？有什么好处？给个例子_
- deepseek-v3.2: `snippet` (conf: 0.95)
- claude-sonnet-4-6: `single-file` (conf: 0.85)

**gen-0029**: _Write a React component that implements infinite scroll with a loading spinner and error handling_
- deepseek-v3.2: `single-file` (conf: 0.95)
- claude-sonnet-4-6: `multi-file` (conf: 0.9)

## 6. Unmapped Tags

| Tag | deepseek-v3.2 | claude-sonnet-4-6 |
|-----|---------------------------------------|---------------------------------------------------|
| CRD | 0 | 1 |
| architecture-decision | 0 | 1 |
| ast-construction | 0 | 1 |
| computer-vision | 0 | 1 |
| concept:idempotent | 0 | 1 |
| concept:observable | 0 | 1 |
| concept:performance-optimized | 1 | 0 |
| controller-runtime | 0 | 1 |
| cuda | 0 | 1 |
| dependency-management | 0 | 1 |
| distributed-systems | 0 | 2 |
| docker-multi-stage-build | 0 | 1 |
| framework-comparison | 0 | 1 |
| helm-deployment | 0 | 1 |
| hyperparameter-tuning | 0 | 1 |
| idempotent | 0 | 1 |
| jit-compilation | 0 | 1 |
| kubernetes-monitoring | 0 | 1 |
| kubernetes-operator | 0 | 1 |
| language:csv | 0 | 1 |
| language:cuda | 1 | 0 |
| llvm-ir-generation | 0 | 1 |
| lsp-server | 0 | 1 |
| machine-learning | 0 | 1 |
| memory-pool-design | 0 | 1 |
| message-broker | 0 | 1 |
| message-queue-selection | 0 | 1 |
| neural-networks | 0 | 1 |
| overfitting | 0 | 1 |
| package-management | 0 | 1 |
| pub-sub-system | 0 | 1 |
| regularization | 0 | 1 |
| system-design | 0 | 1 |
| task:automation | 1 | 0 |
| technology-selection | 0 | 1 |
| zero-copy-parsing | 0 | 1 |

## 7. Model Selection Recommendation

**Overall inter-model agreement: 72.7%**

- Token usage ratio (claude-sonnet-4-6/deepseek-v3.2): 1.19x
- Time ratio (claude-sonnet-4-6/deepseek-v3.2): 0.68x

Moderate agreement (73%). Consider using the stronger model (claude-sonnet-4-6) for dimensions with low agreement, and the lighter model for high-agreement dimensions.

---
_Report generated by `scripts/compare_models.py` at 2026-02-25T12:20:03.379168_