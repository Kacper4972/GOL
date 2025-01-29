const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const cellSize = 20;
const rows = 20;
const cols = 20;
canvas.width = cols * cellSize;
canvas.height = rows * cellSize;

let intervalId = null;
let grid = [];  // Przechowywanie aktualnego stanu planszy

// Pobranie aktualnej planszy z serwera
async function fetchGrid() {
    const response = await fetch("/get_grid");
    grid = await response.json();
    drawGrid();
}

// Rysowanie planszy na canvasie
function drawGrid() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let row = 0; row < rows; row++) {
        for (let col = 0; col < cols; col++) {
            if (grid[row][col] === 1) {
                ctx.fillStyle = "black";
                ctx.fillRect(col * cellSize, row * cellSize, cellSize, cellSize);
            } else {
                ctx.strokeStyle = "gray";
                ctx.strokeRect(col * cellSize, row * cellSize, cellSize, cellSize);
            }
        }
    }
}

// Kliknięcie na komórkę (zmiana jej stanu, jeśli symulacja jest zatrzymana)
canvas.addEventListener("click", async (event) => {
    if (intervalId !== null) return; // Jeśli symulacja działa, nie można edytować

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const col = Math.floor(x / cellSize);
    const row = Math.floor(y / cellSize);

    grid[row][col] = grid[row][col] === 1 ? 0 : 1; // Przełączamy stan komórki
    drawGrid();

    // Aktualizacja stanu w backendzie
    await fetch("/update_grid", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ grid })
    });
});

// Generowanie nowej generacji
async function nextGeneration() {
    const response = await fetch("/next_generation", { method: "POST" });
    grid = await response.json();
    drawGrid();
}

// Start symulacji (powtarza co 500ms)
function startSimulation() {
    if (!intervalId) {
        intervalId = setInterval(nextGeneration, 500);
    }
}

// Stop symulacji
function stopSimulation() {
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
}

// Losowa plansza
async function generateRandomGrid() {
    await fetch("/random_grid", { method: "POST" });
    fetchGrid();
}

// Funkcja do zapisywania symulacji
async function saveSimulation() {
    const simName = prompt("Podaj nazwę dla zapisanej symulacji:");
    if (!simName) return;

    const response = await fetch("/save_simulation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: simName })
    });

    const result = await response.json();
    if (result.success) {
        alert("Symulacja zapisana!");
    } else {
        alert("Błąd zapisu symulacji.");
    }
}

// Obsługa przycisków
document.getElementById("startBtn").addEventListener("click", startSimulation);
document.getElementById("stopBtn").addEventListener("click", stopSimulation);
document.getElementById("randomBtn").addEventListener("click", generateRandomGrid);
document.getElementById("saveBtn").addEventListener("click", saveSimulation);

// Pobranie aktualnej planszy po załadowaniu strony
document.addEventListener("DOMContentLoaded", fetchGrid);


// Pobranie i narysowanie początkowej planszy
fetchGrid();

