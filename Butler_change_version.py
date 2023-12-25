with (open('Butler_version.txt', 'r')) as file:
    version = file.read().split('.')

with (open('Version.txt', 'r')) as file:
    lines = file.readlines()

lines[2] = f"    filevers=({version[0]}, {version[1]}, {version[2]}, 0),\n"
lines[3] = f"    prodvers=({version[0]}, {version[1]}, {version[2]}, 0),\n"
lines[18] = f"        StringStruct(u'FileVersion', u'v{version[0]}.{version[1]}.{version[2]}'),\n"
lines[23] = f"        StringStruct(u'ProductVersion', u'v{version[0]}.{version[1]}.{version[2]}')])\n"

with (open('Version.txt', 'w')) as file:
    file.writelines(lines)
