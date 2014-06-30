/**
 * ording
 */
function sendorder(){
	
	var app_name	 = $("#app_name").val().trim();
	var enable_choose_from_library	 = $("#enable_choose_from_library").val().trim();
	var enable_map	 = $("#enable_map").val().trim();
	var enable_nfc	 = $("#enable_nfc").val().trim();
	var enable_photo_capturing	 = $("#enable_photo_capturing").val().trim();
	var enable_photo_location_modification	 = $("#enable_photo_location_modification").val().trim();
	var enable_photo_manipulation	 = $("#enable_photo_manipulation").val().trim();

	if(app_name==""){
		return;
	}

	$.ajax({
		url : "/cgi-bin/orders/order",
		type : "GET",
		data:{
			"app_name":app_name,
			"enable_choose_from_library":enable_choose_from_library,
			"enable_map":enable_map,
			"enable_nfc":enable_nfc,
			"enable_photo_capturing":enable_photo_capturing,
			"enable_photo_location_modification":enable_photo_location_modification,
			"enable_photo_manipulation":enable_photo_manipulation
		},
		success : function(data) {
			var json = eval("(" + data + ")");

			if (json.result == "error") {
				location.href="/static/login.html";
				return;
			}else{
				location.href="/static/app_config.html";
				return;
			}
		}
	});
}
