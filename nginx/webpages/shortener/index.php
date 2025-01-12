<?php

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $long_url = $_POST['long_url'];

    $short_hash = substr(hash('sha256', $long_url), 0, 6);
    $short_url = "fondomarcador.com/$short_hash";

    $script_path = realpath("post_txt.sh"); 
    $command = "bash $script_path $short_hash \"$long_url\""; 
    exec($command, $output, $return_var);

    if ($return_var === 0) {
        $message = "Your shortened URL is: <a href='https://$short_url' target='_blank'>$short_url</a>";
    } else {
        $message = "There was an error creating the shortened URL. Please try again.";
    }
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Shortener - Fondomarcador.com</title>
    <link rel="stylesheet" href="../CSS/all.css">
</head>
<body>
    <canvas id="canvas"></canvas>

    <a href="/" class="return-button">
        <span class="exit-icon">
            <img src="../CSS/run.png" alt="Exit Stickman Running" width="24px" />
        </span>
        <span class="exit-text">EXIT</span>
    </a>

    <div class="container">
        <div class="header">
            <h1>URL Shortener</h1>
        </div>

        <div class="content">
            <p>Use this tool to shorten your links and share them with ease.</p>

            <form action="index.php" method="POST">
                <label for="long_url">Long URL:</label>
                <input type="text" id="long_url" name="long_url" placeholder="https://example.com" required />
                <button type="submit" class="button">Shorten</button>
            </form>

            <?php if (isset($message)) { ?>
                <div class="message">
                    <?= $message; ?>
                </div>
            <?php } ?>
        </div>
    </div>

    <div class="footer">
        <p>&copy; 2024 Fondomarcador.com | All rights reserved.</p>
    </div>
    
    <script src="../index.js"></script>
</body>
</html>
