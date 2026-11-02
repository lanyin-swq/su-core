[app]
title = SuCore
package.name = sucore
package.domain = org.lanyin
source.dir = .
source.include_exts = py,db
version = 0.1

# 带有 cmake 和 ninja，这是 llama-cpp 编译必需的
requirements = python3,kivy,requests,llama-cpp-python,cmake,ninja

orientation = portrait
fullscreen = 1
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET, WAKE_LOCK, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 26
android.archs = arm64-v8a
android.accept_sdk_license = True

# 只留这一行！关掉不需要的加速
p4a.env = CMAKE_ARGS="-DLLAMA_BLAS=OFF -DLLAMA_CUDA=OFF -DLLAMA_METAL=OFF -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF"
