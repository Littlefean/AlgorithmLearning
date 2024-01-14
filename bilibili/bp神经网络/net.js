class Net {
  constructor() {
    // 学习率
    this.studyRate = 0.025;
    // 正确的目标亮度值
    this.trueValue = 0.999;
    // 错误的目标亮度值
    this.falseValue = 0.001;

    // 所有的节点列表表示的数组
    // 第一个元素表示输入层的节点数量，
    // 最后一个元素表示输出层的节点数量
    // 所有的中间元素表示隐含层
    this.layerCountArr = [28 * 28, 16, 16, 10];

    // 权重数组
    this.weightArray = [];

    // 临时记录所有点亮的节点的值，包涵了第一层
    this.tempNodeLightList = Array.from(
      { length: this.layerCountArr.length },
      () => []
    );

    // 每个节点头顶上有一个缓存误差值
    this.errNodeLightList = Array.from(
      { length: this.layerCountArr.length },
      () => []
    );

    this.arrayInit();
  }

  arrayInit() {
    const arr = this.layerCountArr;
    for (let i = 0; i < arr.length; i++) {
      this.tempNodeLightList[i] = new Array(arr[i]).fill(0);
      this.errNodeLightList[i] = new Array(arr[i]).fill(0);

      if (i === 0) continue;

      const height = arr[i - 1];
      const width = arr[i];

      const weightLayer = Array.from({ length: height }, () =>
        Array.from({ length: width }, () =>
          this.gaussRandom(0, 1 / Math.sqrt(width))
        )
      );

      this.weightArray.push(weightLayer);
    }
  }

  static getNetFromJson(dic) {
    let res = new Net();
    res.trueValue = dic["true_value"];
    res.falseValue = dic["false_value"];
    res.studyRate = dic["study_rate"];
    res.layerCountArr = dic["layer_count_arr"];
    res.weightArray = dic["_weight_array"];
    res.tempNodeLightList = dic["_temp_node_light_list"];
    res.errNodeLightList = dic["_err_node_light_list"];
    return res;
  }

  gaussRandom(mean, std) {
    // 生成符合高斯分布的随机数
    let u = 2 * Math.random() - 1;
    let v = 2 * Math.random() - 1;
    let r = u * u + v * v;
    if (r === 0 || r > 1) return this.gaussRandom(mean, std);
    let c = Math.sqrt((-2 * Math.log(r)) / r);
    return mean + u * c * std;
  }

  input(arr) {
    // 输入一个一维数组 长度刚好是
    if (arr.length !== this.layerCountArr[0]) {
      throw new Error("Input array length does not match input layer size.");
    }
    // 直接填充第一层
    for (let i = 0; i < arr.length; i++) {
      this.tempNodeLightList[0][i] = arr[i];
    }
  }

  leftToRight() {
    for (
      let layerIndex = 0;
      layerIndex < this.tempNodeLightList.length - 1;
      layerIndex++
    ) {
      const leftArr = this.tempNodeLightList[layerIndex];
      const rightArr = this.tempNodeLightList[layerIndex + 1];

      for (let i = 0; i < leftArr.length; i++) {
        for (let j = 0; j < rightArr.length; j++) {
          rightArr[j] += this.getWeight(layerIndex, i, j) * leftArr[i];
        }
      }

      for (let i = 0; i < rightArr.length; i++) {
        rightArr[i] = this.sigmoid(rightArr[i]);
      }
    }
  }

  sigmoid(x) {
    return 1 / (1 + Math.exp(-x));
  }

  // Add other methods as needed...

  getWeight(leftLayer, i, j) {
    return this.weightArray[leftLayer][i][j];
  }

  // 获取所有结果的可能性
  getResult() {
    return this.tempNodeLightList[this.tempNodeLightList.length - 1];
  }
}