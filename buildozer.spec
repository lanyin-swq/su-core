[app]
p4a.pip_options = --prefer-binary
title = SuCore
package.name = sucore
package.domain = org.lanyin
source.dir = .
source.include_exts = py,db
version = 0.1
requirements = python3,kivy,requests
orientation = portrait
fullscreen = 1
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET, WAKE_LOCK
android.api = 33
android.minapi = 26
android.archs = arm64-v8a
android.accept_sdk_license = True
