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
    <title>Acortador de URL</title>
    <link rel="stylesheet" href="../CSS/shortener.css">
</head>
<body>
    <main>
        <a href="/" class="back-button">Return to Home</a>
        
        <h1>URL Shortener</h1>
        <p>Use this tool to shorten your links.</p>

        <form action="index.php" method="POST">
            <label for="long_url">Long URL:</label>
            <input type="text" id="long_url" name="long_url" placeholder="https://example.com" required />
            <br>
            <button type="submit">Shorten</button>
        </form>

        <?php if (isset($message)) { ?>
            <div class="message"><?= $message; ?></div>
        <?php } ?>

    </main>
</body>
</html>

