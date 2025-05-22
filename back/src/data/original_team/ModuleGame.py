"""
The Main file of the game
"""


import sys
from os import path, makedirs, geteuid, seteuid
from pwd import getpwnam
import signal
import GoLLib
import typing
import numpy


BAD_BUILTINS: dict[str, typing.Any] = {  # Risk Level
    '__name__': __name__,                # Not useful
    '__doc__': __doc__,                  # Not useful
    '__package__': __package__,          # Not useful
    '__loader__': __loader__,            # Not useful
    '__spec__': __spec__,                # Not useful
    '__build_class__': __build_class__,  # Not useful
    'breakpoint': breakpoint,            # medium and useless
    'compile': compile,                  # high and useless
    'delattr': delattr,                  # high
    'eval': eval,                        # high and useless
    'exec': exec,                        # high and useless
    'getattr': getattr,                  # high
    'globals': globals,                  # medium
    'hasattr': hasattr,                  # high
    'input': input,                      # low but useless
    'locals': locals,                    # medium to see if can be enabled
    'print': print,                      # high and useless
    'setattr': setattr,                  # high
    'vars': vars,                        # same as locals()
    'memoryview': memoryview,            # medium
    'open': open                         # high
}
SAFE_BUILTINS: dict[str, typing.Any] = {
    '__import__': None,
    'abs': abs,
    'all': all,
    'any': any,
    'ascii': ascii,
    'bin': bin,
    'callable': callable,
    'chr': chr,
    'dir': dir,
    'divmod': divmod,
    'format': format,
    'hash': hash,
    'hex': hex,
    'id': id,
    'isinstance': isinstance,
    'issubclass': issubclass,
    'iter': iter,
    'aiter': aiter,
    'len': len,
    'max': max,
    'min': min,
    'next': next,
    'anext': anext,
    'oct': oct,
    'ord': ord,
    'pow': pow,
    'repr': repr,
    'round': round,
    'sorted': sorted,
    'sum': sum,
    'None': None,
    'Ellipsis': Ellipsis,
    'NotImplemented': NotImplemented,
    'False': False,
    'True': True,
    'bool': bool,
    'bytearray': bytearray,
    'bytes': bytes,
    'classmethod': classmethod,
    'complex': complex,
    'dict': dict,
    'enumerate': enumerate,
    'filter': filter,
    'float': float,
    'frozenset': frozenset,
    'property': property,
    'int': int,
    'list': list,
    'map': map,
    'object': object,
    'range': range,
    'reversed': reversed,
    'set': set,
    'slice': slice,
    'staticmethod': staticmethod,
    'str': str,
    'super': super,
    'tuple': tuple,
    'type': type,
    'zip': zip,
    '__debug__': __debug__,
    'BaseException': BaseException,
    'BaseExceptionGroup': BaseExceptionGroup,
    'Exception': Exception,
    'GeneratorExit': GeneratorExit,
    'KeyboardInterrupt': KeyboardInterrupt,
    'SystemExit': SystemExit,
    'ArithmeticError': ArithmeticError,
    'AssertionError': AssertionError,
    'AttributeError': AttributeError,
    'BufferError': BufferError,
    'EOFError': EOFError,
    'ImportError': ImportError,
    'LookupError': LookupError,
    'MemoryError': MemoryError,
    'NameError': NameError,
    'OSError': OSError,
    'ReferenceError': ReferenceError,
    'RuntimeError': RuntimeError,
    'StopAsyncIteration': StopAsyncIteration,
    'StopIteration': StopIteration,
    'SyntaxError': SyntaxError,
    'SystemError': SystemError,
    'TypeError': TypeError,
    'ValueError': ValueError,
    'Warning': Warning,
    'FloatingPointError': FloatingPointError,
    'OverflowError': OverflowError,
    'ZeroDivisionError': ZeroDivisionError,
    'BytesWarning': BytesWarning,
    'DeprecationWarning': DeprecationWarning,
    'EncodingWarning': EncodingWarning,
    'FutureWarning': FutureWarning,
    'ImportWarning': ImportWarning,
    'PendingDeprecationWarning': PendingDeprecationWarning,
    'ResourceWarning': ResourceWarning,
    'RuntimeWarning': RuntimeWarning,
    'SyntaxWarning': SyntaxWarning,
    'UnicodeWarning': UnicodeWarning,
    'UserWarning': UserWarning,
    'BlockingIOError': BlockingIOError,
    'ChildProcessError': ChildProcessError,
    'ConnectionError': ConnectionError,
    'FileExistsError': FileExistsError,
    'FileNotFoundError': FileNotFoundError,
    'InterruptedError': InterruptedError,
    'IsADirectoryError': IsADirectoryError,
    'NotADirectoryError': NotADirectoryError,
    'PermissionError': PermissionError,
    'ProcessLookupError': ProcessLookupError,
    'TimeoutError': TimeoutError,
    'IndentationError': IndentationError,
    'IndexError': IndexError,
    'KeyError': KeyError,
    'ModuleNotFoundError': ModuleNotFoundError,
    'NotImplementedError': NotImplementedError,
    'RecursionError': RecursionError,
    'UnboundLocalError': UnboundLocalError,
    'UnicodeError': UnicodeError,
    'BrokenPipeError': BrokenPipeError,
    'ConnectionAbortedError': ConnectionAbortedError,
    'ConnectionRefusedError': ConnectionRefusedError,
    'ConnectionResetError': ConnectionResetError,
    'TabError': TabError,
    'UnicodeDecodeError': UnicodeDecodeError,
    'UnicodeEncodeError': UnicodeEncodeError,
    'UnicodeTranslateError': UnicodeTranslateError,
    'ExceptionGroup': ExceptionGroup,
    'EnvironmentError': EnvironmentError,
    'IOError': IOError,
    'quit': quit,
    'exit': exit,
    'copyright': copyright,
    'credits': credits,
    'license': license,
    'help': help,
    '_': None
}
BASE_USER: int = geteuid()
SAFE_USER: int = getpwnam("player").pw_uid
PATH: str = path.dirname(path.abspath(__file__))


class Guardian:
    """
    The guardian class
    """
    def __enter__(self: "Guardian") -> None:
        seteuid(SAFE_USER)

    def __exit__(self: "Guardian", *args: typing.Any) -> None:
        seteuid(BASE_USER)


with Guardian():
    import ModulePlayer
ModulePlayer.__builtins__ = SAFE_BUILTINS


def countNeighbor(stage: GoLLib.StageData) -> list[list[int]]:
    """Count the number of neighbor that are alive"""
    res: list[list[int]] = [[0]*stage.WIDTH for _ in range(stage.HEIGHT)]
    w: int
    h: int

    for h in range(1, stage.HEIGHT - 1):
        for w in range(1, stage.WIDTH - 1):
            if not stage.grid[w + stage.WIDTH * h]:
                continue
            res[h - 1][w - 1] += 1
            res[h - 1][w] += 1
            res[h - 1][w + 1] += 1
            res[h][w - 1] += 1
            res[h][w + 1] += 1
            res[h + 1][w - 1] += 1
            res[h + 1][w] += 1
            res[h + 1][w + 1] += 1

    for w in range(1, stage.WIDTH - 1):
        if stage.grid[w]:
            res[0][w - 1] += 1
            res[0][w + 1] += 1
            res[1][w - 1] += 1
            res[1][w] += 1
            res[1][w + 1] += 1
        if stage.grid[w + stage.WIDTH * (stage.HEIGHT - 1)]:
            res[-1][w - 1] += 1
            res[-1][w + 1] += 1
            res[-2][w - 1] += 1
            res[-2][w] += 1
            res[-2][w + 1] += 1

    for h in range(1, stage.HEIGHT - 1):
        if stage.grid[stage.WIDTH * h]:
            res[h - 1][0] += 1
            res[h + 1][0] += 1
            res[h - 1][1] += 1
            res[h][1] += 1
            res[h + 1][1] += 1
        if stage.grid[stage.WIDTH - 1 + stage.WIDTH * h]:
            res[h - 1][-1] += 1
            res[h + 1][-1] += 1
            res[h - 1][-2] += 1
            res[h][-2] += 1
            res[h + 1][-2] += 1

    if stage.grid[0]:
        res[0][1] += 1
        res[1][0] += 1
        res[1][1] += 1
    if stage.grid[stage.WIDTH - 1]:
        res[0][-2] += 1
        res[1][-1] += 1
        res[1][-2] += 1
    if stage.grid[stage.WIDTH * (stage.HEIGHT - 1)]:
        res[-1][1] += 1
        res[-2][0] += 1
        res[-2][1] += 1
    if stage.grid[stage.WIDTH * stage.HEIGHT - 1]:
        res[-1][-2] += 1
        res[-2][-1] += 1
        res[-2][-2] += 1

    return res


def updateNeighbor(neighbor: list[list[int]], w: int, h: int) -> None:
    change: int = 1 if not neighbor[h][w] else -1

    if h > 0 and w > 0:
        neighbor[h - 1][w - 1] += change
    if h > 0:
        neighbor[h - 1][w] += change
    if h > 0 and w < len(neighbor[h]) - 1:
        neighbor[h - 1][w + 1] += change
    if w > 0:
        neighbor[h][w - 1] += change
    if w < len(neighbor[h]) - 1:
        neighbor[h][w + 1] += change
    if h < len(neighbor) - 1 and w > 0:
        neighbor[h + 1][w - 1] += change
    if h < len(neighbor) - 1:
        neighbor[h + 1][w] += change
    if h < len(neighbor) - 1 and w < len(neighbor[h]) - 1:
        neighbor[h + 1][w + 1] += change


def actualizeStage(stage: GoLLib.StageData, neighbor: list[list[int]]) -> None:
    """
    Actualize the stage
    """
    w: int
    h: int
    pos: int
    cnt: int
    for h in range(stage.HEIGHT):
        for w in range(stage.WIDTH):
            pos = w + h * stage.WIDTH
            cnt = neighbor[h][w]
            if stage.grid[pos] and cnt != 2 and cnt != 3:
                stage.grid[pos] = False
                updateNeighbor(neighbor, w, h)
            elif not stage.grid[pos] and cnt == 3:
                stage.grid[pos] = True
                updateNeighbor(neighbor, w, h)


def handleTimeout(*args: typing.Any) -> None:
    raise TimeoutError()


def callPlayer(stage: GoLLib.StageData, neighbor: list[list[int]], log_file: str) -> None:
    """
    Call the player properly
    """
    player_action: list[GoLLib.Coord] = []
    try:
        with Guardian():
            signal.signal(signal.SIGALRM, handleTimeout)
            signal.alarm(5)
            ModulePlayer.play(stage, player_action)
            signal.alarm(0)
    except Exception as e:
        print(e)

    with open(log_file, "a", encoding="iso8859") as f:
        f.write(f"Frame: {stage.gen}")
        for pos in player_action[:stage.moves]:
            if stage.moves <= 0:
                break
            if isinstance(pos, GoLLib.Pos):
                pos = pos.w + pos.h * stage.WIDTH
            if pos < 0 or pos >= stage.WIDTH * stage.HEIGHT:
                continue
            stage.grid[pos] = not stage.grid[pos]
            stage.moves -= 1
            updateNeighbor(neighbor, pos % stage.WIDTH, pos // stage.WIDTH)
            f.write(f" {pos}")
        f.write("\n")


def actualizeMoves(stage: GoLLib.StageData) -> int:
    """
    Actualize the moves
    """
    match stage.GOAL:
        case GoLLib.Goal.MORE | GoLLib.Goal.LESS:
            return (500 * 500) if (stage.gen >= stage.LAST_GEN - 5) else (stage.moves // 2 + 5)
        case GoLLib.Goal.ODD | GoLLib.Goal.EVEN:
            return (500 * 500 // 2) if (stage.gen >= stage.LAST_GEN - 5) else (stage.moves // 2 + 3)
        case GoLLib.Goal.BORDER:
            return (500 + 500 + 500 + 500) if (stage.gen >= stage.LAST_GEN - 5) else (15)
        case GoLLib.Goal.FIX | GoLLib.Goal.CLING:
            return 30
        case GoLLib.Goal.YOU:
            return 30


def getStageData(file: str, log_file: str) -> GoLLib.StageData:
    """
    Get the stage data
    """
    lines: list[str]
    with open(file, "r", encoding="iso8859") as f:
        lines = f.readlines()

    with open(log_file, "w", encoding="iso8859") as log:
        log.write("")
        for line in lines:
            log.write(line)
        log.write("---------------------------------\n")

    width, height = map(int, lines[0].split(None, 3)[1:3])
    goal: int = int(lines[1].split(None, 2)[1])
    last_gen: int = int(lines[2].split(None, 2)[1])
    grid: list[bool] = [False] * (width * height)

    for h in range(height):
        line = lines[h + 3].strip()
        for w in range(width):
            grid[w + h * width] = line[w] == 'O'

    return GoLLib.StageData(width, height, GoLLib.Goal(goal), last_gen, grid)


def maximumBorder(stage: GoLLib.StageData) -> int:
    res: int = 0
    for i in range(5):
        res += (5 - i) * 2 * ((stage.WIDTH - 2 * i) + (stage.HEIGHT - 2 * i) - 2)
    return res


def calculateBorder(stage: GoLLib.StageData) -> float:
    percent: float = 0
    for i in range(5):
        for w in range(i, stage.WIDTH - i):
            percent += (5 - i) * stage.grid[w + i * stage.WIDTH]
            percent += (5 - i) * stage.grid[w + (stage.HEIGHT - i - 1) * stage.WIDTH]
        for h in range(i + 1, stage.HEIGHT - i - 1):
            percent += (5 - i) * stage.grid[i + h * stage.WIDTH]
            percent += (5 - i) * stage.grid[stage.WIDTH - i - 1 + h * stage.WIDTH]
    percent /= maximumBorder(stage)
    return percent


def maximumFix(stage: GoLLib.StageData) -> int:
    return (1 + (stage.WIDTH - 4) // 3 + ((stage.WIDTH - 4) % 3 == 2)) * (1 + (stage.HEIGHT - 4) // 3 + ((stage.HEIGHT - 4) % 3 == 2))


def calculateFix(stage: GoLLib.StageData) -> float:
    data_array = numpy.zeros((stage.HEIGHT + 2, stage.WIDTH + 2), dtype=bool)
    data_array[1:-1, 1:-1] = numpy.array([stage.grid[w + h * stage.WIDTH] for w in range(stage.WIDTH) for h in range(stage.HEIGHT)]).reshape((stage.HEIGHT, stage.WIDTH))
    patern_array = numpy.zeros((4, 4), dtype=bool)
    patern_array[1:-1, 1:-1] = numpy.ones((2, 2), dtype=bool)

    data_rows, data_cols = data_array.shape
    patern_rows, patern_cols = patern_array.shape

    percent: float = 0

    for i in range(data_rows - patern_rows + 1):
        for j in range(data_cols - patern_cols + 1):
            if numpy.array_equal(data_array[j:j + patern_cols, i:i + patern_rows], patern_array):
                percent += 1

    percent /= maximumFix(stage)
    return percent


def maximumCling(stage: GoLLib.StageData) -> int:
    return (1 + (stage.WIDTH - 5) // 4 + ((stage.WIDTH - 5) % 4 == 3)) * (1 + (stage.HEIGHT - 5) // 4 + ((stage.HEIGHT - 5) % 4 == 3))


def calculateCling(stage: GoLLib.StageData) -> float:
    data_array = numpy.zeros((stage.HEIGHT + 2, stage.WIDTH + 2), dtype=bool)
    data_array[1:-1, 1:-1] = numpy.array([stage.grid[w + h * stage.WIDTH] for w in range(stage.WIDTH) for h in range(stage.HEIGHT)]).reshape((stage.HEIGHT, stage.WIDTH))
    patern_array_1 = numpy.array([
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, True, True, True, False],
        [False, False, False, False, False],
        [False, False, False, False, False]
    ], dtype=bool)
    patern_array_2 = numpy.array([
        [False, False, False, False, False],
        [False, False, True, False, False],
        [False, False, True, False, False],
        [False, False, True, False, False],
        [False, False, False, False, False]
    ], dtype=bool)

    data_rows, data_cols = data_array.shape
    patern_rows, patern_cols = patern_array_1.shape

    percent: float = 0

    for i in range(data_rows - patern_rows + 1):
        for j in range(data_cols - patern_cols + 1):
            if numpy.array_equal(data_array[j:j + patern_cols, i:i + patern_rows], patern_array_1):
                percent += 1
            elif numpy.array_equal(data_array[j:j + patern_cols, i:i + patern_rows], patern_array_2):
                percent += 1

    percent /= maximumFix(stage)
    return percent


def calculateResult(stage: GoLLib.StageData) -> int:
    percent: float
    match stage.GOAL:
        case GoLLib.Goal.MORE | GoLLib.Goal.LESS:
            percent = sum(stage.grid) if (stage.GOAL == GoLLib.Goal.MORE) else (stage.WIDTH * stage.HEIGHT - sum(stage.grid))
            percent /= (stage.WIDTH * stage.HEIGHT)
        case GoLLib.Goal.ODD | GoLLib.Goal.EVEN:
            percent = sum(v for i, v in enumerate(stage.grid) if ((i % 2) == (stage.GOAL == GoLLib.Goal.ODD)))
            percent *= 2
            percent /= (stage.WIDTH * stage.HEIGHT)
        case GoLLib.Goal.BORDER: percent = calculateBorder(stage)
        case GoLLib.Goal.FIX:    percent = calculateFix(stage)
        case GoLLib.Goal.CLING:  percent = calculateCling(stage)
        case GoLLib.Goal.YOU:    percent = 0
    res: int = round(percent * 1_000_000)
    return res


def main(stages: list[int]) -> None:
    """
    The main function of the game
    """
    stage_dir: str = f"{PATH}/stages"
    logs_dir: str = f"{PATH}/logs"
    all_logs_file: str = f"{logs_dir}/all.log"

    makedirs(logs_dir, mode=755, exist_ok=True)
    with open(all_logs_file, "w", encoding="iso8859") as file:
        file.write("")

    result: int = 0

    file_name: str
    log_file: str
    stage: GoLLib.StageData
    neighbor: list[list[int]]
    res_tmp: int
    for stage_id in stages:
        file_name = GoLLib.Goal(stage_id).name.lower()
        file_path = path.join(stage_dir, file_name + ".in")
        log_file = path.join(logs_dir, file_name + ".log")

        if not path.isfile(file_path):
            continue

        stage = getStageData(file_path, log_file)
        neighbor = countNeighbor(stage)

        while stage.gen < stage.LAST_GEN:
            actualizeStage(stage, neighbor)
            callPlayer(stage, neighbor, log_file)
            stage.moves = actualizeMoves(stage)
            stage.gen += 1

        res_tmp = calculateResult(stage)
        with open(all_logs_file, "a", encoding="iso8859") as file:
            file.write(f"Score {file_name}: {res_tmp}\n")
        result += res_tmp

    with open(all_logs_file, "a", encoding="iso8859") as file:
        file.write(f"Total: {result}\n")


if __name__ == "__main__":
    main(list(map(int, sys.argv[1:])))
