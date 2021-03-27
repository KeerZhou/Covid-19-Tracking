// 基于准备好的dom，初始化echarts实例
var accuChart = echarts.init(document.getElementById('country_line_accu'));

// 指定图表的配置项和数据
var option = {
    title: {
        text: '累计确诊人数',
        left: 'center',
        top: 'top',
        textStyle: {
            fontSize: 15
        }
    },
    tooltip: {
        trigger: 'axis',
        formatter: '{b0}: {c0}'
    },
    legend: {
        left: 'right',
        top: 'top'
    },
    grid: {
        x: 76
    },
    xAxis: {
        name: '日期',
        data: [],
        nameTextStyle: {
            fontSize: 12,
            fontWeight: 'bold',
            fontFamily: 'msyh'
        },
        axisLabel: {
            interval: [],
            showMaxLabel: true,
            rotate: 35,
            textStyle: {
                fontSize: 12,
                fontWeight: 'bold',
            }
        },
    },
    yAxis: [{
        type: 'value',
        name: '人数',
        show: true,
        nameTextStyle: {
            fontSize: 12,
            fontWeight: 'bold',
            fontFamily: 'msyh'
        },
        splitLine: {
            show: true,
            lineStyle: {
                color: ['#baddeb'],
                width: 2,
            }
        },
        axisLine: {
            lineStyle: {
                width: 1,
            }
        },
        axisLabel: {
            textStyle: {
                fontSize: 12,
                fontWeight: 'bold'
            }
        }
    }],
    series: [{
        type: 'bar',
        barWidth: '50%',
        data: [],
        itemStyle: {
            color: '#ee9b90'
        }
    },{
        type: 'line',
        smooth: true,
        data: [],
        itemStyle: {
            color: '#c33531',
        },
        lineStyle: {
            width: 3
        }
    }]
};


// 使用刚指定的配置项和数据显示图表。
accuChart.setOption(option);

// 基于准备好的dom，初始化echarts实例
var incrChart = echarts.init(document.getElementById('country_line_incr'));

// 指定图表的配置项和数据
var option = {
    title: {
        text: '新增确诊人数',
        left: 'center',
        top: 'top',
        textStyle:{
            fontSize:15
        }
    },
    tooltip: {
        trigger:'axis',
        formatter: '{b0}: {c0}'
    },
    legend: {
        left: 'right',
        top: 'top'
    },
    grid: {
      x:70
    },
    xAxis: {
        name: '日期',
        data: [],
        nameTextStyle:{
            fontSize: 12,
            fontWeight: 'bold',
            fontFamily:'msyh'
        },
        axisLabel:{
            interval:[],
            showMaxLabel: true,
            rotate:35,
            textStyle: {
                fontSize: 12,
                fontWeight: 'bold',
            }
        },
    },
    yAxis: [ {
        type: 'value',
        name: '人数',
        show:true,
        nameTextStyle:{
            fontSize: 12,
            fontWeight: 'bold',
            fontFamily:'msyh'
        },
        splitLine:{
            show: true,
            lineStyle:{
               color: ['#baddeb'],
               width: 2,
          }
        },
        axisLine: {
            lineStyle: {
                width: 1,
            }
        },
        axisLabel: {
            textStyle: {
                fontSize: 12,
                fontWeight: 'bold'
            }
        }
    }],
    series: [{
        type: 'bar',
        barWidth : '50%',
        data: [],
        itemStyle: {
            color: '#ee9b90'
        }
    },{
        type: 'line',
        smooth:true,
        data: [],
        itemStyle: {
            color: '#c33531',
        },
        lineStyle: {
            width: 3
        }
    }]
};

// 使用刚指定的配置项和数据显示图表。
incrChart.setOption(option);



// 基于准备好的dom，初始化echarts实例
var deadChart = echarts.init(document.getElementById('country_line_deadincr'));

// 指定图表的配置项和数据
var option = {
    title: {
        text: '新增死亡人数',
        left: 'center',
        top: 'top',
        textStyle:{
            fontSize:15
        }
    },
    tooltip: {
        trigger:'axis',
        formatter: '{b0}: {c0}'
    },
    legend: {
        left: 'right',
        top: 'top'
    },
    grid: {
      x:70
    },
    xAxis: {
        name: '日期',
        data: [],
        nameTextStyle:{
            fontSize: 12,
            fontWeight: 'bold',
            fontFamily:'msyh'
        },
        axisLabel:{
            interval:[],
            showMaxLabel: true,
            rotate:35,
            textStyle: {
                fontSize: 12,
                fontWeight: 'bold',
            }
        },
    },
    yAxis: [ {
        type: 'value',
        name: '人数',
        show:true,
        nameTextStyle:{
            fontSize: 12,
            fontWeight: 'bold',
            fontFamily:'msyh'
        },
        splitLine:{
            show: true,
            lineStyle:{
               color: ['#baddeb'],
               width: 2,
          }
        },
        axisLine: {
            lineStyle: {
                width: 1,
            }
        },
        axisLabel: {
            textStyle: {
                fontSize: 12,
                fontWeight: 'bold'
            }
        }
    }],
    series: [{
        type: 'bar',
        barWidth : '50%',
        data: [],
        itemStyle: {
            color: '#919191'
        }
    },{
        type: 'line',
        smooth:true,
        data: [],
        itemStyle: {
            color: '#000000',
        },
        lineStyle: {
            width: 3
        }
    }]
};

// 使用刚指定的配置项和数据显示图表。
deadChart.setOption(option);


var charts_background_block = document.getElementById("charts_background");
var list_block_name = document.getElementById("country_select_name")
var list_block = document.getElementById("country_select_list")
list_block_name.onmouseover = function () {
    list_block.style.display = 'block';
    };
charts_background_block.onclick = function(){
    list_block.style.display = 'none';
}
var lis = document.getElementById("country_select_list").getElementsByTagName("li");
var select_day = document.getElementById("select_day_btn");
var select_day_btn_14 = document.getElementById("select_day_btn_14");
var select_day_btn_90 = document.getElementById("select_day_btn_90");

//全球地图
var global_line = document.getElementById("global_line");
var country_line = document.getElementById("country_line");
for(var i = 0; i<lis.length; i++){
    if(lis[i].innerHTML == "全球"){
        lis[i].onclick = function() {
            show_world_sitn(this);
        }
    }else if(lis[i].innerHTML == "英国"){
        lis[i].onclick = function (){
            show_country_sitn(this);
            update(country_accu_data['date_14'],2,country_accu_data['英国_14'],country_incr_data['英国_14'],country_dead_data['英国_14']);
        };
    }else if(lis[i].innerHTML == "美国"){
        lis[i].onclick = function (){
            show_country_sitn(this);
            update(country_accu_data['date_14'],2,country_accu_data['美国_14'],country_incr_data['美国_14'],country_dead_data['美国_14']);
        };
    }else if(lis[i].innerHTML == "中国"){
        lis[i].onclick = function (){
            show_country_sitn(this);
            update(country_accu_data['date_14'],2,country_accu_data['中国_14'],country_incr_data['中国_14'],country_dead_data['中国_14']);
        };
    }else if(lis[i].innerHTML == "巴西"){
        lis[i].onclick = function (){
            show_country_sitn(this);
            update(country_accu_data['date_14'],2,country_accu_data['巴西_14'],country_incr_data['巴西_14'],country_dead_data['巴西_14']);
        };
    }else if(lis[i].innerHTML == "印度"){
        lis[i].onclick = function (){
            show_country_sitn(this);
            update(country_accu_data['date_14'],2,country_accu_data['印度_14'],country_incr_data['印度_14'],country_dead_data['印度_14']);
        };
    }else if(lis[i].innerHTML == "俄罗斯"){
        lis[i].onclick = function (){
            show_country_sitn(this);
            update(country_accu_data['date_14'],2,country_accu_data['俄罗斯_14'],country_incr_data['俄罗斯_14'],country_dead_data['俄罗斯_14']);
        };
    }else{
        lis[i].onclick = function() {
            show_country_sitn(this);
        }
    }
}

select_day_btn_90.onclick = function () {
    select_day_btn_14.style.border = '2px rgba(0, 0, 0, 0.17) solid';
    select_day_btn_90.style.border = '2px rgba(0, 0, 0, 0.55) solid';
    if(list_block_name.innerHTML == "英国"){
        update(country_accu_data['date_90'], 30, country_accu_data['英国_90'], country_incr_data['英国_90'], country_dead_data['英国_90']);
    }else if (list_block_name.innerHTML == "美国"){
        update(country_accu_data['date_90'], 30, country_accu_data['美国_90'], country_incr_data['美国_90'], country_dead_data['美国_90']);
    }else if (list_block_name.innerHTML == "中国"){
        update(country_accu_data['date_90'], 30, country_accu_data['中国_90'], country_incr_data['中国_90'], country_dead_data['中国_90']);
    }else if (list_block_name.innerHTML == "巴西"){
        update(country_accu_data['date_90'], 30, country_accu_data['巴西_90'], country_incr_data['巴西_90'], country_dead_data['巴西_90']);
    }else if (list_block_name.innerHTML == "印度"){
        update(country_accu_data['date_90'], 30, country_accu_data['印度_90'], country_incr_data['印度_90'], country_dead_data['印度_90']);
    }else if (list_block_name.innerHTML == "俄罗斯"){
        update(country_accu_data['date_90'], 30, country_accu_data['俄罗斯_90'], country_incr_data['俄罗斯_90'], country_dead_data['俄罗斯_90']);
    }

};

select_day_btn_14.onclick = function () {
    select_day_btn_14.style.border = '2px rgba(0, 0, 0, 0.55) solid';
    select_day_btn_90.style.border = '2px rgba(0, 0, 0, 0.17) solid';
    if(list_block_name.innerHTML == "英国"){
        update(country_accu_data['date_14'], 2, country_accu_data['英国_14'], country_incr_data['英国_14'], country_dead_data['英国_14']);
    }else if (list_block_name.innerHTML == "美国"){
        update(country_accu_data['date_14'], 2, country_accu_data['美国_14'], country_incr_data['美国_14'], country_dead_data['美国_14']);
    }else if (list_block_name.innerHTML == "中国"){
        update(country_accu_data['date_14'], 2, country_accu_data['中国_14'], country_incr_data['中国_14'], country_dead_data['中国_14']);
    }else if (list_block_name.innerHTML == "巴西"){
        update(country_accu_data['date_14'], 2, country_accu_data['巴西_14'], country_incr_data['巴西_14'], country_dead_data['巴西_14']);
    }else if (list_block_name.innerHTML == "印度"){
        update(country_accu_data['date_14'], 2, country_accu_data['印度_14'], country_incr_data['印度_14'], country_dead_data['印度_14']);
    }else if (list_block_name.innerHTML == "俄罗斯"){
        update(country_accu_data['date_14'], 2, country_accu_data['俄罗斯_14'], country_incr_data['俄罗斯_14'], country_dead_data['俄罗斯_14']);
    }
};

function a(obj) {
    document.getElementById("test").innerHTML = obj.innerHTML;
}

//展示国家情况
function show_country_sitn(obj) {
    global_line.style.display = 'none';
    country_line.style.display = 'block';
    select_day.style.display = 'inline-block';
    select_day_btn_14.style.border = '2px rgba(0, 0, 0, 0.55) solid';
    select_day_btn_90.style.border = '2px rgba(0, 0, 0, 0.17) solid';
    document.getElementById("country_select_name").innerHTML = obj.innerHTML;
    list_block.style.display = 'none';
}

//展示世界情况
function show_world_sitn(obj) {
    country_line.style.display = 'none';
    global_line.style.display='block';
    select_day.style.display = 'none';
    document.getElementById("country_select_name").innerHTML = obj.innerHTML;
    list_block.style.display='none';
}

function update(date,interval,data1,data2,data3) {
    //刷新数据
    var option1 = accuChart.getOption();
    option1.xAxis[0].data = date;
    option1.xAxis[0].axisLabel.interval = interval;
    option1.series[0].data = data1;
    option1.series[1].data = data1;
    accuChart.setOption(option1);

    var option2 = incrChart.getOption();
    option2.xAxis[0].data = date;
    option2.xAxis[0].axisLabel.interval = interval;
    option2.series[0].data = data2;
    option2.series[1].data = data2;
    incrChart.setOption(option2);

    var option3 = deadChart.getOption();
    option3.xAxis[0].data = date;
    option3.xAxis[0].axisLabel.interval = interval;
    option3.series[0].data = data3;
    option3.series[1].data = data3;
    deadChart.setOption(option3);
}