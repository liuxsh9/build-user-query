# Wiki 版本使用说明

这个目录包含专门为Wiki平台优化的标签可视化页面。

## 文件说明

### 1. tag-visualization-wiki-embed.html (~138KB)
**推荐用于：支持JavaScript的Wiki平台**

特点：
- ✅ 完整的交互功能（搜索、过滤、实时筛选）
- ✅ 无边距设计，直接内嵌到Wiki页面
- ✅ 卡片式布局，展示完整信息
- ✅ 响应式设计，支持移动端
- ✅ 去除了 `<html>`, `<head>`, `<title>` 标签
- ✅ 无外边距，适合内嵌

使用场景：
- Confluence
- GitBook
- 自建Wiki（支持HTML）
- Notion（部分功能）

### 2. tag-visualization-wiki-compact.html (~135KB)
**推荐用于：需要节省空间的场景**

特点：
- ✅ 手风琴折叠式布局，初始占用空间小
- ✅ 搜索自动展开相关类别
- ✅ 简化的卡片设计
- ✅ 更小的DOM树，性能更好
- ✅ 适合大量标签的场景

使用场景：
- 页面较长的Wiki
- 需要在一屏显示更多内容
- 性能敏感的环境

## 在Wiki中嵌入

### Confluence

#### 方法一：HTML宏（推荐）
1. 编辑页面，插入 "HTML" 宏
2. 复制整个HTML文件内容
3. 粘贴到HTML宏中
4. 保存页面

#### 方法二：iframe
1. 将HTML文件上传到Web服务器
2. 使用iframe嵌入：
   ```html
   <iframe src="https://your-server.com/tag-visualization.html"
           width="100%" height="800px"
           frameborder="0"></iframe>
   ```

### GitBook

1. 创建 `.md` 文件
2. 使用HTML块嵌入：
   ```markdown
   # 标签系统

   {% raw %}
   <!-- 粘贴HTML内容 -->
   {% endraw %}
   ```

### Notion

1. 创建嵌入块 (Embed block)
2. 将HTML文件托管到GitHub Pages或其他服务
3. 粘贴URL

### GitHub Wiki

1. 创建 `.md` 文件
2. 直接粘贴HTML代码（GitHub Markdown支持内联HTML）

### 自建Wiki

直接粘贴HTML内容到页面编辑器中。

## 更新数据

从项目根目录运行：

```bash
# 更新所有版本（包括Wiki版本）
python scripts/generate_tags_data.py --update-wiki

# 只更新Wiki版本
python scripts/generate_tags_data.py --wiki-only
```

## 版本对比

| 特性 | Embed版 | Compact版 |
|------|---------|-----------|
| 文件大小 | ~138KB | ~135KB |
| 布局方式 | 网格卡片 | 折叠列表 |
| 初始显示 | 全部展开 | 全部折叠 |
| 适合场景 | 专门展示页面 | 混合内容页面 |
| 性能 | 较好 | 更好 |
| 美观度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 空间效率 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 浏览器兼容性

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers

## 性能优化

两个版本都包含以下优化：
- 数据内嵌（无需额外HTTP请求）
- CSS作用域隔离（不影响Wiki主题）
- 懒加载搜索（输入时才过滤）
- 最小化JavaScript（压缩数据格式）

## 故障排除

### Wiki不支持JavaScript

如果Wiki平台禁用了JavaScript，两个版本都会失效。此时请考虑：
1. 生成Markdown表格版本（联系管理员）
2. 使用外部链接指向完整HTML版本
3. 使用截图+链接的方式

### 样式冲突

如果Wiki的CSS与可视化样式冲突：
1. 所有样式都使用了类名前缀 (`.tag-viz-` / `.tag-compact-`)
2. 可以手动调整CSS优先级（添加 `!important`）

### 内容被截断

某些Wiki平台有内容长度限制：
1. 使用Compact版本（稍小）
2. 分成多个页面（按类别）
3. 托管到外部服务器，使用iframe嵌入

## 技术细节

### 样式隔离
所有CSS选择器都带有唯一前缀，避免与Wiki主题冲突。

### 数据格式
标签数据以JSON格式内嵌在JavaScript中，格式：
```javascript
{
  "Category": [
    {
      "id": "tag-id",
      "name": "Tag Name",
      "description": "...",
      ...
    }
  ]
}
```

### 事件处理
使用全局函数（`window.setVizFilter`）处理点击事件，兼容性更好。

## 示例

查看 `examples/` 目录（如果有）获取实际嵌入示例。

## 支持

如有问题，请检查：
1. Wiki平台是否支持JavaScript
2. 浏览器控制台是否有错误
3. 网络请求是否被CSP策略阻止
