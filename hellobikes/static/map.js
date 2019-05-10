function MapOperate() {

}

MapOperate.prototype.listensubmit = function () {
    var self = this;
    var submitBut = $(".submit-btn");


    var time_id = $("#time-id");
    var time_now = new Date(time_id.html());


    submitBut.click(function () {
        var btn = $(this);
        var data_id = btn.attr('data-id');
        var datas = self.format(time_now, "yyyy-MM-dd HH:mm");
        switch (data_id) {
            case data_id = "a":
                console.log("a");
                time_now = new Date(time_id.html());
                var t = time_now.getTime();
                t -= 1900000;
                datas = new Date(t);
                datas = self.format(datas, "yyyy-MM-dd HH:mm");
                break;
            case data_id = "b":
                console.log("b");
                time_now = new Date(time_id.html());
                var t = time_now.getTime();
                t -= 120000;
                datas = new Date(t);
                datas = self.format(datas, "yyyy-MM-dd HH:mm");
                break;
            case data_id = "c":
                console.log("c");
                datas = "2019-05-05 12:01";
                break;
            case data_id = "d":
                console.log("d");
                time_now = new Date(time_id.html());
                var t = time_now.getTime();
                t += 120000;
                datas = new Date(t);
                datas = self.format(datas, "yyyy-MM-dd HH:mm");
                break;
            case data_id = "e":
                console.log("e");
                time_now = new Date(time_id.html());
                var t = time_now.getTime();
                t += 1900000;
                datas = new Date(t);
                datas = self.format(datas, "yyyy-MM-dd HH:mm");
                break;

        }
        console.log(datas);
        var div = document.getElementById("time-id");
        div.innerText = datas;


        $.ajax({
            type: 'post',
            async: false,
            url: '/index',
            data: {
                "datas": datas,
            },
            success: function (result) {
                //stringify()用于从一个对象解析出字符串
                // jsonData = JSON.stringify(result['result']);
                // console.log(jsonData);
                //JSON.parse用于从一个字符串中解析出json对象
                var map = new AMap.Map('container', {
                    zoom:15,
                    center: [119.03797, 33.548503]
                });
                var jsondata = JSON.stringify(result['result']);
                var dt = JSON.parse(jsondata);
                if (dt.length > 0) {
                    var style = [{
                        url: 'https://a.amap.com/jsapi_demos/static/images/mass0.png',
                        anchor: new AMap.Pixel(6, 6),
                        size: new AMap.Size(8, 8)
                    }, {
                        url: 'https://a.amap.com/jsapi_demos/static/images/mass0.png',
                        anchor: new AMap.Pixel(3, 3),
                        size: new AMap.Size(8, 8)
                    }, {
                        url: 'https://a.amap.com/jsapi_demos/static/images/mass0.png',
                        anchor: new AMap.Pixel(4, 4),
                        size: new AMap.Size(8, 8)
                    }
                    ];
                    var massMarks = [];
                    for (var i = 0; i < dt.length; i++) {
                        var point = {'lnglat': [dt[i][0], dt[i][1]], 'name': "1", 'id': i};
                        massMarks.push(point);
                    }
                    var mass = new AMap.MassMarks(massMarks, {
                        opacity: 0.8,
                        zIndex: 111,
                        cursor: 'pointer',
                        style: style
                    });

                    var marker = new AMap.Marker({content: ' ', map: map});
                    mass.on('mouseover', function (e) {
                        marker.setPosition(e.data.lnglat);
                        marker.setLabel({content: e.data.name})
                    });
                    mass.setMap(map);

                }
            }
        });


    });
};

MapOperate.prototype.run = function () {
    var self = this;
    self.listensubmit();
};


MapOperate.prototype.tool = function (ResultList) {
    // 创建地图实例
    var map = new AMap.Map("container", {
        zoom: 13,
        center: [119.038, 33.548],
        resizeEnable: true,
        mapStyle: 'amap://styles/whitesmoke'
    });
    var positions = ResultList;
    var anchor = [
        'bottom-left',
        'bottom-center',
        'bottom-right',
        'middle-left',
        'center',
        'middle-right',
        'top-left',
        'top-center',
        'top-right'
    ];
    var pos_icon = [];
    var pos_marker = [];
    var icon = [];
    var marker = [];
    for (var i = 0; i < 100; i++) {
        // 创建一个 Icon
        pos_icon[i] = new AMap.Icon({
            // 图标尺寸
            size: new AMap.Size(12, 12),
            // 图标的取图地址
            image: '//a.amap.com/jsapi_demos/static/demo-center/marker/marker.png',
            // 图标所用图片大小
            imageSize: new AMap.Size(12, 12),
        });


        // 将 Icon 传入 marker
        pos_marker[i] = new AMap.Marker({
            position: positions[i],
            icon: pos_icon[i],
            anchor: 'center', //设置锚点
            offset: new AMap.Pixel(0, 0) //设置偏移量
        });
        map.add(pos_marker[i]);

    }
};

$(function () {
    var map = new MapOperate();
    map.run();
});

MapOperate.prototype.format = function (now, mask) {

    var d = now;
    var zeroize = function (value, length) {
        if (!length) length = 2;
        value = String(value);
        for (var i = 0, zeros = ''; i < (length - value.length); i++) {
            zeros += '0';
        }
        return zeros + value;
    };

    return mask.replace(/"[^"]*"|'[^']*'|\b(?:d{1,4}|m{1,4}|yy(?:yy)?|([hHMstT])\1?|[lLZ])\b/g, function ($0) {
        switch ($0) {
            case 'd':
                return d.getDate();
            case 'dd':
                return zeroize(d.getDate());
            case 'ddd':
                return ['Sun', 'Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat'][d.getDay()];
            case 'dddd':
                return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][d.getDay()];
            case 'M':
                return d.getMonth() + 1;
            case 'MM':
                return zeroize(d.getMonth() + 1);
            case 'MMM':
                return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][d.getMonth()];
            case 'MMMM':
                return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][d.getMonth()];
            case 'yy':
                return String(d.getFullYear()).substr(2);
            case 'yyyy':
                return d.getFullYear();
            case 'h':
                return d.getHours() % 12 || 12;
            case 'hh':
                return zeroize(d.getHours() % 12 || 12);
            case 'H':
                return d.getHours();
            case 'HH':
                return zeroize(d.getHours());
            case 'm':
                return d.getMinutes();
            case 'mm':
                return zeroize(d.getMinutes());
            case 's':
                return d.getSeconds();
            case 'ss':
                return zeroize(d.getSeconds());
            case 'l':
                return zeroize(d.getMilliseconds(), 3);
            case 'L':
                var m = d.getMilliseconds();
                if (m > 99) m = Math.round(m / 10);
                return zeroize(m);
            case 'tt':
                return d.getHours() < 12 ? 'am' : 'pm';
            case 'TT':
                return d.getHours() < 12 ? 'AM' : 'PM';
            case 'Z':
                return d.toUTCString().match(/[A-Z]+$/);
            // Return quoted strings with the surrounding quotes removed
            default:
                return $0.substr(1, $0.length - 2);
        }
    });

}




