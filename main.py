from contextlib import suppress

from src.game import main as main_


def main():
    with suppress((KeyboardInterrupt, EOFError)):
        main_()


if __name__ == '__main__':
    main()
