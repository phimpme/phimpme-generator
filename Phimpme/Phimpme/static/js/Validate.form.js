$.extend(validateFunction, {
	FORM_validate:function() {
		$("#pwd").jdValidate(validatePrompt.pwd, validateFunction.pwd, true)
		$("#pwd2").jdValidate(validatePrompt.pwd2, validateFunction.pwd2, true);
		$("#mail").jdValidate(validatePrompt.mail, validateFunction.mail, true);
		return validateFunction.FORM_submit(["#pwd","#pwd2","#mail"]);
	}
});

//表单提交验证和服务器请求
function registsubmit(){
	var flag = validateFunction.FORM_validate();
    if (flag) {
      $.ajax({
			url : "/cgi-bin/usermgt/register/",
			type : "POST",
			data:{
				"userpwd":$("#pwd").val(),
				"email":$("#mail").val()
			},
			success : function(data) {
				var json = eval("(" + data + ")");

				if (json.result == "success") {
					location.href="/cgi-bin/usermgt/login/";
					return;
				}else{
					location.href="/static/registration.html";
					return;
				}
			}
		});
    }
}

$(document).ready(function(){
	
	//默认下用户名框获得焦点
	setTimeout(function() {
		$("#mail").get(0).focus();
	}, 0);
	//邮箱验证
	$("#mail").jdValidate(validatePrompt.mail, validateFunction.mail);
	//密码验证
	$("#pwd").bind("keyup",function(){
		validateFunction.pwdstrength();
	}).jdValidate(validatePrompt.pwd, validateFunction.pwd)
	//二次密码验证
	$("#pwd2").jdValidate(validatePrompt.pwd2, validateFunction.pwd2);


});