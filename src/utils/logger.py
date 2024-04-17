import logging
import logging.config
import os

from config.settings import get_server_helper_config_from_yaml
from utils.time_utils import TimeUtils


class Logger:
    
    @staticmethod
    def configure_logger(log_file_name: str) -> None:
        log_file_dir: str = Logger.__get_log_file_dir()
        date_time_str: str = TimeUtils.get_today_date_str(time=True)
        log_file_dir_with_date: str = os.path.join(log_file_dir, TimeUtils.get_today_date_str())
        if not os.path.exists(log_file_dir_with_date):
            os.makedirs(log_file_dir_with_date)
            print("New directory created==>", log_file_dir_with_date)
        Logger.__config_root_logger(log_file_dir_with_date + f"/{log_file_name}_{date_time_str}.log")
        
    @staticmethod    
    def __config_root_logger(log_file: str) -> None:

        formatter = "%(asctime)-15s" \
                    "| %(levelname)-s " \
                    "| %(process)s " \
                    "| %(thread)s " \
                    "| %(filename)s " \
                    "| %(funcName)s " \
                    "| %(lineno)d " \
                    "| %(name)-s " \
                    "| %(message)s"

        logging.config.dictConfig({
            'version': 1,
            'formatters': {
                'root_formatter': {
                    'format': formatter
                }
            },
            'handlers': {
                'log_file': {
                    'class': 'logging.FileHandler',
                    'level': 'DEBUG',
                    'filename': log_file,
                    'formatter': 'root_formatter',
                }
            },
            'loggers': {
                '': {
                    'handlers': [
                        'log_file',
                    ],
                    'level': 'DEBUG',
                    'propagate': True
                }
            }
        })
        
    @staticmethod
    def __get_log_file_dir() -> str:
        server_config: dict = get_server_helper_config_from_yaml()
        log_file_dir: str = server_config.get('paths','').get('logs')
        return log_file_dir