import math
from typing import *
import random


def sigmoid(x):
    # if x < -700:
    #     return 0
    return 1 / (1 + math.e ** (-x))
    # try:
    #     return 1 / (1 + math.e ** (-x))
    # except OverflowError:
    #     print("sigmoid函数承受不住了，x：", x)
    #     return 1 if x > 0 else 0


def matrix_mul(m: List[List[float]], v: List[float]):
    """
    列向量v左乘一个矩阵m
    这个过程不会对原有数据进行改变
    :param m:
    :param v:
    :return:
    """
    mH = len(m)
    mW = len(m[0])
    try:
        res = [0] * mH
        for y in range(mH):
            n = 0
            for x in range(mW):
                n += m[y][x] * v[x]
            res[y] = n
    except IndexError:
        print("矩阵乘法出现 IndexError")
        print(mH, mW, len(v))
        exit(0)
    return res


def matrix_trans(m: List[List[float]]):
    """转置一个矩阵并返回一个新的矩阵"""
    mH = len(m)
    mW = len(m[0])
    res = [[0.0] * mH for _ in range(mW)]
    for y in range(mH):
        for x in range(mW):
            res[x][y] = m[y][x]
    return res


def main():
    print(sigmoid(-100.0))
    # a = [
    #     [1, 2, 3],
    #     [4, 5, 6],
    # ]
    # print(matrixTrans(a))

    ...


if __name__ == "__main__":
    main()
