"""
The main file of the game
"""


import sys
from os import path, makedirs, remove
from shutil import copy, copytree, rmtree
from subprocess import Popen, PIPE, STDOUT
from enum import Enum
from random import randint, random
from collections import defaultdict


PATH: str = path.dirname(path.abspath(__file__))
BANNED_WORDS: list[str] = [
    'breakpoint',
    'compile'
    'delattr',
    'eval',
    'exec',
    'getattr',
    'globals',
    'hasattr',
    'input',
    'locals',
    'print',
    'setattr',
    'vars',
    'memoryview',
    'open',
    '__name__',
    '__doc__',
    '__package__',
    '__loader__',
    '__spec__',
    '__annotations__',
    '__file__',
    '__cached__',
    '__build_class__',
    'import',
    'builtins'
]


def sanatizeLine(line: str) -> bool:
    """
    """
    finded: defaultdict[str, int] = defaultdict(int)
    for c in line:
        for word in BANNED_WORDS:
            if word[finded[word]] == c:
                finded[word] += 1
                if finded[word] >= len(word):
                    return True
            else:
                finded[word] = 0
    return False


def initEnvironement(team_id: int, root: str) -> None:
    """
    """
    src: str = f"{root}/tmp/{team_id}.py"
    dst: str = f"{root}/teams/{team_id}"

    if not path.isfile(src):
        raise FileNotFoundError(src)

    makedirs(dst, mode=755, exist_ok=True)
    copytree(f"{root}/original_team", dst, dirs_exist_ok=True)

    lines: list[str]
    with open(src, "r", encoding="iso8859") as file:
        lines = file.readlines()
    with open(f"{dst}/ModulePlayer.py", "w", encoding="iso8859") as file:
        file.write("import GoLLib, types, typing, collections, functools, itertools, dataclasses, enum, time, random, math, cmath, heapq, bisect, array, decimal, fractions, statistics, numpy, sympy, networkx, sortedcontainers\n")
        for line in lines:
            if sanatizeLine(line):
                continue
            file.write(line)

    try:
        remove(src)
    except OSError:
        pass


class Stages(Enum):
    """
    """
    MORE = 1
    LESS = 2
    ODD = 3
    EVEN = 4
    BORDER = 5
    FIX = 6
    CLING = 7


def generateStage(dst: str, stages: tuple[str, ...]) -> None:
    """
    """
    return
    makedirs(dst, mode=755, exist_ok=True)

    for stage_id in map(int, stages):
        stage: Stages = Stages(stage_id)
        width: int = 500
        height: int = 500
        gen: int = 100

        grid: list[list[int]] = [[random() < 0.3 for _ in range(width)] for _ in range(height)]
        res = ""
        for row in grid:
            for cell in row:
                res += "O" if cell else "."
            res += "\n"

        with open(f"{dst}/{stage.name.lower()}.in", "w", encoding="iso8859") as file:
            file.write(f"Dimension: {width} {height}\n")
            file.write(f"Goal: {stage.value}\n")
            file.write(f"Generation: {gen}\n")
            file.write(res)


def callInsideDocker(team_id: int, root: str, stages: tuple[str, ...]) -> None:
    """
    """
    dst: str = f"{root}/teams/{team_id}"
    if not path.isdir(dst):
        raise NotADirectoryError(dst)

    process = Popen(
        f"docker run --rm --cap-drop ALL --cap-add SETUID --security-opt no-new-privileges --network none --cpus=1 -v {dst}:/app -e STAGES='{' '.join(stages)}' secure-python-runner",
        shell=True,
        stdout=PIPE,
        stderr=STDOUT,
        encoding="iso8859",
        errors="ignore"
    )

    try:
        output, _ = process.communicate()
        with open(f"{root}/logs/{team_id}.log", "w", encoding="iso8859") as log_file:
            log_file.write(output)
    except Exception as e:
        process.kill()
        raise e


def closeEnvironement(team_id: int, root: str) -> None:
    """
    """
    src: str = f"{root}/teams/{team_id}"
    dst: str = f"{root}/logs/{team_id}"

    if not path.isdir(src):
        raise NotADirectoryError(src)

    makedirs(dst, mode=755, exist_ok=True)
    copy(f"{src}/ModulePlayer.py", dst + ".py")
    copytree(f"{src}/logs", dst, dirs_exist_ok=True)

    result: str = "["
    with open(f"{dst}/logs/all.log", "r", encoding="iso8859") as file:
        for line in file.readlines():
            _, stage_name, score, *_ = line.split()
            stage_name = stage_name[:-1]
            result += "{" + f"stage_name: {stage_name}:, score: {score}" + "},"
    result = result[:-1]
    result += "]"
    print(result)

    try:
        rmtree(src)
    except OSError as e:
        print(e)


def main(team_id: int, root: str, *stages: str) -> None:
    """
    The main function for executing the game for a team
    Parameters:
        team_id (int): The id of the team
        root (str): The path to the root folder
    """
    initEnvironement(team_id, root)
    generateStage(f"{root}/teams/{team_id}/stages", stages)
    callInsideDocker(team_id, root, stages)
    closeEnvironement(team_id, root)


if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2], *sys.argv[3:])
