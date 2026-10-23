# Atlas-10 APK — build notes

App: "Atlas-10" (`org.atlas10.app`), single Activity with a full-screen
WebView loading `file:///android_asset/atlas10_mobile.html` (the mobile
variant of the Atlas-10 constellation browser, bundled in
`app/src/main/assets/`). Works fully offline. minSdk 24, targetSdk 34,
versionCode 1 / versionName 1.0.

Built 2026-10-09 with the raw-SDK-tools pipeline documented in
~/workspace/lemma-db/_apk/android/BUILD_NOTES.md (javac → d8 → aapt2 →
zipalign → apksigner; JDK ~/jdk/jdk-17.0.11+9, SDK ~/android-sdk;
Gradle cannot start on this VM).

Fresh debug keystore for THIS app (do NOT reuse the lemma one):
_atlas10/_apk/debug-atlas10.keystore_ (kept outside build/ so `rm -rf build`
cannot wipe it). storepass/keypass: android, alias androiddebugkey.

Rebuild: copy the command sequence from the lemma BUILD_NOTES.md, replacing
paths/package/asset names, signing with ../debug-atlas10.keystore and
outputting ../atlas10-debug.apk.

Install (sideload): debug-signed — Android will warn about an unknown
developer (expected). Uninstall any older Atlas-10 build first if the
signature changed. No network needed.
