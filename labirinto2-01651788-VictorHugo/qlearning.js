// Alterado para treinamento mais eficaz
const canvas = document.getElementById('mazeCanvas');
const ctx = canvas.getContext('2d');

const rows = 10;
const cols = 10;
const cellSize = canvas.width / cols;

const numAgents = 3;
const episodes = 5000; // Aumentado para permitir mais aprendizado

let alpha, gamma, epsilon;

let maze = [];
let agents = [];
let Q = {};
let episode = 0;
let trainingInterval = null;
let showPolicy = false;

// Labirinto fixo para aprendizado consistente
function generateMaze() {
  maze = Array.from({ length: rows }, () =>
    Array.from({ length: cols }, () => 0)
  );
  for (let i = 1; i < 9; i++) maze[5][i] = 1;
  for (let i = 1; i < 6; i++) maze[i][3] = 1;
  for (let i = 1; i < 6; i++) maze[i][3] = 1;
  maze[0][0] = 0;
  maze[rows - 1][cols - 1] = 0;
}

function drawPolicyArrows(x, y) {
  const state = getState(x, y);
  if (!Q[state]) return;
  const bestAction = Q[state].indexOf(Math.max(...Q[state]));
  ctx.fillStyle = 'black';
  ctx.font = `${cellSize / 2}px Arial`;
  const arrow = ['↑', '↓', '←', '→'][bestAction];
  ctx.fillText(arrow, x * cellSize + cellSize / 3, y * cellSize + 2 * cellSize / 3);
}

function drawMaze() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      if (maze[y][x] === 1) {
        ctx.fillStyle = 'black';
        ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
      } else {
        ctx.strokeStyle = '#ccc';
        ctx.strokeRect(x * cellSize, y * cellSize, cellSize, cellSize);
        if (showPolicy) drawPolicyArrows(x, y);
      }
    }
  }
  agents.forEach((agent, i) => {
    ctx.fillStyle = ['red', 'blue', 'green'][i % 3];
    ctx.beginPath();
    ctx.arc(
      agent.x * cellSize + cellSize / 2,
      agent.y * cellSize + cellSize / 2,
      cellSize / 3,
      0,
      Math.PI * 2
    );
    ctx.fill();
  });
}

function resetMaze(preserveQ = false) {
  episode = 0;
  generateMaze();
  initializeAgents();
  if (!preserveQ) Q = {};
  drawMaze();
  updateParams();
  document.getElementById('episodeCounter').textContent = 'Episódio: 0';
  if (trainingInterval) clearInterval(trainingInterval);
  window.rewardHistory.length = 0;
  window.updateRewardChart();
}

function updateParams() {
  alpha = parseFloat(document.getElementById('alpha').value);
  gamma = parseFloat(document.getElementById('gamma').value);
  epsilon = parseFloat(document.getElementById('epsilon').value);
}

function initializeAgents() {
  agents = Array.from({ length: numAgents }, () => ({ x: 0, y: 0 }));
}

function getState(x, y) {
  return `${x},${y}`;
}

function chooseAction(x, y) {
  const state = getState(x, y);
  if (Math.random() < epsilon || !Q[state]) {
    return Math.floor(Math.random() * 4);
  }
  const values = Q[state];
  return values.indexOf(Math.max(...values));
}

function takeAction(x, y, action) {
  let nx = x, ny = y;
  if (action === 0 && y > 0) ny--;
  else if (action === 1 && y < rows - 1) ny++;
  else if (action === 2 && x > 0) nx--;
  else if (action === 3 && x < cols - 1) nx++;

  if (maze[ny][nx] === 1) {
    return [x, y, -10]; // penalidade maior por bater na parede
  }

  const goalX = cols - 1;
  const goalY = rows - 1;
  const distBefore = Math.abs(x - goalX) + Math.abs(y - goalY);
  const distAfter = Math.abs(nx - goalX) + Math.abs(ny - goalY);
  const progress = distBefore - distAfter;

  return [nx, ny, -1 + progress];
}

function updateQTable(x, y, action, reward, nx, ny) {
  const state = getState(x, y);
  const nextState = getState(nx, ny);

  if (!Q[state]) Q[state] = [0, 0, 0, 0];
  if (!Q[nextState]) Q[nextState] = [0, 0, 0, 0];

  Q[state][action] =
    Q[state][action] + alpha * (reward + gamma * Math.max(...Q[nextState]) - Q[state][action]);
}

function trainStep() {
  let episodeReward = 0;

  for (let a = 0; a < numAgents; a++) {
    let agent = agents[a];
    const action = chooseAction(agent.x, agent.y);
    const [nx, ny, reward] = takeAction(agent.x, agent.y, action);

    let done = false;
    if (nx === cols - 1 && ny === rows - 1) {
      updateQTable(agent.x, agent.y, action, 100, nx, ny);
      episodeReward += 100;
      done = true;
    } else {
      updateQTable(agent.x, agent.y, action, reward, nx, ny);
      episodeReward += reward;
    }

    agent.x = done ? 0 : nx;
    agent.y = done ? 0 : ny;
  }

  episode++;
  epsilon *= 0.999; // decaimento mais lento
  epsilon = Math.max(epsilon, 0.05);

  document.getElementById('episodeCounter').textContent = `Episódio: ${episode}`;
  window.rewardHistory.push(episodeReward);
  if (window.rewardHistory.length > 200) window.rewardHistory.shift();
  window.updateRewardChart();

  drawMaze();

  if (episode >= episodes) {
    clearInterval(trainingInterval);
    console.log('Treinamento finalizado.');
  }
}

function startTraining() {
  updateParams();
  if (trainingInterval) clearInterval(trainingInterval);
  trainingInterval = setInterval(trainStep, 50);
}

function pauseTraining() {
  if (trainingInterval) clearInterval(trainingInterval);
}

function resumeTraining() {
  if (!trainingInterval) {
    trainingInterval = setInterval(trainStep, 50);
  }
}

function stepTraining() {
  updateParams();
  trainStep();
}

function saveQTable() {
  localStorage.setItem('q_table', JSON.stringify(Q));
  alert('Q-Table salva no localStorage!');
}

function loadQTable() {
  const qData = localStorage.getItem('q_table');
  if (qData) {
    Q = JSON.parse(qData);
    alert('Q-Table carregada!');
  } else {
    alert('Nenhuma Q-Table salva encontrada.');
  }
  drawMaze();
}

function resetAll() {
  localStorage.removeItem('q_table');
  Q = {};
  resetMaze(false);
  alert("Q-Table apagada. Aprendizado reiniciado.");
}

function togglePolicy() {
  showPolicy = !showPolicy;
  drawMaze();
}

function openQTableInNewTab() {
  const newWindow = window.open('', '_blank');
  newWindow.document.write(`
    <html>
    <head>
      <title>Q-Table</title>
      <style>
        body { background: #121212; color: #eee; font-family: sans-serif; padding: 20px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px; border: 1px solid #555; text-align: center; }
        th { background: #7f5af0; }
        tr:hover { background: rgba(127, 90, 240, 0.15); }
      </style>
    </head>
    <body>
      <h1>Q-Table</h1>
      <table>
        <tr><th>Estado</th><th>↑</th><th>↓</th><th>←</th><th>→</th></tr>
  `);
  for (const state in Q) {
    newWindow.document.write(`<tr><td>${state}</td>`);
    Q[state].forEach(v => newWindow.document.write(`<td>${v.toFixed(2)}</td>`));
    newWindow.document.write(`</tr>`);
  }
  newWindow.document.write(`</table></body></html>`);
  newWindow.document.close();
}

// Inicialização
resetMaze(false);
const savedQ = localStorage.getItem('q_table');
if (savedQ) {
  Q = JSON.parse(savedQ);
  console.log("Q-Table carregada automaticamente.");
  drawMaze();
}
