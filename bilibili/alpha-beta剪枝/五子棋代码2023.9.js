export default {
  tempSymbol: 0,
  mySymbol: 1,
  opSymbol: 2,

  /**
   * 系统会不断调用这个函数
   * @param board
   * @returns {{x, y}}
   */
  action(board) {
    if (board[7][7] === this.tempSymbol) {
      return {x: 7, y: 7};
    }

    const bestMove = this.alphaBeta(board, -this.INF, this.INF, true, this.maxDeep);
    this.printf(bestMove);
    return {x: bestMove.x, y: bestMove.y};
  },
  maxDeep: 2,

  /**
   * 五子棋alpha-beta剪枝算法
   * @param board {number[][]} 15*15 大小的棋盘
   * @param alpha {number}
   * @param beta {number}
   * @param maximizingPlayer {boolean} 是否是max层
   * @param deep {number} 递归深度限制
   * @returns {{
   *     score: number,
   *     x: number,
   *     y: number,
   * }}
   * 当前局面得分
   */
  alphaBeta(board, alpha, beta, maximizingPlayer, deep) {
    const emptyCells = this.getRoundCells(board);

    if (this.isGameOver(board) || emptyCells.length === 0) {
      // 下满了或者结束了
      const score = this.evaluate(board, maximizingPlayer);
      return {score, x: -1, y: -1};
    }

    if (deep === 0) {
      // 到达递归深度，
      const score = this.evaluate(board, maximizingPlayer);
      // 随机抽取一个边缘位置下
      const rI = Math.floor(Math.random() * emptyCells.length);
      const {x, y} = emptyCells[rI];
      return {score, x, y};  // 这里的xy不重要
    }


    let bestMove;
    const INF = this.INF;

    if (maximizingPlayer) {
      // 我方视角
      bestMove = {score: -INF};
      for (const {x, y} of emptyCells) {
        board[y][x] = this.mySymbol;
        let move = this.alphaBeta(board, alpha, beta, false, deep - 1);
        move = {...move, x, y};
        board[y][x] = this.tempSymbol;
        if (move.score > bestMove.score) {
          bestMove = move;
        }
        // 向上更新自己当前结点的最低期望分数
        alpha = Math.max(alpha, bestMove.score);
        if (alpha >= beta) {
          break;
        }
        if (beta <= alpha) {
          break;
        }
      }
    } else {
      // 对手视角
      bestMove = {score: INF};
      for (const {x, y} of emptyCells) {
        board[y][x] = this.opSymbol;
        let move = this.alphaBeta(board, alpha, beta, true, deep - 1);
        move = {...move, x, y};
        board[y][x] = this.tempSymbol;
        if (move.score < bestMove.score) {
          bestMove = move;
        }
        beta = Math.min(beta, bestMove.score);
        if (beta <= alpha) {
          break;
        }
      }
    }

    return bestMove;
  },
  /**
   * 获取棋盘上所有棋子外层的空气结点
   * @param board
   */
  getRoundCells(board) {
    const emptyCells = [];
    const locSet = new Set();

    for (let y = 0; y < 15; y++) {
      for (let x = 0; x < 15; x++) {

        if (board[y][x] !== this.tempSymbol) {
          // 不是空气，把它的一圈内是空气的都加进来
          for (let dx = -1; dx <= 1; dx++) {
            for (let dy = -1; dy <= 1; dy++) {
              const loc = {x: x + dx, y: y + dy};

              if (locSet.has(JSON.stringify(loc))) {
                continue;
              }
              if (dx === 0 && dy === 0) continue;

              if (this.inBoard(loc) && board[y + dy][x + dx] === this.tempSymbol) {
                locSet.add(JSON.stringify(loc));
                emptyCells.push(loc);
              }
            }
          }
        }
      }
    }
    return emptyCells;
  },
  // 判断一个坐标点是否在棋盘内
  inBoard(loc) {
    return 0 <= loc.y && loc.y < 15 && 0 <= loc.x && loc.x < 15;
  },

  /**
   * 判断五子棋是否结束了
   * @param board {number[][]} 15 * 15 大小的数字，0代表空地 this.mySymbol 代表自己的棋子，this.opSymbol 代表对方的棋子
   * @return boolean
   */
  isGameOver(board) {
    const rows = board.length;
    const cols = board[0].length;

    // 检查水平方向
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols - 4; col++) {
        if (
          board[row][col] !== 0 &&
          board[row][col] === board[row][col + 1] &&
          board[row][col] === board[row][col + 2] &&
          board[row][col] === board[row][col + 3] &&
          board[row][col] === board[row][col + 4]
        ) {
          return true; // 游戏结束
        }
      }
    }

    // 检查垂直方向
    for (let col = 0; col < cols; col++) {
      for (let row = 0; row < rows - 4; row++) {
        if (
          board[row][col] !== 0 &&
          board[row][col] === board[row + 1][col] &&
          board[row][col] === board[row + 2][col] &&
          board[row][col] === board[row + 3][col] &&
          board[row][col] === board[row + 4][col]
        ) {
          return true; // 游戏结束
        }
      }
    }

    // 检查正斜对角线方向
    for (let row = 0; row < rows - 4; row++) {
      for (let col = 0; col < cols - 4; col++) {
        if (
          board[row][col] !== 0 &&
          board[row][col] === board[row + 1][col + 1] &&
          board[row][col] === board[row + 2][col + 2] &&
          board[row][col] === board[row + 3][col + 3] &&
          board[row][col] === board[row + 4][col + 4]
        ) {
          return true; // 游戏结束
        }
      }
    }

    // 检查反斜对角线方向
    for (let row = 4; row < rows; row++) {
      for (let col = 0; col < cols - 4; col++) {
        if (
          board[row][col] !== 0 &&
          board[row][col] === board[row - 1][col + 1] &&
          board[row][col] === board[row - 2][col + 2] &&
          board[row][col] === board[row - 3][col + 3] &&
          board[row][col] === board[row - 4][col + 4]
        ) {
          return true; // 游戏结束
        }
      }
    }
    return false;
  },


  evaluate(board, isMyTurn) {
    // 在这里实现你的评估函数
    // 返回一个代表当前局面得分的数字
    // 更高的得分表示更好的局面
    // 更低的得分表示更差的局面
    // 你可以根据需要自定义自己的评估函数
    // 这里只是一个简单的示例

    if (this.isWinning(board, this.mySymbol)) {
      this.printf('findWin!');
      return this.INF;
    } else if (this.isWinning(board, this.opSymbol)) {
      this.printf('findLouse!');
      return -this.INF;
    } else {
      // 还在下的情况
      return this.evaluateNormal(board, isMyTurn);
    }
  },

  /**
   * 评估当前局面的分数，调用该函数的上游能够保证当前局面不是游戏结束的局面
   * @param board {number[][]} 15 * 15 大小的五子棋棋盘
   * @param isMy {boolean} 当前要下的是否是我方
   * @return {number} 分数
   */
  evaluateNormal(board, isMy) {
    const ROW = 15;
    const COL = 15;
    let score = 0;

    // 遍历横向条
    for (let y = 0; y < ROW; y++) {
      score += this.evaluateLine(board[y], isMy);
    }

    // 遍历竖向条
    for (let x = 0; x < COL; x++) {
      const line = [];
      for (let y = 0; y < ROW; y++) {
        line.push(board[y][x]);
      }
      score += this.evaluateLine(line, isMy);
    }
    // 遍历正斜向条
    for (let d = 0; d <= ROW + COL - 2; d++) {
      const line = [];
      for (let x = Math.max(0, d - ROW + 1); x <= Math.min(d, COL - 1); x++) {
        const y = d - x;
        line.push(board[y][x]);
      }
      score += this.evaluateLine(line, isMy);
    }
    // 遍历反斜向条
    for (let d = 0; d <= ROW + COL - 2; d++) {
      const line = [];
      for (let x = Math.max(0, d - ROW + 1); x <= Math.min(d, COL - 1); x++) {
        const y = ROW - 1 - (d - x);
        line.push(board[y][x]);
      }
      score += this.evaluateLine(line, isMy);
    }

    return score;
  },

  INF: 99_9999_9999,

  getScoreTable() {

    if (this.scoreTable) {
      // 如果已经绑定了缓存，先去绑定缓存
      return this.scoreTable;
    }

    // 不用下，已经赢了
    const p0 = 1_0000_0000;
    // 一步代价
    const p1 = 1000;
    // 两步代价
    const p2 = 100;
    const p3 = 10;
    const p4 = 1;

    const d4 = p1;  // 死4价值
    const d3 = p2;   // 死3价值
    const d2 = p3;   // 死2价值
    const d1 = p4;    // 死1价值
    
    const f = arr => {
      return [arr[0] + arr[1], arr[1]];
    }
    
    let res = {
      // [自己即将要下一个子，对手下之后自己才能下]

      '11111': f([p0, p0]),
      // 4 系列
      '_1111_': f([p1, d4]),
      '_111_1_': f([p1, d3 + d1]),
      '_11_11_': f([p1, d2 * 2]),
      '21111_': f([p1, 0]),
      '2111_1_': f([p1, d1]),
      '21_1112': f([p1, 0]),
      '211_112': f([p1, 0]),

      // 3 系列
      '__111__': f([p2, d3]),
      '_1_11_': f([p2, d2 + d1]),
      '_1__11_': f([p2, d2 + d1]),
      '2_111__': f([p2, 0]),
      '2111__': f([p2, 0]),
      '21_11_': f([p2, 0]),
      '21__11_': f([p2, d2]),
      '2__1112': f([p2, 0]),
      '2_111_2': f([p2, 0]),
      '21_11_2': f([p2, 0]),
      '21_1_12': f([p2, 0]),

      '_1_1_1_': f([p2, d2 + d1]),
      '211_1__': f([p2, 0]),
      '211_1_2': f([p2, 0]),
      // 2 系列
      '__11__': f([p3, d2]),
      '_1_1_': f([p3, 2 * d1]),
      '211___': f([p3, 0]),
      '21_1__': f([p3, 0]),
      '21__1_': f([p3, 0]),
      // 1
      '__1__': [p4, d1],
    };

    // 翻转tab字典
    let newDic = {...res};

    for (let key in res) {
      let reversedKey = key.split('').reverse().join('');
      // 将key这个字符串反转，放在newDic中
      newDic[reversedKey] = res[key];
    }
    // 加入缓存
    this.scoreTable = newDic;
    return newDic;
  },

  /**
   * 辅助函数，评估一条切割条的分数
   * @param line {number[]} 这条切割线是贯穿棋盘上一整条直线上的棋子所构成的数组。
   * 其中 0 代表空地，this.opSymbol 代表对方棋子，this.mySymbol 代表我方棋子
   * @param isMy {boolean} 现在是否是自己要下了
   * @returns {number} 这条切割线的分数
   */
  evaluateLine(line, isMy) {
    if (line.length < 5) {
      // 这个切割线可能由于是斜向的角落，导致长度不够
      return 0;
    }

    // 直接用字符串转化后匹配

    // 我方视角下的字符串
    let myLineStr = '';
    let opLineStr = '';
    for (const num of line) {
      if (num === this.tempSymbol) {
        myLineStr += '_';
        opLineStr += '_';
      } else if (num === this.opSymbol) {
        myLineStr += '2';
        opLineStr += '1';
      } else if (num === this.mySymbol) {
        myLineStr += '1';
        opLineStr += '2';
      }
    }
    // 开始和this.scoreTable 进行遍历匹配
    // 如果isMy 为 true，则累加 小数组第一个位置的分数，
    // 否则累加小数组第二个位置的分数
    let score = 0;
    const patterns = Object.keys(this.getScoreTable());
    for (const pattern of patterns) {
      const [score1, score2] = this.getScoreTable()[pattern];
      if (myLineStr.includes(pattern)) {
        score += isMy ? score1 : score2;
      }
      if (opLineStr.includes(pattern)) {
        score -= isMy ? score2 : score1;
      }
    }
    return score;
  },


  /**
   * 检查五子棋棋盘是否有人赢了
   * @param board {number[][]} 15 * 15 大小的数字，0代表空地 this.mySymbol 代表自己的棋子，this.opSymbol 代表对方的棋子
   * @param symbol {number} 检查的那一方的棋子
   */
  isWinning(board, symbol) {
    const rows = board.length;
    const cols = board[0].length;
    const target = 5;
    const rowBoundary = rows - target;
    const colBoundary = cols - target;

    // 水平方向检查
    for (let row = 0; row < rows; row++) {
      let count = 0;
      for (let col = 0; col <= colBoundary; col++) {
        if (board[row][col] === symbol) {
          count++;
          if (count === target) {
            return true;
          }
        } else {
          count = 0;
        }
      }
    }

    // 垂直方向检查
    for (let col = 0; col < cols; col++) {
      let count = 0;
      for (let row = 0; row <= rowBoundary; row++) {
        if (board[row][col] === symbol) {
          count++;
          if (count === target) {
            return true;
          }
        } else {
          count = 0;
        }
      }
    }
    // 对角线方向检查
    const diagonalOffsets = [[1, 1], [-1, 1]]; // 正对角线和反对角线的偏移量
    for (const [rowOffset, colOffset] of diagonalOffsets) {
      for (let row = 0; row <= rowBoundary; row++) {
        for (let col = 0; col <= colBoundary; col++) {
          let count = 0;
          for (let i = 0; i < target; i++) {
            if (row + i * rowOffset >= 0 && row + i * rowOffset < rows && col + i * colOffset >= 0 && col + i * colOffset < cols) {
              if (board[row + i * rowOffset][col + i * colOffset] === symbol) {
                count++;
                if (count === target) {
                  return true;
                }
              } else {
                count = 0;
              }
            }
          }
        }
      }
    }
    return false;
  },

  printf(...args) {

  }
};
