[app]
title = Кто импостер
package.name = imposter
package.domain = org.test
source.dir = .
source.filename = main.py
source.include_exts = py,png,jpg,jpeg,mp3,json
version = 1.0.0

requirements = python3==3.10.0,hostpython3==3.10.0,kivy==2.3.0

orientation = portrait
fullscreen = 1

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
