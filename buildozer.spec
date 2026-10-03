[app]

title = SpotIt
package.name = spotit
package.domain = org.spotit

source.dir = .
source.include_exts = py,png,jpg,jpeg,json

version = 1.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0

icon.filename = assets/icon.png


[buildozer]

log_level = 2
warn_on_root = 1


[buildozer:android]

android.accept_sdk_license = True
