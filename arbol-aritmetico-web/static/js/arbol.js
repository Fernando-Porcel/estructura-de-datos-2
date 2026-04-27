let expresion = ''

function esOperador(caracter) {
    return ['+', '-', '*', '/', '^'].includes(caracter)
}

function presionar(caracter) {
    if (caracter === 'C') {
        expresion = ''
        document.getElementById('expresion-display').textContent = '0'
        document.getElementById('resultado-display').textContent = ''
        limpiarArbol()
        return
    }

    if (expresion == '' && ['+', '*', '/', '^'].includes(caracter)) return
    
    if (expresion == '-' && esOperador(caracter)) return

    if (caracter === '.' && expresion.at(-1) === '.') return

    if (expresion !== '' && esOperador(caracter) && esOperador(expresion.at(-1))) {
        expresion = expresion.slice(0, -1) + caracter
    }else {
        expresion += caracter
    }

    document.getElementById('expresion-display').textContent = expresion
    document.getElementById('resultado-display').textContent = ''
}

function borrar() {
    expresion = expresion.slice(0, -1)
    if (expresion != '') {
        document.getElementById('expresion-display').textContent = expresion
        document.getElementById('resultado-display').textContent = ''
    } else {
        document.getElementById('expresion-display').textContent = '0'
    }
}

function calcular() {
    if (expresion == '') return;

    fetch('/evaluar', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({expresion: expresion})
    })
    .then(response => response.json())
    .then(datos => {
        if (datos.error) {
            document.getElementById('resultado-display').textContent = datos.error;
            expresion = ''
            limpiarArbol()
        } else {
            document.getElementById('resultado-display').textContent = datos.resultado;
            expresion = String(datos.resultado)
            dibujarArbol(datos.arbol)
        }
        document.getElementById('expresion-display').textContent = ''
    })
}

function limpiarArbol() {
    const svg = document.getElementById('svg-arbol');
    svg.innerHTML = '';
    document.getElementById('mensaje-arbol').style.display = 'flex';
}
 
function dibujarArbol(raiz) {
    const svg = document.getElementById('svg-arbol');
    svg.innerHTML = '';
 
    document.getElementById('mensaje-arbol').style.display = 'none';
    const ancho = svg.clientWidth;
 
    dibujarNodo(svg, raiz, ancho / 2, 50, 0, ancho, ancho / 2, 50);
}
 
function dibujarNodo(svg, nodo, x, y, xMin, xMax, xPadre, yPadre) {
    if (nodo === null) return;
 
    // Línea hacia el padre (no dibuja para la raíz)
    if (x !== xPadre || y !== yPadre) {
        dibujarLinea(svg, xPadre, yPadre, x, y);
    }
 
    const esOpe = esOperador(nodo.valor);
 
    dibujarCirculo(svg, x, y, esOpe);
    dibujarTexto(svg, x, y, nodo.valor);
 
    // Recursión hijos
    dibujarNodo(svg, nodo.izquierdo, (xMin + x) / 2, y + 60, xMin, x, x, y);
    dibujarNodo(svg, nodo.derecho, (x + xMax) / 2, y + 60, x, xMax, x, y);
}
 
function dibujarLinea(svg, x1, y1, x2, y2) {
    const radio = 16;
    const angulo = Math.atan2(y2 - y1, x2 - x1);
    
    // La línea empieza en el borde del círculo padre
    const inicioX = x1 + Math.cos(angulo) * radio;
    const inicioY = y1 + Math.sin(angulo) * radio;
    
    // La línea termina en el borde del círculo hijo
    const finX = x2 - Math.cos(angulo) * radio;
    const finY = y2 - Math.sin(angulo) * radio;

    const linea = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    linea.setAttribute('x1', inicioX);
    linea.setAttribute('y1', inicioY);
    linea.setAttribute('x2', finX);
    linea.setAttribute('y2', finY);
    linea.setAttribute('stroke', '#6b7280');
    linea.setAttribute('stroke-width', '1.5');
    svg.appendChild(linea);
}
 
function dibujarCirculo(svg, x, y, esOpe) {
    const circulo = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circulo.setAttribute('cx', x);
    circulo.setAttribute('cy', y);
    circulo.setAttribute('r', 16);
    circulo.setAttribute('fill', esOpe ? '#00d4aa' : '#151c24');
    circulo.setAttribute('stroke', esOpe ? '#00d4aa' : '#1e2a36');
    circulo.setAttribute('stroke-width', '1.5');
    svg.appendChild(circulo);
}
 
function dibujarTexto(svg, x, y, valor) {
    const texto = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    texto.setAttribute('x', x);
    texto.setAttribute('y', y);
    texto.setAttribute('text-anchor', 'middle');
    texto.setAttribute('dominant-baseline', 'central');
    texto.setAttribute('fill', esOperador(valor) ? '#0a0e12' : '#ffffff');
    texto.setAttribute('font-size', '14');
    texto.setAttribute('font-weight', '600');
    texto.setAttribute('font-family', 'JetBrains Mono, monospace');
    texto.textContent = valor;
    svg.appendChild(texto);
}