NCKU OIA 公告爬蟲系統
=======================

.. toctree::
   :maxdepth: 2
   :caption: 目錄:

   introduction
   installation
   usage
   api
   contributing

簡介
----

NCKU OIA 公告爬蟲系統是一個自動化工具，用於爬取成功大學國際事務處網站的公告，並通過電子郵件發送通知。

功能特點
--------

* 自動爬取最新公告
* 過濾重複公告
* 電子郵件通知
* 完整的日誌記錄
* 配置文件管理

快速開始
--------

1. 安裝依賴：

   .. code-block:: bash

      pip install -r requirements.txt

2. 設置配置文件：

   .. code-block:: bash

      cp config/email_config.example.yaml config/email_config.yaml

3. 運行爬蟲：

   .. code-block:: bash

      ./run_crawler.sh

貢獻
----

我們歡迎任何形式的貢獻！請查看 :doc:`contributing` 了解更多信息。

授權
----

本項目採用 MIT 授權條款 - 詳見 LICENSE 文件。 