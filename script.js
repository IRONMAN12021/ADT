let board = ['', '', '', '', '', '', '', '', ''];
let currentPlayer = 'X';
let gameCount = 0;
let playerScore = 0;
let aiScore = 0;
let isGameOver = false;
const cells = document.querySelectorAll('.cell');
const messageElement = document.getElementById('message');
const playerScoreElement = document.getElementById('playerScore');
const aiScoreElement = document.getElementById('aiScore');
const restartButton = document.getElementById('restartButton');
const startScreen = document.getElementById('startScreen');
const gameScreen = document.getElementById('gameScreen');
const startButton = document.getElementById('startButton');

function checkWinner() {
    const winPatterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], // Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8], // Vertical
        [0, 4, 8], [2, 4, 6]  // Diagonal
    ];

    for (let pattern of winPatterns) {
        const [a, b, c] = pattern;
        if (board[a] && board[a] === board[b] && board[a] === board[c]) {
            return board[a];
        }
    }

    return board.includes('') ? null : 'Draw';
}

function displayMessage(text) {
    messageElement.textContent = text;
    messageElement.classList.remove('hidden');
    messageElement.classList.add('visible');
}

function updateScore() {
    playerScoreElement.textContent = `You: ${playerScore}`;
    aiScoreElement.textContent = `AI: ${aiScore}`;
}

function handleCellClick(event) {
    const index = event.target.getAttribute('data-index');
    if (board[index] !== '' || isGameOver) return;

    board[index] = currentPlayer;
    event.target.textContent = currentPlayer;
    event.target.style.transform = 'scale(1.2)';
    setTimeout(() => event.target.style.transform = 'scale(1)', 100);

    const winner = checkWinner();
    if (winner) {
        isGameOver = true;
        if (winner === 'X') {
            playerScore++;
            displayMessage('Congratulations! You win!');
        } else if (winner === 'O') {
            aiScore++;
            displayMessage('AI wins!');
        } else {
            displayMessage("It's a draw!");
        }
        confettiEffect();
        updateScore();
    } else {
        currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
        if (currentPlayer === 'O') aiMove();
    }
}

function aiMove() {
    const availableMoves = board.map((cell, index) => cell === '' ? index : null).filter(index => index !== null);
    const move = availableMoves[Math.floor(Math.random() * availableMoves.length)];
    board[move] = 'O';
    cells[move].textContent = 'O';
    cells[move].style.transform = 'scale(1.2)';
    setTimeout(() => cells[move].style.transform = 'scale(1)', 100);

    const winner = checkWinner();
    if (winner) {
        isGameOver = true;
        if (winner === 'O') {
            aiScore++;
            displayMessage('AI wins!');
        } else {
            displayMessage("It's a draw!");
        }
        confettiEffect();
        updateScore();
    } else {
        currentPlayer = 'X';
    }
}

function restartGame() {
    board = ['', '', '', '', '', '', '', '', ''];
    isGameOver = false;
    currentPlayer = gameCount % 2 === 0 ? 'X' : 'O';
    cells.forEach(cell => {
        cell.textContent = '';
        cell.style.transform = 'scale(1)';
    });
    messageElement.classList.add('hidden');
    messageElement.classList.remove('visible');

    gameCount++;
    if (currentPlayer === 'O') aiMove();
}

function confettiEffect() {
    // Basic confetti animation can be implemented here or using a library like confetti.js
}

startButton.addEventListener('click', () => {
    startScreen.classList.add('hidden');
    gameScreen.classList.remove('hidden');
});

cells.forEach(cell => cell.addEventListener('click', handleCellClick));
restartButton.addEventListener('click', restartGame);
restartGame(); // Start the first game
