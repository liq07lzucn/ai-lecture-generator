#!/bin/bash
# 整理输出目录 - 按课程分类

cd /data/projects/work/ai-lecture-generator

output_dir="./workspace/output"

echo "🧹 整理输出目录..."
echo ""

# 创建课程目录
mkdir -p "$output_dir/courses"

# 移动所有非 meta 文件到课程目录
for file in "$output_dir"/*; do
    if [ -f "$file" ] && [[ ! "$(basename $file)" =~ ^meta_ ]] && [[ ! "$(basename $file)" =~ ^\. ]]; then
        # 提取课程名前缀 (例如：geant4_讲义.md → geant4)
        filename=$(basename "$file")
        course_name=$(echo "$filename" | sed 's/[_-].*//')
        
        if [ -n "$course_name" ] && [ "$course_name" != "output" ]; then
            course_dir="$output_dir/courses/$course_name"
            mkdir -p "$course_dir"
            mv "$file" "$course_dir/" 2>/dev/null
            echo "✅ 移动：$filename → courses/$course_name/"
        fi
    fi
done

# 移动 meta 文件到对应课程目录
for meta_file in "$output_dir"/meta_*.json; do
    if [ -f "$meta_file" ]; then
        mv "$meta_file" "$output_dir/courses/" 2>/dev/null
    fi
done

echo ""
echo "✅ 整理完成!"
echo ""
echo "目录结构:"
echo "  workspace/output/"
echo "  ├── courses/          # 按课程分类"
echo "  │   ├── geant4/"
echo "  │   ├── AI 基础/"
echo "  │   └── ..."
echo "  └── meta_*.json       # 元数据"
echo ""
