[app]
title = Running Game
package.name = runninggame
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = landscape
fullscreen = 1

android.api = 35
android.minapi = 23
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

log_level = 2

[buildozer]
log_level = 2
