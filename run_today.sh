#!/bin/bash

# 獲取腳本所在的目錄的絕對路徑
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 初始化conda
eval "$(conda shell.bash hook)"

# 啟動conda環境
conda activate ncku-notify

# 切換到專案目錄
cd "$SCRIPT_DIR"

echo "只爬取今天的公告"
# 執行主程式，帶上參數
python src/main.py --only-today

# 完成後保持終端機開啟
echo "程式執行完成。按任意鍵關閉視窗..."
read -n 1 