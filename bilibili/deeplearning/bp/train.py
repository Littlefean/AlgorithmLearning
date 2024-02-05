"""
训练模块
"""
from typing import Dict, List
import os
from time import perf_counter
from random import shuffle
from datetime import datetime

from PIL import Image

from bilibili.deeplearning.tools.img_generate import get_img_list
from bilibili.deeplearning.net import Net


def train1():
    """
    训练
    :return:
    """

    data_set: Dict[int, List[Image.Image]] = {n: [] for n in range(0, 10)}
    number_set = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    # 生成数据集
    for number in number_set:  # 修改这里，实现只训练固定的数字
        path = f'../imgs/in/{number}'
        for img_filename in os.listdir(path):
            data_set[number] += get_img_list(Image.open(path + os.sep + img_filename))

    # 打乱数据集
    for img_list in data_set.values():
        shuffle(img_list)

    # 分割训练集和测试集，3/4训练，1/4测试
    split = int(len(data_set[0]) * 3 / 4)  # 假设每个数据集的数字图片库数量都是相同的。
    train_set: Dict[int, List[Image.Image]] = {n: data_set[n][:split] for n in range(0, 10)}
    test_set: Dict[int, List[Image.Image]] = {n: data_set[n][split:] for n in range(0, 10)}

    # 开始训练
    t1 = perf_counter()
    nt = Net()
    for i in range(split):
        for number in number_set:
            nt.input_know_and_change(train_set[number][i], number)
        print(f"{i}/{split}")

    # 将网络保存在本地，方便后续手动测试
    now = datetime.now()
    nt.save_net_to_file(f'../net-{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}.py')

    t2 = perf_counter()
    print('训练耗时：', t2 - t1, 's')

    # 开始测试
    correct_dict = {n: 0 for n in range(0, 10)}  # 答正确的次数
    test_count_pre_number = len(test_set[0])

    # 测试每一个数字，累加正确率
    for i in range(test_count_pre_number):
        for number in number_set:
            nt.input_img(test_set[number][i])
            nt.left_to_right()
            res_num = nt.get_result()
            if res_num == number:
                correct_dict[number] += 1

    for n in range(10):
        print(f'数字{n}正确率：{correct_dict[n] / test_count_pre_number}')

    pass


def transform_file():
    """将文件转换为json格式，用于前端读取"""
    net = Net.get_net_from_path_file('../save_net/test-2024-1-9-0123456789.py')
    net.save_net_to_js('../save_net/test-2024-1-9-0123456789.js')


def test1():
    net = Net.get_net_from_path_file('../save_net/test-2024-1-9-0123456789.py')
    net.input_img(Image.open('test.png'))
    net.left_to_right()
    net.show_input_img_matrix()
    net.show_result()

    pass


def main():
    # train1()
    test1()
    # transform_file()
    pass


if __name__ == '__main__':
    main()
