[app]
title = SuCore
package.name = sucore
package.domain = org.lanyin
source.dir = .
source.include_exts = py,db
version = 0.1

# 锁定兼容的 Python 3.13 和稳定版引擎，同时加入所有 C++ 编译依赖
requirements = python3==3.13,hostpython3==3.13,requests,kivy==2.3.1,llama-cpp-python==0.2.77,cmake,ninja,scikit-build-core

orientation = portrait
fullscreen = 1
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET, WAKE_LOCK, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 26
android.archs = arm64-v8a
android.accept_sdk_license = True

# 关闭不必要的硬件加速，防止底层 CMake 找错方向
p4a.env = CMAKE_ARGS="-DLLAMA_BLAS=OFF -DLLAMA_CUDA=OFF -DLLAMA_METAL=OFF -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF"
