$(document).ready(function() {
        userToken = getCookie('token')
        decoded_token = tokenDecode(userToken)        
        $.ajax({
            url: API_URL+"/get-my-carts", // Replace with your API endpoint
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
                my_cart_list_html = ``;
                if(data.my_cart_list.length>0) {
                    $(data.my_cart_list).each(function(ind,val){
                        cart_name_html = ``;
                        if(checkVarError(val['cart_name'])) {
                            cart_name_html = `<div class="row mb-1 cart_name_disp text-right">`+val['cart_name']+`</div>`;
                        }
                        my_cart_list_html += `<div class="mb-2 pb-3 cart_block">`+cart_name_html+`
                        <div class="row mb-1">
                            <div class="col-8 text-left cart_date">`+val['created_date']+`</div>
                            <div class="col-4 text-right assignBtn"><button class="btn btn-primary" onclick="assignUserList(`+val['cart_id']+`)">Assign</button></div>
                        </div>
                        <div class="row d-flex justify-content-center">
                            <button class="btn btn-primary mr-2" onclick="viewCart(`+val['cart_id']+`)">View</button>
                            <button class="btn btn-primary mr-2" onclick="editCart(`+val['cart_id']+`)">Edit</button>
                            <button class="btn btn-danger" onclick="delCart(`+val['cart_id']+`)">Delete</button>
                        </div>
                    </div>`
                    })
                } else {
                    my_cart_list_html += `<div class="col-12 text-center"><h4>No Carts Added</h4></div>`
                }
                assigned_cart_list_html = ``;
                if(data.assigned_cart_list.length>0) {
                    $(data.assigned_cart_list).each(function(ind,val){
                        cart_name_html = ``;
                        if(checkVarError(val['cart_name'])) {
                            cart_name_html = `<div class="row mb-1 cart_name_disp text-right">`+val['cart_name']+`</div>`;
                        }
                            assigned_cart_list_html += `<div class="mb-2 pb-3 cart_block">`+cart_name_html+`
                            <div class="row mb-1">
                                <div class="col-12 text-left cart_date">`+val['created_date']+`</div>
                            </div>
                            <div class="row d-flex justify-content-center">
                                <button class="btn btn-primary mr-2" onclick="viewCart(`+val['cart_id']+`)">View</button>
                                <button class="btn btn-primary mr-2" onclick="editCart(`+val['cart_id']+`)">Edit</button>
                            </div>
                        </div>`
                    })
                } else {
                    assigned_cart_list_html += `<div class="col-12 text-center"><h4>No Carts Assigned</h4></div>`
                }
                $("#myCartsDiv").html(my_cart_list_html)
                $("#assignedCartsDiv").html(assigned_cart_list_html)
            },
            error: function(xhr, textStatus, errorThrown) {
                toastr.error(errorThrown)
            }
        });
});


function assignUserList(cart_id) {
    $.ajax({
        url: API_URL+"/get-fam-users", // Replace with your API endpoint
        type: "POST",
        dataType: "JSON",
        contentType: "application/json",
        headers: {
            "Authorization": "Bearer " + userToken
        },
        success: function(data) {
            var fam_users_list_html = ``;
            var thisCartAssignees = []
            if(data.fam_users.length>0) {
                var fam_users_list = data.fam_users
                let payload = {
                    "cart_id":cart_id
                }
                console.log(payload)
                $.ajax({
                    url: API_URL+"/cart-assignees", // Replace with your API endpoint
                    type: "POST",
                    dataType: "JSON",
                    data: JSON.stringify(payload),
                    contentType: "application/json",
                    headers: {
                        "Authorization": "Bearer " + userToken
                    },
                    success: function(data) {
                        if(checkVarError(data.assigned_users)) {
                            thisCartAssignees = data.assigned_users;
                        }
                        $(fam_users_list).each(function(ind,user_data){
                            let assignedCheck = thisCartAssignees.indexOf(user_data['user_id'])>-1 ? "checked":"";
                            let userName = user_data['user_id']==decoded_token['user_id']?"You :)":user_data['user_name'];
                            fam_users_list_html += `<div class="button-checkbox">
                            <input class="itemCheckBox" type="checkbox" item-id="`+user_data['user_id']+`" item-name="`+user_data['user_name']+`" id="button_`+user_data['user_id']+`" class="hidden" onclick="assigneeCheck(this,`+user_data['user_id']+`,`+cart_id+`)" `+assignedCheck+`>
                            <label for="button_`+user_data['user_id']+`">`+userName+`</label>
                            </div>`;
                        }).promise().done(function() {
                            $("#customModalBody").html(fam_users_list_html)
                        });
                    },
                    error: function(xhr, textStatus, errorThrown) {
                        // Failed login
                        $("#error-message").removeClass("hidden");
                    }
                });
                
            }
            $("#customModalHeader").html("Assign To Family Members");
            $("#customModalBody").html(fam_users_list_html);
            $("#customModal").modal('show');
        },
        error: function(xhr, textStatus, errorThrown) {
            // Failed login
            $("#error-message").removeClass("hidden");
        }
    });
}