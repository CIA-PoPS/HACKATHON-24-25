import React, { useContext, useEffect } from 'react';
import { GlobalContextProvider, globalContext, dataURL } from '../../script/Values';
import ReactMarkdown from "react-markdown";
import '../../styles/Doc.css';

const markdownText = `
# Documentation

## Introduction

Pour ce hackathon, vous devrez coder une IA capable de jouer au jeu de la vie selon un certain objectif.

## Le jeu de la vie

Le jeu de la vie est un automate cellulaire imaginé par John Conway en 1970.\n
Il se joue sur une grille de cellules carrées, chacune ayant 8 voisins (horizontaux, verticaux et diagonaux).\n
Chaque cellule est soit vivante, soit morte.\n
Le jeu se déroule en générations successives, où chaque génération est déterminée par la précédente.\n
L'état suivant d'une cellule est : (S = 3) OU (E = 1 ET S = 2).\n
Avec :
- S : nombre actuel de cellules vivantes dans son voisinage (entier naturel compris entre 0 et 8 inclus) ;
- E : état actuel de la cellule (entier naturel égal à 0 pour une cellule morte et égal à 1 pour une cellule vivante).

## Objectif

C'est à vous de réussir à trouver l'objectif cacher derrière chaque partie.\n
Cependant, vous aurez des indices pour vous aider à trouver l'objectif.\n
Votre IA devra être capable de jouer au jeu de la vie en respectant l'objectif donné.\n
Après un certain temps, nous vous donnerons un indice pour vous aider à trouver l'objectif.\n


## Règles

- Vous avez le droit de coder en Python uniquement.
- Vous avez le droit d'utiliser des librairies externes, celle-ci sont importées automatiquement (comme si vous aviez fait \`import math\`).
- les librairies suivantes sont automatiquement importées (si vous en voulez d'autres, demandez-nous) :
  - GoLLib (librairie du jeu de la vie)
  - \`types\`
  - \`typing\`
  - \`collections\`
  - \`functools\`
  - \`itertools\`
  - \`dataclasses\`
  - \`enum\`
  - \`time\`
  - \`random\`
  - \`math\`
  - \`cmath\`
  - \`heapq\`
  - \`bisect\`
  - \`array\`
  - \`decimal\`
  - \`fractions\`
  - \`statistics\`
  - \`numpy\`
  - \`sympy\`
  - \`networkx\`
  - \`sortedcontainers\`
- Votre code est importé dans un environnement sécurisé, vous ne pouvez pas accéder à internet.
- Votre code n'est importé qu'une seule fois, puis une fonction nommée \`play\` est appelée avec un argument \`stage\` de type \`GoLLib.StageData\` et un autre \`played\` de type \`list[GoLLib.Coord]\`, ce dernier étant la valeur a modifié pour interagir avec le jeu.
- Vous ne pouvez pas modifier l'argument \`stage\` de la fonction \`play\`.
- Tous les built-ins de Python sont autorisés, sauf les suivants :
  - \`breakpoint\`
  - \`compile\`
  - \`delattr\`
  - \`eval\`
  - \`exec\`
  - \`getattr\`
  - \`globals\`
  - \`hasattr\`
  - \`input\`
  - \`locals\`
  - \`print\`
  - \`setattr\`
  - \`vars\`
  - \`memoryview\`
  - \`open\`
- Si une ligne dans votre code contient l'une de ces chaînes de caractères, la ligne en qustion sera supprimée :
  - \`breakpoint\`
  - \`compil\`
  - \`delattr\`
  - \`eval\`
  - \`exec\`
  - \`getattr\`
  - \`globals\`
  - \`hasattr\`
  - \`input\`
  - \`locals\`
  - \`print\`
  - \`setattr\`
  - \`vars\`
  - \`memoryview\`
  - \`open\`
  - \`__name__\`
  - \`__doc__\`
  - \`__package__\`
  - \`__loader__\`
  - \`__spec__\`
  - \`__annotations__\`
  - \`__file__\`
  - \`__cached__\`
  - \`__build_class__\`
  - \`import\`
  - \`builtins\`

## Librairie GoLLib et affichage du jeu de la vie

Vous pouvez retrouver la librairie GoLLib ainsi qu'un module pour afficher le jeu de la vie sur le lien suivant :
[GoLLib & ModuleDisplay](https://bde-pops.github.io/VPS-DATA/cia/hackathon/)

## Exemple de code
\`\`\`
"""
The module for the player
"""


def play(stage: GoLLib.StageData, played: list[GoLLib.Coord]) -> None:
    """
    The function to play the game
    You must return a list of Coord for cells to edit (-1 for no cell)

    Args:
        stage (StageData): the stage to play
        played (list[Coord]): the list of cells to swap
    """
    # TODO: Implement your AI here
\`\`\`
`;

const Code: React.FC = () => {
    const context: GlobalContextProvider = useContext(globalContext);

    useEffect(() => {
        if (context.dev) console.log('Rendering Docu');
    });

    return (
        <section className='submit'>
            <div className='container markdown'>
                <ReactMarkdown children={markdownText}/>
            </div>
        </section>
    );
};

export default Code;
