var chartVal = []; // グラフデータ（描画するデータ）
var userName;

  // グラフデータを取得
  function getChartData() {
    chartVal = []; // 配列を初期化
    userName = "";
    {% for obj in event_list %}
      chartVal.push({
        x: '{{ obj.date_at|date:"n/j" }}',
        y: {{ obj.evaluation }},
        uuid: '{{ obj.uuid }}',
        title:'{{obj.title}}'
      });
      userName = '{{obj.user}}';
    {% endfor %}
    
  }

    // グラフ描画処理
    function drawChart() {
      let lineCtx = document.getElementById("canvas");
      Chart.defaults.global.elements.point = {
        radius: 5,
        pointStyle: 'circle',
        hitRadius: 20,
        hoverRadius: 20,
        backgroundColor: '#blue',
      };
      Chart.defaults.global.elements.line = {
        tension: 0,
        borderDash: [],
      };
      // 線グラフの設定
      let lineConfig = {
        type: 'line',
        data: {
          // X軸のラベル
          labels: [
            {% for obj in event_list %}
          '{{ obj.date_at|date:"y/n/j" }}',
        {% endfor %}
      ],
      datasets: [{
        label: userName,
        data: chartVal,
        borderColor: '#0000000',
        pointBackgroundColor: '#47EAF4'
      }]
    },
    options: {
      scales: {
        // Y軸の最大値・最小値、目盛りの範囲などを設定する
        y: {
          min: 0,
          max: 10,
        }
      },
      tooltips:{
        backgroundColor: "rgba(19, 56, 95, 0.9)",
        callbacks:{
          title:function(tooltipItem,data){
            return chartVal[tooltipItem[0].index].title;
          }
        }
      },
      onClick: function(event, elements) {
        if (elements.length > 0) {
          let datasetIndex = elements[0].datasetIndex;
          let index = elements[0].index;
          window.location.href = "/event/" + chartVal[elements[0]._index].uuid + "/";
        }
      },
    }
  };
    let lineChart = new Chart(lineCtx, lineConfig);
}

