# (list) Application requirements
# Agar aap Pygame use kar rahe hain to 'pygame' likhein, agar Kivy hai to 'kivy' likhein.
requirements = python3,pygame

# (int) Android API to use (Target SDK)
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use (Isse exact r25b/r25c match hoga)
android.ndk = 25.2.9519653

# (int) Android NDK API to use
android.ndk_api = 21

# (bool) Use ccache to speed up compilation
android.ccache = 1

# (list) The Android architectures to build for
# Actions par build fast karne aur size chota rakhne ke liye ye do standard archs sahi hain
android.archs = armeabi-v7a, arm64-v8a

# (bool) Skip byte compile for .py files
android.skip_byte_compile = False

