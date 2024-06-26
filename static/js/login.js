$(document).ready(function() {
    $("#login").click(function(event) {
        event.preventDefault();

        // Get form data
        var username = $("#username").val();
        var password = $("#password").val();

        // Perform client-side validation (e.g., check for empty fields)

        // Make an AJAX request to your authentication API endpoint
        payload = {
            "email": username,
            "password": password
        }
        $.ajax({
            url: API_URL+"/login",
            type: "POST",
            data: JSON.stringify(payload),
            dataType: "JSON",
            contentType: "application/json",
            success: function(data) {
                if(checkVarError(data.error)) {
                    toastr.error(data.error)
                    return false;
                }
                // Successful login
                if(data.token && data.token!='') {
                    setCookie('token', data.token, cookieeExpireLimit);
                    window.location.href = "/my-carts"; // Redirect to the dashboard
                } else {
                    toastr.error("Invalid Access")
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                toastr.error(errorThrown)
            }
        });
    });
});