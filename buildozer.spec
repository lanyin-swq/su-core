[app]
title = SuCore
package.name = sucore
package.domain = org.lanyin
source.dir = .
source.include_exts = py,db
version = 0.1

# 锁定 Python 3.11 这个黄金兼容版本，并补齐所有编译工具
requirements = python3==3.11,hostpython3==3.11,requests,kivy==2.3.1,llama-cpp-python==0.2.79,cmake,ninja,scikit-build-core

orientation = portrait
fullscreen = 1
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET, WAKE_LOCK, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 26
android.archs = arm64-v8a
android.accept_sdk_license = True

# 强制只编译 CPU 版本，关闭所有不需要的硬件加速，防止 CMake 迷失方向
p4a.env = CMAKE_ARGS="-DLLAMA_BLAS=OFF -DLLAMA_CUDA=OFF -DLLAMA_METAL=OFF -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF"
