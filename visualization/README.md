# 标签可视化

这个目录包含标签系统的交互式可视化页面。

## 文件说明

- `tag-visualization.html` - 交互式标签浏览器（单文件HTML应用）
- `tags_data.json` - 从YAML生成的标签数据（626个标签）

## 使用方法

### 查看可视化页面

1. 启动本地HTTP服务器：
   ```bash
   python3 -m http.server 8000
   ```

2. 在浏览器中访问：
   ```
   http://localhost:8000/visualization/tag-visualization.html
   ```

3. 使用页面功能：
   - **搜索**: 在顶部搜索框输入关键词查找标签
   - **过滤**: 点击类别按钮只显示特定类别的标签
   - **浏览**: 滚动查看所有标签卡片，点击卡片查看详细信息

### 更新数据

当taxonomy/tags/*.yaml文件更新后，运行以下命令重新生成JSON数据：

```bash
python scripts/generate_tags_data.py --stats
```

选项说明：
- `--stats` - 显示统计信息
- `--pretty` - 格式化输出（更易读但文件更大）
- `--output <path>` - 指定输出路径（默认: visualization/tags_data.json）

## 技术细节

- 纯前端HTML/CSS/JavaScript，无需构建步骤
- 响应式设计，适配移动设备
- 支持实时搜索和过滤
- 数据来源：`tags_data.json`（从taxonomy/tags/*.yaml自动生成）

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
