function setCookie(cookieName, cookieValue, minutesToExpire) {
    var currentDate = new Date();
    currentDate.setTime(currentDate.getTime() + (minutesToExpire * 60 * 1000));
    var expires = "expires=" + currentDate.toUTCString();
    document.cookie = cookieName + "=" + cookieValue + "; " + expires + "; path=/";
}

function getCookie(cookieName) {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(cookieName + '=')) {
            return cookie.substring(cookieName.length + 1);
        }
    }
    return null; // Cookie not found
}

function deleteAllCookies() {
    const cookies = document.cookie.split(";");

    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const eqPos = cookie.indexOf("=");
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
    }
    location.reload();
}

function tokenDecode(tokenStr) {
    if(!checkVarError(tokenStr)) {
        window.location.href = APP_URL;
    }
    // Split the token into header, payload, and signature parts
    const parts = tokenStr.split('.');
    
    if (parts.length !== 3) {
        throw new Error('Invalid JWT format');
    }
    
    // Decode the payload (the second part) using base64 decoding
    const decodedPayload = atob(parts[1]);
    
    // Parse the decoded payload as JSON to get the claims
    const claims = JSON.parse(decodedPayload);
    return claims;
}

function checkVarError(decVar) {
	if(typeof decVar !== 'undefined' && decVar != null && (decVar.length > 0 || Object.keys(decVar).length > 0) ){
		return true;
	}else{
		return false;
	}
}

function getQueryParameters() {
    const queryParams = new URLSearchParams(window.location.search);
    const params = {};
    for (const [key, value] of queryParams.entries()) {
        params[key] = value;
    }
    return params;
}

function pageRedirect(page) {
    window.location.href = APP_URL+"/"+page;
}