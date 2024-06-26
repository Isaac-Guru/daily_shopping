var params = getQueryParameters();
var cart_id = params['cart_id'];
var g_total_items = 0;
var g_purchased_items = 0;
$(document).ready(function() {
    userToken = getCookie('token')
    decoded_token = tokenDecode(userToken)

    $.when(getAllCatItems()).done(function(response){
        var params = getQueryParameters();
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
                    return false;
                }
                if(checkVarError(data['data'])) {
                    let cart_data = data.data;
                    $("#cart_head").html(cart_data['cart_name'])
                    $(".cart_date").html(cart_data['created_date'])
                    let items = cart_data.item_json;
                    var cart_html = ``;
                    cart_html += `<div id="accordion">`;
                    $.each(items,function(category,allItems){
                        
                        if(allItems.length<1) {
                            return
                        }
                        cart_html += `<div class="card">
                        <div class="card-header" category_id="`+category+`" id="heading_`+category+`">
                            <h5 class="mb-0">
                                <button class="btn btn-link" data-toggle="collapse" data-target="#collapse_`+category+`" aria-expanded="true" aria-controls="collapseOne">
                                    `+g_all_categories[category]['category_name']+`
                                </button>
                            </h5>
                        </div>
            
                        <div id="collapse_`+category+`" class="collapse show" aria-labelledby="heading_`+category+`" data-parent="#accordion">
                            <div class="card-body"><div class="row d-flex flex-wrap all_cat_items">`;
                            if(Object.keys(allItems).length>0) {
                                $.each(allItems,function(index,itemDetail){
                                    g_total_items = g_total_items+1;
                                    let checked = '';
                                    if(checkVarError(itemDetail['item_purchased']) && itemDetail['item_purchased']=="1") {
                                        checked = 'checked';
                                        g_purchased_items = g_purchased_items+1;
                                    }
                                    cart_html += `<div class="button-checkbox">
                                        <input class="itemCheckBox" type="checkbox" item-id="`+itemDetail['id']+`" item-name="`+itemDetail['name']+`" id="button_`+itemDetail['id']+`" class="hidden" onclick="" `+checked+`>
                                        <label for="button_`+itemDetail['id']+`">`+itemDetail['name']+`</label>
                                    </div>`;
                                })
                            } else {
                                cart_html += `<div class="col-12 text-center"><h4>No `+g_all_categories[category]['category_name']+` Added</h4></div>`;
                            }
                            cart_html += `</div></div>
                        </div>
                    </div>`;
                    }) 
                    cart_html += `</div>`;
                    $(".tot_items").html(`Total Items : `+g_total_items)
                    $(".purchased_items").html(`Purchased Items : `+g_purchased_items)
                    $("#cartDispDiv").html(cart_html);
                } else {
                    $("#cartDispDiv").html("No Cart Found");
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                toastr.error(errorThrown)
            }
        });
    })

    $(".purchased_btn").click(function(){
        var item_json = {}
        $("#cartDispDiv").find(".card").each(function(){
            let cat_key = $(this).find(".card-header").attr("category_id");
            let itemArray = [];
            $catItemsDiv = $(this).find(".all_cat_items");
            $catItemsDiv.find(".button-checkbox").each(function(){
                let itemDet = {};
                if($(this).find(".itemCheckBox").prop('checked')) {
                    itemDet['item_purchased'] = "1";
                }
                itemDet['id'] = $(this).find(".itemCheckBox").attr("item-id");
                itemDet['name'] = $(this).find(".itemCheckBox").attr("item-name");
                itemArray.push(itemDet)
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
            url: API_URL+"/update-purchase-details",
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
                    location.reload()
                },1000)
            },
            error: function(xhr, textStatus, errorThrown) {
                toastr.error(errorThrown)
            }
        });
    })
});