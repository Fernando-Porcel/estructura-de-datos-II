// view/static/juego.js

const selectorModo = document.getElementById('modo');
const botonNueva = document.getElementById('btn-nueva');
const textoMensaje = document.getElementById('mensaje');
const casillas = document.querySelectorAll('.casilla');
const metricaNodos = document.getElementById('metrica-nodos');
const metricaTiempo = document.getElementById('metrica-tiempo');
const selectorDificultad = document.getElementById('dificultad');

function dibujar(estado) {
    const terminada = estado.ganador !== null || estado.empate;

    casillas.forEach(boton => {
        const fila = Number(boton.dataset.fila);
        const columna = Number(boton.dataset.columna);
        const ficha = estado.casillas[fila][columna];

        boton.textContent = ficha.trim();
        boton.classList.toggle('x', ficha === 'X');
        boton.classList.toggle('o', ficha === 'O');
        boton.disabled = ficha !== ' ' || terminada;
    });

    textoMensaje.textContent = estado.mensaje;
    metricaNodos.textContent = estado.nodos;
    metricaTiempo.textContent = estado.tiempo;
}

async function nuevaPartida() {
    const respuesta = await fetch('/api/nueva', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ modo: selectorModo.value, dificultad: selectorDificultad.value }),
    });
    const datos = await respuesta.json();

    if (!respuesta.ok) {
        textoMensaje.textContent = datos.error;
        return;
    }
    dibujar(datos);
}

botonNueva.addEventListener('click', nuevaPartida);

// La dificultad solo se usa en el modo Minimax
function actualizarDificultad() {
    selectorDificultad.disabled = selectorModo.value !== 'humano_vs_minimax';
}
selectorModo.addEventListener('change', actualizarDificultad);

async function jugar(fila, columna) {
    // Bloqueamos el tablero mientras el servidor responde (Minimax puede tardar)
    casillas.forEach(boton => boton.disabled = true);

    const respuesta = await fetch('/api/jugar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fila: fila, columna: columna }),
    });
    const datos = await respuesta.json();

    if (!respuesta.ok) {
        await cargarEstado();               // restablece el tablero tal como está
        textoMensaje.textContent = datos.error;
        return;
    }
    dibujar(datos);
}

casillas.forEach(boton => {
    boton.addEventListener('click', () => {
        jugar(Number(boton.dataset.fila), Number(boton.dataset.columna));
    });
});

async function cargarEstado() {
    const respuesta = await fetch('/api/estado');
    const estado = await respuesta.json();

    if (estado) {
        selectorModo.value = estado.modo;
        if (estado.dificultad) selectorDificultad.value = estado.dificultad;
        actualizarDificultad();
        dibujar(estado);
    } else {
        // Todavía no hay partida: nada se puede pulsar
        casillas.forEach(boton => boton.disabled = true);
    }
}

actualizarDificultad();
cargarEstado();