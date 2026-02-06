# 历史收集数据

这个目录包含标签收集和处理过程中的中间数据文件，用于记录和追溯数据来源。

## 目录说明

这些文件是在构建taxonomy过程中生成的临时或中间数据，已完成其历史使命，但保留用于：

1. **追溯性**: 了解标签是如何被收集和演变的
2. **参考**: 未来扩展时可参考之前的收集策略
3. **审计**: 验证标签来源和决策过程

## 文件类型

### 收集数据 (collected_*.json)

从各种来源收集的原始标签数据：

- `collected_all_tags.json` - 汇总文件（55KB），包含所有来源的标签
- `collected_concept_*.json` - Concept类别的收集数据（基础、高级、工程）
- `collected_library_*.json` - Library子类别的收集数据（Web、Data、Database、Testing、Infrastructure）
- `collected_domain*.json` - Domain类别的收集数据（原始+扩展）
- `collected_language*.json` - Language类别的收集数据（原始+覆盖分析）
- `collected_*_expansion.json` - 各类别的扩展数据

这些文件通常由以下脚本生成：
- `scripts/collect_tags.py` - 基础标签收集
- `scripts/collect_tags_multisource.py` - 多源收集（Stack Overflow、npm、PyPI、GitHub）

### 辅助数据

- `alias_candidates.json` - 自动化别名扩展建议（由 `expand_aliases.py` 生成）
- `concept_gap_filling.json` - Concept类别扩展时的缺口填充记录

## 使用这些数据

如果需要重新生成或验证标签：

1. **查看原始收集**:
   ```bash
   python3 -c "import json; print(json.dumps(json.load(open('archive/collections/collected_all_tags.json')), indent=2))" | head -50
   ```

2. **统计分析**:
   ```bash
   python3 << EOF
   import json
   from pathlib import Path

   for f in Path('archive/collections').glob('collected_*.json'):
       data = json.load(open(f))
       if isinstance(data, list):
           print(f"{f.name}: {len(data)} items")
   EOF
   ```

3. **重新运行收集**（如果需要）:
   ```bash
   python scripts/collect_tags_multisource.py --category concept --subcategory fundamentals
   ```

## 注意事项

- 这些文件**不应该被修改**，它们是历史记录
- 当前生产数据在 `taxonomy/tags/*.yaml`
- 如需添加新标签，应直接编辑YAML文件或使用tag-manager应用
- 这些JSON文件可能包含未被最终采纳的标签

## 文件大小

总计约200KB的历史数据，包含数千个候选标签和分析结果。
