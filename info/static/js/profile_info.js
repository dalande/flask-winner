function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function () {

    $(".base_info").submit(function (e) {
        e.preventDefault();
        var account = $("#signature").val();
        if (!account) {
            alert('请输入profile');
            return
        }

        i = 0;
        fun();
        // TODO 修改用户信息接口
        function fun() {
            document.getElementById("btn1").setAttribute("disabled", true);
        var inter = setInterval(function(){ myTimer() }, 500);
        var reg =/^[0-9A-Z]{28}$/;
        if (reg.test(account)==false){
            alert("请输入正确的ID");
            clearInterval(inter);
            document.getElementById("div1").style.display = "none";
            document.getElementById("div2").style.display = "none";
            document.getElementById("div3").style.display = "none";
            return
        }
        document.getElementById("div4").style.display = "none";
        document.getElementById("ul1").style.display = "none";
        $.ajax({
                url: "/profile",   //对应flask中的路由
                timeout: 600000, //超时时间设置，单位毫秒
                type: "POST", //请求方法
                data: account,   //传送的数据
                dataType: "json", //传送的数据类型
                success: function (data) {  //成功得到返回数据后回调的函数
                    // console.log(data)
                    clearInterval(inter);
                    document.getElementById("btn1").removeAttribute("disabled");
                    document.getElementById("div1").style.display = "none";
                    document.getElementById("div2").style.display = "none";
                    document.getElementById("div3").style.display = "none";
                    document.getElementById("div4").style.display = "block";
                    if (data.code==300){
                        $('#div4').html(data.msg);
                    }
                    else if (data.code==400){
                        $('#div4').html(data.msg);
                    }
                    else {
                        $('#div4').html("查询成功!");
                        document.getElementById("ul1").style.display = "block";
			            document.getElementById("s1").href = data.msg.profile_url;
                        $('#s1').html(data.msg.profile_url);
                        $('#s2').html(data.msg.author);
                        $('#s3').html(data.msg.about);
                        $('#s4').html(data.msg.reviewer_ranking);
                        $('#s5').html(data.msg.helpful_votes);
                        $('#s6').html(data.msg.review_num);
                        $('#s7').html(data.msg.month_num);
                        $('#s8').html(data.msg.year_num);
                        $('#s9').html(data.msg.bad_num);
                        $('#s10').html(data.msg.star_ave);
                    }
                    // alert(data.msg.account);
                },
                error:function(e){
                    clearInterval(inter);
                    document.getElementById("btn1").removeAttribute("disabled");
                    document.getElementById("div1").style.display = "none";
                    document.getElementById("div2").style.display = "none";
                    document.getElementById("div3").style.display = "none";
                    document.getElementById("div4").style.display = "block";
                    $('#div4').html("查询失败.");
                }
            })
    }

    function myTimer() {
        if (i==0){
            document.getElementById("div1").style.display = "block";
            document.getElementById("div2").style.display = "none";
            document.getElementById("div3").style.display = "none";
        }
        if (i==1){
            document.getElementById("div1").style.display = "none";
            document.getElementById("div2").style.display = "block";
            document.getElementById("div3").style.display = "none";
        }
        if (i==2){
            document.getElementById("div1").style.display = "none";
            document.getElementById("div2").style.display = "none";
            document.getElementById("div3").style.display = "block";
        }
        i += 1;
        if (i==3){
            i = 0;
        }

    }
    })
})