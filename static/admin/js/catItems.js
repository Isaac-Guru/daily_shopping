$(document).ready(function() {
    userToken = getCookie('admin_token')
    decoded_token = tokenDecode(userToken)
    g_all_items = {}
    all_cat_select_html = ``;
    $.ajax({
        url: API_URL+"/admin/default-items",
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
            all_cat_items_html = ``;
            all_cat_select_html += `<select id="category_select_tag" class="form-control">`;
            all_cat_select_html += `<option value="">Category Select</option>`
            if(checkVarError(data.all_categories)) {
                g_all_categories = data.all_categories
                $.each(g_all_categories,function(catId,catDetail){
                    all_cat_select_html += `<option value="`+catId+`">`+catDetail['category_name']+`</option>`;
                })
            }
            all_cat_select_html += `</select>`;
            if(checkVarError(data.all_categories_item)) {
                all_cat_items_html += `<div id="accordion">`;
                $.each(data.all_categories_item,function(category,allItems){
                    all_cat_items_html += `<div class="card">
                    <div class="card-header" id="heading_`+category+`">
                        <h5 class="mb-0">
                            <button class="btn btn-link" data-toggle="collapse" data-target="#collapse_`+category+`" aria-expanded="true" aria-controls="collapseOne">
                                `+g_all_categories[category]['category_name']+`
                            </button>
                            <button class="btn btn-warning float-right" onclick=catEdit(`+g_all_categories[category]['category_id']+`)>Edit</button>
                        </h5>
                    </div>
        
                    <div id="collapse_`+category+`" class="collapse show" aria-labelledby="heading_`+category+`" data-parent="#accordion">
                        <div class="card-body" id="myCartsDiv"><div class="row"><div class="d-flex flex-wrap">`;
                        if(Object.keys(allItems).length>0) {
                            $.each(allItems,function(index,itemDetail){
                                g_all_items[itemDetail['item_id']] = itemDetail
                                all_cat_items_html += `<div class="mb-3 col-3"><button type="button" class="btn btn-primary" onClick="editItemView(this)" item-id="`+itemDetail['item_id']+`">`+itemDetail['item_name']+`</button></div>`;
                            })
                        }
                        all_cat_items_html += `</div></div></div>
                    </div>
                </div>`;
                }) 
                all_cat_items_html += `</div>`;
                $("#displayAll").html(all_cat_items_html);
            } else {
                $("#displayAll").html("No Data Found");
            }
        },
        error: function(xhr, textStatus, errorThrown) {
            toastr.error(errorThrown)
        }
    });
});

function addCat() {
    modalHtml = `<input type="text" class="form-control" id="catName">
    <button class="btn btn-success" onclick="catAddEdit()">Add</button>`
    $("#customModalHeader").html("Add Category");
    $("#customModalBody").html(modalHtml);
    $("#customModal").modal('show');
}

function catEdit(catId) {
    modalHtml = `<input type="text" class="form-control" id="catName" value="`+g_all_categories[catId]['category_name']+`">
    <button class="btn btn-success" onclick="catAddEdit(`+catId+`)">Edit</button>`
    $("#customModalHeader").html("Edit Category");
    $("#customModalBody").html(modalHtml);
    $("#customModal").modal('show');
}

function catAddEdit(catId=0) {

    catName = $("#catName").val();
    if(catName.length<2) {
        toastr.error("please fill the category name")
    }
    // return false;
    URL = API_URL+"/admin/add-category"
    var payload = {
        "category_name": catName,
        "category_name_alias": catName
    }
    if(catId!=0) {
        URL = API_URL+"/admin/update-category"
        var payload = {
            "category_id": catId,
            "category_name": catName,
            "category_name_alias": catName
        }
    }

    $.ajax({
        url: URL,
        type: "POST",
        dataType: "JSON",
        contentType: "application/json",
        data: JSON.stringify(payload),
        headers: {
            "Authorization": "Bearer " + userToken
        },
        success: function(data) {
            if(checkVarError(data.error)) {
                toastr.error(data.error)
                return false;
            }
            toastr.success("success")
            setTimeout(function(){
                location.reload()
            },1000)
        },
        error: function(xhr, textStatus, errorThrown) {
            toastr.error(errorThrown)
        }
    });

}


function addItemsModal() {
    modalHtml = `<div class="col-12 mb-5 category_select">`+all_cat_select_html+`</div>
    <div id="addMainDiv" class="col-12 "></div>
    <div class="mb-2"><button class="btn btn-primary" onclick="addItemDiv()">+Add New Item</button></div>
    <div class="col-12 mb-4"><button class="form-control btn btn-success" onclick="saveAllItems()">Save Items</button></div>`
    $("#customModalHeader").html("Add Items");
    $("#customModalBody").html(modalHtml);
    addItemDiv()
    $("#customModal").modal('show');
}
function addItemDiv() {
    addItemDivHtml = `<div class="addNewItemDiv mb-2">
        <input type="text" class="form-control add_item_name">
    </div>`
    $("#addMainDiv").append(addItemDivHtml)
}

function saveAllItems() {
    var allNewItems = [];
    var this_category_id = $("#category_select_tag").val();
    if(!checkVarError(this_category_id)) {
        toastr.error("Pls select category")
        return false;
    }
    $("#addMainDiv .addNewItemDiv").each(function(){
        let itemDet = {
            'item_name': $(this).find(".add_item_name").val(),
            'item_name_alias': $(this).find(".add_item_name").val(),
            'created_by_admin': true,
            'category_id': this_category_id
        }
        allNewItems.push(itemDet);
    })
    var payload = allNewItems;
    $.ajax({
        url: API_URL+"/admin/add-items",
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
            toastr.success("Addedd")
            setTimeout(function(){
                location.reload()
            },1000)
        },
        error: function(xhr, textStatus, errorThrown) {
            toastr.error(errorThrown)
        }
    });
}

function editItemView(thisEle) {
    let itemName = $(thisEle).text();
    let itemId = $(thisEle).attr("item-id");
    modalHtml = `<input type="text" class="form-control" id="itemNameEdit" value="`+itemName+`">
    <input type="hidden" class="form-control" id="itemNameEditId" value="`+itemId+`">
    <label>Item Image</label>
    <input type="file" name="item_image" id="item_image">
    <div class="row col-12 mt-1"><button class="btn btn-success col-12" onclick="itemEditDel('edit')">Edit Item</button></div>
    <div class="row col-12 mt-2"><button class="btn btn-danger col-12" onclick="itemEditDel('delete')">Delete Item</button></div>`
    $("#customModalHeader").html("Edit/Del Items");
    $("#customModalBody").html(modalHtml);
    $("#customModal").modal('show');
}

function itemEditDel(fnType) {
    let item_edit_id = $("#itemNameEditId").val();
    var formData = new FormData();
    var URL = '';
    if(fnType=='edit') {
        let item_edit_name = $("#itemNameEdit").val()
        formData.append("item_image", $("#item_image")[0].files[0]);
        formData.append("item_id", item_edit_id);
        formData.append("item_name", item_edit_name);
        formData.append("item_name_alias", item_edit_name);
        // payload = {'item_id':item_edit_id,'item_name':item_edit_name,'item_name_alias':item_edit_name}
        URL = API_URL+"/admin/update-item"
    } else {
        payload = {'item_id':item_edit_id}
        URL = API_URL+"/admin/del-item"
    }
    $.ajax({
        url: URL,
        type: "POST",
        dataType: "JSON",
        data: formData,
        contentType: "application/json",
        headers: {
            "Authorization": "Bearer " + userToken
        },
        success: function(data) {
            if(checkVarError(data.error)) {
                toastr.error(data.error)
                return false;
            }
            toastr.success("Success")
            setTimeout(function(){
                location.reload()
            },1000)
        },
        error: function(xhr, textStatus, errorThrown) {
            toastr.error(errorThrown)
        }
    });
}