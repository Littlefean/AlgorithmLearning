from typing import List
from random import random, uniform, gauss
from PIL import Image

from copy import deepcopy


class Net:
    """神经网络类"""

    def __init__(self):
        # 学习率
        self.study_rate = 0.025
        # 正确的目标亮度值
        self.true_value = 0.999
        # 错误的目标亮度值
        self.false_value = 0.001

        # 所有的节点列表示的数组
        # 第一个元素表示输入层的节点数量，
        # 最后一个元素表示输出层的节点数量
        # 所有的中间元素表示隐含层
        self.layer_count_arr = [28 * 28, 16, 16, 10]

        # 里面的每个线段权重都是二维表，二维数组表示权重
        self._weight_array: List[List[List[float]]] = []

        # 临时记录所有点亮的节点的值，包涵了第一层
        self._temp_node_light_list: List[List[float]] = []  # 存放点亮的节点，有第一层

        # 每个节点头顶上有一个缓存误差值
        self._err_node_light_list: List[List[float]] = []  # 存放点亮的节点，有第一层

        self._array_init()

        ...

    def _array_init(self):
        """给所有的高纬数组初始化"""
        arr = self.layer_count_arr
        for i, n in enumerate(arr):
            # 构建临时点亮节点数组
            self._temp_node_light_list.append([0] * n)
            # 构建临时误差数组
            self._err_node_light_list.append([0] * n)

            if i == 0:
                continue
            height = arr[i - 1]
            width = n
            # 权值随机范围是在 -1/✓n ~ 1/✓n

            weightLayer = [
                # [uniform(-1 / (n ** 0.5), 1 / (n ** 0.5)) for _ in range(width)] for _ in range(height)
                [gauss(0, 1 / (n ** 0.5)) for _ in range(width)] for _ in range(height)
            ]
            self._weight_array.append(weightLayer)

    def __dict__(self):
        """将这个网络转成可以保存的对象，用于保存内部结构"""
        return {
            "layerCountArr": self.layer_count_arr,
            "_weightArray": self._weight_array,
            "_tempNodeLightList": self._temp_node_light_list,
            "_errNodeLightList": self._err_node_light_list,
            # 学习率
            "studyRate": self.study_rate,
            # 正确的目标亮度值
            "trueValue": self.true_value,
            # 错误的目标亮度值
            "falseValue": self.false_value,
        }

    def saveNetToFile(self, fileName):
        """把当前的网络保存到saveNet文件夹下"""
        with open(f"saveNet/{fileName}.py", "w", encoding="utf-8") as f:
            f.write(repr(self.__dict__()))

    @classmethod
    def getNetFromFile(cls, fileName):
        """打开一个网络"""
        with open(f"saveNet/{fileName}.py", encoding="utf-8") as f:
            dicStr = f.read()
        dic = eval(dicStr)
        res = cls()
        res.true_value = dic["trueValue"]
        res.false_value = dic["falseValue"]
        res.study_rate = dic["studyRate"]
        res.layer_count_arr = dic["layerCountArr"]
        res._weight_array = dic["_weightArray"]
        res._temp_node_light_list = dic["_tempNodeLightList"]
        res._err_node_light_list = dic["_errNodeLightList"]
        return res

    def saveCurrentNetImage(self, number: int):
        """保存当前的网络内部状态，生成一个图片"""
        # 先保存权重值
        for i, table in enumerate(self._weight_array):
            tableToImage(table).save(f"netImg/第{i}层权值/{str(number).zfill(5)} 轮训练.png")
        ...

    def input(self, arr: list):
        # 输入一个一维数组 长度刚好是
        assert len(arr) == self.layer_count_arr[0]
        # 直接填充第一层
        for i, n in enumerate(arr):
            self._temp_node_light_list[0][i] = n

    def leftToRight(self):
        """
        从左到右扩散传播，此时的暂存是已经填好了的
        一般在此之前会调用input函数
        :return:
        """
        for layerIndex, leftArr in enumerate(self._temp_node_light_list):
            if layerIndex == len(self._temp_node_light_list) - 1:
                # 已经到了最后一层了，不能再向下传播了
                break
            # leftArr 左侧一列神经元  nextArr 右侧一列神经元
            rightArr = self._temp_node_light_list[layerIndex + 1]

            # 遍历左侧每个神经元 ai
            for i, a in enumerate(leftArr):
                # 遍历右侧每个神经元 bj
                for j, b in enumerate(rightArr):
                    # 开始累加数字
                    # 亮度乘以权重
                    self._temp_node_light_list[layerIndex + 1][j] += self._getWeight(layerIndex, i, j) * a

                ...
            # 累加完了之后开始对右边统计进行 sigmoid(x + 偏置)
            for i, sumNumber in enumerate(rightArr):
                # rightArr[i] = sigmoid(x + self._getBias(layerIndex + 1, i))
                rightArr[i] = sigmoid(sumNumber)
        # 最终填好的数字就到最右侧了
        ...

    def showNode(self):
        """打印当前网络的点亮状态"""
        for arr in self._temp_node_light_list:
            print(arr)
            # for n in arr:
            #     strN = str(n)
            #     if "." in strN:
            #         z, x = strN.split(".")
            #         print(f"{z}.{x[:2]}", end="\t")
            #     else:
            #         print(n, end="\t")
        print("=" * 50)

    def showResult(self):
        """打印当前网络结果层的点亮状态"""
        a = []
        for i, n in enumerate(self._temp_node_light_list[-1]):
            print(f"[{i}] {round(n, 3)}", end="\t")
            a.append((i, round(n, 3)))
        print()
        print("可能性最高：", max(a, key=lambda x: x[1])[0])
        print("-" * 50)

    def getResult(self):
        """获取当前网络得到的结果"""
        maxLight = -float("INF")
        maxIndex = 0
        for y in range(self.layer_count_arr[-1]):
            lightness = self._getNodeLight(len(self.layer_count_arr) - 1, y)
            if lightness > maxLight:
                maxLight = lightness
                maxIndex = y
        return maxIndex

    def showInner(self):
        """展示网络的内部结构，所有的偏和权"""
        print("========")
        for table in self._weight_array:
            for line in table:
                print(line)
            print()
        # print("偏重：")
        # for col in self._biasArray:
        #     print(col)
        print("--------")

    def _getNodeLight(self, colIndex, i):
        """获取某一个位置上节点的亮度"""
        return self._temp_node_light_list[colIndex][i]

    def _getNodeErr(self, colIndex, i):
        """获取某一个位置上节点的误差值"""
        return self._err_node_light_list[colIndex][i]

    def _setNodeErr(self, colIndex, i, value):
        """设置某一个位置节点的误差值"""
        self._err_node_light_list[colIndex][i] = value

    def _getWeight(self, leftLayer, i, j):
        """
        获取权重
        :param leftLayer: 从左边列出发，左边列的列编号是多少
        :param i: 左列的第多少个节点
        :param j: 右侧列的第几个节点
        网络示意图
        → a  b →
        → c  d →
        [
            [a→b   a→d],
            [c→b   c→d],
        ]
        [
            [w11   w12],
            [w21   w22],
        ] 与python神经网络那本书上刚好是转置的对应关系
        :return:
        """
        return self._weight_array[leftLayer][i][j]

    def _setWeight(self, leftLayer, i, j, value):
        """更改一条权重"""
        self._weight_array[leftLayer][i][j] = value

    def _getWeightMatrix(self, leftLayer):
        """获取权重矩阵，这个和书上是一致的，不是转置的"""
        return matrixTrans(self._weight_array[leftLayer])

    def inputImg(self, img: Image):
        """输入一张灰度图"""
        arr = []
        for y in range(img.height):
            for x in range(img.width):
                tup = img.getpixel((x, y))
                if len(tup) == 3:
                    r, g, b = tup
                elif len(tup) == 4:
                    r, g, b, _ = tup
                arr.append((r + g + b) // 3 / 255)
        self.input(arr)

    def showInputImgMatrix(self):
        # 默认图片是正方形的
        length = int(self.layer_count_arr[0] ** 0.5)
        for y in range(length):
            for x in range(length):
                m = self._getNodeLight(0, y * length + x)
                if m <= 0:
                    print("   ", end="  ")
                else:
                    print(round(m, 3), end="  ")
            print()

    def inputKnowAndChange(self, im: Image, number: int):
        """
        传入一个已经知道是数字几的图片
        并反向传播填写期待更改的数字
        反向传播误差，然后更改每一个权重
        """
        self.inputImg(im)
        self.leftToRight()
        rightIndex = len(self.layer_count_arr) - 1
        # ===== 更新每一层节点头顶上的误差数字
        # 先更新最右侧的
        for n in range(self.layer_count_arr[-1]):  # 0123456789
            light = self._getNodeLight(rightIndex, n)  # 遍历获取最右侧节点的亮度

            if n == number:
                e = self.true_value - light
            else:
                e = self.false_value - light
            self._setNodeErr(rightIndex, n, e)
        for i in reversed(range(rightIndex)):  # 0 1 ... rightIndex-1    反着来
            m = self._getWeightMatrix(i)
            v = self._err_node_light_list[i + 1]
            v1 = matrixMul(matrixTrans(m), v)
            for j, n in enumerate(v1):
                self._setNodeErr(i, j, n)
        # =====

        # 对每一条权重 进行求梯度，更改
        for leftLayer in range(len(self.layer_count_arr) - 1):
            # 遍历每一个左竖列 ，最右边不需要 所以 -1
            for i in range(self.layer_count_arr[leftLayer]):
                leftLight = self._getNodeLight(leftLayer, i)

                for j in range(self.layer_count_arr[leftLayer + 1]):
                    oldW = self._getWeight(leftLayer, i, j)
                    rightLight = self._getNodeLight(leftLayer + 1, j)
                    rightErr = self._getNodeErr(leftLayer + 1, j)
                    rate = -rightErr * rightLight * (1 - rightLight) * leftLight
                    self._setWeight(leftLayer, i, j, oldW - self.study_rate * rate)
                    # todo 每输入一个数字图片就整体更改一次权重，可能会出现打架的问题

            ...

    ...
