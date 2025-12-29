import os

Ding_dir = ".ding"


def init():
    cwd = os.getcwd()
    ding_path = os.path.join(cwd, Ding_dir)

    if os.path.exists(ding_path):
        print("It is already a ding repository")
        return

    os.mkdir(ding_path)
    print(f"Initialisied a ding repo in {ding_path}")
