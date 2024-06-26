g_all_categories_item = {};
g_all_categories = {};

function getAllCatItems() {
    return new Promise(function(resolve, reject) {
        if( checkVarError(getCookie('all_categories_item')) && checkVarError(getCookie('all_categories')) ) {
            g_all_categories = JSON.parse(getCookie('all_categories'))
            g_all_categories_item = JSON.parse(getCookie('all_categories_item'))
            resolve();
        } else {
            $.ajax({
                url: API_URL+"/get-default-items",
                type: "POST",
                dataType: "JSON",
                contentType: "application/json",
                headers: {
                    "Authorization": "Bearer " + userToken
                },
                success: function(data) {
                    if(checkVarError(data.error)) {
                        toastr.error(data.error)
                        return false;
                    }
                    add_cart_html = ``;
                    if(data.all_categories_item) {
                        g_all_categories_item = data.all_categories_item;
                    }
                    if(data.all_categories) {
                        g_all_categories = data.all_categories;
                    }
                    setCookie('all_categories_item', JSON.stringify(g_all_categories_item), cookieeExpireLimit);
                    setCookie('all_categories', JSON.stringify(g_all_categories), cookieeExpireLimit);
                    console.log("cookies added")
                    resolve();
                },
                error: function(xhr, textStatus, errorThrown) {
                    reject(errorThrown);
                    toastr.error(errorThrown)
                }
            });
        }
    });
}


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

function assigneeCheck(thisEle, assigned_to, cart_id) {
    var URL = APP_URL+"/remove-assignee";
    var msg = "Assignee Removed"
    if($(thisEle).prop('checked')) {
        URL = APP_URL+"/add-assignee";
        msg = "Assignee Added"
    }
    payload = {
        "cart_id": cart_id,
        "assigned_to": assigned_to
    }
    $.ajax({
        url: URL,
        type: "POST",
        dataType: "JSON",
        data: JSON.stringify(payload),
        contentType: "application/json",
        headers: {
            "Authorization": "Bearer " + userToken
        },
        success: function(data) {
            if(checkVarError(data.error)) {
                toastr.error(data.error)
                return false;
            }
            toastr.success(msg)
        },
        error: function(xhr, textStatus, errorThrown) {
            toastr.error(errorThrown)
        }
    });
}

function editThis() {
    var params = getQueryParameters();
    editCart(params['cart_id'])
}

function viewCart(cart_id) {
    window.location.href = "/view-cart?cart_id="+cart_id;
}
function createCart() {
    window.location.href = "/add-new-cart";
}
function editCart(cart_id) {
    window.location.href = "/edit-cart?cart_id="+cart_id;
}
function delCart(cart_id) {
    payload = {
        "cart_id": cart_id
    }
    $.ajax({
        url: APP_URL+"/del-cart",
        type: "POST",
        dataType: "JSON",
        data: JSON.stringify(payload),
        contentType: "application/json",
        headers: {
            "Authorization": "Bearer " + userToken
        },
        success: function(data) {
            if(checkVarError(data.error)) {
                toastr.error(data.error)
                return false;
            }
            toastr.success("Cart Deleted")
            setTimeout(function(){
                location.reload();
            },1000)
        },
        error: function(xhr, textStatus, errorThrown) {
            toastr.error(errorThrown)
        }
    });
}




$(document).on("input",".search_item_input", function(){
    let cat_id = $(this).attr("cat-id");
    let searchText = $(this).val().toLowerCase();

    $("#cat_items_"+cat_id+" .button-checkbox").each(function() {
        var divText = $(this).find("input").attr("item-name").toLowerCase();
        console.log(divText)
        if (divText.includes(searchText)) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
    
})