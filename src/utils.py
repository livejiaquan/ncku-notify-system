import logging
from datetime import datetime
import os

def setup_logger():
    """設置日誌配置"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(project_root, 'data', 'logs')
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f'crawler_{datetime.now().strftime("%Y%m%d")}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def format_message(message):
    """格式化輸出消息"""
    return f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}" 