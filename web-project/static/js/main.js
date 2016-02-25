$.ajaxSetup({
    beforeSend: function(jqXHR, settings) { type = settings.type if (type != 'GET' && type != 'HEAD' && type != 'OPTIONS') { var pattern = /(.+; *)?_xsrf *= *([^;" "]+)/; var xsrf = pattern.exec(document.cookie); if (xsrf) {
                    jqXHR.setRequestHeader('X-Xsrftoken', xsrf[2]);
                }
            }
    }});

function getHTML() {
    var device_id = $("#device_id").val();
    if (device_id.trim() == '') {
        alert('请输入ID');
        return false;
    }
    $('input#button').val('查询中...');

    $.ajax({
        url: '/post_html/',
        type: 'POST',
        data: {
            'device_id': device_id.trim(),
        },
        success: function(r) {
            $('#results').html(r)
            $('input#button').val('查询成功');
        }
    });
}
