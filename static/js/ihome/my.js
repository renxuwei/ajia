function logout() {
    $.ajax({
         url:'/user/logout',
         type:'GET',
         dataType:'json',
         success:function(data){
            if ('200' == data.code) {
                location.href = '/user/login/'
            }
         }
    })
}

$(document).ready(function(){
    $.ajax({
        url:'/user/user_info/',
        dataType:'json',
        type:'GET',
        success:function(data){
            console.log(data)
            $('#user-name').html(data.data.name)
            $('#user-mobile').html(data.data.phone)
            $('#user-avatar').attr('src', '/static/media/' + data.data.avatar)
        }
    })

})