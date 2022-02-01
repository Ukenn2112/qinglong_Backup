#!/usr/bin/env python3
# coding: utf-8
'''
项目名称: Ukenn2112 / qinglong_Backup
Author: Ukenn2112
功能：自动备份qinglong基本文件至阿里云盘
Date: 2022/02/02 下午23:30
cron: 0 0 * * *
new Env('备份qinglong');
'''
#!/usr/bin/env python3
# coding: utf-8
import os
import tarfile
import time

from aligo import Aligo

exclude_names = ['log', 'backups']  # 排除目录名
backups_path = 'backups'  # 备份目标目录


def start():
    """开始运行"""
    print('登录阿里云盘')
    ali = Aligo(show=show)
    print('将所需备份目录文件进行压缩...')
    retval = os.getcwd()
    mkdir(backups_path)
    now_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    files_name = f'{backups_path}/qinglong_{now_time}.tar.gz'
    print(f'创建备份文件: {retval}/{files_name}')
    if make_targz(files_name, retval):
        print('备份文件压缩完成...开始上传至阿里云盘')
        remote_folder = ali.get_file_by_path('qinglong_backups')  # 云盘目录
        ali.sync_folder(f'{retval}/{backups_path}/',
                        flag=True,  # 以本地为主
                        remote_folder=remote_folder.file_id)  # 本地目录
        print('---------------------备份完成---------------------')
    else:
        return


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
        print(f'压缩失败: {str(e)}')
        return False


def mkdir(path):
    """创建备份目录"""
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        print(f'第一次备份,创建备份目录: {backups_path}')
        os.makedirs(path)  # 创建文件时如果路径不存在会创建这个路径
    else:
        pass


def show(qr_link: str):
    """打印二维码链接"""
    print('请手动复制以下链接，打开阿里网盘App扫描登录')
    print(f'https://cli.im/api/qrcode/code?text={qr_link}')


if __name__ == '__main__':
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('---------' + str(nowtime) + ' 备份程序开始执行------------')
    os.chdir('/ql/')  # 设置运行目录
    start()
