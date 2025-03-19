import re
import os
from pathlib import Path

def clean_markdown(content):
    # 移除标题
    content = re.sub(r'^#+\s*', '', content, flags=re.MULTILINE)
    # 移除列表符号
    content = re.sub(r'^[\*\-+]\s+', '', content, flags=re.MULTILINE)
    # 移除链接和图片
    content = re.sub(r'\!?\[([^\]]*)\]\([^\)]+\)', r'\1', content)
    # 移除粗体/斜体
    content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
    content = re.sub(r'\*(.*?)\*', r'\1', content)
    # 移除代码块标记（保留内容）
    content = re.sub(r'```.*?\n', '', content, flags=re.DOTALL)
    content = re.sub(r'`{1,3}', '', content)
    # 移除引用块标记
    content = re.sub(r'^>\s*', '', content, flags=re.MULTILINE)
    # 合并多余空行
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()

def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    cleaned = clean_markdown(content)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned)

def main():
    input_dir = Path('txt')
    output_dir = Path('output')
    processed_files = 0  # 新增计数器

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):
                src_path = Path(root) / file
                rel_path = src_path.relative_to(input_dir)
                clean_name = f"{rel_path.stem}_clean{rel_path.suffix}"
                
                # 添加处理进度提示
                print(f"正在清理：{src_path}")
                process_file(src_path, output_dir / rel_path.with_name(clean_name))
                processed_files += 1  # 更新计数器

    # 添加完成提示
    if processed_files > 0:
        print(f"\n✅ 已完成！共清理 {processed_files} 个文件")
        print(f"输出目录：{output_dir.absolute()}")
    else:
        print("\n⚠️ 未找到可处理的.txt文件")

if __name__ == '__main__':
    main()