function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$('#form-house-info').submit(function(e){
    e.preventDefault();
    $(this).ajaxSubmit({
        url:'/home/newhouse/',
        type:'POST',
        dataType:'json',
        success:function(data){
            if(data.code == '200'){
                $('#form-house-image').show()
                $('#form-house-info').hide()
                $('#house-id').val(data.house_id)
            }
        },
        error:function(data){
            alert('失败')
        }
    });
});

$('#form-house-image').submit(function(e){
    e.preventDefault();
    $(this).ajaxSubmit({
        url:'/home/image/',
        type:'POST',
        dataType:'json',
        success:function(data){
            if(data.code == '200'){
                img = '<img src="/static/media/'+ data.url +'">'
                $('.house-image-cons').append(img)
            }
        },
        error:function(data){
            alert('失败')
        }
    });
});