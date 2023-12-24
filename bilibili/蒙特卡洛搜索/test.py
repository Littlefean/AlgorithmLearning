"""


"""
from random import random, choice, randint
import math


class Tiger:
    # 随机初始化一个老虎机，每次初始化生成一个老虎机的时候，这个老虎机的胜率可能都是不一样的。
    def __init__(self):
        self.r = random()
        pass

    def run(self):
        return random() < self.r

    pass


class SuperTiger:
    # 超级老虎机
    # 从一开始有一个随机胜率，经过 change_step 次摇动之后，胜率会变为 end_rate 次，这中间胜率是线性过度过去的。
    def __init__(self):
        self.start_rate = random()  # 一开始的胜率
        self.end_rate = random()  # 结束的胜率
        self.change_step = randint(10, 1000)  # 从开始渐变到结束的时候需要摇动多少次

        # 记录这个老虎机被摇动了多少次
        self.run_count = 0
        self.current_rate = self.start_rate  # 当前的胜率，初始化为开始的胜率
    
    def run(self):
        # 摇动一次机械臂
        self.run_count += 1
        if self.run_count <= self.change_step:
            # 如果摇动次数小于等于渐变次数，胜率进行线性过渡
            self.current_rate = self.start_rate + (self.end_rate - self.start_rate) * (self.run_count / self.change_step)
        return random() < self.current_rate


class Person:
    def __init__(self, faced_tiger_list):
        # 当前的得分
        self._score = 0
        # 剩余的测试数量
        self._test_count = 1000
        # 面对的老虎机
        self.faced_tiger_list = faced_tiger_list
        pass

    def run_tiger(self, idx):
        # 摇动一次老虎机，返回是否成功
        if self.faced_tiger_list[idx].run():
            self._score += 1
            return True
        self._test_count -= 1
        return False

    def mode1(self):
        # 顺序从左边到右边摇动
        while self._test_count > 0:
            self.run_tiger(self._test_count % len(self.faced_tiger_list))
        pass

    def mode2(self):
        # bug：只摇动了最后一个
        # 记住每一个老虎机的得分，根据得分来选择摇动
        if not hasattr(self, 'score_list'):
            self.score_list = [0 for _ in range(len(self.faced_tiger_list))]
        while self._test_count > 0:
            # 找到分数最大的那个，选择摇动
            max_value = -float("INF")
            max_index = -1
            for i, value in enumerate(self.score_list):
                if value > max_value:
                    max_index = i
            # 找到了
            if self.run_tiger(max_index):
                self.score_list[max_index] += 1
        print(self.score_list)

    def mode3(self):
        """
        记录每一个老虎机的胜率，胜率来如选择
        胜率 = 得分次数 / 次数
        每一个胜率都是1 默认，纯粹的利用型
        """
        if not hasattr(self, 'score_list'):
            self.score_list = [0 for _ in range(len(self.faced_tiger_list))]
        if not hasattr(self, 'count_list'):
            self.count_list = [0 for _ in range(len(self.faced_tiger_list))]

        while self._test_count > 0:
            # 找到分数最大的那个，选择摇动
            max_value = -float("INF")
            max_index = -1

            def f(s, c):
                return float("INF") if c == 0 else s / c

            for i, value in enumerate(self.faced_tiger_list):
                if f(self.score_list[i], self.count_list[i]) > max_value:
                    max_index = i
                    max_value = f(self.score_list[i], self.count_list[i])
            # 找到了
            self.count_list[max_index] += 1
            if self.run_tiger(max_index):
                self.score_list[max_index] += 1

        print(self.score_list)
        print(self.count_list)
        pass

    def mode4(self):
        # UCB
        if not hasattr(self, 'score_list'):
            self.score_list = [0 for _ in range(len(self.faced_tiger_list))]
        if not hasattr(self, 'count_list'):
            self.count_list = [0 for _ in range(len(self.faced_tiger_list))]

        total_count = 0

        while self._test_count > 0:
            # 找到分数最大的那个，选择摇动
            max_value = -float("INF")
            max_index = -1

            def ucb(s, c):
                return float("INF") if c == 0 else (s / c) + 2 * math.sqrt(math.log(total_count) / c)

            # 选择出ucb值最大的那个
            for i, value in enumerate(self.faced_tiger_list):
                if ucb(self.score_list[i], self.count_list[i]) > max_value:
                    max_index = i
                    max_value = ucb(self.score_list[i], self.count_list[i])
            # 找到了
            self.count_list[max_index] += 1
            total_count += 1
            if self.run_tiger(max_index):
                self.score_list[max_index] += 1


        print(self.score_list)
        print(self.count_list)
        pass

    def mode5(self):
        # 贝叶斯
        pass

    def mode6(self):
        # 树形
        pass

    def mode7(self):
        # 神经网络
        pass

    def mode8(self):
        # 遗传算法
        pass

    def mode9(self):
        # 深度学习
        pass

    def mode10(self):
        # 强化学习
        pass

    def mode11(self):
        pass

    pass


def main():
    t_list = [Tiger() for _ in range(100)]
    p1 = Person(t_list)
    p2 = Person(t_list)
    p3 = Person(t_list)
    p4 = Person(t_list)

    p1.mode1()
    print(p1._score)
    p2.mode2()
    print(p2._score)
    p3.mode3()
    print(p3._score)
    p4.mode4()
    print(p4._score)
    pass


if __name__ == "__main__":
    main()