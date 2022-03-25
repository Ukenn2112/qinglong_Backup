# qinglong_Backup

- 将[青龙](https://github.com/whyour/qinglong)的基本配置文件及脚本备份至阿里网盘

# 使用

- 将 `aligo` 添加 Python3 依赖至 qinglong 面板

  - `依赖管理` --> `Python3` --> `新建依赖` --> 名称内输入 `aligo` 保存 --> 等待安装完成

- 拉库命令

  - 可以直链github/国外机:   `ql repo https://github.com/Ukenn2112/qinglong_Backup.git`
  
  - 国内镜像(部分人不可用):  `ql repo https://github.com.cnpmjs.org/qinglong_Backup.git`

- 第一次使用

  - 请先手动运行一次复制登录二维码链接扫码登录阿里云盘

# 变量

  - `QLBK_EXCLUDE_NAMES` 排除备份`/ql/`下的目录

    默认为 `['log', '.git', '.github', 'node_modules', 'backups']`

  - `QLBK_BACKUPS_PATH` 备份目录`/ql/<QLBK_BACKUPS_PATH>`
  
    默认为 `backups`

  - `QLBK_MAX_FLIES` 最大备份数

    默认为 `5`

# 恢复备份

  1. 解压缩备份文件 qinglong_xxx.tar.gz

  2. 提取名称为 `ql` 的文件夹

  3. 删除之前的qinglong容器重新创建映射以下对应目录：

  - qinglong 2.11.3 及其之前版本

        ```
        /ql/config
        /ql/db
        /ql/repo
        /ql/raw
        /ql/scripts
        /ql/jbot (如有jbot)
        /ql/ninja (如有ninja)
        ```
  - qinglong 2.12.0 及其之后版本

        ```
        /ql/data
        ```

   例 qinglong 2.11.3（docker-compose） `+ 号后为可选,如果备份文件里有这些文件则加上`：

   ```diff
   version: "3"
   services:
     qinglong:
       image: whyour/qinglong:latest
       container_name: qinglong
       restart: unless-stopped
       tty: true
       ports:
         - 5700:5700
   +     - 5701:5701 (如有ninja)
       environment:
         - ENABLE_HANGUP=true
         - ENABLE_WEB_PANEL=true
       volumes:
         - /ql/config:/ql/config
         - /ql/log:/ql/log
         - /ql/db:/ql/db
         - /ql/repo:/ql/repo
         - /ql/raw:/ql/raw
         - /ql/scripts:/ql/scripts
   +     - /ql/jbot:/ql/jbot  (如有jbot)
   +     - /ql/jbot:/ql/jbot  (如有ninja)
   ```

   例 qinglong 2.11.3（docker-run） `+ 号后为可选 解释同上`：

   ```diff
   docker run -dit \
     -v $PWD/ql/config:/ql/config \
     -v $PWD/ql/log:/ql/log \
     -v $PWD/ql/db:/ql/db \
     -v $PWD/ql/repo:/ql/repo \
     -v $PWD/ql/raw:/ql/raw \
     -v $PWD/ql/scripts:/ql/scripts \
   + -v $PWD/ql/jbot:/ql/jbot \
   + -v $PWD/ql/ninja:/ql/ninja \
     -p 5700:5700 \
   + -p 5701:5701 \
     --name qinglong \
     --hostname qinglong \
     --restart unless-stopped \
     whyour/qinglong:latest
   ```

# 感谢

  - [aligo SDK 提供上传阿里网盘支持](https://github.com/foyoux/aligo)