import argparse
from src import data


def init(args):
    data.init()


def hash_objects(args):
    data.hash_objects(args)

def parse_args():
    parser = argparse.ArgumentParser(prog="ding")

    commands = parser.add_subparsers(dest="command", required=True)

    init_parser = commands.add_parser("init")
    init_parser.set_defaults(func=init)

    hash_parser = commands.add_parser("hash")
    hash_parser.add_argument("file")
    hash_parser.set_defaults(func=hash_objects)


    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
