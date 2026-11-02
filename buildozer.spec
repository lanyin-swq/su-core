[app]
title = SuCore
package.name = sucore
package.domain = org.lanyin
source.dir = .
source.include_exts = py,db
version = 0.1

# 核心：加入 C++ 大模型引擎
requirements = python3,kivy,requests,llama-cpp-python

orientation = portrait
fullscreen = 1
# 必须包含 MANAGE_EXTERNAL_STORAGE，否则读不到 Download 里的模型
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET, WAKE_LOCK, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 26
android.archs = arm64-v8a
android.accept_sdk_license = True

# 强制编译 CPU 版
p4a.env = CMAKE_ARGS="-DLLAMA_BLAS=OFF -DLLAMA_CUDA=OFF -DLLAMA_METAL=OFF"
