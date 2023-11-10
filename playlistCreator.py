import os
import threading

def incrementAlphaSmall(x):
    if x == '':
        return 'a'
    if x == 'z':
        x = ord('a')
    else:
        x = ord(x) + 1
    return chr(x)

def incrementAlphaCapital(x):
    if x == '':
        return 'A'
    if x == 'Z':
        x = ord('A')
    else:
        x = ord(x) + 1
    return chr(x)


def decrementAlphaSmall(x):
    if x == '':
        return 'a'
    if x == 'a':
        x = ord('z')
    else:
        x = ord(x) - 1
    return chr(x)


def decrementAlphaCapital(x):
    if x == '':
        return 'A'
    if x == 'A':
        x = ord('Z')
    else:
        x = ord(x) - 1
    return chr(x)

