#!/bin/sh

PKG_USER="sc-docker-port-viewer"
SUDO_RULE="${PKG_USER} ALL=(ALL) NOPASSWD: ALL"

service_postinst ()
{
    # 1. 临时赋予主配置文件写权限
    chmod 0640 /etc/sudoers
    
    # 2. 保险起见，先删掉可能存在的旧记录，防止重复
    sed -i "/${PKG_USER} ALL=(ALL) NOPASSWD/d" /etc/sudoers
    
    # 3. 暴力将免密码特权追加到文件最末尾（末尾优先级最高！）
    echo "${SUDO_RULE}" >> /etc/sudoers
    
    # 4. 恢复只读权限，否则系统安全机制会警报
    chmod 0440 /etc/sudoers
}

service_postuninst ()
{
    # 卸载套件时，懂事地把我们加的后门擦除干净
    chmod 0640 /etc/sudoers
    sed -i "/${PKG_USER} ALL=(ALL) NOPASSWD/d" /etc/sudoers
    chmod 0440 /etc/sudoers
}