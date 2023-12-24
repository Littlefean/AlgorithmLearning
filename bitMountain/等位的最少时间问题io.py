def main():
    N = input()
    arr = list(map(int, input().split()))
    m = int(input())
    # print(arr, m, "----")
    print(func0(arr, m))


def func0(arr, m):
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


main()
