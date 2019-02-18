function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


    $('#form-auth').submit(function(e){
        e.preventDefault();
        read_name = $('#real-name').val()
        id_card = $('#id-card').val()
        $.ajax({
            url:'/user/auth/',
            data:{'read_name': read_name, 'id_card': id_card},
            dataType:'json',
            type:'POST',
            success:function(data){
                if(data.code == '200'){
                    if(data.user.id_name){
                        $('#real-name').val(data.user.id_name)
                        $('#id-card').val(data.user.id_card)
                        $('.btn-success').hide()
                    }
                }
                if(data.code == '1013'){
                    $('#real-name span').html(data.msg)
                    $('#real-name').show()
                }
                if(data.code == '1014'){
                    $('#id-card span').html(data.msg)
                    $('#id-card').show()
                }
                if(data.code == '1015'){
                    $('#error-msg span').html(data.msg)
                    $('#error-msg').show()
                }
            },
            error:function(data){
                alert('请求失败')
            }
        });
    })


function auth(){
    $.get('/user/read_user_info/', function(data){
        if(data.code == '200'){
            if(data.user.id_name){
                $('#real-name').val(data.user.id_name).attr('disabled', 'disabled')
                $('#id-card').val(data.user.id_card).attr('disabled', 'disabled')
                $('.btn-success').hide()
            }
        }
    })
}
auth()