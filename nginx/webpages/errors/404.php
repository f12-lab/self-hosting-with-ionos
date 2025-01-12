<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - Page Not Found</title>
    <link rel="stylesheet" href="../CSS/all.css">
</head>
<body>
    <canvas id="canvas"></canvas>
    
    <div class="container">
        <div class="header">
            <h1>404 - Page Not Found</h1>
        </div>
        <div class="content">
            <p>The page you're looking for doesn't exist.</p>
            <p>
                Return to 
                <a href="/" class="button" style="display: inline;">Fondomarcador.com</a>
            </p>
        </div>
    </div>

    <div class="footer">
        <p>&copy; 2024 Fondomarcador.com | All rights reserved.</p>
    </div>
    
    <script src="../index.js"></script>
</body>
</html>

<?php
// Obtener el esquema (http o https)
$scheme = isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http";

// Obtener el host (por ejemplo, pumukydev.com)
$host = $_SERVER['HTTP_HOST'];

// Obtener la ruta (por ejemplo, /2feb9a)
$uri = $_SERVER['REQUEST_URI'];

// Construir la URL completa
$url = $scheme . "://" . $host . $uri;

$short_hash = basename($uri);

// Construye la URL del servicio de Google para consultar el TXT record
$dns_query_url = "https://dns.google/resolve?name=$short_hash.shortener.fondomarcador.com&type=TXT";

// Intentar realizar la solicitud al servicio de DNS de Google
$response = file_get_contents($dns_query_url);

// Si la solicitud falló, escribe en los logs de errores
if ($response === false) {
    error_log("Error en la consulta DNS para el hash: $short_hash");
    header("HTTP/1.1 404 Not Found");
    exit;
}

// Decodificar la respuesta JSON
$data = json_decode($response, true);

// Verificar si la respuesta contiene los registros TXT
if (!isset($data['Answer'])) {
    error_log("No se encontraron registros TXT para el hash: $short_hash");
    header("HTTP/1.1 404 Not Found");
    exit;
}

// Obtener el último registro TXT (la URL larga)
$txt_records = $data['Answer'];
$last_record = end($txt_records);
$long_url = $last_record['data'];

// Eliminar las comillas que pueden existir alrededor de la URL larga
$long_url = trim($long_url, '"');

// Redirigir al usuario a la URL larga
header("Location: $long_url", true, 301);
exit;
?>
