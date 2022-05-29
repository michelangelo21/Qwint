# Qwint
Adaptation of Gwent game on quantum computer.

![game example](/screenshot-game-example.png)

In order to run this game:
install required libraries
```bash
pip install -r requirements.txt
```
and start playing!
```bash
python qwent.py
```
Enjoy :)

## Problem
We know from our experience that learning about quantum computing might not be so easy-peasy. Besides the technical side of it, you have to understand math, and physics behind it. One of the first essential things one have to master is operating on qubits with quantum logic gates. We wanted to show that the process of learning about quantum logic gates doesn't have to be scary and it can bring joy.

## Our solution
Our goal was to make learning about quantum computing as interesting and enjoyable as possible.  We came up with the idea of quantum card game, in which the cards are quantum logic gates. Rules of our game are pretty much based on very popular card game - [Gwent](https://www.playgwent.com/). Both players operate on the same 6-qubit quantum circuit. Each player starts the game with random set of quantum logic gates. During his turn player can do one of two things:
- use one of his one-, two- or three-qubit gates on chosen set of qubits from circuit
- pass
After both players passed or run out of cards the round ends. Then we measure all 6 qubits from our circuit. If there is more of |0> state qubits measured, player one wins te round and gains 1 point. If there is more of |1> state qubits, second player wins the round, gaining 1 point. If there are as many |0> qubits as |1> (in case of 6 qubits it will be 3:3), round ends with draw and both players get a point.
The circuit is reset, both players draw 5 cards and next round begins.
The game ends when one of the players has 2 points - he wins (if both players have 2 points - it is a tie)


This repo is a project for [Q-munity Hack-Q-Thon](https://www.qmunity.tech/hackqthon).

Authors:
[Michał Łukomski](https://github.com/michelangelo21),
[Jakub Opala](https://github.com/JakubOpala)