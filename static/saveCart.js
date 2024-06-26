$(document).ready(function() {
    userToken = getCookie('token')
    decoded_token = tokenDecode(userToken)
    var params = getQueryParameters();
    $.ajax({
        url: API_URL+"/get-default-items", // Replace with your API endpoint
        type: "POST",
        dataType: "JSON",
        data: JSON.stringify({'cart_id':params['cart_id']}),
        contentType: "application/json",
        headers: {
            "Authorization": "Bearer " + userToken
        },
        success: function(data) {
            console.log(data)
            if(typeof data['data']!=='undefined' && typeof data['data']['cart_name']!=='undefined') {
                let cart_data = data.data;
                $("#cart_head").html(cart_data['cart_name'])
                let items = cart_data.item_json;
                var cart_html = ``;
                cart_html += `<div id="accordion">`;
                $.each(items,function(category,allItems){
                    cart_html += `<div class="card">
                    <div class="card-header" id="`+category+`_heading">
                        <h5 class="mb-0">
                            <button class="btn btn-link" data-toggle="collapse" data-target="#`+category+`_collapse" aria-expanded="true" aria-controls="collapseOne">
                                `+category+`
                            </button>
                        </h5>
                    </div>
        
                    <div id="`+category+`_collapse" class="collapse show" aria-labelledby="`+category+`_heading" data-parent="#accordion">
                        <div class="card-body" id="myCartsDiv">`;

                        $.each(allItems,function(index,itemDetail){
                            cart_html += `<div class="row mb-3">`+itemDetail['name']+`</div>`;
                        })
                            
                        cart_html += `</div>
                    </div>
                </div>`;
                }) 
                cart_html += `</div>`;
                $("#cartDispDiv").html(cart_html);
            } else {
                $("#cartDispDiv").html("No Cart Found");
            }
        },
        error: function(xhr, textStatus, errorThrown) {
            // Failed login
            $("#error-message").removeClass("hidden");
        }
    });
});