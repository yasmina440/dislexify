[app]

title = Dislexify
package.name = dislexify
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_dirs = venv, __pycache__,.git,.github
version = 0.1
requirements = python3,kivy,kivymd,requests
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = android.permission.INTERNET
android.api = 31
android.minapi = 21
android.ndk = 25b
#android.ndk_path = ./android-ndk
android.skip_update = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

ios.codesign.allowed = false

[buildozer]
log_level = 2
warn_on_root = 1
