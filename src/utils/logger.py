import datetime
import logging
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(module)s:%(lineno)d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

log_file = f'logs/app-{datetime.datetime.now().strftime("%Y-%m-%d")}.log'
os.makedirs(os.path.dirname(log_file), exist_ok=True)
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(module)s:%(lineno)d - %(levelname)s - %(message)s', 
                                  datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
