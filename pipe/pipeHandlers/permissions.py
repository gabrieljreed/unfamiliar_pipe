import os


def set_permissions(path, mode=0o777):
    """Set permissions on a file or directory.
    @param path: The path to the file or directory.
    @param mode: The permissions to set (octal). Defaults to 0777 (rwxrwxrwx)"""

    for root, dirs, files in os.walk(path):
        for dir in dirs:
            try:
                os.chmod(os.path.join(root, dir), mode)
            except Exception as e:
                print(f"Unable to change permissions on folder: {os.path.join(root, dir)}")
                print(e)
        for file in files:
            try:
                os.chmod(os.path.join(root, file), mode)
            except Exception as e:
                print(f"Unable to change permissions on file: {os.path.join(root, dir)}")
                print(e)


def check_permissions(path):
    """Check the permissions on a file or directory.
    @param path: The path to the file or directory.
    @return: The permissions (octal)."""

    return oct(os.stat(path).st_mode)[-3:]
