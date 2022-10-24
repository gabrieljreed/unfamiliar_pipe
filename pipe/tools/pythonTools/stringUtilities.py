def stripSuffix(string, suffix):
    if string.endswith(suffix):
        return string[:-len(suffix)]
    return string


def stripPrefix(string, prefix):
    if string.startswith(prefix):
        return string[len(prefix):]
    return string
