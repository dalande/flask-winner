function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function () {

    $(".base_info").submit(function (e) {
        e.preventDefault();
        var keywords = $("#signature").val();
        if (!keywords) {
            alert('请输入关键词');
            return
        }

        i = 0;
        fun();
        // TODO 修改用户信息接口
        function fun() {
            document.getElementById("btn1").setAttribute("disabled", true);
        var inter = setInterval(function(){ myTimer() }, 500);

        document.getElementById("div4").style.display = "none";
        document.getElementById("ul1").style.display = "none";
        $.ajax({
                url: "/scatter",   //对应flask中的路由
                type: "POST", //请求方法
                data: keywords,   //传送的数据
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
                                var MyScatter = echarts.init(document.getElementById('ul1'));
                                var data = data.msg;
                                var textStyle = {
                                    color: '#333',
                                    fontStyle: 'normal',
                                    fontWeight: 'normal',
                                    fontFamily: '微软雅黑',
                                    fontSize: 14,
                                };
                                option = {
                                    tooltip: {
                                        /*鼠标移上去，返回需要的信息*/
                                        formatter: function (param) {
                                            var value = param.value;
                                            return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 16px;"> ' + value[3] +
                                                '</div>';
                                        }
                                    },
                                    xAxis: {
                                        type: 'value',
                                        name: 'x轴',
                                        max: 4,
                                        min: 1,
                                        interval: 1,
                                    },
                                    yAxis: {
                                        type: 'value',
                                        name: 'y轴',

                                        max: data.length/4,
                                        min: 1,
                                        interval:1,
                                    },
                                    series: [{
                                        name: '',
                                        data: data,
                                        type: 'scatter',
                                        symbolSize: 20,
                                        itemStyle: {
                                            normal: {
                                                color: param=>{
                                                    var value = param.value;
                                                    switch(value[2]){
                                                        case 0:
                                                            return 'gray';
                                                        case 1:
                                                            return 'green';
                                                    }
                                                },
                                                opacity: 0.6,
                                            }
                                        },
                                    }]
                                };

                                MyScatter.setOption(option);

                    }
                    // alert(data.msg.account);
                    // $.ajax({
                    //     url: "/kw_history",   //对应flask中的路由
                    //     type: "POST", //请求方法
                    //     data: keywords,   //传送的数据
                    //     dataType: "json", //传送的数据类型
                    // })
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