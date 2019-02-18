
function logout() {
    $.ajax({
        url:'/user/logout/',
        type:'DELETE',
        success:function(data){
            if(data.code == '200'){
                location.href = '/house/index/'
            }
        }
    })
//    $.get("/api/logout", function(data){
//        if (0 == data.errno) {
//            location.href = "/";
//        }
//    })
}


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


function profile(){
    $.ajax({
        url:'/user/profile/',
        type:'GET',
        success:function(data){
            console.log(data)
        }
    })
}