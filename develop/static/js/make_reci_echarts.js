function make_reci_echarts(num){
    var data = {
         data: JSON.stringify({"cur_year": num})
    }
    var msg = {};
    $.ajax({
        url:"/ajaxlrz",
        type: 'POST',
        data: data,
        async:false,
        success: function (xmsg) {
            console.log(xmsg);
            msg = xmsg;
        }
    })
    var cur_year = num + '年'
    var myChart = echarts.init(document.getElementById('charts'));

    console.log(msg);
    var wordlist = msg["word_list"].reverse();
    var cipinlist = msg["frequency_list"].reverse();
    // 指定图表的配置项和数据
    var option = {
        color:function(params) {
		    	     //自定义颜色
            var colorList = [
             '#C1232B','#B5C334','#FCCE10','#E87C25','#27727B',
             '#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD',
             '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'
            ];
            return colorList[params.dataIndex]
        },

        title: {
            text: cur_year + '年度热词柱状图',
            x:'center',
            y:'top',
            textAlign:'left',
            textStyle:{
                fontSize: 18,
                color: '#ffffff'
            },
        },
        tooltip: {},
        legend: {
            x: 'right',
            y: 'top',
            textStyle:{
                fontSize: 18,
                color: '#ffffff'
            },
            data:['词热度']
        },
        xAxis: {
            type: 'value',
            data: cipinlist,
            axisLabel:{
                show: true,
                textStyle:{
                    fontSize: 18,
                    color: '#ffffff'
                },
            },
            axisLine:{
                lineStyle:{
                    color:'#ffffff',
                    width:1,//这里是为了突出显示加上的
                }
            },
        },
        yAxis: {
            type : 'category',
            data: wordlist,
            axisLabel:{
                show: true,
                textStyle:{
                    fontSize: 18,
                    color: '#ffffff'
                },
            },
            axisLine:{
                lineStyle:{
                    color:'#ffffff',
                    width:1,//这里是为了突出显示加上的
                }
            },
        },
        series: [{
            name: '词热度',
            type: 'bar',
            data: cipinlist,
            label: { //柱体上显示数值
                show: true,//开启显示
                position: 'right',//在上方显示
                textStyle: {//数值样式
                    fontSize: '8px',
                    color: '#fff'
                },
                formatter: '{@cipinlist}',
            }
        }]
    };
    myChart.setOption(option);
}