[app]

# (str) Title of your application
title = Paheli Universe

# (str) Package name
package.name = paheliuniverse

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,jpeg,ttf,json

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,pygame

# (int) Android API to use (Target SDK)
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use (Locked to stable r25c release format)
android.ndk = r25c

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

# (str) Format used to package the app for release (apk or aab)
android.release_artifact = apk

# (str) Format used to package the app for debug (apk or aab)
android.debug_artifact = apk

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
