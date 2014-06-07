#!/usr/bin/env python

# The prototype of Phimpme Generator
# To test it, simplely run this file
# The output APK will be put in the working directory

import os

def set_name(path, app_name):
    raw_str = '<string name="app_name">Phimpme</string>'
    target_str = '<string name="app_name">' + app_name + '</string>'
    strings_xml = path + "/Phimpme/src/main/res/values/strings.xml"

    # Read strings.xml
    file = open(strings_xml, 'r')
    lines = file.readlines()
    file.close()
    
    # Raplace app_name
    for i in range(0, len(lines)):
        lines[i] = lines[i].replace(raw_str, target_str)
        if lines[i].find(target_str) != -1:
            break
    
    # Write back
    file = open(strings_xml, 'w')
    file.writelines(lines)
    file.close()

def set_package_name(path, package_name):
    # manifest = path + "/Phimpme/src/main/AndroidManifest.xml"
    pass

def set_logo(path, app_logo):
    pass

def set_config(path, configs):
    pass

def compile(path):
    gradlew = path + "/gradlew"
    # os.chmod(gradlew, stat.S_IEXEC)
    os.system("chmod 777 " + gradlew)  # TODO: Why os.chmod and chmod +x don't work?
    os.system("cd " + path + " && " + gradlew + " assembleDebug")  # TODO: Change to release
    os.system("cp " + path + "/Phimpme/build/apk/*.apk ./")

def copy_project(src_path):
    dest_path = "/tmp/Phimpme"
    os.system("rm -r " + dest_path)
    r = os.system("cp -r " + src_path + " " + dest_path)
    assert(r == 0)
    return dest_path

def generate(template_path, app_name, app_logo, configs):
    path = copy_project(template_path)
    set_name(path, app_name)
    set_logo(path, app_logo)
    set_config(path, configs)
    compile(path)

if __name__ == "__main__":
    generate(template_path="/Users/yzq/Documents/GitHub/The-Generator/Android/Phimpme",
        app_name="YZQ-Phimpme",
        app_logo=None,
        configs=None)
