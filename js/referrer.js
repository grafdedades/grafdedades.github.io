// Comprova que s'ha accedit des de la pàgina de login

var login_url = "https://grafdedades.github.io/";
var ref = document.referrer;

if (ref != login_url) {
    window.location.replace(login_url);
    window.location.href = login_url;
    window.location = login_url;
}
