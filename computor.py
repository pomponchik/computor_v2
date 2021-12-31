from srcs.interpretator.interpretator import Interpretator
from srcs.interpretator.console_runner import ConsoleRunner


def main():
    runner = ConsoleRunner(' > ')
    interpretator = Interpretator(runner)
    interpretator.run()


if __name__ == '__main__':
    main()
