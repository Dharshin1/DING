import os
import hashlib
 
Ding_dir = ".ding"


def init():
    cwd = os.getcwd()
    ding_path = os.path.join(cwd, Ding_dir)
    objects_path = os.path.join(ding_path, "objects")
  
    if os.path.exists(ding_path):
        print("It is already a ding repository")
        return

    os.mkdir(ding_path)
    os.mkdir(objects_path)
    print(f"Initialisied a ding repo in {ding_path}")


def repo_path():
    cwd = os.getcwd()

    while True:
        ding_path = os.path.join(cwd, Ding_dir)

        if os.path.exists(ding_path):
            return cwd

        parent = os.path.dirname(cwd)
        if parent == cwd:
            break
        cwd = parent
    
    return None


def hash_objects(args):
    repo = repo_path()
    if repo is None:
        print("error: not inside a ding repository")
        return
    ding_path = os.path.join(repo, Ding_dir)
        
    objects_path= os.path.join(ding_path, "objects")
    if not os.path.exists(objects_path):
        os.mkdir(objects_path)

    filename = args.file
    try:
        with open(filename, "rb") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"error: file not found: {filename}")
        return

    oid = hashlib.sha256(content).hexdigest()
    print(oid)
    object_file_path = os.path.join(objects_path, oid)
    with open(object_file_path, "wb") as f:
        f.write(content)


