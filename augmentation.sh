#!/bin/bash
# 图像处理工具 - 使用 argparse 的 Python 脚本的外壳脚本

# 帮助信息
function show_help() {
    echo "图像处理工具"
    echo ""
    echo "用法：augmentation.sh [命令] [参数]"
    echo ""
    echo "可用命令："
    echo "  flip         翻转图片（左右和上下）"
    echo "  translate    平移图片并填充黑色区域"
    echo ""
    echo "选项："
    echo "  --help       显示帮助信息"
}

# 处理翻转命令
function handle_flip() {
    if [ $# -lt 2 ]; then
        echo "错误：缺少参数。用法：image_tool.sh flip --input_dir <图片dir> --savedir <保存目录>"
        exit 1
    fi

    # 提取参数
    input_dir=
    save_dir=
    
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            --input_dir)
                input_dir="$2"
                shift
                ;;
            --savedir)
                save_dir="$2"
                shift
                ;;
            *)
                echo "错误：未知参数 $1"
                exit 1
                ;;
        esac
        shift
    done

    if [ -z "$input_dir" ] || [ -z "$save_dir" ]; then
        echo "错误：必须提供 --input_dir 和 --savedir 参数。"
        exit 1
    fi

    # 调用 Python 脚本进行翻转操作
    python augmentation.py flip --input_dir "$input_dir" --savedir "$save_dir"
}

# 处理平移命令
function handle_translate() {
    if [ $# -lt 2 ]; then
        echo "错误：缺少参数。用法：image_tool.sh translate --input_dir <图片路径> --savedir <保存目录> [--distance <距离>] "
        exit 1
    fi

    # 提取参数
    input_dir=
    save_dir=
    distance=10  # 默认距离为 10 像素
    
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            --input_dir)
                input_dir="$2"
                shift
                ;;
            --savedir)
                save_dir="$2"
                shift
                ;;
            --distance)
                distance="$2"
                shift
                ;;
            *)
                echo "错误：未知参数 $1"
                exit 1
                ;;
        esac
        shift
    done

    if [ -z "$input_dir" ] || [ -z "$save_dir" ]; then
        echo "错误：必须提供 --input_dir 和 --savedir 参数。"
        exit 1
    fi

    # 调用 Python 脚本进行平移操作
    python augmentation.py translate --input_dir "$input_dir" --savedir "$save_dir" --distance "$distance"
}

# 主程序
if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

case "$1" in
    flip)
        shift
        handle_flip "$@"
        ;;
    translate)
        shift
        handle_translate "$@"
        ;;
    *)
        echo "错误：未知命令 $1。"
        show_help
        exit 1
        ;;
esac