language_exts = {
    "python" :["#","py"],
    "python3" :["#","py"],
    "cpp": ["//","cpp","cc"],
    "java": ["//","java"],
    "golang": ["//","go"],
    "go": ["//","go"],
    "php": ["//","php"],
    "javascript": ["//","js","ts"],
    "js": ["//","js","ts"]
}
def ext2language(ext):
    for key,value in language_exts.items():
        if ext.lower() in value:
            return key
    raise Exception(f"can`t find file extension {ext} for language")


def language2extAndComemnt(language):
    exts = language_exts.get(language.lower())
    if exts and len(exts)>0:
        return exts[1], exts[0]
    raise Exception(f"can`t find language: {language}" )


if __name__ == "__main__":
    print(ext2language("py"))
    print(language2ext("Go"))

