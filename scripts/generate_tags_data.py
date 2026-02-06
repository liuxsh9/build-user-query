#!/usr/bin/env python3
"""
生成标签可视化数据

从 taxonomy/tags/*.yaml 读取所有标签，转换为JSON格式供可视化页面使用。
"""

import yaml
import json
import argparse
from pathlib import Path


def load_all_tags(taxonomy_dir):
    """从taxonomy目录加载所有标签"""
    tags_dir = Path(taxonomy_dir) / "tags"

    if not tags_dir.exists():
        raise FileNotFoundError(f"Tags目录不存在: {tags_dir}")

    all_tags = {}

    # 读取所有YAML文件
    for yaml_file in sorted(tags_dir.glob("*.yaml")):
        with open(yaml_file, 'r', encoding='utf-8') as f:
            tags = yaml.safe_load(f)

            if not tags:
                continue

            # 按category分组
            for tag in tags:
                category = tag.get('category', 'Unknown')
                if category not in all_tags:
                    all_tags[category] = []
                all_tags[category].append(tag)

    return all_tags


def generate_stats(all_tags):
    """生成统计信息"""
    total_tags = sum(len(tags) for tags in all_tags.values())
    category_stats = {cat: len(tags) for cat, tags in all_tags.items()}

    return {
        'total_tags': total_tags,
        'total_categories': len(all_tags),
        'categories': category_stats
    }


def main():
    parser = argparse.ArgumentParser(description='生成标签可视化数据')
    parser.add_argument(
        '--taxonomy-dir',
        default='taxonomy',
        help='Taxonomy目录路径 (默认: taxonomy)'
    )
    parser.add_argument(
        '--output',
        default='visualization/tags_data.json',
        help='输出JSON文件路径 (默认: visualization/tags_data.json)'
    )
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='格式化输出JSON（更易读但文件更大）'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='显示统计信息'
    )

    args = parser.parse_args()

    # 加载所有标签
    print(f"正在从 {args.taxonomy_dir}/tags/ 加载标签...")
    all_tags = load_all_tags(args.taxonomy_dir)

    # 生成统计
    stats = generate_stats(all_tags)

    if args.stats:
        print("\n=== 标签统计 ===")
        print(f"总类别数: {stats['total_categories']}")
        print(f"总标签数: {stats['total_tags']}")
        print("\n各类别标签数:")
        for category, count in sorted(stats['categories'].items()):
            print(f"  {category}: {count}")

    # 写入JSON文件
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        if args.pretty:
            json.dump(all_tags, f, ensure_ascii=False, indent=2)
        else:
            json.dump(all_tags, f, ensure_ascii=False)

    print(f"\n✓ 成功生成 {output_path}")
    print(f"  包含 {stats['total_tags']} 个标签，{stats['total_categories']} 个类别")


if __name__ == '__main__':
    main()
