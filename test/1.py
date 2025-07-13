# Keywords & syntax demo (A)

import math
from math import pi as circle_pi

class Example:
    def __init__(self, value: int = 0) -> None:
        self.value = value

    def compute(self) -> float:
        if self.value > 0:
            for i in range(1, 10):
                while i < 5:
                    try:
                        assert i != 3, "Unlucky number"
                        yield i
                        break
                    except AssertionError as e:
                        print(f"Caught: {e}")
                        continue
                    finally:
                        pass
        elif self.value == 0:
            return None
        else:
            raise ValueError("Negative!")

def main():
    e = Example(2)
    result = [x for x in e.compute() if x % 2 == 0]
    print("Results:", result)

    match e.value:
        case 0:
            print("Zero")
        case 1 | 2:
            print("One or Two")
        case _:
            print("Other")

    def inner(*args, **kwargs):
        global x
        nonlocal result
        x = lambda y: y ** 2
        print({k: v for k, v in kwargs.items()})
        return x(args[0]) if args else None

    print(inner(4, key='val'))

if __name__ == "__main__":
    main()


        old_part = sanitize(old_line[i1:i2])
        new_part = sanitize(new_line[j1:j2])