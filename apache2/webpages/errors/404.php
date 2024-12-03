<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - Page Not Found</title>
    <link rel="stylesheet" href="../CSS/errors.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>404 - Page Not Found</h1>
        </div>
        <div class="content">
            <p>The page you're looking for doesn't exist.</p>
            <p>
                Return to 
                <a href="/" style="color: #00ff00; font-weight: bold;">Fondomarcador.com</a>
            </p>
        </div>
        <div>
            <?php
                // Obtener el esquema (http o https)
                $scheme = isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http";

                // Obtener el host (por ejemplo, pumukydev.com)
                $host = $_SERVER['HTTP_HOST'];

                // Obtener la ruta (por ejemplo, /2feb9a)
                $uri = $_SERVER['REQUEST_URI'];

                // Construir la URL completa
                $url = $scheme . "://" . $host . $uri;

                echo "La URL actual es: " . $url;

                $short_hash = basename($uri);

                // Construye la URL del servicio de Google para consultar el TXT record
                $dns_query_url = "https://dns.google/resolve?name=$short_hash.shortener.fondomarcador.com&type=TXT";

                // Realiza la solicitud al servicio de DNS de Google utilizando file_get_contents
                $response = file_get_contents($dns_query_url);

                // Verifica si la solicitud fue exitosa
                if ($response === false) {
                    header("HTTP/1.1 500 Internal Server Error");
                    echo "Error al consultar el servicio de DNS.";
                    exit;
                }

                // Decodifica la respuesta JSON
                $data = json_decode($response, true);

                // Verifica si hay respuestas TXT en el campo `Answer`
                if (!isset($data['Answer'])) {
                    header("HTTP/1.1 404 Not Found");
                    echo "URL no encontrada.";
                    exit;
                }

                // Obtén el último registro TXT (la URL larga)
                $txt_records = $data['Answer'];
                $last_record = end($txt_records);
                $long_url = $last_record['data'];

                // Limpia las comillas del contenido TXT
                $long_url = trim($long_url, '"');

                // Redirige al usuario a la URL larga
                header("Location: $long_url", true, 301);
                exit;
            ?>
        </div>
        <div class="footer">
            <p>&copy; 2024 Fondomarcador.com | All rights reserved.</p>
        </div>
    </div>
</body>
</html>

