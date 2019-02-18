$(document).ready(function(){
    $(".auth-warn").show();
    $.ajax({
        url:'/home/myhouse_info/',
        type:'GET',
        dataType:'json',
        success:function(data){
            console.log(data)
            if(data.user.id_name){
                $('.auth-warn').hide()
            }
        },
        error:function(data){
            alert('not ok')
        }
    });
})