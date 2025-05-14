#!/bin/bash

# 獲取腳本所在的目錄的絕對路徑
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 設置環境變量
export PATH="/Users/jiaquan/opt/anaconda3/bin:$PATH"
export HOME="/Users/jiaquan"

# 初始化conda
source "/Users/jiaquan/opt/anaconda3/etc/profile.d/conda.sh"

# 啟動conda環境
conda activate ncku-notify

# 切換到專案目錄
cd "$SCRIPT_DIR"

# 檢查參數
if [ "$1" == "--only-today" ]; then
    echo "只爬取今天的公告"
    # 執行主程式，帶上參數
    python src/main.py --only-today
else
    echo "爬取所有公告"
    # 執行主程式，不帶參數
    python src/main.py
fi

# 完成後保持終端機開啟
echo "程式執行完成。按任意鍵關閉視窗..."
read -n 1 