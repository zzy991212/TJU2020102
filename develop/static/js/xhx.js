function make_reci_echarts(num){
    var n = 10;
    let mp = new Map();
    for(var i = 0; i < n; i ++){
        var data = {
            data: JSON.stringify({"cur_year": num + i})
        }
        var msg = {};
        $.ajax({
            url:"/ajaxlrz",
            type: 'POST',
            data: data,
            async:false,
            success: function (xmsg) {
                msg = xmsg;
            }
        })
        // var wordlist = msg["word_list"].reverse();
        // var qwq = msg["frequency_list"].reverse();
        var wordlist = msg["word_list"];
        var qwq = msg["frequency_list"];
        var cipinlist = new Array();
        var sum = 0;
        for(var j = 0; j < qwq.length; j ++){
            sum += Number(qwq[j]);
        }
        for(var j = 0; j < qwq.length; j ++){
            cipinlist[j] = ((Number(qwq[j])/sum)*100).toFixed(2);
            // cipinlist[j] = (((Number(qwq[j])/sum).toFixed(4))*100).toString();
        }
        // var cipinlist = msg["frequency_list"].reverse();
        var tmp = [];
        for(var j = 0; j < wordlist.length; j ++){
            tmp.push(
                {
                    type: wordlist[j],
                    value: cipinlist[j]
                }
            );
        }
        mp.set(num + i, tmp);
    }

    var cur_year = num + '年'
    var cur_10year = num + 9 + '年'
    var myChart = echarts.init(document.getElementById('charts'));

    var ten_year = new Array();
    var n = 10;
    for(var i = 0; i < n; i ++){
        ten_year[i] = num + i;
    }

    let xAixsData = [];
    let seriesData = [];
    // let colorBag = ["#893448", "#d95850", "#eb8146", "#ffb248", "#f2d643", "#ebdba4"];
    let colorBag = ["#893448", "#a85658", "#c05850", "#d95850", "#d67573", "#eb8146", "#ffb248", "#ffca0f", "#f2d643", "#ffd986", "#ebdba4"];
    // let colorBag = ["#f3eb1a", "#fae609", "#ffc90a", "#fcaa18", "#f99120", "#f77622", "#f26225", "#ef3826", "#ec1d23", "#e5194a"];
    // let colorBag = ["#e01f54","#f5e8c8","#b8d2c7","#c6b38e","#a4d8c2","#f3d999","#d3758f","#dcc392","#2e4783",
    // "#82b6e9","#ff6347","#a092f1","#0a915d","#eaf889","#6699FF","#ff6666","#3cb371","#d5b158","#38b6b6"];
    // let colorBag = ["#de6f64","#ebbcb6","#fee0b4","#f3c89b","#de6f64","#945c4c"];

    // let colorBag = [
    //     '#C1232B','#B5C334','#FCCE10','#E87C25','#27727B',
    //     '#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD',
    //     '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'
    //    ];
    let idx = 0;
    for (let item of mp) {
        xAixsData.push(item[0]);
        let columnData = [];
        for (let ano of mp) {
            columnData.push(ano[1][idx]);
            if(columnData.length == 10) break;
        }
        seriesData.push({
            type: 'bar',
            stack: 1,
            data: columnData,
            label: {
                show: true,
                formatter:  (params) => params.data.type,
            },
            itemStyle: {
                normal: {
                    color: colorBag[idx % colorBag.length]
                    // color: (params) => colorBag[params.dataIndex % colorBag.length],  // 按柱子区分颜色？
                }
            },
            barMaxWidth: 60,
        });
        idx++;
    }
    let option = {
        title: {
            text: cur_year + '-' + cur_10year + '年度热词柱状图',
            x:'center',
            y:'top',
            textAlign:'left',
            textStyle:{
                fontSize: 18,
                color: '#ffffff'
            },
        },
        grid: {
            right: 100,
            containLabel: true //防止标签溢出
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow',
                label: { // 移上去以后坐标轴高亮
                    show: true,
                    backgroundColor: '#444141',
                },
            },
            formatter: (params) => {
                let words = '<div style="padding:0.1rem">' + params[0].name + '</div>';
                params.reverse();
                for (let param of params) {
                    if (!param.data) continue;
                    // words += param.marker + 'word:&nbsp;' + param.data.type + '&nbsp;&nbsp;freq:&nbsp;' + param.data.value + '<br>';
                    words += param.marker + param.data.type + '&nbsp:&nbsp;' + param.data.value + '%' + '<br>';
                }
                return words;
            }
        },
        xAxis: [{
            type: 'category',
            data: ten_year,
            axisLabel: {
                show: true,
                textStyle:{
                    fontSize: 18,
                    color: '#ffffff'
                },
                // interval: 0,
                // rotate: 30,
            },
            axisLine:{
                lineStyle:{
                    color:'#ffffff',
                    width:1,//这里是为了突出显示加上的
                }
            },
        }],
        yAxis: [{
            type: 'value',
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
        }],
        series: seriesData
    }
    myChart.setOption(option);
}