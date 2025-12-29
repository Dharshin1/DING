import argparse
from src import data


def init(args):
    data.init()


def parse_args():
    parser = argparse.ArgumentParser(prog="ding")

    commands = parser.add_subparsers(dest="command", required=True)

    init_parser = commands.add_parser("init")
    init_parser.set_defaults(func=init)

    return parser.parse_args()


def main():
    print("Ding Dong, who's there \nThe IRS \nOh Shit")


if __name__ == "__main__":
    main()
