def read_file(path,mode):
    if mode == "rb":
        with open(path,mode) as f:
            return f.read()
    else:
        with open(path,mode,encoding = 'utf-8') as f:
            return f.read()
def write_file(path,mode,data):
    if mode == "wb":
        with open(path,mode) as f:
            f.write(data)
    else:
        with open(path,mode,encoding = 'utf-8') as f:
            f.write(data)