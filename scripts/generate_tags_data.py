#!/usr/bin/env python3
"""
生成标签可视化数据

从 taxonomy/tags/*.yaml 读取所有标签，转换为JSON格式供可视化页面使用。
"""

import yaml
import json
import re
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


def update_html_embedded_data(html_path, tags_data):
    """更新HTML文件中的内嵌数据"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 生成新的数据（压缩格式以减小文件大小）
    new_data_json = json.dumps(tags_data, ensure_ascii=False, separators=(',', ':'))

    # 查找并替换内嵌数据
    # 匹配 "let tagsData = {任何内容};" 这一整行
    start_marker = "let tagsData = "
    end_marker = ";\n        let currentFilter"

    start_idx = html_content.find(start_marker)
    end_idx = html_content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        return False

    # 构建新的内容
    new_html_content = (
        html_content[:start_idx + len(start_marker)] +
        new_data_json +
        html_content[end_idx:]
    )

    # 写回文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html_content)

    return True


def update_wiki_versions(tags_data):
    """更新所有Wiki版本的HTML文件"""
    wiki_dir = Path('visualization/wiki-versions')
    if not wiki_dir.exists():
        return []

    updated_files = []

    # 查找所有Wiki版本HTML文件
    for html_file in wiki_dir.glob('tag-visualization-wiki-*.html'):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 替换数据占位符
            data_json = json.dumps(tags_data, ensure_ascii=False, separators=(',', ':'))

            # 查找并替换 {TAGS_DATA_PLACEHOLDER} 或已有的数据
            if '{TAGS_DATA_PLACEHOLDER}' in content:
                new_content = content.replace('{TAGS_DATA_PLACEHOLDER}', data_json)
            else:
                # 查找已有的内嵌数据
                start_marker = "let tagsData = "
                end_marker_variants = [
                    ";\n    let searchTerm",  # compact版本
                    ";\n    let currentFilter"  # embed版本
                ]

                updated = False
                for end_marker in end_marker_variants:
                    start_idx = content.find(start_marker)
                    end_idx = content.find(end_marker)

                    if start_idx != -1 and end_idx != -1:
                        new_content = (
                            content[:start_idx + len(start_marker)] +
                            data_json +
                            content[end_idx:]
                        )
                        updated = True
                        break

                if not updated:
                    continue

            # 写回文件
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            updated_files.append(html_file.name)

        except Exception as e:
            print(f"⚠️  更新 {html_file.name} 失败: {e}")

    return updated_files


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
        '--html',
        default='visualization/tag-visualization.html',
        help='HTML可视化文件路径，将更新其中的内嵌数据 (默认: visualization/tag-visualization.html)'
    )
    parser.add_argument(
        '--update-html',
        action='store_true',
        default=True,
        help='自动更新HTML文件中的内嵌数据 (默认: True)'
    )
    parser.add_argument(
        '--no-update-html',
        action='store_false',
        dest='update_html',
        help='不更新HTML文件'
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
    parser.add_argument(
        '--update-wiki',
        action='store_true',
        help='同时更新Wiki版本的HTML文件'
    )
    parser.add_argument(
        '--wiki-only',
        action='store_true',
        help='仅更新Wiki版本，不更新主HTML文件'
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

    # 更新HTML文件中的内嵌数据
    if args.update_html and not args.wiki_only:
        html_path = Path(args.html)
        if html_path.exists():
            if update_html_embedded_data(html_path, all_tags):
                print(f"\n✓ 成功更新 {html_path} 中的内嵌数据")
            else:
                print(f"\n⚠️  未能更新 {html_path}（可能数据格式已改变）")
        else:
            print(f"\n⚠️  HTML文件不存在: {html_path}")

    # 更新Wiki版本
    if args.update_wiki or args.wiki_only:
        updated_files = update_wiki_versions(all_tags)
        if updated_files:
            print(f"\n✓ 成功更新 {len(updated_files)} 个Wiki版本:")
            for filename in updated_files:
                print(f"  - {filename}")
        else:
            print("\n⚠️  未找到Wiki版本文件")


if __name__ == '__main__':
    main()
