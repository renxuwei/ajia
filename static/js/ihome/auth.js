function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}
$(document).ready(function() {
    $.ajax({
        url:'/user/auth_info/',
        type:'GET',
        dataType:'json',
        success:function(data){
            console.log(data)
            if(data.user.id_name){
                $("#real-name").val(data.user.id_name)
                $("#id-card").val(data.user.id_card)
                $('#real-name').attr('disabled', 'disabled')
                $('#id-card').attr('disabled', 'disabled')
                $('.error-msg').hide()
                $('.btn-success').hide()
            }
        },
        error:function(data){
            alert('not ok')
        }
    });


    $("#form-auth").submit(function(e){
        e.preventDefault();
        name = $("#real-name").val()
        num = $("#id-card").val()
        $.ajax({
            url:'/user/auth/',
            type:'POST',
            dataType:'json',
            data:{'name':name, 'num':num},
            success:function(data){
                console.log(data)
               if(data.code == '1102'){
                   $('.error-msg span').html(data.msg)
                   $('.error-msg').show()
               }
               if(data.code == '1103'){
                   $('.error-msg span').html(data.msg)
                   $('.error-msg').show()
               }
               if (data.code == '200'){
                   $('#real-name').attr('disabled', 'disabled')
                   $('#id-card').attr('disabled', 'disabled')
                   $('.error-msg').hide()
                   $('.btn-success').hide()
               }

            },
            error:function(data){
                alert('not ok')
            }
        })
    });
})