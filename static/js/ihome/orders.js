//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    $(".order-comment").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-comment").attr("order-id", orderId);
    });
    $.ajax({
        url:'/home/myorders/',
        type:'GET',
        dataType:'json',
        success:function(data){
            console.log(data)
            if(data.code == '200'){
                for(var i=0; i<data.orders_list.length; i++){

                    console.log(data.orders_list[i])
                    var orders_li = ''
                    orders_li += '<li><div class="order-title"><h3>订单编号：'+ data.orders_list[i].order_id +'</h3>'
                    orders_li += '<div class="fr order-operate"><button type="button" class="btn btn-success order-comment" data-toggle="modal" data-target="#comment-modal">发表评价</button></div></div>'
                    orders_li += '<div class="order-content"><img src="/static/media/'+ data.orders_list[i].image +'">'
                    orders_li += '<div class="order-text"><h3>订单</h3><ul> <li>创建时间：'+ data.orders_list[i].create_date +'</li>'
                    orders_li += '<li>入住日期：'+ data.orders_list[i].create_date +'</li>'
                    orders_li += '<li>离开日期：'+ data.orders_list[i].end_date +'</li>'
                    orders_li += '<li>合计金额：'+ data.orders_list[i].amount +'元(共'+ data.orders_list[i].days +'晚)</li>'
                    orders_li += '<li>订单状态：<span>'+ data.orders_list[i].status +'</span></li>'
                    orders_li += '<li>我的评价：'+ data.orders_list[i].comment +'</li>'
                    orders_li += '<li>拒单原因：</li></ul>'
                    orders_li += '</ul></div></div></li>'

                    $('.orders-list').append(orders_li)

                }


            }
        },
        error:function(data){
            alert('not ok')
        }

    })
});