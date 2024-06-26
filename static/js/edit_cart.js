var params = getQueryParameters();
var cart_id = params['cart_id']
$(document).ready(function() {
    userToken = getCookie('token')
    decoded_token = tokenDecode(userToken)
    // $.when(getAllCatItems()).done(function(response){
    //     getCartDetail()
    // })
    getAllCatItems()
    .then(function () {
        return getCartDetail();
    })
    .then(function () {
        
    })
    .catch(function (error) {
        console.error("At least one operation failed:", error);
    });

});

function getCartDetail() {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: API_URL+"/get-cart",
            type: "POST",
            dataType: "JSON",
            data: JSON.stringify({'cart_id':params['cart_id']}),
            contentType: "application/json",
            headers: {
                "Authorization": "Bearer " + userToken
            },
            success: function(data) {
                if(checkVarError(data.error)) {
                    toastr.error(data.error)
                    reject(errorThrown)
                    return false;
                }
                g_allItem = {}
                if(data.data) {
                    var cart_data = data.data;
                    $("#cart_name").val(cart_data['cart_name'])
                    var cart_item_json = cart_data['item_json'];
                    $.each(cart_item_json, function(catId,catItems){
                        $.each(catItems, function(itemIndex,itemDetail){
                            g_allItem[itemDetail['id']] = itemDetail
                        })
                    })

                }
                generateEditCartHtml();
                resolve();
            },
            error: function(xhr, textStatus, errorThrown) {
                toastr.error(errorThrown)
                reject(errorThrown)
            }
        })
    })
}

function generateEditCartHtml() {
    var add_cart_html = ``;
    if(Object.keys(g_all_categories).length>0) {
        for(var index in g_all_categories) {
            var category_data = g_all_categories[index]
            add_cart_html += `<div class="card">
                <div class="card-header" category_id="`+category_data['category_id']+`" id="heading_`+category_data['category_name']+`">
                    <h5 class="mb-0">
                        <button class="btn btn-link" data-toggle="collapse" data-target="#collapse_`+category_data['category_name']+`" aria-expanded="true" aria-controls="collapse_`+category_data['category_name']+`">
                            `+category_data['category_name']+`
                        </button>
                    </h5>
                </div>

                <div id="collapse_`+category_data['category_name']+`" class="collapse show" aria-labelledby="heading_`+category_data['category_name']+`" data-parent="#accordion">
                    <div class="card-body">
                    <div class="row mb-2"><input type="text" class="form-control search_item_input" cat-id="`+category_data['category_id']+`" id="search_`+category_data['category_id']+`" placeholder="Search `+category_data['category_name']+`"></div>
                    <div class="row"><div id="cat_items_`+category_data['category_id']+`" class="all_cat_items d-flex flex-wrap btn-group" role="group" aria-label="Checkbox Buttons">`;
                        this_category_item = g_all_categories_item[category_data['category_id']];
                        $(this_category_item).each(function(itemIndex,itemDetails){
                            // _`+itemDetails['item_id']+`
                            let checked = '';
                            if(checkVarError(g_allItem[itemDetails['item_id']])) {
                                checked = 'checked';
                            }
                            let itemPurchased = ``;
                            if(checkVarError(g_allItem[itemDetails['item_id']]) && checkVarError(g_allItem[itemDetails['item_id']]['item_purchased'])) {
                                itemPurchased = 'purchased_item';
                            }
                            add_cart_html += `<div class="button-checkbox `+itemPurchased+`">
                            <input class="itemCheckBox" type="checkbox" item-id="`+itemDetails['item_id']+`" item-name="`+itemDetails['item_name'].toLowerCase()+`" id="button_`+itemDetails['item_id']+`" class="hidden" onclick="" `+checked+`>
                            <label for="button_`+itemDetails['item_id']+`">`+itemDetails['item_name']+`</label>
                        </div>`;
                        })
                    add_cart_html += `</div></div></div>
                </div>
            </div>`;
        }
        $(".allItems").html(add_cart_html)
    }
}

function updateCart() {
    var item_json = {}
    $(".allItems").find(".card").each(function(){
        let cat_key = $(this).find(".card-header").attr("category_id");
        let itemArray = [];
        $catItemsDiv = $(this).find(".all_cat_items");
        $catItemsDiv.find(".button-checkbox").each(function(){
            if($(this).find(".itemCheckBox").prop('checked')) {
                let itemDet = {};
                itemDet['id'] = $(this).find(".itemCheckBox").attr("item-id");
                itemDet['name'] = $(this).find(".itemCheckBox").attr("item-name");
                itemDet['item_purchased'] = $(this).hasClass("purchased_item") ? "1" : "0";
                itemArray.push(itemDet)
            }
        })
        item_json[cat_key] = itemArray
    })
    let cart_name = $("#cart_name").val();

    payload = {
        "cart_id": cart_id,
        "cart_name": cart_name,
        "item_json": item_json
    }
    $.ajax({
        url: API_URL+"/update-cart", // Replace with your API endpoint
        type: "POST",
        data: JSON.stringify(payload),
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
            toastr.success("Cart Updated")
            setTimeout(function(){
                pageRedirect('my-carts')
            },1000)
        },
        error: function(xhr, textStatus, errorThrown) {
            toastr.error(errorThrown)
        }
    });
}