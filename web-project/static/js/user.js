function Fixuser() {
    var grade = $('#Grade').find('option:selected').val();
    if (grade == '') {
        $('p#p_err').html('请选择年级');
        document.getElementById('err').style.display="block";
        return false;
    }
    var phonenum = $('#inputPhone').val();
    var place = $('#inputPlace').val();
    var _xsrf = $("input[name='_xsrf']").val();
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'grade': grade,
            'phonenum': phonenum,
            'place': place,
            '_xsrf': _xsrf
        },
        success: function(r) {
            if (r=='1' || r=='0') {
                $('p#p_err').html('修改成功');
                document.getElementById('err').style.display="block";
                return false;
            } else {
                $('p#p_err').html('服务器异常,请重试');
                document.getElementById('err').style.display="block";
                return false;
            }
        }
    });

}
