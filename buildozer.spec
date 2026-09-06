[app]

title = La Roue du Destin
package.name = rouedudestin
package.domain = org.destin

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf,json,txt

version = 1.0

requirements = python3,pygame

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

android.permissions = INTERNET

android.api = 33
android.minapi = 21

android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
