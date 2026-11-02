[app]
title = SuCore
package.name = sucore
package.domain = org.lanyin
source.dir = .
source.include_exts = py,db
version = 0.1

# 必须带上 cmake 和 ninja 来编译 llama-cpp
requirements = python3,kivy,requests,llama-cpp-python,cmake,ninja

orientation = portrait
fullscreen = 1
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET, WAKE_LOCK, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 26
android.archs = arm64-v8a
android.accept_sdk_license = True

# 强行指定 Android NDK 中的 C/C++ 编译器，并把 CMake 参数压进去
p4a.env = CC=$ANDROIDNDK/toolchains/llvm/prebuilt/darwin-x86_64/bin/clang
p4a.env = CXX=$ANDROIDNDK/toolchains/llvm/prebuilt/darwin-x86_64/bin/clang++
p4a.env = CMAKE_ARGS="-DLLAMA_BLAS=OFF -DLLAMA_CUDA=OFF -DLLAMA_METAL=OFF -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF"
