[app]
title = La Roue du Destin
package.name = rouedudestin
package.domain = org.destin
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,pygame

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
