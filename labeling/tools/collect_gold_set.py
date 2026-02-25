"""
SFT Gold Set Generator — Concurrent Version

Generates diverse code SFT conversations using LLM API with asyncio concurrency.
Supports resuming from partial runs.

Usage:
  python3 labeling/collect_gold_set.py [--concurrency 30] [--resume]
"""

import json
import time
import asyncio
import hashlib
from pathlib import Path
from datetime import datetime

import httpx

OUTPUT_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "raw_samples.json"

# Import API settings from config
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import LITELLM_BASE, LITELLM_KEY, DEFAULT_MODEL, DEFAULT_CONCURRENCY

BASE_URL = LITELLM_BASE
API_KEY = LITELLM_KEY
MODEL = DEFAULT_MODEL
CONCURRENCY = DEFAULT_CONCURRENCY

# ──────────────────────────────────────────────
# System prompts
# ──────────────────────────────────────────────

SYSTEM_SINGLE = """You are an expert coding assistant. Provide a high-quality, detailed response to the user's coding question or request.

Rules:
- Include actual working code (not pseudocode or placeholders)
- Add brief explanations for key decisions
- If debugging, explain the root cause before giving the fix
- If reviewing, be specific about issues and suggest concrete fixes
- Code should be idiomatic and follow best practices
- Respond in the same language as the user's query (Chinese or English)
- Be concise but thorough — don't pad with unnecessary commentary"""

SYSTEM_MULTITURN_AGENTIC = """You are an expert at generating realistic SFT training data for AI coding assistants.

Generate a realistic multi-turn conversation in ShareGPT format where an AI coding assistant (like Claude Code, Cursor, or Copilot) helps a user with a coding task.

The conversation MUST include tool usage shown as separate turns with role "tool":
Example pattern:
  {"from": "gpt", "value": "Let me check the current project structure."}
  {"from": "tool", "value": "$ ls -la src/\\ntotal 24\\n-rw-r--r-- 1 user staff  1234 main.py\\n..."}
  {"from": "gpt", "value": "I see. Let me read the main file."}

Requirements:
- Include ACTUAL code (not placeholders)
- Show realistic file contents, error messages, command outputs
- Include file paths, package names, versions, config values
- Vary conversation length (4-12 turns total including tool turns)
- If debugging, show the iterative process: read → hypothesis → try fix → verify
- Code must be syntactically correct and idiomatic

Output ONLY valid JSON:
{"conversations": [{"from": "human"|"gpt"|"tool", "value": "..."}]}"""

SYSTEM_MULTITURN_PLAIN = """You are an expert at generating realistic SFT training data for AI coding assistants.

Generate a realistic multi-turn conversation where a user asks a coding question, gets an answer, then asks a follow-up that builds on the first answer.

Requirements:
- The follow-up should naturally extend the first question
- Include actual working code in responses
- Respond in the same language as the user

Output ONLY valid JSON:
{"conversations": [{"from": "human", "value": "..."}, {"from": "gpt", "value": "..."}, {"from": "human", "value": "..."}, {"from": "gpt", "value": "..."}]}"""

# ──────────────────────────────────────────────
# Scenarios (same as before)
# ──────────────────────────────────────────────

SCENARIOS = [
    # Learn beginner (8)
    {"query": "Python 列表推导式和生成器表达式的区别是什么？给个例子", "category": "learn-beginner"},
    {"query": "JavaScript 的 var、let、const 有什么区别？", "category": "learn-beginner"},
    {"query": "什么是 SQL 的 JOIN？INNER JOIN 和 LEFT JOIN 区别是什么？举个例子", "category": "learn-beginner"},
    {"query": "HTML 里 div 和 span 有什么区别？什么时候用哪个？", "category": "learn-beginner"},
    {"query": "Git 的 merge 和 rebase 有什么区别？", "category": "learn-beginner"},
    {"query": "什么是 HTTP 状态码？常用的有哪些？", "category": "learn-beginner"},
    {"query": "Python 的 *args 和 **kwargs 是什么意思？怎么用？", "category": "learn-beginner"},
    {"query": "CSS 的 Flexbox 布局怎么用？帮我讲讲主轴和交叉轴的概念", "category": "learn-beginner"},
    # Learn intermediate (8)
    {"query": "Rust 的 ownership 和 borrowing 是什么意思？为什么要这样设计？", "category": "learn-intermediate"},
    {"query": "解释一下 React 的 useEffect 的依赖数组，什么时候用空数组，什么时候不写？", "category": "learn-intermediate"},
    {"query": "Go 语言的 goroutine 和 channel 怎么用？和 Java 线程有什么区别？", "category": "learn-intermediate"},
    {"query": "请解释动态规划的背包问题，0/1 背包和完全背包有什么区别？用 Python 代码举例", "category": "learn-intermediate"},
    {"query": "TypeScript 的泛型 (Generics) 是什么？什么时候该用？给几个实际的使用场景", "category": "learn-intermediate"},
    {"query": "什么是数据库的事务隔离级别？Read Committed 和 Repeatable Read 有什么区别？", "category": "learn-intermediate"},
    {"query": "Docker 的 multi-stage build 是什么？有什么好处？给个例子", "category": "learn-intermediate"},
    {"query": "讲讲 Python 的 GIL（全局解释器锁），为什么多线程在 CPU 密集型任务上没用？", "category": "learn-intermediate"},
    # Learn advanced (5)
    {"query": "Explain the difference between optimistic and pessimistic locking in databases. When would you use each?", "category": "learn-advanced"},
    {"query": "什么是 CAP 定理？在实际分布式系统设计中怎么做取舍？", "category": "learn-advanced"},
    {"query": "解释 Rust 的 Pin 和 Unpin trait，为什么异步编程需要它们？", "category": "learn-advanced"},
    {"query": "什么是 CRDT (Conflict-free Replicated Data Type)？和 OT 算法比有什么优劣？", "category": "learn-advanced"},
    {"query": "Explain how the Linux kernel's CFS (Completely Fair Scheduler) works", "category": "learn-advanced"},
    # Build beginner (7)
    {"query": "帮我写一个 Python 脚本，读取 CSV 文件，按某一列排序后输出到新的 CSV", "category": "build-beginner"},
    {"query": "Write a simple HTML page with a form that validates email and password on submit using JavaScript", "category": "build-beginner"},
    {"query": "帮我写一个 Bash 脚本，遍历目录下所有 .log 文件，统计每个文件的行数", "category": "build-beginner"},
    {"query": "用 Python 写一个简单的计算器，支持加减乘除，处理除零错误", "category": "build-beginner"},
    {"query": "帮我用 Go 写一个 Hello World 的 HTTP 服务，监听 8080 端口，返回 JSON 响应", "category": "build-beginner"},
    {"query": "Write a Python function that checks if a string is a valid palindrome, ignoring spaces and punctuation", "category": "build-beginner"},
    {"query": "帮我写一个 SQL 建表语句，用户表包含 id、用户名、邮箱、创建时间，加上合适的索引", "category": "build-beginner"},
    # Build intermediate (12)
    {"query": "帮我用 Flask 写一个 REST API，支持对用户的 CRUD 操作，用 SQLite 存储", "category": "build-intermediate"},
    {"query": "Write a React component that implements infinite scroll with a loading spinner and error handling", "category": "build-intermediate"},
    {"query": "帮我写一个 Python 装饰器，实现函数级别的缓存，支持 TTL 过期和最大缓存条数", "category": "build-intermediate"},
    {"query": "Implement a binary search tree in TypeScript with insert, delete, search, and in-order traversal", "category": "build-intermediate"},
    {"query": "帮我写一个 Docker Compose 文件，包含 Nginx + Node.js app + PostgreSQL + Redis", "category": "build-intermediate"},
    {"query": "用 Go 写一个简单的 HTTP 反向代理，支持根据路径前缀路由到不同后端", "category": "build-intermediate"},
    {"query": "帮我用 Python + Click 写一个 CLI 工具，支持子命令，可以管理 TODO 列表（增删改查）", "category": "build-intermediate"},
    {"query": "Write a Next.js API route that handles file uploads, validates file type and size, stores to local disk", "category": "build-intermediate"},
    {"query": "帮我写一个 GitHub Actions workflow，push 时跑 pytest，生成覆盖率报告发到 PR comment", "category": "build-intermediate"},
    {"query": "Implement a rate limiter middleware in Express.js using the sliding window algorithm with Redis", "category": "build-intermediate"},
    {"query": "用 Rust 的 clap 库写一个 CLI 工具，解析 JSON 文件并格式化输出", "category": "build-intermediate"},
    {"query": "帮我用 Vue 3 Composition API 写一个带搜索过滤和分页的数据表格组件", "category": "build-intermediate"},
    # Build advanced (7)
    {"query": "Implement a connection pool in Go with configurable max connections, idle timeout, and health checks", "category": "build-advanced"},
    {"query": "帮我设计一个分布式限流器，要求支持滑动窗口算法，用 Redis + Lua 脚本实现", "category": "build-advanced"},
    {"query": "Write a custom Webpack plugin that generates a build manifest with chunk hashes and dependency graph", "category": "build-advanced"},
    {"query": "用 Python 实现一个简单的 LSP (Language Server Protocol) 服务端，支持代码补全和悬停提示", "category": "build-advanced"},
    {"query": "Implement a simple MVCC (Multi-Version Concurrency Control) storage engine in Rust", "category": "build-advanced"},
    {"query": "帮我写一个 Kubernetes Operator (用 Go + controller-runtime)，管理自定义资源 MyApp 的生命周期", "category": "build-advanced"},
    {"query": "Design and implement a pub/sub message broker in Node.js with topic-based routing and at-least-once delivery", "category": "build-advanced"},
    # Build expert (5)
    {"query": "Implement a lock-free concurrent skip list in C++ using std::atomic with proper memory ordering (acquire/release)", "category": "build-expert"},
    {"query": "用 Rust 实现一个 B+ tree，支持范围查询、分裂合并、持久化到磁盘", "category": "build-expert"},
    {"query": "Implement an epoch-based garbage collector for a lock-free data structure in Rust", "category": "build-expert"},
    {"query": "Write a JIT compiler for a simple expression language using LLVM C API in C", "category": "build-expert"},
    {"query": "用 CUDA 实现矩阵乘法，要求支持 tiling、shared memory 优化、处理非对齐维度", "category": "build-expert"},
    # Debug (11)
    {"query": "我的 React 组件无限重渲染了，代码如下：\n```jsx\nfunction Counter() {\n  const [count, setCount] = useState(0);\n  useEffect(() => {\n    setCount(count + 1);\n  });\n  return <div>{count}</div>;\n}\n```\n怎么修？", "category": "debug-beginner"},
    {"query": "Python pandas merge 两个 DataFrame 后行数比两个原始表都多，为什么？\n```python\ndf1 = pd.DataFrame({'key': ['a','a','b'], 'val1': [1,2,3]})\ndf2 = pd.DataFrame({'key': ['a','a','c'], 'val2': [4,5,6]})\nresult = df1.merge(df2, on='key')\n```", "category": "debug-beginner"},
    {"query": "Docker build 报错 COPY failed: file not found in build context，但文件明明在目录里。Dockerfile:\n```dockerfile\nFROM node:18\nWORKDIR /app\nCOPY ../shared/utils.js ./\n```", "category": "debug-beginner"},
    {"query": "这段 Rust 代码编译不过：\n```rust\nfn longest(x: &str, y: &str) -> &str {\n    if x.len() > y.len() { x } else { y }\n}\n```\n报错 `missing lifetime specifier`，怎么修？", "category": "debug-intermediate"},
    {"query": "我的 Spring Boot 应用连接 PostgreSQL 时报 HikariPool-1 Connection is not available request timed out after 30000ms，连接池配置是默认的，QPS 大概 500，怎么解决？", "category": "debug-advanced"},
    {"query": "Nginx 反向代理 WebSocket 连接总是在 60 秒后自动断开，配置如下：\n```nginx\nlocation /ws {\n    proxy_pass http://backend:3000;\n    proxy_http_version 1.1;\n    proxy_set_header Upgrade $http_upgrade;\n    proxy_set_header Connection \"upgrade\";\n}\n```", "category": "debug-intermediate"},
    {"query": "Go 程序偶现 panic: concurrent map writes，但我已经用了 sync.Mutex，代码：\n```go\ntype Cache struct {\n    mu    sync.Mutex\n    items map[string]string\n}\nfunc (c *Cache) Set(k, v string) {\n    c.mu.Lock()\n    c.items[k] = v\n    c.mu.Unlock()\n}\nfunc (c *Cache) GetAll() map[string]string {\n    c.mu.Lock()\n    defer c.mu.Unlock()\n    return c.items\n}\n```", "category": "debug-advanced"},
    {"query": "Kubernetes Pod 一直处于 CrashLoopBackOff 状态，kubectl logs 显示 Error: EACCES: permission denied, open '/app/data/config.json'", "category": "debug-intermediate"},
    {"query": "我的 Python async 代码 CPU 占用 100%：\n```python\nasync def poll_status():\n    while True:\n        status = await check_status()\n        if status == 'done':\n            break\n```", "category": "debug-intermediate"},
    {"query": "MySQL 查询很慢，EXPLAIN 显示 type=ALL，rows=500000：\n```sql\nSELECT * FROM orders WHERE customer_id = 123 AND status = 'pending' ORDER BY created_at DESC LIMIT 10;\n```\n表上有 customer_id 的单列索引，为什么没用上？", "category": "debug-advanced"},
    {"query": "TypeScript 报错 Type 'string | undefined' is not assignable to type 'string'：\n```typescript\nfunction process(map: Map<string, string>) {\n    const key = 'test';\n    if (map.has(key)) {\n        const value: string = map.get(key);\n    }\n}\n```", "category": "debug-intermediate"},
    # Review (5)
    {"query": "帮我 review 一下这段 Go 的并发缓存实现：\n```go\ntype Cache struct {\n    mu    sync.Mutex\n    items map[string]interface{}\n    ttl   time.Duration\n}\nfunc (c *Cache) Set(key string, val interface{}) {\n    c.mu.Lock()\n    defer c.mu.Unlock()\n    c.items[key] = val\n    go func() {\n        time.Sleep(c.ttl)\n        c.mu.Lock()\n        delete(c.items, key)\n        c.mu.Unlock()\n    }()\n}\n```", "category": "review-intermediate"},
    {"query": "Review this Python function:\n```python\ndef process_users(data):\n    result = []\n    for item in data:\n        try:\n            user = json.loads(item)\n            result.append({'name': user['name'], 'age': int(user['age'])})\n        except:\n            pass\n    return result\n```", "category": "review-beginner"},
    {"query": "请帮我审查这个 React 登录组件的安全性：\n```tsx\nfunction Login() {\n  const [password, setPassword] = useState('');\n  const handleSubmit = async () => {\n    const res = await fetch('/api/login', { method: 'POST', body: JSON.stringify({ password }) });\n    const { token } = await res.json();\n    localStorage.setItem('token', token);\n  };\n  return <input type='text' value={password} onChange={e => setPassword(e.target.value)} />;\n}\n```", "category": "review-intermediate"},
    {"query": "Review this Dockerfile:\n```dockerfile\nFROM node:latest\nWORKDIR /app\nCOPY . .\nRUN npm install\nENV NODE_ENV=production\nEXPOSE 3000\nCMD [\"node\", \"server.js\"]\n```", "category": "review-intermediate"},
    {"query": "帮我 review 这个 SQL 查询的性能，表有 1000 万行：\n```sql\nSELECT u.name, COUNT(o.id) as order_count, SUM(o.amount) as total_amount\nFROM users u LEFT JOIN orders o ON u.id = o.user_id\nWHERE o.created_at >= '2024-01-01'\nGROUP BY u.name HAVING total_amount > 1000\nORDER BY total_amount DESC;\n```", "category": "review-advanced"},
    # Decide (8)
    {"query": "PostgreSQL vs MongoDB，做一个电商系统应该选哪个？", "category": "decide-intermediate"},
    {"query": "新项目选 Next.js 还是 Nuxt.js？团队 React 和 Vue 都会", "category": "decide-intermediate"},
    {"query": "微服务还是单体？我们是 5 人团队做一个 SaaS 产品", "category": "decide-intermediate"},
    {"query": "Python 项目的包管理用 pip + venv, Poetry, 还是 uv？", "category": "decide-beginner"},
    {"query": "React 和 Vue 我该学哪个？我是前端新手", "category": "decide-beginner"},
    {"query": "GraphQL vs REST，多端内容管理系统选哪个？", "category": "decide-intermediate"},
    {"query": "Kafka vs RabbitMQ vs Redis Streams，日均 100 万条消息的异步任务队列选哪个？", "category": "decide-advanced"},
    {"query": "SQLite vs DuckDB 做嵌入式分析？Python CLI 工具里做 OLAP 查询", "category": "decide-intermediate"},
    # Agentic multi-turn (20)
    {"query": "帮我从零搭建一个 Next.js 14 项目，要 TypeScript + Tailwind + Prisma + PostgreSQL", "category": "agentic-build-intermediate", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "bash-execution", "dependency-installation", "multi-file-coordination", "planning"]},
    {"query": "我的 FastAPI 应用在生产环境偶现 500 错误，日志显示 sqlalchemy.exc.TimeoutError", "category": "agentic-debug-advanced", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "bash-execution", "iterative-refinement", "error-recovery", "multi-step-reasoning"]},
    {"query": "帮我把这个 2000 行的 Express.js 单文件 API 重构成模块化结构", "category": "agentic-refactor-intermediate", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "multi-file-coordination", "planning", "test-running"]},
    {"query": "Fix the failing CI — tests pass locally but fail in GitHub Actions", "category": "agentic-debug-intermediate", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "bash-execution", "git-operations", "iterative-refinement"]},
    {"query": "帮我给这个 Go REST API 写完整的单元测试和集成测试", "category": "agentic-test-intermediate", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "test-running", "multi-file-coordination", "iterative-refinement"]},
    {"query": "Deploy our Django app to AWS ECS with Terraform", "category": "agentic-deploy-advanced", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "bash-execution", "multi-file-coordination", "planning"]},
    {"query": "帮我排查 Node.js WebSocket 服务的内存泄漏问题", "category": "agentic-debug-advanced", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "bash-execution", "code-execution", "iterative-refinement", "error-recovery"]},
    {"query": "帮我搭建一个 monorepo：React 前端 + Node.js 后端 + 共享 types 包，用 Turborepo", "category": "agentic-build-intermediate", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "bash-execution", "dependency-installation", "multi-file-coordination", "planning"]},
    {"query": "帮我做数据库迁移，从 MySQL 5.7 到 PostgreSQL 16，需要转换 schema 和迁移数据", "category": "agentic-migration-advanced", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "database-query", "bash-execution", "planning", "multi-step-reasoning"]},
    {"query": "帮我给 React 项目加 Storybook，配好常用 addon，为 Button 和 Modal 写 stories", "category": "agentic-build-intermediate", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "bash-execution", "dependency-installation", "multi-file-coordination"]},
    {"query": "Set up Prometheus + Grafana for our K8s cluster with alerts", "category": "agentic-deploy-advanced", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "bash-execution", "multi-file-coordination", "planning"]},
    {"query": "帮我实现 OAuth2 + PKCE 登录：React 前端 + Express 后端 + Google", "category": "agentic-build-advanced", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "multi-file-coordination", "api-calling", "planning", "iterative-refinement"]},
    {"query": "优化这个 Django ORM 查询，页面加载 12 秒，有 N+1 问题", "category": "agentic-optimize-advanced", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "database-query", "iterative-refinement", "multi-step-reasoning"]},
    {"query": "帮我把 Python 同步代码重构为异步，用 asyncio + aiohttp 替换 requests", "category": "agentic-refactor-intermediate", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "multi-file-coordination", "test-running", "iterative-refinement"]},
    {"query": "帮我配置 ESLint + Prettier + Husky + lint-staged，TypeScript + React", "category": "agentic-config-intermediate", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "bash-execution", "dependency-installation", "multi-file-coordination"]},
    {"query": "Debug this race condition — Go service returns stale cache data intermittently", "category": "agentic-debug-expert", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "code-execution", "iterative-refinement", "error-recovery", "multi-step-reasoning"]},
    {"query": "帮我写 Terraform module：AWS Lambda + API Gateway + DynamoDB serverless 骨架", "category": "agentic-build-advanced", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "multi-file-coordination", "bash-execution", "planning"]},
    {"query": "帮我容器化多服务应用：React + Flask API + Celery + Redis + PostgreSQL", "category": "agentic-build-advanced", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "multi-file-coordination", "bash-execution", "build-execution", "iterative-refinement", "planning"]},
    {"query": "Write a GitHub Action: build Rust project, clippy, tests, publish to crates.io on tag", "category": "agentic-deploy-intermediate", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "multi-file-coordination", "git-operations", "planning"]},
    {"query": "帮我给 Python 项目加完整 CI：ruff + mypy + pytest + coverage，用 GitHub Actions", "category": "agentic-config-intermediate", "multi_turn": True, "tool_calls": True, "agentic_signals": ["file-operations", "bash-execution", "multi-file-coordination", "test-running", "planning"]},
    # Multi-turn plain (5)
    {"query": "帮我用 Python 实现一个 LRU Cache", "followup": "能加上线程安全吗？用 threading.Lock", "category": "multiturn-build-intermediate", "multi_turn": True, "tool_calls": False},
    {"query": "怎么用 React Context 做全局状态管理？", "followup": "如果状态很复杂，Context 会不会导致不必要的重渲染？怎么优化？", "category": "multiturn-learn-intermediate", "multi_turn": True, "tool_calls": False},
    {"query": "帮我写一个 Python 日志装饰器", "followup": "能支持异步函数吗？async def 的那种", "category": "multiturn-build-intermediate", "multi_turn": True, "tool_calls": False},
    {"query": "Explain how PostgreSQL's MVCC works", "followup": "When does vacuum reclaim dead tuples? Can it cause performance issues?", "category": "multiturn-learn-advanced", "multi_turn": True, "tool_calls": False},
    {"query": "帮我写一个 express middleware 记录请求日志", "followup": "怎么排除 /health 路径？还有能加上请求耗时吗？", "category": "multiturn-build-beginner", "multi_turn": True, "tool_calls": False},
    # Domain-specific (12)
    {"query": "用 PyTorch 实现一个简单的 CNN 图像分类模型，数据集用 CIFAR-10", "category": "build-advanced-ml"},
    {"query": "我的 XGBoost 模型过拟合了，训练集 AUC 0.99 但验证集只有 0.72，怎么办？", "category": "debug-intermediate-ml"},
    {"query": "帮我用 pandas 做数据清洗：处理缺失值、异常值检测、特征编码", "category": "build-intermediate-ds"},
    {"query": "帮我用 Python 写一个简单的端口扫描器，支持 TCP connect scan", "category": "build-intermediate-security"},
    {"query": "Review this Express.js app for common security vulnerabilities", "category": "review-advanced-security"},
    {"query": "用 Swift 写一个简单的 iOS TODO 应用，SwiftUI + Core Data", "category": "build-intermediate-mobile"},
    {"query": "React Native 和 Flutter 对比，社交媒体 app 选哪个？", "category": "decide-intermediate-mobile"},
    {"query": "用 Python + Pygame 写一个简单的贪吃蛇游戏", "category": "build-beginner-game"},
    {"query": "Implement A* pathfinding in C++ for a 2D grid-based game", "category": "build-intermediate-game"},
    {"query": "Write a simple memory allocator in C (malloc, free, handle fragmentation)", "category": "build-expert-systems"},
    {"query": "用 Rust 实现一个简单的 TCP echo server，使用 tokio", "category": "build-intermediate-systems"},
    {"query": "帮我用 Python 实现一个简单的股票回测框架", "category": "build-intermediate-fintech"},
    # More domain
    {"query": "帮我写 Ansible playbook，自动化配置 Nginx + Let's Encrypt SSL", "category": "build-intermediate-devops"},
    {"query": "Write an ERC-20 token contract in Solidity with mint, burn, transfer", "category": "build-intermediate-blockchain"},
    # Constraint-heavy (5)
    {"query": "帮我写一个高性能 JSON parser in C, 要求零拷贝、无动态内存分配", "category": "build-expert-constraint"},
    {"query": "Implement an idempotent payment processing endpoint in Node.js + PostgreSQL", "category": "build-advanced-constraint"},
    {"query": "帮我写一个线程安全的对象池 in Java，要求 lock-free", "category": "build-expert-constraint"},
    {"query": "Write a GDPR-compliant user data export API in Python Django", "category": "build-advanced-constraint"},
    {"query": "帮我实现一个可移植的配置文件解析器（C语言），Linux/macOS/Windows 都能编译", "category": "build-intermediate-constraint"},
    # Code translation (2)
    {"query": "帮我把这段 Python 代码转成 Go：\n```python\nimport asyncio\nasync def fetch_all(urls):\n    async with aiohttp.ClientSession() as session:\n        tasks = [session.get(url) for url in urls]\n        responses = await asyncio.gather(*tasks)\n        return [await r.json() for r in responses]\n```", "category": "translate-intermediate"},
    {"query": "Convert this JS class to Rust struct:\n```javascript\nclass EventEmitter {\n  constructor() { this.listeners = {}; }\n  on(event, fn) { (this.listeners[event] ||= []).push(fn); }\n  emit(event, ...args) { (this.listeners[event] || []).forEach(fn => fn(...args)); }\n}\n```", "category": "translate-advanced"},
]


# ──────────────────────────────────────────────
# Async generation
# ──────────────────────────────────────────────

async def async_llm_call(http_client, messages, model, temperature=0.7, max_tokens=4096, max_retries=3):
    """Make async LLM call via LiteLLM proxy with retry + backoff."""
    url = f"{BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    for attempt in range(max_retries + 1):
        try:
            resp = await http_client.post(url, json=payload, headers=headers, timeout=180)
            if resp.status_code in (429, 502, 503):
                wait = min(2 ** attempt * 2 + 1, 30)
                if attempt < max_retries:
                    await asyncio.sleep(wait)
                    continue
                resp.raise_for_status()
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            if attempt < max_retries:
                wait = min(2 ** attempt * 2 + 1, 30)
                await asyncio.sleep(wait)
                continue
            raise


def parse_json_from_llm(content):
    """Extract JSON from LLM output that might be wrapped in markdown or truncated."""
    # Strip markdown fences
    text = content.strip()
    if text.startswith("```"):
        parts = text.split("```")
        for part in parts:
            cleaned = part.strip()
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
            if cleaned.startswith("{"):
                text = cleaned
                break

    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to find the JSON object in the text
    start = text.find("{")
    if start >= 0:
        # Find matching closing brace
        depth = 0
        in_string = False
        escape_next = False
        for i in range(start, len(text)):
            c = text[i]
            if escape_next:
                escape_next = False
                continue
            if c == '\\':
                escape_next = True
                continue
            if c == '"' and not escape_next:
                in_string = not in_string
            if not in_string:
                if c == '{':
                    depth += 1
                elif c == '}':
                    depth -= 1
                    if depth == 0:
                        try:
                            return json.loads(text[start:i+1])
                        except json.JSONDecodeError:
                            break

    # If all else fails, try to fix common truncation issues
    # Add missing closing brackets/braces
    if text.startswith("{") or text.startswith("["):
        fixed = text
        open_braces = fixed.count("{") - fixed.count("}")
        open_brackets = fixed.count("[") - fixed.count("]")
        # Try to close any open strings
        in_str = False
        for c in fixed:
            if c == '"' and not escape_next:
                in_str = not in_str
            escape_next = (c == '\\')
        if in_str:
            fixed += '"'
        fixed += "]" * open_brackets + "}" * open_braces
        try:
            return json.loads(fixed)
        except json.JSONDecodeError:
            pass

    raise json.JSONDecodeError("Could not parse JSON from LLM output", text, 0)


async def generate_single(http_client, scenario, index, sem):
    """Generate a single-turn conversation."""
    async with sem:
        query = scenario["query"]
        messages = [
            {"role": "system", "content": SYSTEM_SINGLE},
            {"role": "user", "content": query}
        ]
        try:
            answer = await async_llm_call(http_client, messages, MODEL)
            if len(answer) < 50:
                return None
            conversations = [
                {"from": "human", "value": query},
                {"from": "gpt", "value": answer}
            ]
            full_text = query + " " + answer
            return {
                "id": f"gen-{index:04d}",
                "conversations": conversations,
                "metadata": {
                    "source": "generated", "generator_model": MODEL,
                    "category": scenario["category"],
                    "est_tokens": len(full_text) // 4,
                    "num_turns": 2, "is_multi_turn": False,
                    "has_tool_calls": False,
                    "has_code": "```" in full_text
                }
            }
        except Exception as e:
            return {"error": str(e), "index": index, "category": scenario["category"]}


async def generate_agentic(http_client, scenario, index, sem):
    """Generate a multi-turn agentic conversation."""
    async with sem:
        signals = scenario.get("agentic_signals", [])
        user_prompt = f"""Generate a conversation for this scenario:

User request: {scenario['query']}
Expected agent behaviors: {', '.join(signals)}

Make the conversation realistic with actual tool usage (file reads, shell commands, code writing).
Show the full problem-solving process."""

        messages = [
            {"role": "system", "content": SYSTEM_MULTITURN_AGENTIC},
            {"role": "user", "content": user_prompt}
        ]
        try:
            content = await async_llm_call(http_client, messages, MODEL, temperature=0.8, max_tokens=8192)
            data = parse_json_from_llm(content)
            conversations = data.get("conversations", [])
            if len(conversations) < 3:
                return None
            full_text = " ".join(c.get("value", "") for c in conversations)
            return {
                "id": f"gen-{index:04d}",
                "conversations": conversations,
                "metadata": {
                    "source": "generated", "generator_model": MODEL,
                    "category": scenario["category"],
                    "expected_agentic": signals,
                    "est_tokens": len(full_text) // 4,
                    "num_turns": len(conversations),
                    "is_multi_turn": True,
                    "has_tool_calls": any(c.get("from") == "tool" for c in conversations),
                    "has_code": "```" in full_text
                }
            }
        except Exception as e:
            return {"error": str(e), "index": index, "category": scenario["category"]}


async def generate_multiturn_plain(http_client, scenario, index, sem):
    """Generate a multi-turn conversation without tools."""
    async with sem:
        followup = scenario.get("followup", "Can you extend this further?")
        user_prompt = f"""Generate a 2-round conversation:
Round 1 user: {scenario['query']}
Round 2 user (follow-up): {followup}
Provide detailed, code-rich responses for both rounds."""

        messages = [
            {"role": "system", "content": SYSTEM_MULTITURN_PLAIN},
            {"role": "user", "content": user_prompt}
        ]
        try:
            content = await async_llm_call(http_client, messages, MODEL, max_tokens=6144)
            data = parse_json_from_llm(content)
            conversations = data.get("conversations", [])
            if len(conversations) < 4:
                return None
            full_text = " ".join(c.get("value", "") for c in conversations)
            return {
                "id": f"gen-{index:04d}",
                "conversations": conversations,
                "metadata": {
                    "source": "generated", "generator_model": MODEL,
                    "category": scenario["category"],
                    "est_tokens": len(full_text) // 4,
                    "num_turns": len(conversations),
                    "is_multi_turn": True,
                    "has_tool_calls": False,
                    "has_code": "```" in full_text
                }
            }
        except Exception as e:
            return {"error": str(e), "index": index, "category": scenario["category"]}


async def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--concurrency", type=int, default=15)
    parser.add_argument("--resume", action="store_true", help="Resume from existing output, only generate missing items")
    args = parser.parse_args()

    concurrency = args.concurrency
    total = len(SCENARIOS)

    # Resume support: load existing results and skip already-generated indices
    existing_results = []
    existing_ids = set()
    if args.resume and OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            existing_results = json.load(f)
        existing_ids = {r["id"] for r in existing_results}
        print(f"Resuming: found {len(existing_results)} existing samples")

    # Determine which scenarios still need generation
    scenarios_to_gen = []
    for i, scenario in enumerate(SCENARIOS):
        sample_id = f"gen-{i:04d}"
        if sample_id not in existing_ids:
            scenarios_to_gen.append((i, scenario))

    remaining = len(scenarios_to_gen)
    if remaining == 0:
        print(f"All {total} samples already generated. Nothing to do.")
        return

    print(f"Generating {remaining} SFT samples using {MODEL} with concurrency={concurrency}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    sem = asyncio.Semaphore(concurrency)

    async with httpx.AsyncClient(proxy=None, timeout=180) as http_client:
        tasks = []
        for i, scenario in scenarios_to_gen:
            is_multi = scenario.get("multi_turn", False)
            has_tools = scenario.get("tool_calls", False)

            if is_multi and has_tools:
                tasks.append(generate_agentic(http_client, scenario, i, sem))
            elif is_multi:
                tasks.append(generate_multiturn_plain(http_client, scenario, i, sem))
            else:
                tasks.append(generate_single(http_client, scenario, i, sem))

        # Gather all with progress tracking
        start = time.time()
        new_results = []
        done_count = 0
        for coro in asyncio.as_completed(tasks):
            result = await coro
            done_count += 1
            if result and "error" not in result:
                new_results.append(result)
                cat = result["metadata"]["category"]
                turns = result["metadata"]["num_turns"]
                tokens = result["metadata"]["est_tokens"]
                tool = " [tool]" if result["metadata"].get("has_tool_calls") else ""
                print(f"[{done_count:3d}/{remaining}] ok {cat:40s} | {turns:2d} turns | ~{tokens:4d} tok{tool}")
            elif result and "error" in result:
                print(f"[{done_count:3d}/{remaining}] FAIL {result.get('category','?'):40s} | {result['error'][:80]}")
            else:
                print(f"[{done_count:3d}/{remaining}] FAIL (None result)")

    elapsed = time.time() - start

    # Merge with existing results
    all_results = existing_results + new_results
    # Sort by id for consistency
    all_results.sort(key=lambda x: x.get("id", ""))

    # Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    # Summary
    total_generated = len(all_results)
    multi_turn = sum(1 for s in all_results if s["metadata"]["is_multi_turn"])
    has_tool = sum(1 for s in all_results if s["metadata"].get("has_tool_calls"))
    avg_tokens = sum(s["metadata"]["est_tokens"] for s in all_results) / max(total_generated, 1)

    print(f"\n{'='*60}")
    print(f"GENERATION COMPLETE in {elapsed:.1f}s")
    print(f"{'='*60}")
    print(f"New samples this run: {len(new_results)} / {remaining}")
    print(f"Total samples: {total_generated} / {total}")
    print(f"Single-turn: {total_generated - multi_turn}")
    print(f"Multi-turn:  {multi_turn}")
    print(f"Has tool calls: {has_tool}")
    print(f"Avg tokens: {avg_tokens:.0f}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
