#!/bin/bash

# 獲取腳本所在的目錄的絕對路徑
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 初始化conda
eval "$(conda shell.bash hook)"

# 啟動conda環境
conda activate ncku-notify

# 切換到專案目錄
cd "$SCRIPT_DIR"

# 執行主程式
python src/main.py

# 完成後保持終端機開啟
echo "程式執行完成。按任意鍵關閉視窗..."
read -n 1 