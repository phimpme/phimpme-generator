#!/usr/bin/env python

# The prototype of Phimpme Generator
# To test it, simplely run this file
# The output APK will be put in the working directory

import os
import re
import shutil
import stat
import sys


def set_name(path, app_name):
	re_str = r'<string name="app_name">.*</string>'
	target_str = '<string name="app_name">' + app_name + '</string>'
	strings_xml = path + "/Phimpme/src/main/res/values/strings.xml"
	content = open(strings_xml, 'r').read().encode('utf-8')
	content, count = re.subn(re_str, target_str, content)
	assert (count == 1)
	open(strings_xml, 'w').write(content)


def set_package_name(path, package_name):
	""" Must be called at last
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
	source = os.path.join(path, "Phimpme/src/main/java/com/phimpme/phimpme")
	destination = os.path.join(path, "Phimpme/src/main/java/com/phimpme/", package_name)
	if os.path.isdir(destination):
		raise Exception("Package name conflict")
	shutil.move(source, destination)


def set_logo(path, app_logo):
	if app_logo != None and os.path.isfile(app_logo):
		src_logo_path = os.path.join(path, "Phimpme/src/main/res/drawable-xxhdpi/ic_launcher.png")
		shutil.copy(app_logo, src_logo_path)


def set_enable(path, enables):
	configuration_java = os.path.join(path, "Phimpme/src/main/java/com/phimpme/phimpme/Configuration.java")
	content = open(configuration_java, 'r').read()
	# Disable all before enabling selected features
	content = re.sub(r'(ENABLE_.*=).*;', r'\1 false;', content)
	for feature in enables:
		# RegEx string, something like "ENABLE_XXX = true;"
		# "\s*" means 0 or more spaces
		# TODO: make sure 'feature' contains only capitals and underlines
		re_str = feature + r"\s*=.*;"
		target_str = feature + " = true;"
		print(feature)
		content, count = re.subn(re_str, target_str, content)
		assert (count == 1)
	open(configuration_java, 'w').write(content)


def compile_apk(path, output_path):
	gradlew = os.path.join(path, "gradlew")
	os.chmod(gradlew, os.stat(gradlew).st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
	ret = os.system("cd " + path + " && " + gradlew + " assembleRelease")  # TODO: Change to release
	if ret != 0:
		raise Exception("Generation failed")
	shutil.copy(os.path.join(path, "Phimpme/build/outputs/apk/Phimpme-debug.apk"), output_path)


def copy_project(src_path, order_id):
	assert (isinstance(order_id, int))
	dest_path = os.path.join("/tmp/Phimpme/", str(order_id))
	shutil.rmtree(dest_path, ignore_errors=True)
	shutil.copytree(src_path, dest_path)
	return dest_path


def generate(order_id, output_path, app_name, app_logo, package_name, enables):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	# TODO: Change it to the path of the source code of Phimp.me Android app
	template_path = "/Users/yzq/Documents/GitHub/phimpme-android/Phimpme"
	assert (os.path.isdir(template_path))
	path = copy_project(template_path, order_id)
	set_name(path, app_name)
	set_logo(path, app_logo)
	set_enable(path, enables)
	set_package_name(path, package_name)
	compile_apk(path, output_path)
	shutil.rmtree(path, ignore_errors=True)  # remove temp files


if __name__ == "__main__":
	generate(order_id=0, output_path="./output.apk", app_name="TEST-Phimpme", app_logo=None, package_name="phimpme",
	         enables=['ENABLE_MAP', 'ENABLE_PHOTO_CAPTURING', 'ENABLE_PHOTO_MANIPULATION'])
