function Register() {
    var username = $('#inputEmail').val();
    if (username=='' || username.length<6){
        $('p#p_err').html("请输入6位长度以上账号");
        document.getElementById('err').style.display="block";
        return false;
    }
    var nickname = $('#inputNickname').val();
    if (nickname=='') {
        $('p#p_err').html("昵称不能为空");
        document.getElementById('err').style.display="block";
        return false;
    }
    var password = $('#inputPassword').val().toString();
    if (password=='' || password.length < 8 || password.length > 16) {
        $('p#p_err').html("请输入8-16位密码");
        document.getElementById('err').style.display="block";
        return false;
    }
    var re_password = $('#inputRePassword').val();
    if (password != re_password) {
        $('p#p_err').html("两次密码输入不一致");
        document.getElementById('err').style.display="block";
        return false;
    }
    var secretcode = $('#inputSecretcode').val();
    if (secretcode=='') {
        $('p#p_err').html("请输入注册码");
        document.getElementById('err').style.display="block";
        return false;
    }
    var _xsrf = $("input[name='_xsrf']").val();
    $.ajax({
        url: '/register',
        type: 'POST',
        data: {
            'username': username,
            'nickname': nickname,
            'password': password,
            'secretcode': secretcode,
            '_xsrf': _xsrf
        },
        success: function(r) {
            if (r=='0') {
                $('p#p_err').html("请输入正确的激活码！");
                document.getElementById('err').style.display="block";
                return false;
            }
            else if (r=='-1') {
                $('p#p_err').html("该账号已注册！");
                document.getElementById('err').style.display="block";
                return false;
            }
            else if (r=='1') {
                window.location='/login';
            }
        }
    });
}
