var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');

// Configuración de fuente y número de gotas
var fontSize = 16;
var str = "01";

// Inicializar el array de gotas
var drops = [];

// Función para redimensionar el canvas y garantizar que cubra la altura total del contenido
function resizeCanvas() {
    canvas.width = window.innerWidth; // Ajustar el ancho
    canvas.height = document.documentElement.scrollHeight; // Ajustar la altura al contenido total de la página
    initializeDrops();  // Reiniciar las gotas tras redimensionar
}

// Función para inicializar las gotas
function initializeDrops() {
    var columns = Math.floor(canvas.width / fontSize); // Número de columnas basadas en el ancho
    drops = [];

    // Inicializamos las gotas aleatoriamente
    for (var i = 0; i < columns; i++) {
        drops.push(Math.random() * canvas.height); // Las gotas comienzan en posiciones aleatorias
    }
}

// Función para dibujar las gotas en el canvas
function draw() {
    // Aplica un fondo oscuro translúcido para el "efecto de lluvia"
    context.fillStyle = "rgba(0, 0, 0, 0.05)";
    context.fillRect(0, 0, canvas.width, canvas.height); // Rellena todo el canvas

    context.font = fontSize + "px monospace"; // Fuente
    context.fillStyle = "#00ff00";  // Color de las gotas

    // Dibuja las gotas en pantalla
    for (var i = 0; i < drops.length; i++) {
        var char = str[Math.floor(Math.random() * str.length)];
        var x = i * fontSize;  // Posición x, depende de la columna
        var y = drops[i] * fontSize; // Posición y, depende de la gota

        context.fillText(char, x, y);  // Dibuja la gota

        // Si la gota llega al fondo, vuelve a subir a una posición aleatoria
        if (y >= canvas.height && Math.random() > 0.98) {
            drops[i] = 0;
        } else {
            drops[i]++;
        }
    }
}

// Llamar a resizeCanvas y initializeDrops al cargar la página
resizeCanvas();  // Asegura el canvas correcto al cargar
initializeDrops();

// Ejecuta el dibujo de las gotas a intervalos regulares
setInterval(draw, 35);

// Llama a resizeCanvas cuando cambie el tamaño de la ventana
window.addEventListener("resize", function () {
    resizeCanvas();  // Redimensiona el canvas cuando cambie el tamaño de la ventana
});
