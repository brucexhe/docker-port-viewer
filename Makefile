SPK_NAME = docker-port-viewer
SPK_VERS = 1.0.0
SPK_REV = 1
SPK_ICON = src/icon.png
MAINTAINER = brucexhe
DESCRIPTION = NAS docker port viewer.
DISPLAY_NAME = Docker port viewer
CHANGELOG = Initial release 1.0.0
# ==================== Web 界面及权限配置 ====================
ADMIN_PORT = 16888
SERVICE_USER = auto

LICENSE  = AGPL-3.0
# ==========================================================

SSS_SCRIPT = src/start-stop-status
SERVICE_PORT = 16888

# Minimum DSM version
SPK_MIN_DSM = 6.0

TC_STRIP = yes

PRE_COPY_TARGET = install_my_python_server

# 引入官方安装钩子机制，注入我们的 sudoers 脚本！
#SERVICE_SETUP = src/service-setup.sh


include ../../mk/spksrc.spk.mk

# === 注入 Python 脚本 ===
install_my_python_server:
	@echo "===> Injecting Python server and fixing PLIST..."
    
	mkdir -p $(INSTALL_DIR)$(INSTALL_PREFIX)/bin
    
	cp src/docker-port-viewer.py $(INSTALL_DIR)$(INSTALL_PREFIX)/bin/docker-port-viewer.py
	cp src/start-stop-status $(INSTALL_DIR)$(INSTALL_PREFIX)/bin/start-stop-status
    
	chmod +x $(INSTALL_DIR)$(INSTALL_PREFIX)/bin/docker-port-viewer.py
	chmod +x $(INSTALL_DIR)$(INSTALL_PREFIX)/bin/start-stop-status
    
	mkdir -p $(WORK_DIR)
    
	echo "bin/docker-port-viewer.py" >> $(WORK_DIR)/PLIST
	echo "bin/start-stop-status" >> $(WORK_DIR)/PLIST

