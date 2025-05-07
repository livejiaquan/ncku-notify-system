# NCKU OIA 公告爬蟲系統

自動爬取成功大學國際事務處網站公告，並通過電子郵件發送通知。

## 功能特點

- 自動爬取成大國際處最新公告
- 過濾重複公告
- 通過電子郵件發送新公告通知
- 完整的日誌記錄
- 配置文件管理敏感信息

## 安裝需求
```bash
pip install -r requirements.txt
```

## Conda 環境設置
1. 建立新的 conda 環境：
```bash
conda create -n ncku-notify python=3.10
conda activate ncku-notify
pip install -r requirements.txt
```

2. 導出環境設定（用於分享）：
```bash
conda env export > environment.yml
```

3. 在其他電腦上導入環境：
```bash
conda env create -f environment.yml
```

## 快速開始
您可以使用提供的腳本來運行爬蟲：

1. 設置腳本執行權限：
```bash
chmod +x run_crawler.sh
```

2. 執行腳本：
```bash
./run_crawler.sh
```

腳本將會：
- 自動啟動 conda 環境
- 運行爬蟲程式
- 等待使用者按鍵後關閉

2. 修改 `email_config.yaml` 中的郵件設置：
- SMTP 服務器信息
- 發件人郵箱和密碼
- 收件人郵箱

## 使用方法

運行爬蟲：
```bash
python src/main.py
```
## 目錄結構
```
project_root/
├── config/ # 配置文件
├── data/ # 數據存儲
│ ├── announcements/ # 公告存儲
│ └── logs/ # 日誌文件
├── src/ # 源代碼
├── test/ # 測試文件
└── experiments/ # 實驗性功能
```
## 注意事項

- 請確保 `email_config.yaml` 不會被提交到版本控制系統
- 建議使用 Gmail 應用程序密碼而不是賬戶密碼
- 建議每天執行一次爬蟲，避免過於頻繁的請求

## 作者

- 作者：LIM JIA QUAN
- 郵箱：livejiaquan010313@gmail.com
