function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
    $.ajax({
        url:'/home/booking/' + location.search.split('=')[1] + '/',
        type:'GET',
        dataType:'json',
        success:function(data){
            console.log(data)
            if(data.code == '200'){
                $('.house-info img').attr('src', '/static/media/' + data.img)
                $('.house-info .house-text h3').html(data.title)
                $('.house-text p span').html(data.price)

            }

        },
        error:function(data){
            alert('not ok')
        }
    })
})

function hrefBackll(){
    house_id = location.search.split('=')[1]
    num1 = $("#start-date").val()
    num2 = $("#end-date").val()
    num3 = $(".order-amount span").html()
    $.ajax({
        url:'/home/orders/',
        type:'POST',
        dataType:'json',
        data:{'start':num1, 'end':num2, 'span':num3, 'house_id':house_id},
        success:function(data){
            console.log(data)
            if(data.code == '200'){
                location.href = '/home/my_orders/'
            }
            if(data.code == '1122'){
                alert('未登录')
                location.href = '/user/login/'
            }

        },
        error:function(data){

        }

    })
}