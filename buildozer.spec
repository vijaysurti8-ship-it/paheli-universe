[app]

# (str) Title of your application
title = Paheli Universe

# (str) Package name
package.name = paheliuniverse

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,ttf,json

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,pygame

# (int) Android API to use (Target SDK)
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use (Isko khali chhod rahe hain kyunki env variable upar set kar diya hai)
android.ndk = 

# (int) Android NDK API to use
android.ndk_api = 21

# (bool) Use ccache to speed up compilation
android.ccache = 1

# (list) The Android architectures to build for
android.archs = armeabi-v7a, arm64-v8a

# (list) Permissions
android.permissions = INTERNET

# (bool) Skip byte compile for .py files
android.skip_byte_compile = False

# (str) Format used to package the app for debug
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
