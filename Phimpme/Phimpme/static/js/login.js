/**
 *登陆
 */
function sendLogin(){
	
	var userName = $("#name").val().trim();
	var pwd		 = $("#passwd").val().trim();
	if(userName==""||pwd==""){
		return;
	}

	$.ajax({
		url : "/cgi-bin/usermgt/login/",
		type : "POST",
		data:{
			"username":userName,
			"userpwd":pwd
		},
		success : function(data) {
			var json = eval("(" + data + ")");

			if (json.result == "success") {
				location.href="/static/app_config.html"; 
				return;
			}else{
				location.href="/static/error.html";
				return;
			}
		}
	});
}
