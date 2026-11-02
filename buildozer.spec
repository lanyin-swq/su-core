[app]
title = SuCore
package.name = sucore
package.domain = org.lanyin
source.dir = .
source.include_exts = py,db
version = 0.1

# 绝对纯净，不带任何版本号，防止 p4a 版本打架
requirements = python3,kivy,requests

orientation = portrait
fullscreen = 1
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET, WAKE_LOCK
android.api = 33
android.minapi = 26
android.archs = arm64-v8a
android.accept_sdk_license = True

# 移除所有关于 p4a.branch 的配置，使用 buildozer 默认稳定版
