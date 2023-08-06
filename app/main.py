from app.utils import add


def calc() -> int:
    result = add(10, 10)
    return result


def main():
    calc()
    print("hello my app")


if __name__ == "__main__":
    main()
