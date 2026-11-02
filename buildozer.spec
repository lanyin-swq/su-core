[app]
title = SuCore
package.name = sucore
package.domain = org.lanyin
source.dir = .
source.include_exts = py,db
version = 0.1

# 锁定 Python 3.11 和旧版引擎，绝对不碰 3.14 的坑
requirements = python3==3.11,hostpython3==3.11,requests,kivy,llama-cpp-python==0.2.77,cmake,ninja

orientation = portrait
fullscreen = 1
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET, WAKE_LOCK, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 26
android.archs = arm64-v8a
android.accept_sdk_license = True

# 强行指定编译参数，一行搞定，不写多行避免报错
p4a.env = CMAKE_ARGS="-DLLAMA_BLAS=OFF -DLLAMA_CUDA=OFF -DLLAMA_METAL=OFF -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF"
