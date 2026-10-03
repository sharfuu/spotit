[app]

title = Spotit
package.name = spotit
package.domain = org.spotit

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf

version = 1.0

requirements = python3,kivy

icon.filename = %(source.dir)s/icon.png

orientation = portrait

services =


[buildozer]

log_level = 2
warn_on_root = 1


[android]

android.api = 35
android.minapi = 23
android.sdk = 35
android.ndk = 27c

android.arch = arm64-v8a

android.entrypoint = org.kivy.android.PythonActivity

android.permissions = INTERNET

android.allow_backup = True

android.apptheme = @android:style/Theme.Material.Light.NoActionBar

android.private_storage = True

android.accept_sdk_license = True