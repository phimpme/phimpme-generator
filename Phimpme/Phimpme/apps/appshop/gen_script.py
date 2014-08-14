#!/usr/bin/env python

# The prototype of Phimpme Generator
# To test it, simply run this file
# The output APK will be put in the working directory

import os
import re
import shutil
import stat
import sys


def set_name(path, app_name):
	re_str = r'<string name="app_name">.*</string>'
	target_str = r'<string name="app_name">' + app_name + r'</string>'
	strings_xml = path + r"/Phimpme/src/main/res/values/strings.xml"
	content = open(strings_xml, 'r').read().encode('utf-8')
	content, count = re.subn(re_str, target_str, content)
	assert (count == 1)
	open(strings_xml, 'w').write(content)


def set_package_name(path, package_name):
	""" Must be called at last as it changes the path of the Java source code of the app
	"""

	# Replace all "com.phimpme.phimpme" into "com.phimpme."+package_name
	for root, dirs, files in os.walk(path):
		for f in files:
			if f.endswith(".java") or f.endswith(".xml"):
				file_path = os.path.join(root, f)
				content = open(file_path, 'r').read()
				content = content.replace("com.phimpme.phimpme", "com.phimpme." + package_name)
				open(f, 'w').write(content)

	# Move src folder
	if re.match(r"^[a-z0-9]+$", package_name) is None:
		raise Exception("Package name invalid")
	source = os.path.join(path, r"Phimpme/src/main/java/com/phimpme/phimpme")
	destination = os.path.join(path, r"Phimpme/src/main/java/com/phimpme/", package_name)
	if os.path.isdir(destination):
		raise Exception("Package name conflict")
	shutil.move(source, destination)


def set_logo(path, app_logo):
	if app_logo is not None and os.path.isfile(app_logo):
		src_logo_path = os.path.join(path, r"Phimpme/src/main/res/drawable-xxhdpi/ic_launcher.png")
		os.remove(src_logo_path)
		shutil.copy(app_logo, src_logo_path)


def set_enable(path, enables):
	configuration_java = os.path.join(path, r"Phimpme/src/main/java/com/phimpme/phimpme/Configuration.java")
	content = open(configuration_java, 'r').read()
	# Disable all before enabling selected features
	content = re.sub(r'(boolean\s+ENABLE_\s*=).*;', r'\1 false;', content)
	for (feature, value) in enables.items():
		# RegEx string, something like "boolean ENABLE_XXX = true;"
		# "\s*" means 0 or more spaces
		assert (re.match(r"^[A-Z_]*$", feature) is not None)
		if value.isinstanceof(bool):
			value = str(value).lower()
		re_str = feature + r"\s*=.*;"
		target_str = feature + " = " + value + ";"
		content, count = re.subn(re_str, target_str, content)
		assert (count == 1)
	open(configuration_java, 'w').write(content)


def compile_apk(path, output_path):
	gradlew = os.path.join(path, "gradlew")
	os.chmod(gradlew, os.stat(gradlew).st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
	ret = os.system("cd " + path + " && " + gradlew + " assembleRelease")  # TODO: Change to release
	if ret != 0:
		raise Exception("Generation failed")
	shutil.copy(os.path.join(path, r"Phimpme/build/outputs/apk/Phimpme-debug.apk"), output_path)


def copy_project(src_path, order_id):
	dist_path = os.path.join("/tmp/Phimpme/", str(order_id))
	shutil.rmtree(dist_path, ignore_errors=True)
	shutil.copytree(src_path, dist_path)
	return dist_path


def set_background(path, background):
	if background is not None and os.path.isfile(background):
		src_background_path = os.path.join(path, r"Phimpme/src/main/res/drawable-xxhdpi/background.jpg")
		os.remove(src_background_path)
		(src_path_root, src_path_ext) = os.path.splitext(src_background_path)
		(background_root, background_ext) = os.path.splitext(background)
		shutil.copy(background, src_path_root + background_ext)


def generate(order_id, output_path, app_name, app_logo, package_name, enables, background=None):
	"""
	This is the core function of this script
	:param order_id: An identification of orders
	:param output_path: path to put the generated apk
	:param app_name: the name of the Android app
	:param app_logo: the logo of the app, should be in png format
	:param package_name: ONLY THE LAST PART of the full package name "com.phimpme.XXX"
	:param enables: a dict which describes the enabled functions and configurations, as the Configuration.java in the app
	:param background: the background image of the app home screen, if webpage is not selected in enables
	"""
	reload(sys)
	sys.setdefaultencoding('utf-8')
	# TODO: Change it to the path of the source code of Phimp.me Android app
	template_path = r"/Users/yzq/Documents/GitHub/phimpme-android/Phimpme"
	assert (os.path.isdir(template_path))
	path = copy_project(template_path, order_id)
	set_name(path, app_name)
	set_logo(path, app_logo)
	set_background(path, background)
	set_enable(path, enables)
	set_package_name(path, package_name)
	compile_apk(path, output_path)
	shutil.rmtree(path, ignore_errors=True)  # remove temp files


if __name__ == "__main__":
	generate(order_id=0, output_path="./output.apk", app_name="TEST-Phimpme", app_logo=None, package_name="phimpme",
	         enables={'ENABLE_MAP': True, 'ENABLE_PHOTO_CAPTURING': True, 'ENABLE_PHOTO_MANIPULATION': True})
