import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
am5.ready(function() {

  var root = am5.Root.new('chartdiv');

  root.setThemes([
    am5themes_Animated.new(root)

  ]);


  var chart = root.container.children.push(
    am5xy.XYChart.new(root, {
      panX: true,
      panY: true,
      wheelX: 'panX',
      wheelY: 'zoomX',
      layout: root.verticalLayout,
      pinchZoomX: true
    })
  );


  var cursor = chart.set('cursor', am5xy.XYCursor.new(root, {
    behavior: 'none'
  }));
  cursor.lineY.set('visible', false);


  var data = [
    {
      year: '1',
      irancell: 3,
      mokh: 5,
      mci: 2
    },
    {
      year: '2',
      irancell: 3,
      mokh: 5,
      mci: 2
    },
    {
      year: '3',
      irancell: 3,
      mokh: 5,
      mci: 2
    },
    {
      year: '4',
      irancell: 3,
      mokh: 5,
      mci: 2
    },
    {
      year: '5',
      irancell: 3,
      mokh: 5,
      mci: 2
    },
    {
      year: '6',
      irancell: 3,
      mokh: 5,
      mci: 2
    },
    {
      year: '7',
      irancell: 3,
      mokh: 5,
      mci: 2
    },
    {
      year: '8',
      irancell: 3,
      mokh: 5,
      mci: 2
    },
    {
      year: '9',
      irancell: 3,
      mokh: 3,
      mci: 2
    },
    {
      year: '10',
      irancell: 6,
      mokh: 5,
      mci: 2
    },
    {
      year: '11',
      irancell: 3,
      mokh: 2,
      mci: 1
    },
    {
      year: '12',
      irancell: 3,
      mokh: 6,
      mci: 2
    },
    {
      year: '13',
      irancell: 2,
      mokh: 3,
      mci: 4
    },
    {
      year: '14',
      irancell: 5,
      mokh: 2,
      mci: 7
    },
    {
      year: '15',
      irancell: 2,
      mokh: 3,
      mci: 6
    },
    {
      year: '16',
      irancell: 3,
      mokh: 5,
      mci: 2
    },
    {
      year: '17',
      irancell: 1,
      mokh: 2,
      mci: 4
    },
    {
      year: '18',
      irancell: 2,
      mokh: 6,
      mci: 1
    },
    {
      year: '19',
      irancell: 6,
      mokh: 2,
      mci: 5
    },
    {
      year: '20',
      irancell: 3,
      mokh: 7,
      mci: 4
    },
    {
      year: '21',
      irancell: 4,
      mokh: 1,
      mci: 2
    },
    {
      year: '22',
      irancell: 6,
      mokh: 2,
      mci: 2
    }
  ];


  var xRenderer = am5xy.AxisRendererX.new(root, {
    minorGridEnabled: true
  });
  xRenderer.grid.template.set('location', 0.5);
  xRenderer.labels.template.setAll({
    location: 0.5,
    multiLocation: 0.5
  });

  var xAxis = chart.xAxes.push(
    am5xy.CategoryAxis.new(root, {
      categoryField: 'year',
      renderer: xRenderer,
      tooltip: am5.Tooltip.new(root, {})
    })
  );

  xAxis.data.setAll(data);

  var yAxis = chart.yAxes.push(
    am5xy.ValueAxis.new(root, {
      maxPrecision: 0,
      renderer: am5xy.AxisRendererY.new(root, {
        inversed: true
      })
    })
  );


  function createSeries(name, field) {
    var series = chart.series.push(
      am5xy.LineSeries.new(root, {
        name: name,
        xAxis: xAxis,
        yAxis: yAxis,
        valueYField: field,
        categoryXField: 'year',
        tooltip: am5.Tooltip.new(root, {
          pointerOrientation: 'horizontal',
          labelText: '[bold]{name}[/]\n{categoryX}: {valueY}'
        })
      })
    );


    series.bullets.push(function() {
      return am5.Bullet.new(root, {
        sprite: am5.Circle.new(root, {
          radius: 5,
          fill: series.get('fill')
        })
      });
    });


    series.set('setStateOnChildren', true);
    series.states.create('hover', {});

    series.mainContainer.set('setStateOnChildren', true);
    series.mainContainer.states.create('hover', {});

    series.strokes.template.states.create('hover', {
      strokeWidth: 4
    });

    series.data.setAll(data);
    series.appear(1000);
  }

  createSeries('ایرانسل', 'irancell');
  createSeries('همراه اول', 'mci');
  createSeries('مخابرات', 'mokh');


  chart.set('scrollbarX', am5.Scrollbar.new(root, {
    orientation: 'horizontal',
    marginBottom: 20
  }));

  var legend = chart.children.push(
    am5.Legend.new(root, {
      centerX: am5.p50,
      x: am5.p50
    })
  );


  legend.itemContainers.template.states.create('hover', {});

  legend.itemContainers.template.events.on('pointerover', function(e) {
    e.target.dataItem.dataContext.hover();
  });
  legend.itemContainers.template.events.on('pointerout', function(e) {
    e.target.dataItem.dataContext.unhover();
  });

  legend.data.setAll(chart.series.values);


  chart.appear(1000, 100);

});
