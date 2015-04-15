var req;

// Sends a new request to update the to-do list
function loadSleepJsonDoc() {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange = handleResponseSleep;
    req.open("GET", "jsonGetOneDayLettters", true);
    req.send(); 
} 

// This function is called for each request readystatechange,
// and it will eventually parse the XML response for the request
function handleResponseSleep() {
    if (req.readyState != 4 || req.status != 200) {
        return;
    }
    var removesleepchart = document.getElementById("sleepChart");
    while (removesleepchart.hasChildNodes()) {
        removesleepchart.removeChild(removesleepchart.firstChild);
    }

    var dataset = JSON.parse(req.responseText);

    var margin ={top:20, right:30, bottom:30, left:40};
    width=450-margin.left - margin.right, 
    height=380-margin.top-margin.bottom;


    // scale to ordinal because x axis is not numerical
    var x = d3.scale.ordinal().rangeRoundBands([0, width], .1);

    //scale to numerical value by height
    var y = d3.scale.linear().range([height, 0]);

    var chart = d3.select("#sleepChart")  

                  .append("svg")  //append svg element inside #chart
                  .attr("width", width+(2*margin.left)+margin.right)    //set width
                  .attr("height", height+margin.top+margin.bottom);  //set height
        // var chart = d3.select("#selfChart")  
        //           .append("svg")  //append svg element inside #chart
        //           .attr("width", 400)    //set width
        //           .attr("height", 400);  //set height

    var xAxis = d3.svg.axis()
                  .scale(x)
                  .orient("bottom");  //orient bottom because x-axis will appear below the bars

    var yAxis = d3.svg.axis()
                  .scale(y)
                  .orient("left");

    d3.json("jsonGetOneDayLettters", function(error, data){
      x.domain(data.map(function(d){ return d.key}));
      y.domain([0, 1.1 *  d3.max(data, function(d){return d.value})]);
      
      var bar = chart.selectAll("g")
                        .data(data)
                      .enter()
                        .append("g")
                        .attr("transform", function(d, i){
                          return "translate("+x(d.key)+", 0)";
                        });
      
      bar.append("rect")
          .attr("y", function(d) { 
            return y(d.value); 
          })
          .attr("x", function(d,i){
            return 2 * (x.rangeBand()+(margin.left/4)) ;
          })
          .attr("height", function(d) { 
            return height - y(d.value); 
          })
          .attr("width", x.rangeBand());  //set width base on range on ordinal data

      bar.append("text")
          .attr("x", x.rangeBand()+margin.left )
          .attr("y", function(d) { return y(d.value) -10; })
          .attr("dy", ".75em")
          .text(function(d) { return d.value; });
      
      chart.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate("+margin.left+","+ height+")")        
            .call(xAxis)
            .append("text")
            .attr("x", 200 )
            .attr("y",  20 )
            .attr("dy", ".71em")
            .style("text-anchor", "middle")
            .text("Time");

            chart.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate("+margin.left+",0)")
            .call(yAxis)
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Number");
    });

    function type(d) {
        d.key = +d.key; // coerce to number
        return d;
      }
  }


