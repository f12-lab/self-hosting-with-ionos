> [!IMPORTANT]  
> This Readme is under construction

<!-- # Apache2 Configuration and Webpages

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

## Performance Tests

Apache Benchmark (`ab`) was used to evaluate the server’s performance. Multiple tests were conducted with varying concurrency (`-c`) and total requests (`-n`), both with and without headers.

### Testing Structure

#### Test 1: `-c 100` and `-n 1000` (Without Headers)
1. **/admin:**
   ```bash
   sudo ab -k -c 100 -n 1000 -A admin:asir https://fondomarcador.com/admin/
   ```
   
   ![info-ab1001000admin.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/1001000/admin/info-ab1001000admin.png)

2. **/fondomarcador.com** (SSL3 and TLS1.2):
   ```bash
   sudo ab -f SSL3 -k -c 100 -n 1000 https://fondomarcador.com/
   ```

   ![info-ab1001000SSL3.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/1001000/SSL3/info-ab1001000SSL3.png)

   ```bash
   sudo ab -f TLS1.2 -k -c 100 -n 1000 https://fondomarcador.com/
   ```

   ![info-ab1001000TLS1.2.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/1001000/TLS1.2/info-ab1001000TLS1.2.png)

3. **/logo.png:**
   ```bash
   sudo ab -k -c 100 -n 1000 https://fondomarcador.com/logo.png
   ```

   ![info-ab1001000foto.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/1001000/foto/info-ab1001000foto.png)

#### Test 2: `-c 100` and `-n 1000` (With Headers)
1. **/admin:**
   ```bash
   sudo ab -k -c 100 -n 1000 -A admin:asir -H "Accept-Encoding: gzip, deflate" https://fondomarcador.com/admin/
   ```

   ![info-Hab1001000admin.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/1001000%20header/admin/info-Hab1001000admin.png)

2. **/fondomarcador.com** (SSL3 and TLS1.2):
   ```bash
   sudo ab -f SSL3 -k -c 100 -n 1000 -H "Accept-Encoding: gzip, deflate" https://fondomarcador.com/
   ```

   ![info-Hab1001000SSL3.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/1001000%20header/SSL3/info-Hab1001000SSL3.png)

   ```bash
   sudo ab -f TLS1.2 -k -c 100 -n 1000 -H "Accept-Encoding: gzip, deflate" https://fondomarcador.com/
   ```

   ![info-Hab1001000TLS1.2.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/1001000%20header/TLS1.2/info-Hab1001000TLS1.2.png)

3. **/logo.png:**
   ```bash
   sudo ab -k -c 100 -n 1000 -H "Accept-Encoding: gzip, deflate" https://fondomarcador.com/logo.png
   ```

   ![info-Hab1001000foto.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/1001000%20header/foto/info-Hab1001000foto.png)

#### Test 3: `-c 1000` and `-n 10000` (Without Headers)
1. **/admin:**
   ```bash
   sudo ab -k -c 1000 -n 10000 -A admin:asir https://fondomarcador.com/admin/
   ```

   ![info-ab100010000admin.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/100010000/admin/info-ab100010000admin.png)

2. **/fondomarcador.com** (SSL3 and TLS1.2):
   ```bash
   sudo ab -f SSL3 -k -c 1000 -n 10000 https://fondomarcador.com/
   ```

   ![info-ab100010000SSL3.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/100010000/SSL3/info-ab100010000SSL3.png)

   ```bash
   sudo ab -f TLS1.2 -k -c 1000 -n 10000 https://fondomarcador.com/
   ```

   ![info-ab100010000TLS1.2.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/100010000/TLS1.2/info-ab100010000TLS1.2.png)

3. **/logo.png:**
   ```bash
   sudo ab -k -c 1000 -n 10000 https://fondomarcador.com/logo.png
   ```

   ![error-ab100010000foto.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/100010000/foto!!!/error-ab100010000foto.png)

   ![info-ab100010000foto.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/100010000/foto!!!/info-ab100010000foto.png)

#### Test 4: `-c 1000` and `-n 10000` (With Headers)
1. **/admin:**
   ```bash
   sudo ab -k -c 1000 -n 10000 -A admin:asir -H "Accept-Encoding: gzip, deflate" https://fondomarcador.com/admin/
   ```

   ![info-Hab100010000admin.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/100010000header/admin/info-Hab100010000admin.png)

2. **/fondomarcador.com** (SSL3 and TLS1.2):
   ```bash
   sudo ab -f SSL3 -k -c 1000 -n 10000 -H "Accept-Encoding: gzip, deflate" https://fondomarcador.com/
   ```

   ![info-Hab100010000SSL3.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/100010000header/SSL3/info-Hab100010000SSL3.png)

   ```bash
   sudo ab -f TLS1.2 -k -c 1000 -n 10000 -H "Accept-Encoding: gzip, deflate" https://fondomarcador.com/
   ```

   ![info-Hab100010000TLS1.2.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/100010000header/TLS1.2/info-Hab100010000TLS1.2.png)

3. **/logo.png:**
   ```bash
   sudo ab -k -c 1000 -n 10000 -H "Accept-Encoding: gzip, deflate" https://fondomarcador.com/logo.png
   ```

   ![error-Hab100010000foto.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/100010000header/foto!!!/error-Hab100010000foto.png)

   ![info-Hab100010000foto.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/100010000header/foto!!!/info-Hab100010000foto.png)

### Observations

1. Under higher loads (`-c 1000`, `-n 10000`), static resources like `/logo.png` caused server saturation, leading to errors and downtime.

![serverDown.png](https://github.com/M-L56/self-hosting-with-ionos/blob/44bed96fff5f720ed74e53f46b126dda28fd794d/images/performance/100010000header/foto!!!/serverDown.png)

2. Dynamic routes like `/admin` showed better resilience under moderate load but struggled with higher concurrency.
3. Adding headers helped reduce overall bandwidth usage but didn’t entirely mitigate server overload.

### Recommendations

- Optimize static resource delivery by enabling caching mechanisms or integrating a CDN.
- Increase server scalability to handle heavy concurrency and high request volumes.
- Regularly test server capacity and fine-tune configurations using tools like Grafana and Prometheus for real-time insights.

---

## Conclusion
This directory integrates essential configurations and functionalities for `fondomarcador.com`. It combines Apache2’s flexibility with a custom URL shortener to provide a secure and robust web experience. For detailed provisioning, refer to the [apache.yml](../ansible/tasks/apache.yml) file. While functional under typical load, the system experiences performance issues during high concurrency tests. These observations underscore the importance of proactive scaling and caching strategies to enhance reliability during peak traffic periods. -->