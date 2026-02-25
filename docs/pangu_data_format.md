# Pangu 训练数据 JSONL 格式规范

本文档详细描述了 Pangu SFT（监督微调）训练数据的 JSONL 格式，涵盖所有可能出现的变体。

## 目录

- [数据结构总览](#数据结构总览)
- [特殊标记说明](#特殊标记说明)
- [单轮对话格式](#单轮对话格式)
- [多轮对话格式](#多轮对话格式)
- [工具调用格式](#工具调用格式)
- [思考过程模式](#思考过程模式)
- [格式规则总结](#格式规则总结)
- [数据质检规则](#数据质检规则)

---

## 数据结构总览

每行 JSONL 数据包含一个完整的对话记录：

```json
{
  "meta_prompt": ["系统指令内容"],
  "tools": "[{\"name\": \"tool_name\", \"description\": \"工具描述\"}]",
  "data": [
    {"role": "user", "content": "用户内容"},
    {"role": "assistant", "content": "助手内容"},
    {"role": "tool", "content": "工具返回内容"}
  ]
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `meta_prompt` | `list[str]` | 否 | 系统指令或提示词列表 |
| `tools` | `str` | 否 | 工具列表，JSON 字符串格式 |
| `data` | `list[dict]` | 是 | 对话数据，每条为一个字典 |

---

## 特殊标记说明

### 思考过程标记

| 标记 | 名称 | 用途 |
|------|------|------|
| `[unused16]` | 思考开始标记 | 标识思考过程开始 |
| `[unused17]` | 思考结束标记 | 标识思考过程结束 |
| `/no_think` | 快思考标记 | 表示跳过思考，用于历史上下文 |

**注意：**
- 慢思考：`[unused16]{思考内容}[unused17]` （思考内容开头结尾不应有空格、换行等）
- 快思考：`[unused16][unused17]`（中间无内容）
- ` /no_think`：附加在用户/工具内容末尾，注意前面存在一个空格

### 伪多轮标记

| 标记 | 名称 | 用途 |
|------|------|------|
| `[unused10][unused9]` | 会话分隔符 | 在用户内容的伪多轮中分隔不同轮次 |

**示例：** `用户：问题 /no_think[unused10][unused9]助手：回答[unused10][unused9]用户：问题2`

### 工具调用标记（嵌入方式）

| 标记 | 名称 | 用途 |
|------|------|------|
| `[unused11]...[unused12]` | 工具调用及结果 | 嵌在 assistant 内容中 |
| `[unused13]...[unused14]` | 第二个工具调用 | 用于多个工具调用 |
| `[unused15]...[unused16]` | 第三个工具调用 | 用于三个及以上工具调用 |

---

## 单轮对话格式

### 1. 快思考单轮（Fast Thinking）

用户不需要思考过程，快速回答。

```json
{
  "meta_prompt": ["你是一个有用的助手"],
  "data": [
    {"role": "user", "content": "北京的天气怎么样？ /no_think"},
    {"role": "assistant", "content": "[unused16][unused17]抱歉，我无法获取实时天气信息。建议您查看天气预报应用或网站。"}
  ]
}
```

**特点：**
- 用户内容末尾有 `/no_think`
- 助手使用 `[unused16][unused17]` 空标记

### 2. 慢思考单轮（Slow Thinking）

需要展示思考过程。

```json
{
  "meta_prompt": ["你是一个有用的助手"],
  "data": [
    {"role": "user", "content": "解释为什么天空是蓝色的"},
    {"role": "assistant", "content": "[unused16]天空呈蓝色是因为一个称为瑞利散射的现象。当太阳光穿过大气层时，短波长的蓝光被散射得更多，所以我们看到的天空是蓝色的。这是一个物理现象，解释需要考虑光学的原理。[unused17]天空之所以呈现蓝色，是因为瑞利散射现象。太阳光包含七种颜色的光，其中蓝光的波长最短。当阳光穿过大气层时，蓝光被空气分子散射得最多，散射的蓝光向各个方向传播，因此从地面看去，天空就呈现出蓝色。"}
  ]
}
```

**特点：**
- 用户内容末尾**没有** `/no_think`
- `[unused16]` 和 `[unused17]` 之间包含完整的思考过程

### 3. 真单无标记对话

最简形式，不使用任何特殊标记。

```json
{
  "data": [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！有什么可以帮助你的？"}
  ]
}
```

---

## 多轮对话格式

多轮对话分为 **伪多轮** 和 **真多轮** 两种形式。

### 伪多轮（Pseudo Multi-turn）

所有对话都压缩在第一个 data 元素中，通过 `[unused10][unused9]` 分隔不同角色。

#### 伪多轮快思考

```json
{
  "meta_prompt": ["你是一个有用的助手"],
  "data": [
    {
      "role": "user",
      "content": "什么是Python？ /no_think[unused10][unused9]助手：[unused16][unused17]Python是一种高级编程语言。[unused10][unused9]用户：Python有什么应用场景？ /no_think"
    },
    {"role": "assistant", "content": "[unused16][unused17]Python广泛应用于数据分析、人工智能、Web开发等领域。"}
  ]
}
```

#### 伪多轮慢思考

```json
{
  "meta_prompt": ["你是一个有用的助手"],
  "data": [
    {
      "role": "user",
      "content": "什么是Python？ /no_think[unused10][unused9]助手：[unused16][unused17]Python是一种高级编程语言。[unused10][unused9]用户：Python有什么应用场景？"
    },
    {"role": "assistant", "content": "[unused16]让我思考Python的应用场景。Python以其简洁的语法和强大的生态系统著称。首先，它在数据科学领域非常流行...[unused17]Python广泛应用于数据分析、人工智能、Web开发等领域。"}
  ]
}
```

**注意：** 伪多轮慢思考中，最后一个 `assistant` 条目包含完整的思考过程（`[unused16]{思考}[unused17]`）。

### 真多轮（True Multi-turn）

每个对话轮次都是一个独立的 data 元素。

#### 真多轮快思考

```json
{
  "meta_prompt": ["你是一个有用的助手"],
  "data": [
    {"role": "user", "content": "什么是Python？ /no_think"},
    {"role": "assistant", "content": "[unused16][unused17]Python是一种高级编程语言。"},
    {"role": "user", "content": "Python有什么应用场景？ /no_think"},
    {"role": "assistant", "content": "[unused16][unused17]Python广泛应用于数据分析、人工智能、Web开发等领域。"},
    {"role": "user", "content": "谢谢"},
    {"role": "assistant", "content": "[unused16][unused17]不客气！"}
  ]
}
```

#### 真多轮慢思考（保留思考过程）

```json
{
  "meta_prompt": ["你是一个有用的助手"],
  "data": [
    {"role": "user", "content": "什么是Python？"},
    {"role": "assistant", "content": "[unused16]我需要解释Python是什么。Python是一种高级编程语言，由Guido van Rossum创建。它的设计哲学强调代码的可读性。[unused17]Python是一种高级编程语言。"},
    {"role": "user", "content": "Python有什么应用场景？"},
    {"role": "assistant", "content": "[unused16]Python的应用场景很多。首先在数据科学领域，它有numpy、pandas等库。在AI领域，有TensorFlow、PyTorch。在Web开发方面，有Django、Flask。[unused17]Python广泛应用于数据分析、人工智能、Web开发等领域。"}
  ]
}
```

**注意：** 真多轮慢思考中，每个 `assistant` 的回答都可以包含独立的思考过程。

---

## 工具调用格式

### 工具嵌入调用（Inline Tool Calls）

工具调用直接嵌入在 assistant 的内容中，使用 `[unused11]...[unused12]` 标记。

#### 单个工具调用

```json
{
  "meta_prompt": ["你可以使用搜索工具"],
  "tools": "[{\"name\": \"search\", \"description\": \"搜索信息\"}]",
  "data": [
    {"role": "user", "content": "搜索Python的创建者"},
    {"role": "assistant", "content": "[unused16][unused17][unused11]{\"name\":\"search\",\"query\":\"Python creator\"}[unused12]Python由Guido van Rossum在1989年创建。"}
  ]
}
```

#### 多个工具调用

```json
{
  "meta_prompt": ["你可以使用搜索工具"],
  "tools": "[{\"name\": \"search\", \"description\": \"搜索信息\"}]",
  "data": [
    {"role": "user", "content": "搜索Python和它的应用场景"},
    {"role": "assistant", "content": "[unused16][unused17][unused11]{\"name\":\"search\",\"query\":\"Python\"}[unused12]Python是一种编程语言。[unused13]{\"name\":\"search\",\"query\":\"Python applications\"}[unused14]Python广泛应用于数据分析、AI等领域。"}
  ]
}
```

#### 三个及以上工具调用

```json
{
  "meta_prompt": ["你可以使用搜索工具"],
  "tools": "[{\"name\": \"search\", \"description\": \"搜索信息\"}]",
  "data": [
    {"role": "user", "content": "搜索Python、应用和库"},
    {"role": "assistant", "content": "[unused16][unused17][unused11]{\"name\":\"search\",\"query\":\"Python\"}[unused12]Python是一种编程语言。[unused13]{\"name\":\"search\",\"query\":\"Python apps\"}[unused14]广泛应用于数据科学。[unused15]{\"name\":\"search\",\"query\":\"Python libraries\"}[unused16]Python有丰富的库如numpy、pandas等。"}
  ]
}
```

### 工具调用+最终回答

```json
{
  "meta_prompt": ["你可以使用搜索工具"],
  "tools": "[{\"name\": \"search\", \"description\": \"搜索信息\"}]",
  "data": [
    {"role": "user", "content": "搜索Python的创建者"},
    {"role": "assistant", "content": "[unused16]我需要搜索Python的创建者信息。[unused17][unused11]{\"name\":\"search\",\"query\":\"Python creator\"}[unused12]Python由Guido van Rossum在1989年创建。[unused16][unused17]Python是一种高级编程语言，以其简洁和强大的生态系统而闻名。"}
  ]
}
```

### 独立工具节点（Tool Nodes）

工具调用和工具结果作为独立的 data 元素。

```json
{
  "meta_prompt": ["你可以使用搜索工具"],
  "tools": "[{\"name\": \"search\", \"description\": \"搜索信息\"}]",
  "data": [
    {"role": "user", "content": "搜索Python的创建者 /no_think"},
    {"role": "assistant", "content": "[unused16][unused17]我需要搜索Python的创建者信息。[unused11]{\"name\":\"search\",\"query\":\"Python creator\"}"},
    {"role": "tool", "content": "Python由Guido van Rossum在1989年创建，最初是一种脚本语言。"},
    {"role": "assistant", "content": "[unused16][unused17]Python由Guido van Rossum在1989年创建。"}
  ]
}
```

**注意：** 独立工具节点不适用于转换到 ShareGPT 格式（会产生连续的 observation）。

---

## 思考过程模式

### 快思考（Fast Thinking）

- 特点：不展示思考过程，直接给出答案
- 标记：`/no_think` + `[unused16][unused17]`（空）
- 用途：简单问题、历史对话、不需要展示推理的场景

### 慢思考（Slow Thinking）

- 特点：展示完整的思考过程
- 标记：`[unused16]{思考过程}[unused17]`
- 用途：复杂问题、需要展示推理能力的场景

### 混合思考模式

```json
{
  "data": [
    {"role": "user", "content": "什么是Python？"},
    {"role": "assistant", "content": "[unused16]Python是一种编程语言。[unused17]Python是一种高级编程语言。"},
    {"role": "user", "content": "搜索Python应用 /no_think"},
    {"role": "assistant", "content": "[unused16][unused17][unused11]{\"name\":\"search\",\"query\":\"Python apps\"}[unused12]Python广泛应用于数据科学。"}
  ]
}
```

同一对话中可以混合使用快思考和慢思考。

---

## 格式规则总结

### 1. 数据完整性规则

| 规则 | 说明 |
|------|------|
| 第一轮 | 第一个角色必须是 `user` |
| 最后一轮 | 最后一个角色必须是 `assistant` |
| data 数组 | 至少包含 2 个元素（user + assistant） |

### 2. 角色顺序规则（真多轮）

| 当前角色 | 下一个角色允许 |
|---------|---------------|
| `user` | `assistant` |
| `assistant` | `user` 或 `tool` |
| `tool` | `user` 或 `assistant` 或 `tool`（但连续tool会有问题） |

### 3. 特殊标记使用规则

| 场景 | `/no_think` | `[unused16][unused17]` 内容 |
|------|-------------|------------------------|
| 用户快思考 | 必须添加 | 不适用 |
| 用户慢思考 | 不添加 | 不适用 |
| 助手快思考 | 不适用 | 空 |
| 助手慢思考 | 不适用 | 包含思考过程 |
| 工具节点（伪多轮内） | 必须添加（除最后一轮） | 不适用 |
| 嵌入工具调用 | 不适用 | 通常为空 |

### 4. 伪多轮与真多轮的 `/no_think` 规则

| 类型 | 用户末尾 | 工具末尾 | 说明 |
|------|----------|---------|------|
| 伪多轮快思考 | 添加 | 添加 | 除最后一个用户外全部添加 |
| 伪多轮慢思考 | 添加 | 添加 | 除最后一个用户外全部添加 |
| 真多轮快思考 | 添加 | 不添加 | 所有用户都添加 |
| 真多轮慢思考 | 不添加 | 不添加 | 都不添加 |

---

## 数据质检规则

### 必检项

1. **结构验证**
   - JSON 格式正确
   - 必含 `data` 字段
   - `data` 至少包含 2 个元素

2. **角色验证**
   - 首条必须是 `user`
   - 末条必须是 `assistant`
   - 无连续 `assistant`（真多轮）

3. **特殊标记平衡**
   - `[unused16]` 与 `[unused17]` 成对出现
   - `[unused10]` 与 `[unused9]` 成对出现

4. **思考过程一致性**
   - 慢思考必须在 assistant 中
   - 用户快思考末尾必须有 `/no_think`
   - 工具快思考（伪多轮）末尾必须有 `/no_think`

### 可选检项

1. **内容质量**
   - content 不为空或仅空格
   - 超长内容标记

2. **工具调用格式**
   - 工具 JSON 合法性
   - 工具名称符合规范

3. **特殊字符**
   - Unicode 处理正确
   - 转义字符正确

---

## 完整示例

### 复杂多轮对话（含工具调用和思考过程）

```json
{
  "meta_prompt": ["你是一个智能助手，可以使用搜索工具"],
  "tools": "[{\"name\": \"search\", \"description\": \"搜索互联网信息\"}, {\"name\": \"calculator\", \"description\": \"计算器\"}]",
  "data": [
    {
      "role": "user",
      "content": "计算 123 * 456 /no_think[unused10][unused9]助手：[unused16][unused17]123 * 456 = 56160[unused10][unordered9]用户：搜索人工智能的最新进展"
    },
    {
      "role": "assistant",
      "content": "[unused16]需要先计算乘法...然后搜索AI进展。[unused17][unused11]{\"name\":\"search\",\"query\":\"artificial intelligence latest progress\"}[unused12]2024年AI领域取得重大突破，包括更大模型、多模态能力提升等。"
    }
  ]
}
```

### 真多轮复杂场景

```json
{
  "meta_prompt": ["你是数据分析师"],
  "tools": "[{\"name\": \"database_query\", \"description\": \"数据库查询\"}]",
  "data": [
    {"role": "user", "content": "查询上个月销售额"},
    {"role": "assistant", "content": "[unused16]需要查询数据库获取销售数据。[unused17][unused11]{\"name\":\"database_query\",\"sql\":\"SELECT SUM(amount) FROM sales WHERE month='last_month'\"}[unused12]上月销售额为 1,234,567 元。"},
    {"role": "user", "content": "按产品类别分析 /no_think"},
    {"role": "assistant", "content": "[unused16]需要按类别分组统计。[unused17][unused16][unused17][unused11]{\"name\":\"database_query\",\"sql\":\"SELECT category, SUM(amount) FROM sales WHERE month='last_month' GROUP BY category\"}[unused12]电子产品：500,000元；服装：300,000元；家居：200,000元..."},
    {"role": "user", "content": "分析增长趋势"},
    {"role": "assistant", "content": "[unused16]需要获取多个月数据进行对比。[unused17][unused11]{\"name\":\"database_query\",\"sql\":\"SELECT month, SUM(amount) FROM sales GROUP BY month ORDER BY month DESC LIMIT 6\"}[unused12][unused16][unused17]根据近6个月数据，销售额呈现上升趋势，平均每月增长约8%。"}
  ]
}
```

---

## 常见问题

### Q1: 什么时候用真多轮，什么时候用伪多轮？

**真多轮（True Multi-turn）：**
- 适合新数据，结构清晰
- 每轮对话相对独立
- 需要保留完整对话结构

**伪多轮（Pseudo Multi-turn）：**
- 适合历史数据处理
- 需要压缩存储空间
- 对话轮次较多

### Q2: 快思考和慢思考如何选择？

| 场景 | 推荐模式 | 原因 |
|------|---------|------|
| 简单问答 | 快思考 | 不需要展示推理 |
| 数计算 | 快思考 | 标准答案即可 |
| 逻辑推理 | 慢思考 | 展示思考价值 |
| 复杂问题 | 慢思考 | 帮助模型学习 |

### Q3: 工具调用可以用哪种格式？

| 格式 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| 嵌入式 | 简洁 | 不够清晰 | 简单工具调用 |
| 独立节点 | 清晰 | 占用空间 | 复杂多工具场景 |
