import logging
from logging import getLogger, FileHandler
from datetime import datetime
import pytz
import os
import re

# ANSIエスケープシーケンスを削除するための正規表現
ANSI_ESCAPE = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')

# カスタムフィルタを作成
class RemoveANSIColorFilter(logging.Filter):
    def filter(self, record):
        record.msg = ANSI_ESCAPE.sub('', record.msg)
        return True

# カスタムフォーマッタを作成
class JSTFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        # 日本時間（JST）を設定
        jst = pytz.timezone('Asia/Tokyo')
        # ログの作成時間を日本時間に変換
        record_time = datetime.fromtimestamp(record.created, jst)
        if datefmt:
            s = record_time.strftime(datefmt)
        else:
            s = record_time.strftime("%Y-%m-%d %H:%M:%S")
        return s

def set_log():
    logfile = f'/workspace/logs/{datetime.now().strftime("%Y%m%d")}.log'
    if not os.path.exists(logfile):
        with open(logfile,'w'):
            pass
    logger = getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    if not logger.hasHandlers():
        file_handler = FileHandler(logfile)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(JSTFormatter('%(asctime)s - %(filename)s - %(lineno)s - %(levelname)s - %(message)s'))
        # カスタムフィルタをハンドラに追加
        # file_handler.addFilter(RemoveANSIColorFilter())
        logger.addHandler(file_handler)
    return logger

if __name__ == '__main__':
    logger = set_log()
    logger.info('test')