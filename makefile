.PHONY: lightrunner

lightrunner: main.py
	-buildozer android debug
	adb install -r .buildozer/android/platform/python-for-android-master/Lightrider-*.apk
	adb shell monkey -p org.test.lightrider 1

build:
	-buildozer android debug

upload:
	adb install -r .buildozer/android/platform/python-for-android-master/Lightrider-*.apk

deploy:
	adb install -r .buildozer/android/platform/python-for-android-master/Lightrider-*.apk
	adb shell monkey -p org.test.lightrider 1

run:
	adb shell monkey -p org.test.lightrider 1
	
debug:
	adb shell monkey -p org.test.lightrider 1
	adb logcat | grep "I python"

all:	
	-buildozer android debug
	adb install -r .buildozer/android/platform/python-for-android-master/Lightrider-*.apk
	adb shell monkey -p org.test.lightrider 1
	adb logcat | grep "I python"
