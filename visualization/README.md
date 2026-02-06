# 标签可视化

这个目录包含标签系统的交互式可视化页面。

## 文件说明

- `tag-visualization.html` - **独立的**交互式标签浏览器（数据已内嵌，无需额外文件）
- `tags_data.json` - 标签数据的JSON格式（可选，仅作为数据备份）

## 使用方法

### 快速开始

**方式一：直接双击打开**
- 直接在浏览器中打开 `tag-visualization.html` 即可使用
- 数据已内嵌在HTML中，无需服务器

**方式二：使用HTTP服务器（推荐）**
1. 启动本地HTTP服务器：
   ```bash
   cd visualization
   python3 -m http.server 8000
   ```

2. 在浏览器中访问：
   ```
   http://localhost:8000/tag-visualization.html
   ```

### 使用页面功能

- **搜索**: 在顶部搜索框输入关键词查找标签
- **过滤**: 点击类别按钮只显示特定类别的标签
- **浏览**: 滚动查看所有标签卡片，鼠标悬停查看详细信息

## 更新数据

当 taxonomy/tags/*.yaml 文件更新后，运行以下命令自动更新HTML中的内嵌数据：

```bash
# 从项目根目录运行
python scripts/generate_tags_data.py --stats
```

这个命令会：
1. 从 YAML 文件读取最新的标签数据
2. 生成 `tags_data.json`（备份文件）
3. **自动更新** `tag-visualization.html` 中的内嵌数据

### 脚本选项

```bash
# 显示统计信息
python scripts/generate_tags_data.py --stats

# 格式化JSON输出（更易读但文件更大）
python scripts/generate_tags_data.py --pretty

# 只生成JSON，不更新HTML
python scripts/generate_tags_data.py --no-update-html

# 自定义输出路径
python scripts/generate_tags_data.py --output custom/path/data.json --html custom/path/page.html
```

## 技术细节

- **完全独立**: HTML文件包含所有必需的数据，可以离线使用
- **零依赖**: 纯前端 HTML/CSS/JavaScript，无需构建步骤
- **响应式设计**: 适配桌面和移动设备
- **实时搜索**: 支持跨字段搜索（名称、ID、描述、别名等）
- **数据来源**: 数据内嵌在HTML中，也可从 `tags_data.json` 获取

## 标签统计

- 总标签数：626
- 类别数：8
  - Agentic: 19
  - Concept: 107
  - Constraint: 25
  - Context: 9
  - Domain: 57
  - Language: 50
  - Library: 339
  - Task: 20

## 文件大小

- `tag-visualization.html`: ~144KB（包含内嵌数据）
- `tags_data.json`: ~137KB（可选备份）
