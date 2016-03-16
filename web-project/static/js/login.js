function getHTML() {
    var username = $('#inputEmail').val();
    var password = $('#inputPassword').val();
    if (username=='') {
        $('p#p-err').html('请输入账号!');
        document.getElementById('err').style.display="block";
        document.getElementById('login-referer').style.display="none";
        return false;
    }else if (password=='') {
        $('p#p-err').html('请输入密码!');
        document.getElementById('err').style.display="block";
        document.getElementById('login-referer').style.display="none";
        return false;
    }
    _xsrf = $("input[name='_xsrf']").val();
    $.ajax({
        url: '/login',
        type: 'POST',
        data: {
            'username': username,
            'password': password,
            '_xsrf': _xsrf
        },
        success: function(r) {
            if (r=='1') {
                var patt_hof = new RegExp("HallofFame");
                var patt_music = new RegExp("Music");
                var search=window.location.search;
                if (patt_hof.test(search)) {
                    window.location='/HallofFame';
                } else if (patt_music.test(search)) {
                    window.location='/Music';
                } else {
                    window.location='/';
                }
            }
            else{
                $('p#p-err').html(r);
                document.getElementById('err').style.display="block";
                document.getElementById('login-referer').style.display="none";
            }
        }
    });
}
