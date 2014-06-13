#!/usr/bin/env python

# The prototype of Phimpme Generator
# To test it, simplely run this file
# The output APK will be put in the working directory

import os, re

def set_name(path, app_name):
    re_str = r'<string name="app_name">.*</string>'
    target_str = '<string name="app_name">' + app_name + '</string>'
    strings_xml = path + "/Phimpme/src/main/res/values/strings.xml"
    
    content = open(strings_xml, 'r').read().encode('utf-8')
    content, count = re.subn(re_str, target_str, content)
    assert(count == 1)
    open(strings_xml, 'w').write(content)

def set_package_name(path, package_name):
    # manifest = path + "/Phimpme/src/main/AndroidManifest.xml"
    pass

def set_logo(path, app_logo):
    pass

def set_enable(path, enables):
    configuration_java = path + "/Phimpme/src/main/java/com/phimpme/phimpme/Configuration.java"
    content = open(configuration_java, 'r').read()
    # Disable all before enabling selected features
    content = re.sub(r'(ENABLE_.*=).*;', r'\1 false;', content)
    for feature in enables:
        # RegEx string, something like "ENABLE_XXX = true;"
        # "\s*" means 0 or more spaces
        # TODO: make sure 'feature' contains only capitals and underlines
        re_str = feature + r"\s*=.*;"
        target_str = feature + " = true;"
        content, count = re.subn(re_str, target_str, content)
        assert(count == 1)
    open(configuration_java, 'w').write(content)

def compile(path):
    gradlew = path + "/gradlew"
    # os.chmod(gradlew, stat.S_IEXEC)
    os.system("chmod 777 " + gradlew)  # TODO: Why os.chmod and chmod +x don't work?
    ret = os.system("cd " + path + " && " + gradlew + " assembleDebug")  # TODO: Change to release
    #os.system("cp " + path + "/Phimpme/build/outputs/apk/*.apk ./")
    return ret, path + "/Phimpme/build/outputs/apk/Phimpme-debug-unaligned.apk"

def copy_project(src_path):
    dest_path = "/tmp/Phimpme"
    os.system("rm -r " + dest_path)
    #import subprocess
    #print subprocess.check_output("cp -r " + src_path + " " + dest_path)
    r = os.system("cp -r " + src_path + " " + dest_path)
    assert(r == 0)
    return dest_path

def generate(app_name, app_logo, enables):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    template_path = "/Users/yzq/Documents/GitHub/phimpme-android/Phimpme"
    path = copy_project(template_path)
    set_name(path, app_name)
    set_logo(path, app_logo)
    set_enable(path, enables)
    return compile(path)

if __name__ == "__main__":
    generate(app_name="YZQ-Phimpme", app_logo=None, enables=['ENABLE_MAP', 'ENABLE_PHOTO_CAPTURING', 'ENABLE_PHOTO_MANIPULATION'])
