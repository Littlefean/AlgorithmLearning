from queue import PriorityQueue
from random import randint


def main():
    res3 = func0([1, 2, 3, 4], 10)
    print(res3)
    # for i in range(20):
    #     arr = [randint(1, 100) for _ in range(randint(10, 1000))]
    #     res1 = func1(arr, 100000)
    #     res2 = func2(arr, 100000)
    #     res3 = func0(arr, 100000)
    #     if (res1 == res2 == res3):
    #         ...
    #     else:
    #         print(res1, res2, res3)
    ...


def func0(arr, m):
    # 左程云
    left = 0
    right = min(arr) * m
    t = 0

    near = 0
    while left <= right:
        t = (left + right) // 2

        cover = 0
        for num in arr:
            cover += t // num + 1

        if cover >= m + 1:
            near = t
            right = t - 1
        else:
            left = t + 1
    return near


def func1(arr, m):
    left = -1
    right = min(arr) * m + 1

    # x x x 1 1 1 1 x x x
    while left + 1 != right:
        t = (left + right) // 2

        # 整个系统，t时间内，总共能服务多少人
        ans = 0
        for speed in arr:
            ans += t // speed + 1

        if ans < m:
            # 能服务的人数小于我排队的人数，t太短了，要增大
            left = t
        else:
            # 能服务的人数大于等于我排队的人数，看看有没有更小的
            right = t
    return left + 1  # 总是会小一个


def func2(arr, m):
    # 对数器，用堆的方法实现
    q = PriorityQueue()
    for num in arr:
        q.put((0, num))

    for _ in range(m):
        index, speed = q.get()
        index += speed
        q.put((index, speed))
    # 获取顶部的元素（不弹出）
    top_item = None
    for item in q.queue:
        top_item = item
        break
    return top_item[0]


if __name__ == '__main__':
    main()
