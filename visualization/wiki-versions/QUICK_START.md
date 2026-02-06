# Wiki 内嵌快速指南

## 🚀 快速开始

### 1. 预览和选择版本

在浏览器中打开：http://localhost:8002/preview.html

或者运行：
```bash
cd visualization/wiki-versions
python3 -m http.server 8002
# 访问 http://localhost:8002/preview.html
```

### 2. 复制代码

在预览页面中：
1. 选择适合的版本（Embed 或 Compact）
2. 点击 "📋 复制代码到剪贴板" 按钮
3. 代码已复制，可以直接粘贴到Wiki

### 3. 嵌入到Wiki

#### Confluence
1. 编辑页面
2. 插入 "HTML" 宏
3. 粘贴复制的代码
4. 保存

#### GitBook / GitHub Wiki
1. 创建或编辑 Markdown 文件
2. 直接粘贴HTML代码（Markdown支持内联HTML）
3. 保存

#### 其他Wiki平台
查看 `README.md` 了解更多平台的嵌入方法

## 📝 版本说明

### Embed 版（推荐）
- **文件大小**: ~138KB
- **布局**: 网格卡片
- **特点**: 美观、完整功能
- **适合**: 专门的标签展示页面

### Compact 版
- **文件大小**: ~135KB
- **布局**: 折叠列表
- **特点**: 节省空间、性能好
- **适合**: 混合内容页面、长文档

## 🔄 更新数据

当标签数据更新后，运行：

```bash
# 更新所有版本（主HTML + Wiki版本）
python scripts/generate_tags_data.py --update-wiki --stats

# 仅更新Wiki版本
python scripts/generate_tags_data.py --wiki-only
```

## ✨ 特性

✅ 无需服务器（数据已内嵌）
✅ 完整搜索功能
✅ 分类过滤
✅ 响应式设计
✅ 零边距（适合内嵌）
✅ 样式隔离（不影响Wiki主题）

## 📁 文件列表

```
wiki-versions/
├── tag-visualization-wiki-embed.html    # 完整交互版
├── tag-visualization-wiki-compact.html  # 轻量折叠版
├── preview.html                         # 预览页面
├── README.md                            # 详细文档
└── QUICK_START.md                       # 本文件
```

## 🛠️ 故障排除

**问题**: Wiki不显示内容
- 检查是否支持JavaScript
- 查看浏览器控制台错误

**问题**: 样式冲突
- Wiki版本已使用样式隔离
- 如有问题，联系管理员

**问题**: 内容被截断
- Wiki可能有长度限制
- 尝试使用Compact版本
- 或使用iframe方式嵌入

## 📞 需要帮助？

查看详细文档：`README.md`

---

**提示**: 推荐先在测试页面预览效果，确认满意后再嵌入到正式Wiki。
