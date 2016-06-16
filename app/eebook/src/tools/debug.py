# -*- coding: utf-8 -*-
import logging
import logging.handlers
import sys

from config import Config


class Debug(object):
    u"""
    打印日志
    """
    handler = logging.StreamHandler()    # 实例化handler
    detail_fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    clean_fmt = '%(message)s'

    formatter = logging.Formatter(detail_fmt)
    handler.setFormatter(formatter)

    logger = logging.getLogger('main')  # 获取名为main的logger
    logger.addHandler(handler)

    # formatter = logging.Formatter(clean_fmt)
    # handler.setFormatter(formatter)

    if Config.debug:
        logger.setLevel(logging.DEBUG)     # debug模式, 显示 debug, info, warning, error, critical 信息
    else:
        logger.setLevel(logging.INFO)      # 发布时关闭log输出,只显示 info, warning, error, critical信息

    # 辅助函数
    @staticmethod
    def print_in_single_line(text=''):
        try:
            sys.stdout.write("\r" + " " * 60 + '\r')
            sys.stdout.flush()
            sys.stdout.write(text)
            sys.stdout.flush()
        except:
            pass
        return

    @staticmethod
    def print_dict(data={}, key='', prefix=''):
        try:
            if isinstance(data, dict):
                for key in data:
                    Debug.print_dict(data[key], key, prefix + '   ')
            else:
                if isinstance(data, basestring):
                    print prefix + unicode(key) + ' => ' + data
                else:
                    print prefix + unicode(key) + ' => ' + unicode(data)
        except UnicodeEncodeError as error:
            Debug.logger.info(u'编码异常')
            Debug.logger.info(u'系统默认编码为：' + sys.getdefaultencoding())
            raise error
        return

    @staticmethod
    def print_config():
        Debug.print_dict(Config.__dict__)
        return
