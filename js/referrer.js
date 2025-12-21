// Comprova que s'ha accedit des de la pàgina de login
// Uses sessionStorage instead of referrer (Cloudflare tunnels strip the Referer header)

var currentOrigin = window.location.origin;
var login_url = currentOrigin + "/";

// Check if password was set via the login page (stored in sessionStorage)
var password = sessionStorage.getItem("pass");

if (!password) {
    // No password in session = user didn't come through login
    window.location.replace(login_url);
}

