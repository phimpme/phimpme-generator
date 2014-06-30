$.extend(validateFunction, {
	FORM_validate:function() {
		$("#username").jdValidate(validatePrompt.username, validateFunction.username, true);
		$("#pwd").jdValidate(validatePrompt.pwd, validateFunction.pwd, true)
		$("#pwd2").jdValidate(validatePrompt.pwd2, validateFunction.pwd2, true);
		$("#mail").jdValidate(validatePrompt.mail, validateFunction.mail, true);
		return validateFunction.FORM_submit(["#username","#pwd","#pwd2","#mail"]);
	}
});

//表单提交验证和服务器请求
function registsubmit(){
	var flag = validateFunction.FORM_validate();
    if (flag) {
      $.ajax({
			url : "/cgi-bin/register/",
			type : "GET",
			data:{
				"username":$("#username").val(),
				"userpwd":$("#pwd").val(),
				"email":$("#mail").val()
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
}

$(document).ready(function(){
	
	//默认下用户名框获得焦点
	setTimeout(function() {
		$("#username").get(0).focus();
	}, 0);
	//用户名验证
	$("#username").jdValidate(validatePrompt.username, validateFunction.username);
	//密码验证
	$("#pwd").bind("keyup",function(){
		validateFunction.pwdstrength();
	}).jdValidate(validatePrompt.pwd, validateFunction.pwd)
	//二次密码验证
	$("#pwd2").jdValidate(validatePrompt.pwd2, validateFunction.pwd2);
	//邮箱验证
	$("#mail").jdValidate(validatePrompt.mail, validateFunction.mail);
});