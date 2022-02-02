#!/usr/bin/env python3
# coding: utf-8
'''
项目名称: Ukenn2112 / qinglong_Backup
Author: Ukenn2112
功能：自动备份qinglong基本文件至阿里云盘
Date: 2022/02/03 上午10:00
cron: 0 0 * * *
new Env('qinglong备份');
'''
import logging
import os
import sys
import tarfile
import time

from aligo import Aligo
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
try:
    from notify import send
except:
    logger.info("无推送文件")

exclude_names = ['log', '.git', '.github', 'node_modules', 'backups']  # 排除目录名
backups_path = 'backups'  # 备份目标目录


def start():
    """开始运行"""
    logger.info('登录阿里云盘')
    try:
        ali = Aligo(level=logging.INFO, show=show)
    except:
        logger.info('登录失败')
        try:
            send('qinglong自动备份', '阿里网盘登录失败,请手动重新运行本脚本登录')
        except:
            logger.info("通知发送失败")
        sys.exit(1)
    logger.info('将所需备份目录文件进行压缩...')
    retval = os.getcwd()
    mkdir(backups_path)
    now_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    files_name = f'{backups_path}/qinglong_{now_time}.tar.gz'
    logger.info(f'创建备份文件: {retval}/{files_name}')
    if make_targz(files_name, retval):
        logger.info('备份文件压缩完成...开始上传至阿里云盘')
        remote_folder = ali.get_file_by_path('qinglong_backups')  # 云盘目录
        ali.sync_folder(f'{retval}/{backups_path}/',
                        flag=True,  # 以本地为主
                        remote_folder=remote_folder.file_id)  # 本地目录
        message_up_time = time.strftime("%Y年%m月%d日 %H时%M分%S秒", time.localtime())
        text = f'已备份至阿里网盘: qinglong_backups/qinglong_{now_time}.tar.gz\n' \
               f'备份时间: {message_up_time}\n' \
               f'\n来自项目: https://github.com/Ukenn2112/qinglong_Backup'
        try:
            send('qinglong自动备份', text)
        except:
            logger.info("通知发送失败")
        logger.info('---------------------备份完成---------------------')
    else:
        try:
            send('qinglong自动备份', '备份压缩失败,请检查日志')
        except:
            logger.info("通知发送失败")
        sys.exit(1)


def make_targz(output_filename, retval):
    """
    压缩为 tar.gz
    :param output_filename: 压缩文件名
    :param retval: 备份目录
    :return: bool
    """
    try:
        tar = tarfile.open(output_filename, "w:gz")
        os.chdir(retval)
        path = os.listdir(os.getcwd())
        for p in path:
            if os.path.isdir(p):
                if p not in exclude_names:
                    pathfile = os.path.join(retval, p)
                    tar.add(pathfile)
        tar.close()
        return True
    except Exception as e:
        logger.info(f'压缩失败: {str(e)}')
        return False


def mkdir(path):
    """创建备份目录"""
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        logger.info(f'第一次备份,创建备份目录: {backups_path}')
        os.makedirs(path)  # 创建文件时如果路径不存在会创建这个路径
    else:
        pass


def show(qr_link: str):
    """打印二维码链接"""
    logger.info('请手动复制以下链接，打开阿里网盘App扫描登录')
    logger.info(f'https://cli.im/api/qrcode/code?text={qr_link}')


if __name__ == '__main__':
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logger.info('---------' + str(nowtime) + ' 备份程序开始执行------------')
    os.chdir('/ql/')  # 设置运行目录
    start()
    sys.exit(0)
