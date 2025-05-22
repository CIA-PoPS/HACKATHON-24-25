"""
The module for the display of the game
"""


import tkinter as tk
from os import path
from typing import Any, Iterable, Literal, Generic, TypeVar, Iterator
from enum import IntEnum, StrEnum
from PIL import ImageTk
from dataclasses import dataclass, field
from time import sleep


class Goal(IntEnum):
    """The goal of the stage"""
    MORE = 1
    LESS = 2
    ODD = 3
    EVEN = 4
    BORDER = 5
    FIX = 6
    CLING = 7
    YOU = 8


class Pos:
    """
    A position on the grid
    Attributes:
        x (int): the column
        y (int): the row
    """
    def __init__(self: "Pos", x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    def __str__(self: "Pos") -> str:
        return f"({self.x}, {self.y})"

    def __iter__(self: "Pos") -> Iterator[int]:
        return iter((self.x, self.y))

    def __next__(self: "Pos") -> int:
        return next(self.__iter__())


Coord = int | Pos


class Grid:
    """
    The grid of the game

    Attributes:
        _width (const private int): the width of the grid
        _height (const private int): the height of the grid
        _data (private list[bool]): grid but linear

    You can not get or set attributes\n
    But you can get or set items:
    - `grid[Pos(x, y)]` is like `grid._data[x + y * grid._width]`
    - `grid[x]` is like `grid._data[x]`
    """
    def __init__(self: "Grid", width: int, height: int, grid: list[bool]) -> None:
        self._width = width
        self._height = height
        self._data = grid.copy()

    def __getitem__(self: "Grid", key: Any) -> bool:
        if not isinstance(key, Coord):
            raise TypeError("Index must be an int or a Pos")

        pos: int
        if isinstance(key, Pos):
            pos = key.x + key.y * self._width
        else:
            pos = key

        if pos < 0 or pos >= (self._width * self._height):
            raise IndexError("Index out of range")
        return self._data[pos]

    def __setitem__(self: "Grid", key: Any, value: Any) -> None:
        if not isinstance(key, Coord):
            raise TypeError("Index must be an int or a Pos")
        if not isinstance(value, bool):
            raise TypeError("Value must be a boolean")

        pos: int
        if isinstance(key, Pos):
            pos = key.x + key.y * self._width
        else:
            pos = key

        if pos < 0 or pos >= (self._width * self._height):
            raise IndexError("Index out of range")
        self._data[pos] = value

    def __len__(self: "Grid") -> int:
        return len(self._data)

    def __contains__(self: "Grid", item: bool) -> bool:
        return item in self._data

    def __iter__(self: "Grid") -> Iterator[bool]:
        return iter(self._data)

    def __next__(self: "Grid") -> bool:
        return next(self.__iter__())


class StageData:
    def __init__(self: "StageData", width: int, height: int, goal: int, last_gen: int, grid: list[bool]) -> None:
        self.WIDTH: int = width
        self.HEIGHT: int = height
        self.GOAL: Goal = Goal(goal)
        self.LAST_GEN: int = last_gen
        self.grid: Grid = Grid(width, height, grid)
        self.moves: int = 0
        self.gen: int = 0


class Color(StrEnum):
    """
    An enumeration to represent colors
    """
    WHITE = "white"
    BLACK = "black"
    GRAY = "gray"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    MAROON = "maroon"
    ORANGE = "orange"
    PURPLE = "purple"
    YELLOW = "yellow"
    PINK = "pink"
    LIGHT_BLUE = "light blue"
    LIGHT_GRAY = "light gray"


class Anchor(StrEnum):
    """
    An enumeration to represent the anchor
    """
    CENTER = "center"
    NW = "nw"
    N = "n"
    NE = "ne"
    W = "w"
    E = "e"
    SW = "sw"
    S = "s"
    SE = "se"


class State(IntEnum):
    """
    An enumeration to represent the state
    """
    DEFAULT = 0
    PLAYING = 1
    FORWARDING = 2
    RESETING = 3


class HoverButton(tk.Button):
    """
    A class to represent a button with hover effect
    """
    def __init__(self, master: Any, defaultbg: str = "SystemButtonFace", activebg: str = "SystemButtonFace", **kwargs: Any) -> None:
        tk.Button.__init__(self, master, **kwargs)
        self.defaultbg = defaultbg
        self.activebg = activebg
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.hover = False

    def on_enter(self, e: Any) -> None:
        if self["state"] == "disabled":
            return
        self.hover = True
        self.config(background=self.activebg)

    def on_leave(self, e: Any) -> None:
        self.hover = False
        self.config(background=self.defaultbg)


T = TypeVar("T")


class Param(Generic[T]):
    def __init__(self, value: T) -> None:
        self.__current: T = value
        self.next: T | None = value

    def __call__(self) -> T:
        return self.__current

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.__current}, {self.next})"

    def __repr__(self) -> str:
        return self.__str__()

    def canUpdate(self) -> bool:
        return self.next is not None

    def update(self) -> T:
        if self.next is not None:
            self.__current = self.next
            self.next = None
        return self.__current


class MoreCanvas:
    """
    a canvas with more features
    """
    def __init__(self, parent: "MoreCanvas | None", **kwargs: Any) -> None:
        if parent is not None:
            self.parent = parent
            self._canvas: tk.Canvas = tk.Canvas(self.parent._canvas)

        self.pos: Param[Pos] = Param(kwargs.get("pos", Pos()))
        self.size: Param[Pos] = Param(kwargs.get("size", Pos()))
        self.__anchor: Param[Anchor] = Param(kwargs.get("anchor", Anchor.NW))
        self.__bordermode: Param[Literal['inside', 'outside', 'ignore']] = Param(kwargs.get("bordermode", 'inside'))

        self.bg: Param[Color] = Param(kwargs.get("bg", kwargs.get("background", self.parent.bg() if parent is not None else Color.WHITE)))
        self.__kwargs: dict[str, Param[Any]] = {
            "borderwidth": Param(kwargs.get("borderwidth", 0)),
            "highlightthickness": Param(kwargs.get("highlightthickness", 0)),
            "bg": Param(self.bg().value)
        }

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(pos={self.pos()}, size={self.size()}, anchor={self.__anchor()}, bordermode={self.__bordermode()}, bg={self.bg()}, kwargs={self.__kwargs})"

    def __repr__(self) -> str:
        return self.__str__()

    def __post_init__(self) -> None:
        self.configure()
        self.place()

        for child in self.children():
            child.__post_init__()

    def configure(self, **kwargs: Any) -> None:
        """
        Change options of canvas\n
        Does not update the canvas\n
        Use self.update to update the canvas
        """
        for key, value in kwargs.items():
            if key in ["bg", "background"]:
                if not isinstance(value, Color):
                    continue
                self.bg.next = value
                value = value.value
                key = "bg"

            self.__kwargs[key].next = value

        todo: dict[str, Any] = {key: value.update() for key, value in self.__kwargs.items() if value.canUpdate()}
        self._canvas.configure(**todo)

    def place(self, **kwargs: Any) -> None:
        """
        Place the canvas in the parent
        Change x, y, width, height, anchor and bordermode of canvas\n
        Does not update the canvas\n
        Use self.update to update the canvas
        """
        for key, value in kwargs.items():
            if key == "x":
                if not isinstance(value, int):
                    continue
                if self.pos.next is None:
                    self.pos.next = Pos(value, self.pos().y)
                else:
                    self.pos.next.x = value
            elif key == "y":
                if not isinstance(value, int):
                    continue
                if self.pos.next is None:
                    self.pos.next = Pos(self.pos().x, value)
                else:
                    self.pos.next.y = value

            elif key == "width":
                if not isinstance(value, int):
                    continue
                if self.size.next is None:
                    self.size.next = Pos(value, self.size().y)
                else:
                    self.size.next.x = value
            elif key == "height":
                if not isinstance(value, int):
                    continue
                if self.size.next is None:
                    self.size.next = Pos(self.size().x, value)
                else:
                    self.size.next.y = value

            elif key == "bordermode":
                if value not in ['inside', 'outside', 'ignore']:
                    continue
                self.__bordermode.next = value

            elif key == "anchor":
                if not isinstance(value, Anchor):
                    continue
                self.__anchor.next = value

        todo: dict[str, Any] = {}

        if self.__anchor.canUpdate():
            todo["anchor"] = self.__anchor.update()

        if self.__bordermode.canUpdate():
            todo["bordermode"] = self.__bordermode.update()

        if self.size.canUpdate():
            todo["width"], todo["height"] = self.size.update()

        if self.pos.canUpdate():
            todo["x"], todo["y"] = self.pos.update()

        self._canvas.place_configure(**todo)

    def update(self) -> None:
        """
        Updating the canvas
        """
        self._canvas.update()

        for child in self.children():
            child.update()

    def clear(self) -> None:
        """
        Clearing the canvas
        """
        for child in self.children():
            child.clear()

        self._canvas.delete("all")

    def sizeChanged(self) -> None:
        """
        Called when the size of the canvas has changed\n
        Its purpose is for logic only\n
        It's not to update the canvas
        """
        for child in self.children():
            child.sizeChanged()

    def center(self) -> Pos:
        """
        Return the center of the canvas
        """
        return Pos(self.size().x // 2, self.size().y // 2)

    def children(self) -> Iterable["MoreCanvas"]:
        """
        Return children of the canvas
        """
        return []


class ControlCanvas(MoreCanvas):
    """
    a canvas for the control of the game (play, pause, restart, frame)
    """
    def __init__(self, parent: MoreCanvas) -> None:
        super().__init__(parent, anchor=Anchor.NE)

        self.frame_label: int = self._canvas.create_text(0, 0, anchor=Anchor.W.value, fill=Color.WHITE)
        self.play_btn: HoverButton = HoverButton(self._canvas, command=play, activebg=Color.LIGHT_BLUE)
        self.pause_btn: HoverButton = HoverButton(self._canvas, command=pause, activebg=Color.LIGHT_BLUE)
        self.restart_btn: HoverButton = HoverButton(self._canvas, command=restart, activebg=Color.LIGHT_BLUE)
        self.forward_btn: HoverButton = HoverButton(self._canvas, command=forward, activebg=Color.LIGHT_BLUE)

    def update(self) -> None:
        if DATA.stage is not None:
            self._canvas.itemconfigure(self.frame_label, text=f"Frame: {DATA.stage.gen}")

        if DATA.file is None:
            self.play_btn.configure(state="disabled")
            self.pause_btn.configure(state="disabled")
            self.restart_btn.configure(state="disabled")
            self.forward_btn.configure(state="disabled")
        else:
            status = DATA.status
            self.play_btn.configure(state="normal" if status == State.DEFAULT else "disabled")
            self.pause_btn.configure(state="normal" if status == State.PLAYING else "disabled")
            self.restart_btn.configure(state="normal" if status == State.DEFAULT else "disabled")
            self.forward_btn.configure(state="normal" if status == State.DEFAULT else "disabled")

        super().update()

    def sizeChanged(self) -> None:
        self.place(
            x=self.parent.size().x - 5,
            y=5,
            width=self.parent.size().x - 10,
            height=60
        )

        self._canvas.itemconfigure(self.frame_label, font=DATA.font["LARGE"])
        self._canvas.coords(self.frame_label, 5, 25)
        self.play_btn.configure(image=DATA.photos["play"])
        self.play_btn.place_configure(x=self.size().x - 60, y=5, anchor=Anchor.NE.value, width=50, height=50)
        self.pause_btn.configure(image=DATA.photos["pause"])
        self.pause_btn.place_configure(x=self.size().x - 115, y=5, anchor=Anchor.NE.value, width=50, height=50)
        self.restart_btn.configure(image=DATA.photos["restart"])
        self.restart_btn.place_configure(x=self.size().x - 170, y=5, anchor=Anchor.NE.value, width=50, height=50)
        self.forward_btn.configure(image=DATA.photos["forward"])
        self.forward_btn.place_configure(x=self.size().x - 5, y=5, anchor=Anchor.NE.value, width=50, height=50)

        super().sizeChanged()


class ConfigChoice(MoreCanvas):
    """
    a canvas for a config choice
    """
    def __init__(self, parent: "ConfigCanvas", num: int, text: str, var: tk.StringVar, values: Iterable[int]) -> None:
        super().__init__(parent, anchor=Anchor.SW, bg=Color.GRAY)

        self.num = num

        self.label: int = self._canvas.create_text(0, 0, text=text, anchor=Anchor.W.value)
        self.menu: tk.OptionMenu = tk.OptionMenu(self._canvas, var, *map(str, values))

        self.menu.config(border=0, highlightthickness=0)

    def sizeChanged(self) -> None:
        new_width: int = (self.parent.size().x - 75) // 3
        self.place(
            x=60 + (self.num - 1) * (5 + new_width),
            y=self.parent.size().y - 5,
            width=new_width,
            height=self.parent.size().y - 10
        )

        self._canvas.itemconfig(self.label, font=DATA.font["MEDIUM"])
        self._canvas.coords(self.label, 5, self.size().y // 2)
        self.menu.config(font=DATA.font["SMALL"])
        self.menu.place(x=self.size().x - 5, y=self.size().y // 2, anchor=Anchor.E.value)

        super().sizeChanged()


class ConfigCanvas(MoreCanvas):
    """
    a canvas for the config of the game (cell size, screen width)
    """
    def __init__(self, parent: MoreCanvas) -> None:
        super().__init__(parent, anchor=Anchor.SE)

        self.speed_choice: ConfigChoice = ConfigChoice(self, 1, "Speed", DATA.speed, range(1, 11))
        self.cell_choice: ConfigChoice = ConfigChoice(self, 2, "Cell", DATA.cell, range(1, 16))
        self.width_choice: ConfigChoice = ConfigChoice(self, 3, "Width", DATA.width, [960, 1024, 1280, 1366, 1440, 1536, 1600, 1920, 2560, 3200, 3840])
        self.update_btn: HoverButton = HoverButton(self._canvas, command=configUpdate, activebg=Color.LIGHT_BLUE)

    def sizeChanged(self) -> None:
        self.place(
            x=self.parent.size().x - 5,
            y=self.parent.size().y - 5,
            width=self.parent.size().x - 10,
            height=60
        )

        self.update_btn.configure(image=DATA.photos["check"])
        self.update_btn.place_configure(x=5, y=self.size().y - 5, anchor=Anchor.SW.value, width=50, height=50)

        super().sizeChanged()

    def children(self) -> Iterable[MoreCanvas]:
        return [self.speed_choice, self.cell_choice, self.width_choice]


class StageCanvas(MoreCanvas):
    """
    a canvas for a stage of the game
    """
    def __init__(self, parent: "ScoreCanvas", num: int, name: str, score: int) -> None:
        self.base_bg: Color = Color.GRAY if num % 2 else Color.LIGHT_GRAY
        super().__init__(parent, anchor=Anchor.NE, bg=self.base_bg)

        self.num = num
        self.name = name

        self.name_label: int = self._canvas.create_text(0, 0, text=self.name, anchor=Anchor.W.value)
        self.score_label: int = self._canvas.create_text(0, 0, text=str(score), anchor=Anchor.E.value)

        self._canvas.bind("<Button-1>", self.changeStage)

    def update(self) -> None:
        self.configure(bg=Color.BLUE if DATA.file == self.name else self.base_bg)

        super().update()

    def sizeChanged(self) -> None:
        new_height: int = 40
        self.place(
            x=self.parent.size().x - 5,
            y=new_height * self.num,
            width=self.parent.size().x - 10,
            height=new_height
        )

        self._canvas.itemconfig(self.name_label, font=DATA.font["BASIC"])
        self._canvas.coords(self.name_label, 5, self.size().y // 2)
        self._canvas.itemconfig(self.score_label, font=DATA.font["BASIC"])
        self._canvas.coords(self.score_label, self.size().x - 5, self.size().y // 2)

        super().sizeChanged()

    def changeStage(self, e: Any) -> None:
        changeStage(self.name)


class TotalCanvas(MoreCanvas):
    """
    a canvas for the total score of the game
    """
    def __init__(self, parent: "ScoreCanvas", num: int, score: int) -> None:
        super().__init__(parent, anchor=Anchor.NE)
        self.num = num

        self.name_label: int = self._canvas.create_text(0, 0, text="TOTAL", anchor=Anchor.W.value, fill=Color.WHITE)
        self.score_label: int = self._canvas.create_text(0, 0, text=str(score), anchor=Anchor.E.value, fill=Color.WHITE)

    def sizeChanged(self) -> None:
        new_height: int = 50
        self.place(
            x=self.parent.size().x - 5,
            y=(new_height - 10) * self.num,
            width=self.parent.size().x - 10,
            height=new_height
        )

        self._canvas.itemconfig(self.name_label, font=DATA.font["LARGE"])
        self._canvas.coords(self.name_label, 5, self.size().y // 2)
        self._canvas.itemconfig(self.score_label, font=DATA.font["LARGE"])
        self._canvas.coords(self.score_label, self.size().x - 5, self.size().y // 2)

        super().sizeChanged()


class ScoreCanvas(MoreCanvas):
    """
    a canvas for every stage of the game
    """
    # TODO: Make it scrollable
    def __init__(self, parent: MoreCanvas) -> None:
        super().__init__(parent, anchor=Anchor.NE)

        scores: dict[str, int] = {}
        score_total: int = 0
        with open(f"{DATA.path}/logs/all.log", "r", encoding="iso8859") as f:
            for line in f.readlines():
                if line.startswith("Score "):
                    name, score = line.split()[1:]
                    scores[name[:-1]] = int(score)
                if line.startswith("Total:"):
                    score_total = int(line.split()[1])

        self.stage_label: int = self._canvas.create_text(0, 0, text="Stage", fill=Color.WHITE, anchor=Anchor.NW.value)
        self.score_label: int = self._canvas.create_text(0, 0, text="Score", fill=Color.WHITE, anchor=Anchor.NE.value)
        self.stages: list[StageCanvas] = [StageCanvas(self, i+1, name, scores[name]) for i, name in enumerate(scores)]
        self.total: TotalCanvas = TotalCanvas(self, len(self.stages) + 1, score_total)

    def sizeChanged(self) -> None:
        self.place(
            x=self.parent.size().x - 5,
            y=70,
            width=self.parent.size().x - 10,
            height=self.parent.size().y - 70 * 2
        )

        self._canvas.itemconfig(self.stage_label, font=DATA.font["LARGE"])
        self._canvas.coords(self.stage_label, 5, 0)
        self._canvas.itemconfig(self.score_label, font=DATA.font["LARGE"])
        self._canvas.coords(self.score_label, self.size().x - 5, 0)

        super().sizeChanged()

    def children(self) -> Iterable[MoreCanvas]:
        return [self.total] + [child for child in self.stages]


class RightCanvas(MoreCanvas):
    """
    a canvas for the right part of the game
    """
    def __init__(self, parent: "RootCanvas") -> None:
        super().__init__(parent, anchor=Anchor.NE)

        self.control: ControlCanvas = ControlCanvas(self)
        self.config: ConfigCanvas = ConfigCanvas(self)
        self.score: ScoreCanvas = ScoreCanvas(self)

    def sizeChanged(self) -> None:
        self.place(
            x=self.parent.size().x,
            y=0,
            width=self.parent.size().x * 7 // 16 - 10,
            height=self.parent.size().y
        )

        super().sizeChanged()

    def children(self) -> Iterable[MoreCanvas]:
        return [self.control, self.config, self.score]


class CellCanvas(MoreCanvas):
    def __init__(self, parent: "DisplayCanvas", i: int, j: int) -> None:
        super().__init__(parent, anchor=Anchor.NW, bg=Color.WHITE, borderwidth=0, highlightthickness=0)

        self.i = i
        self.j = j

    def sizeChanged(self) -> None:
        self.place(
            x=self.i * int(DATA.cell.get()),
            y=self.j * int(DATA.cell.get()),
            width=int(DATA.cell.get()),
            height=int(DATA.cell.get())
        )

        super().sizeChanged()


class DisplayCanvas(MoreCanvas):
    # TODO: Make it scrollable
    def __init__(self, parent: "LeftCanvas") -> None:
        super().__init__(parent, bg=Color.BLACK)

        self.bg: Param[Color] = Param(self.parent.parent.bg())

        self.cells: list[CellCanvas] = []

    def updateCells(self) -> None:
        for cell in self.cells:
            cell._canvas.destroy()

        if DATA.stage is not None:
            self.cells = [CellCanvas(self, i, j) for i in range(DATA.stage.WIDTH) for j in range(DATA.stage.HEIGHT) if DATA.stage.grid[Pos(i, j)]]
        else:
            self.cells = []

        super().update()

    def sizeChanged(self) -> None:
        self.place(
            x=5,
            y=5,
            width=self.parent.size().x - 10,
            height=self.parent.size().y - 10
        )

        super().sizeChanged()

    def children(self) -> Iterable[MoreCanvas]:
        return [cell for cell in self.cells]


class LeftCanvas(MoreCanvas):
    def __init__(self, parent: "RootCanvas") -> None:
        super().__init__(parent, bg=Color.GRAY)

        self.display: DisplayCanvas = DisplayCanvas(self)

    def sizeChanged(self) -> None:
        self.place(
            x=5,
            y=5,
            width=self.parent.size().y - 10,
            height=self.parent.size().y - 10
        )

        super().sizeChanged()

    def children(self) -> Iterable[MoreCanvas]:
        return [self.display]


class RootCanvas(MoreCanvas):
    """
    the root canvas of the game
    """
    def __init__(self, parent: tk.Tk, **kwargs: Any) -> None:
        super().__init__(None, **kwargs, bg=Color.BLACK)

        self.parent: tk.Tk = parent
        self._canvas: tk.Canvas = tk.Canvas(parent)

        self.left: LeftCanvas = LeftCanvas(self)
        self.right: RightCanvas = RightCanvas(self)

        self.__post_init__()

    def __post_init__(self) -> None:
        super().__post_init__()

        self.sizeChanged()
        self.update()

    def place(self, **kwargs: Any) -> None:
        if "width" in kwargs and "height" in kwargs:
            self.parent.geometry(f"{kwargs['width']}x{kwargs['height']}")
        elif "width" in kwargs:
            self.parent.geometry(f"{kwargs['width']}x{self.size().y}")
        elif "height" in kwargs:
            self.parent.geometry(f"{self.size().x}x{kwargs['height']}")

        super().place(**kwargs)

    def sizeChanged(self) -> None:
        self.place(
            x=0,
            y=0,
            width=int(DATA.width.get()),
            height=int(DATA.width.get()) * 9 // 16
        )

        super().sizeChanged()

    def children(self) -> Iterable[MoreCanvas]:
        return [self.left, self.right]


@dataclass
class GlobalData:
    path: str = path.dirname(path.abspath(__file__))

    photos: dict[str, ImageTk.PhotoImage] = field(default_factory=dict)
    font: dict[str, str] = field(default_factory=dict)

    file: str | None = None
    stage: "StageData | None" = None
    frames: dict[int, list[int]] = field(default_factory=dict)

    status: State = State.DEFAULT
    speed: tk.StringVar = field(default_factory=tk.StringVar)
    cell: tk.StringVar = field(default_factory=tk.StringVar)
    width: tk.StringVar = field(default_factory=tk.StringVar)

    window: tk.Tk = field(default_factory=tk.Tk)
    root: "RootCanvas | None" = None


def getStageData(src: str) -> tuple[StageData, list[str]]:
    """
    Get the stage data
    """
    lines: list[str]
    with open(f"{DATA.path}/logs/{src}.log", "r", encoding="iso8859") as f:
        lines = f.readlines()

    width, height = map(int, lines[0].split(None, 3)[1:3])
    goal: int = int(lines[1].split(None, 2)[1])
    last_gen: int = int(lines[2].split(None, 2)[1])
    grid: list[bool] = [False] * (width * height)

    for h in range(height):
        line = lines[h + 3].strip()
        for w in range(width):
            grid[w + h * width] = line[w] == 'O'

    return StageData(width, height, Goal(goal), last_gen, grid), lines[height + 4:]


def parseLogsStage(src: str) -> tuple[StageData, dict[int, list[int]]]:
    """
    Parse every moves of the stage and put them in frames
    """
    stage_data, lines = getStageData(src)
    frames: dict[int, list[int]] = {}

    for line in lines:
        if line.startswith("Frame:"):
            frame, *moves = map(int, line.split()[1:])
            frames[frame] = moves

    return stage_data, frames


def countNeighbor(stage: StageData) -> list[list[int]]:
    """Count the number of neighbor that are alive"""
    res: list[list[int]] = [[0]*stage.WIDTH for _ in range(stage.HEIGHT)]
    w: int
    h: int

    for h in range(1, stage.HEIGHT - 1):
        for w in range(1, stage.WIDTH - 1):
            res[h][w] += stage.grid[Pos(w - 1, h - 1)]
            res[h][w] += stage.grid[Pos(w, h - 1)]
            res[h][w] += stage.grid[Pos(w + 1, h - 1)]
            res[h][w] += stage.grid[Pos(w - 1, h)]
            res[h][w] += stage.grid[Pos(w + 1, h)]
            res[h][w] += stage.grid[Pos(w - 1, h + 1)]
            res[h][w] += stage.grid[Pos(w, h + 1)]
            res[h][w] += stage.grid[Pos(w + 1, h + 1)]

    for w in range(1, stage.WIDTH - 1):
        res[0][w] += stage.grid[Pos(w - 1, 0)]
        res[0][w] += stage.grid[Pos(w + 1, 0)]
        res[0][w] += stage.grid[Pos(w - 1, 1)]
        res[0][w] += stage.grid[Pos(w, 1)]
        res[0][w] += stage.grid[Pos(w + 1, 1)]
        res[-1][w] += stage.grid[Pos(w - 1, stage.HEIGHT - 2)]
        res[-1][w] += stage.grid[Pos(w, stage.HEIGHT - 2)]
        res[-1][w] += stage.grid[Pos(w + 1, stage.HEIGHT - 2)]
        res[-1][w] += stage.grid[Pos(w - 1, stage.HEIGHT - 1)]
        res[-1][w] += stage.grid[Pos(w + 1, stage.HEIGHT - 1)]

    for h in range(1, stage.HEIGHT - 1):
        res[h][0] += stage.grid[Pos(0, h - 1)]
        res[h][0] += stage.grid[Pos(1, h - 1)]
        res[h][0] += stage.grid[Pos(1, h)]
        res[h][0] += stage.grid[Pos(1, h + 1)]
        res[h][0] += stage.grid[Pos(0, h + 1)]
        res[h][-1] += stage.grid[Pos(stage.WIDTH - 1, h - 1)]
        res[h][-1] += stage.grid[Pos(stage.WIDTH - 2, h - 1)]
        res[h][-1] += stage.grid[Pos(stage.WIDTH - 2, h)]
        res[h][-1] += stage.grid[Pos(stage.WIDTH - 2, h + 1)]
        res[h][-1] += stage.grid[Pos(stage.WIDTH - 1, h + 1)]

    res[0][0] += stage.grid[Pos(1, 0)]
    res[0][0] += stage.grid[Pos(1, 1)]
    res[0][0] += stage.grid[Pos(0, 1)]

    res[0][-1] += stage.grid[Pos(stage.WIDTH - 2, 0)]
    res[0][-1] += stage.grid[Pos(stage.WIDTH - 2, 1)]
    res[0][-1] += stage.grid[Pos(stage.WIDTH - 1, 1)]

    res[-1][0] += stage.grid[Pos(0, stage.HEIGHT - 2)]
    res[-1][0] += stage.grid[Pos(1, stage.HEIGHT - 2)]
    res[-1][0] += stage.grid[Pos(1, stage.HEIGHT - 1)]

    res[-1][-1] += stage.grid[Pos(stage.WIDTH - 2, stage.HEIGHT - 2)]
    res[-1][-1] += stage.grid[Pos(stage.WIDTH - 1, stage.HEIGHT - 2)]
    res[-1][-1] += stage.grid[Pos(stage.WIDTH - 2, stage.HEIGHT - 1)]

    return res


def actualizeStage(stage: StageData, frames: dict[int, list[int]]) -> None:
    """
    Actualize the stage
    """
    neighbor: list[list[int]] = countNeighbor(stage)

    w: int
    h: int
    pos: int
    cnt: int
    for h in range(stage.HEIGHT):
        for w in range(stage.WIDTH):
            pos = w + h * stage.WIDTH
            cnt = neighbor[h][w]
            stage.grid[pos] = (cnt == 3) or (cnt == 2 and stage.grid[pos])

    if stage.gen in frames:
        for move in frames[stage.gen]:
            stage.grid[move] = not stage.grid[move]

    stage.gen += 1


def play() -> None:
    """
    Play the game
    """
    if DATA.status != State.DEFAULT:
        return

    if DATA.stage is None:
        return

    DATA.status = State.PLAYING

    while DATA.status == State.PLAYING and DATA.stage.gen < DATA.stage.LAST_GEN:
        actualizeStage(DATA.stage, DATA.frames)
        if DATA.root is not None:
            DATA.root.left.display.updateCells()
            DATA.root.left.display.sizeChanged()
            DATA.root.update()
        sleep(1 / int(DATA.speed.get()))

    DATA.status = State.DEFAULT


def pause() -> None:
    """
    Pause the game
    """
    if DATA.status != State.PLAYING:
        return

    DATA.status = State.DEFAULT

    if DATA.root is not None:
        DATA.root.update()


def restart() -> None:
    """
    Restart the game
    """
    if DATA.status != State.DEFAULT:
        return

    DATA.status = State.RESETING

    DATA.file = None
    DATA.stage = None
    DATA.frames = {}

    if DATA.root is not None:
        DATA.root.left.display.updateCells()
        DATA.root.left.display.sizeChanged()

    DATA.status = State.DEFAULT

    if DATA.root is not None:
        DATA.root.update()


def forward() -> None:
    """
    Go to the next frame
    """
    if DATA.status != State.DEFAULT:
        return

    if DATA.stage is None or DATA.stage.gen >= DATA.stage.LAST_GEN:
        return

    DATA.status = State.FORWARDING

    actualizeStage(DATA.stage, DATA.frames)
    if DATA.root is not None:
        DATA.root.left.display.updateCells()
        DATA.root.left.display.sizeChanged()

    DATA.status = State.DEFAULT

    if DATA.root is not None:
        DATA.root.update()


def configUpdate() -> None:
    """
    Update the configuration
    """
    if DATA.status != State.DEFAULT:
        return

    DATA.status = State.RESETING

    if DATA.root is not None:
        DATA.root.sizeChanged()

    DATA.status = State.DEFAULT

    if DATA.root is not None:
        DATA.root.update()


def changeStage(src: str | None) -> None:
    """
    Change the stage
    """
    DATA.status = State.RESETING

    DATA.file = src
    if src is not None and DATA.root is not None:
        DATA.stage, DATA.frames = parseLogsStage(src)
        DATA.root.left.display.updateCells()
        DATA.root.left.display.sizeChanged()

    DATA.status = State.DEFAULT

    if DATA.root is not None:
        DATA.root.update()


def main() -> None:
    """
    Main function
    """
    global DATA

    try:
        del DATA
    except NameError:
        pass
    DATA = GlobalData()

    DATA.font["SMALL"] = "Arial 8"
    DATA.font["BASIC"] = "Arial 12"
    DATA.font["MEDIUM"] = "Arial 16"
    DATA.font["LARGE"] = "Arial 20"
    DATA.photos["play"] = ImageTk.PhotoImage(file=f"{DATA.path}/photos/play.png")
    DATA.photos["pause"] = ImageTk.PhotoImage(file=f"{DATA.path}/photos/pause.png")
    DATA.photos["restart"] = ImageTk.PhotoImage(file=f"{DATA.path}/photos/restart.png")
    DATA.photos["forward"] = ImageTk.PhotoImage(file=f"{DATA.path}/photos/forward.png")
    DATA.photos["check"] = ImageTk.PhotoImage(file=f"{DATA.path}/photos/check.png")
    DATA.speed.set(str(3))
    DATA.cell.set(str(3))
    DATA.width.set(str(1280))

    DATA.window.resizable(False, False)
    DATA.window.title("CIA - Hackathon 24/25 - Game of Life")
    DATA.root = RootCanvas(DATA.window)

    DATA.window.mainloop()


if __name__ == "__main__":
    main()
