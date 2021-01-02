function pic(xlist){
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('charts'));

        // 指定图表的配置项和数据
        var option = {
            title: {
                text: '2008年事件热度曲线-',
                x:'center',
                y:'top',
                textAlign:'left'
            },
            tooltip: {},
            legend: {
                x: 'right',
                y: 'top',
                data:['事件热度']
            },
            xAxis: {
//                data: ["2008年08月07日","2008年08月08日","2008年08月09日"]
                  data: timelist,
                  axisLabel:{interval:3}
            },
            yAxis: {
                minInterval: 1
//                data : [1,2,3,4,5,6,7,8,9]
            },
            series: [{
                name: '事件热度',
                type: 'line',
                data: xlist
            }]
        };
//        option.xAxis.data.push("2021年")
//        option.series[0].data.push(60)
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
}