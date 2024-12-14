# Apache2 Configuration and Webpages

## Apache2 Configuration Files

### Overview
This directory contains configuration files for the Apache2 web server. The main configuration remains untouched, and customizations are handled via the `fondomarcador.conf` file.

### `apache2.conf`
No modifications have been made to this file. It retains its default configuration, which includes essential directives for the Apache2 server.

### `fondomarcador.conf`
This is the primary virtual host configuration file. It manages multiple functionalities for the `fondomarcador.com` domain, including redirects, authentication, and SSL handling.

#### Configuration Details

1. **HTTP to HTTPS Redirection:**
   - All traffic on port 80 is permanently redirected to HTTPS for secure connections.

2. **DocumentRoot:**
   - Points to `/var/www/webpages` where the website files are hosted.

3. **Custom Error Pages:**
   - `404 Not Found`: Redirected to `/errors/404.php`.
   - `401 Unauthorized`: Redirected to `/errors/401.html`.

4. **Logo File Handling:**
   - The file `logo.png` is set to download automatically when accessed.

5. **Admin Directory Protection:**
   - The `/admin` directory is password-protected using Basic Authentication.
   - Users must authenticate via credentials stored in `/etc/apache2/.htpasswd_admin`.

6. **Server Status:**
   - Accessing `/status` requires `sysadmin` credentials from `/etc/apache2/.htpasswd_sysadmin`.
   - Redirects to a specific Grafana dashboard for server monitoring.

7. **Proxy for Grafana:**
   - Configures `grafana.fondomarcador.com` to proxy traffic to Grafana’s service running on `localhost:3000`.

8. **SSL Setup:**
   - Includes paths for SSL certificate files to enable secure HTTPS connections.
   - Directives like `SSLCertificateFile`, `SSLCertificateKeyFile`, and `SSLCertificateChainFile` are set.

---

## Webpages Directory

The `webpages` directory contains all the HTML, PHP, and resource files for the site. Below is an explanation of its structure and functionality:

### Structure
```plaintext
webpages/
├── index.html
├── logo.png
├── README.md
├── admin/
│   ├── admin.html
│   └── image.png
├── CSS/
│   ├── admin.css
│   ├── errors.css
│   ├── index.css
│   └── shortener.css
├── errors/
│   ├── 401.html
│   └── 404.php
└── shortener/
    ├── index.php
    ├── get_long_url.sh
    ├── get_url.sh
    └── post_txt.sh
```

### Description

1. **Root Files:**
   - `index.html`: Homepage of the site.
   - `logo.png`: The site logo, downloadable when accessed.

2. **Admin Section:**
   - Password-protected directory containing `admin.html` for managing internal resources.

3. **CSS Directory:**
   - Contains stylesheets for various pages, including the shortener and error pages.

4. **Error Pages:**
   - `401.html`: Unauthorized access page.
   - `404.php`: Not Found page. It checks the requested hash against DNS TXT records to see if it corresponds to a stored long URL.
     - If a valid long URL is found, the user is redirected to it.
     - Otherwise, it displays a custom 404 message.

5. **Shortener Section:**
   - A robust URL shortener tool, detailed below.

---

## URL Shortener Functionality

### How It Works
The `shortener` section allows users to create shortened URLs for easier sharing. It integrates with the IONOS DNS API to register mappings between shortened hashes and the full URLs.

#### `index.php`
- Displays a simple interface where users can input a long URL to be shortened.
- Processes the request using the following steps:
  1. Generate a 6-character hash of the input URL.
  2. Save the hash and corresponding long URL to DNS records via `post_txt.sh`.
  3. Provide the user with the shortened URL (e.g., `https://fondomarcador.com/<hash>`).

#### 404 Redirect Handling
- When a user visits a shortened URL, the `404.php` page is triggered if the hash isn’t matched to a file.
- The script:
  1. Extracts the hash from the requested URI.
  2. Queries Google’s DNS service for a TXT record matching the hash.
  3. If a TXT record exists, retrieves the long URL and redirects the user.
  4. If no record is found, displays a custom 404 error.

#### Supporting Shell Scripts

1. **`post_txt.sh`:**
   - Sends a POST request to the IONOS API to create a DNS TXT record mapping the hash to the long URL.

2. **`get_long_url.sh`:**
   - Fetches the long URL from the TXT record using the hash.
   - Queries DNS via `curl` and processes the response.

3. **`get_url.sh`:**
   - Fetches the entire DNS record for the short URL and parses the relevant data.

### Security
Sensitive information like API keys and zone IDs are stored in an `.env` file to ensure they are not exposed.

### Usage Example
1. Access the URL Shortener page at `https://fondomarcador.com/shortener`.
2. Enter the long URL and click on "Shorten".
3. A shortened URL will be displayed, ready for sharing.
4. The mapping is automatically stored in the DNS system for resolution.
5. Attempting to visit a shortened URL checks its existence via the `404.php` logic.

---

## Performance tests

---

## Conclusion
This directory integrates essential configurations and functionalities for `fondomarcador.com`. It combines Apache2’s flexibility with a custom URL shortener to provide a secure and robust web experience. For detailed provisioning, refer to the [apache.yml](../ansible/tasks/apache.yml) file.