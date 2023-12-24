export default {
  tempSymbol: 0,
  mySymbol: 1,
  opSymbol: 2,

  action(board) {
    const bestMove = this.alphaBeta(board, -Infinity, Infinity, true);
    return {x: bestMove.x, y: bestMove.y};
  },

  alphaBeta(board, alpha, beta, maximizingPlayer) {
    const emptyCells = this.getEmptyCells(board);

    if (this.isGameOver(board) || emptyCells.length === 0) {
      const score = this.evaluate(board);
      return {score};
    }

    let bestMove;
    if (maximizingPlayer) {
      bestMove = {score: -Infinity};
      for (let i = 0; i < emptyCells.length; i++) {
        const {x, y} = emptyCells[i];
        board[y][x] = this.mySymbol;
        const move = this.alphaBeta(board, alpha, beta, false);
        board[y][x] = this.tempSymbol;
        move.x = x;
        move.y = y;
        if (move.score > bestMove.score) {
          bestMove = move;
        }
        alpha = Math.max(alpha, bestMove.score);
        if (beta <= alpha) {
          break;
        }
      }
    } else {
      bestMove = {score: Infinity};
      for (let i = 0; i < emptyCells.length; i++) {
        const {x, y} = emptyCells[i];
        board[y][x] = this.opSymbol;
        const move = this.alphaBeta(board, alpha, beta, true);
        board[y][x] = this.tempSymbol;
        move.x = x;
        move.y = y;
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

  getEmptyCells(board) {
    const emptyCells = [];
    for (let y = 0; y < 3; y++) {
      for (let x = 0; x < 3; x++) {
        if (board[y][x] === this.tempSymbol) {
          emptyCells.push({x, y});
        }
      }
    }
    return emptyCells;
  },

  isGameOver(board) {
    // 检查行
    for (let i = 0; i < 3; i++) {
      if (
        board[i][0] !== this.tempSymbol &&
        board[i][0] === board[i][1] &&
        board[i][1] === board[i][2]
      ) {
        return true;
      }
    }

    // 检查列
    for (let i = 0; i < 3; i++) {
      if (
        board[0][i] !== this.tempSymbol &&
        board[0][i] === board[1][i] &&
        board[1][i] === board[2][i]
      ) {
        return true;
      }
    }

    // 检查对角线
    if (
      board[0][0] !== this.tempSymbol &&
      board[0][0] === board[1][1] &&
      board[1][1] === board[2][2]
    ) {
      return true;
    }
    if (
      board[0][2] !== this.tempSymbol &&
      board[0][2] === board[1][1] &&
      board[1][1] === board[2][0]
    ) {
      return true;
    }

    return false;
  },

  evaluate(board) {
    // 在这里实现你的评估函数
    // 返回一个代表当前局面得分的数字
    // 更高的得分表示更好的局面
    // 更低的得分表示更差的局面
    // 你可以根据需要自定义自己的评估函数
    // 这里只是一个简单的示例

    if (this.isWinning(board, this.mySymbol)) {
      return 1;
    } else if (this.isWinning(board, this.opSymbol)) {
      return -1;
    } else {
      return 0;
    }
  },

  isWinning(board, symbol) {
    // 检查行
    for (let i = 0; i < 3; i++) {
      if (
        board[i][0] === symbol &&
        board[i][1] === symbol &&
        board[i][2] === symbol
      ) {
        return true;
      }
    }

    // 检查列
    for (let i = 0; i < 3; i++) {
      if (
        board[0][i] === symbol &&
        board[1][i] === symbol &&
        board[2][i] === symbol
      ) {
        return true;
      }
    }

    // 检查对角线
    if (
      board[0][0] === symbol &&
      board[1][1] === symbol &&
      board[2][2] === symbol
    ) {
      return true;
    }
    return board[0][2] === symbol &&
      board[1][1] === symbol &&
      board[2][0] === symbol;

    
  }
};
