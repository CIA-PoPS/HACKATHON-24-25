"""
The Library file of the game
"""


import inspect
import dataclasses
import enum
import typing


RESTRICTED_LIB: str = "ModulePlayer"


class Goal(enum.IntEnum):
    """The goal of the stage"""
    MORE = 1
    LESS = 2
    ODD = 3
    EVEN = 4
    BORDER = 5
    FIX = 6
    CLING = 7
    YOU = 8


@dataclasses.dataclass
class Pos:
    """
    A position on the grid
    Attributes:
        w (int): the column
        h (int): the row
    """
    w: int = 0
    h: int = 0

    def __str__(self) -> str:
        return f"({self.w}, {self.h})"


Coord = int | Pos


class Grid:
    """
    The grid of the game

    Attributes:
        __width (const private int): the width of the grid
        __height (const private int): the height of the grid
        __data (private list[bool]): grid but linear

    You can not get or set attributes\n
    But you can get or set items (ex: `grid = Grid(w, h)`):
    - `grid[Pos(x, y)]` is like `grid.__data[x + y * grid.__width]`
    - `grid[x]` is like `grid.__data[x]`
    """
    def __init__(self: "Grid", width: int, height: int, grid: list[bool]) -> None:
        super().__setattr__('__width', width)
        super().__setattr__('__height', height)
        super().__setattr__('__data', grid.copy())

    def __getattribute__(self: "Grid", name: typing.Any) -> None:
        raise Exception("Could not get attribute")

    def __getattr__(self: "Grid", name: typing.Any) -> None:
        raise Exception("Could not get attribute")

    def __setattr__(self: "Grid", name: str, value: typing.Any) -> None:
        stack = inspect.stack()
        for frame in stack:
            module = inspect.getmodule(frame[0])
            if module and module.__name__.startswith(RESTRICTED_LIB):
                raise AttributeError(f"Modification not allowed inside {module.__name__}")

        super().__setattr__(name, value)

    def __delattr__(self: "Grid", name: str) -> None:
        raise Exception("Could not delete attribute")

    def __getitem__(self: "Grid", key: typing.Any) -> bool:
        if not isinstance(key, Coord):
            raise TypeError("Index must be an int or a Pos")

        pos: int = -1
        if isinstance(key, Pos):
            pos = key.w + key.h * super().__getattribute__('__width')
        else:
            pos = key

        if pos < 0 or pos >= (super().__getattribute__('__width') * super().__getattribute__('__height')):
            raise IndexError("Index out of range")
        return super().__getattribute__('__data')[pos]

    def __setitem__(self: "Grid", key: typing.Any, value: typing.Any) -> None:
        if not isinstance(key, Coord):
            raise TypeError("Index must be an int or a Pos")
        if not isinstance(value, bool):
            raise TypeError("Value must be a boolean")

        stack = inspect.stack()
        for frame in stack:
            module = inspect.getmodule(frame[0])
            if module and module.__name__.startswith(RESTRICTED_LIB):
                raise AttributeError(f"Modification not allowed inside {module.__name__}")

        pos: int = -1
        if isinstance(key, Pos):
            pos = key.w + key.h * super().__getattribute__('__width')
        else:
            pos = key

        if pos < 0 or pos >= (super().__getattribute__('__width') * super().__getattribute__('__height')):
            raise IndexError("Index out of range")
        super().__getattribute__('__data')[pos] = value

    def __delitem__(self: "Grid", key: typing.Any) -> None:
        raise Exception("Could not delete item")

    def __len__(self: "Grid") -> int:
        return len(super().__getattribute__('__data'))

    def __contains__(self: "Grid", item: bool) -> bool:
        return item in super().__getattribute__('__data')

    def __iter__(self: "Grid"):
        return iter(super().__getattribute__('__data'))

    def __next__(self: "Grid") -> bool:
        return next(self.__iter__())


class StageData:
    """
    The class for the stage data

    Attributes:
        WIDTH (const int): the width of the grid
        HEIGHT (const int): the height of the grid
        GOAL (const Goal): the goal of the stage
        LAST_GEN (const int): the last generation
        grid (Grid): the grid of the stage
        moves (int): the number of moves
        gen (int): the current generation

    You can not set attributes
    """
    def __init__(self: "StageData", width: int, height: int, goal: int, last_gen: int, grid: list[bool]) -> None:
        self.WIDTH: int = width
        self.HEIGHT: int = height
        self.GOAL: Goal = Goal(goal)
        self.LAST_GEN: int = last_gen
        self.grid: Grid = Grid(width, height, grid)
        self.moves: int = 0
        self.gen: int = 0

    def __setattr__(self: "StageData", name: str, value: typing.Any) -> None:
        stack = inspect.stack()
        for frame in stack:
            module = inspect.getmodule(frame[0])
            if module and module.__name__.startswith(RESTRICTED_LIB):
                raise AttributeError(f"Modification not allowed inside {module.__name__}")

        super().__setattr__(name, value)

    def __delattr__(self: "StageData", name: str) -> None:
        raise Exception("Could not delete attribute")
