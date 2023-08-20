(() => {
    'use strict'

    function alert(message) {
        var wrapper = document.querySelector('#alertPlaceHolder');
        if (message == null) {
            wrapper.innerHTML = '';
        }
        else {
            wrapper.innerHTML = '<div class="alert alert-danger d-flex align-items-center" role="alert"><svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg><div id="disconnect_alert_text">'+message+'</div></div>';
        }
    }

    function setProgress(progress) {
        document.querySelector('#progress').setAttribute("value", progress);
    }

    function setResult(nodes) {
        var innerHTML = '<thead><th>#</th><th>IP</th><th>Firewall</th><th>Progress</th><th>Opened Ports</th></thead>';
        var i = 1;
        for (var key in nodes){
            if (nodes[key] != null){
                innerHTML += '<tr><th scope="row">'+i+'</td><td>'+key+'</td><td>';
                innerHTML += nodes[key].firewall_detected == 1 ? 'Y' : 'N'
                innerHTML += '</td><td><div class="progress">';
                innerHTML += '<progress value="'+nodes[key].progress+'" max="100" style="width: 100%; background-color: white;"></progress>';
                innerHTML += '</div></td><td>';
                if (nodes[key].opened_ports.length) {
                    innerHTML += nodes[key].opened_ports;
                } else {
                    innerHTML += 'No opened ports found.';
                }
                innerHTML += '</td></tr>';
            }
            i ++;
        }
        document.querySelector('#discovery_result').innerHTML = innerHTML;
    }
    function showGraph(graph) {
        var gnodes = graph.NODES;
        var nodes = [];
        for (var key in gnodes){
            if (gnodes[key] != null){
                nodes.push({
                    id: key,
                    dataLabels: {
                        enabled: true
                    },
                    marker: {
                        fillColor: gnodes[key].firewall_detected ? 'green' : '#1aadce'
                    }
                });
            }
        }
        Highcharts.chart('networkGraph', {
            chart: {
                type: 'networkgraph',
                plotBorderWidth: 1
            },
            title: {
                text: 'Network Graph',
            },
            series: [{
                nodes: nodes,
                data: graph.EDGES
            }]
        });
    }

    function connect() {
        var socket = new WebSocket('ws://' + window.location.host + '/ws' + window.location.pathname);
        alert("Connecting ...");
        socket.onopen = function(e) {
            alert(null);
        };

        socket.onerror = function(error) {
            alert(error.message);
            socket.close();
        };

        socket.onmessage = function(e) {
            const data = JSON.parse(e.data).data;
            console.log(data);
            setProgress(data.status.progress);
            showGraph(JSON.parse(data.graph));
            setResult(JSON.parse(data.graph).NODES);
            setTimeout(function() {
                socket.send(null);
            }, 10000);
        };

        socket.onclose = function(e) {  
            var distance = 10;
            var x = setInterval(function() {
                alert("Connecting ("+distance+") seconds");
                distance --;
                if (distance == 0) {
                    clearInterval(x);
                    connect();
                }
            }, 1000);
        };
    }
    connect();
})();