function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');

    $("#form-house-info").submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/home/my_newhouse/',
            type:'POST',
            dataType:'json',
            success:function(data){
                console.log(data)
                if(data.code == '200'){
                    $('#form-house-info').hide()
                    $('#form-house-image').show()
                    $('#house-id').val(data.house_id)
                }
            },
            error:function(data){
                alert('not ok')
            }
        })


    });
    $("#form-house-image").submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/home/my_newhouse_info/',
            type:'POST',
            dataType:'json',
            success:function(data){
                console.log(data)
                if(data.code == '200'){
                    var img = '<img src="/static/media/' + data.name + '">'
                    $('.house-image-cons').append(img)
                }
            },
            error:function(data){
                alert('not ok')
            }
        })
    });
})
