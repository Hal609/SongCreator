import os.path

def _walk(path, depth):
    """Recursively list files and directories up to a certain depth"""
    depth -= 1
    with os.scandir(path) as p:
        for entry in p:
            yield entry.path
            if entry.is_dir() and depth > 0:
                yield from _walk(entry.path, depth)

print("voices = {")
for entry in _walk("./samples/", 2):
   if "." in entry[10:]: continue
   if len(entry[entry.rfind("/")+1:]) > 1:
      if entry[entry.rfind("/")+1:] in ["piano", "drums", "guitar", "bass", "synth"]:
          print(f"],\n'{entry[entry.rfind("/")+1:]}': [")
      else:
         print(f"'{entry[entry.rfind("/")+1:]}',")
print("]\n}")