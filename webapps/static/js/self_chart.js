var req;

// Sends a new request to update the to-do list
function loadJsonDoc() {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange = handleResponse;
    req.open("GET", "jsonGetLettters", true);
    req.send(); 
}

// This function is called for each request readystatechange,
// and it will eventually parse the XML response for the request
function handleResponse() {
    if (req.readyState != 4 || req.status != 200) {
        return;
    }

    var dataset = JSON.parse(req.responseText);

    var w = 600;
    var h = 250;

var xScale = d3.scale.ordinal()
                .domain(d3.range(dataset.length))
                .rangeRoundBands([0, w], 0.05); 

var yScale = d3.scale.linear()
                .domain([0, d3.max(dataset, function(d) {return d.value;})])
                .range([0, h]);



var xAxis = d3.svg.axis()
              .scale(x)
              .orient("bottom");  //orient bottom because x-axis will appear below the bars

var yAxis = d3.svg.axis()
              .scale(y)
              .orient("left");

var x = d3.scale.ordinal().rangeRoundBands([0, width], .1);

//scale to numerical value by height
var y = d3.scale.linear().range([height, 0]);

var key = function(d) {
    return d.key;
};

var margin ={top:20, right:30, bottom:30, left:40},
width=960-margin.left - margin.right, 
height=500-margin.top-margin.bottom;

//Create SVG element
var svg = d3.select("#selfChart")
            .append("svg")
            .attr("width", w)
            .attr("height", h);

//Create bars
svg.selectAll("rect")
   .data(dataset, key)
   .enter()
   .append("rect")
   .attr("x", function(d, i) {
        return xScale(i);
   })
   .attr("y", function(d) {
        return h - yScale(d.value);
   })
   .attr("width", xScale.rangeBand())
   .attr("height", function(d) {
        return yScale(d.value);
   })
   .attr("fill", function(d) {
        return "rgb(0, 0, " + (d.value * 10) + ")";
   })

    //Tooltip
    .on("mouseover", function(d) {
        //Get this bar's x/y values, then augment for the tooltip
        var xPosition = parseFloat(d3.select(this).attr("x")) + xScale.rangeBand() / 2;
        var yPosition = parseFloat(d3.select(this).attr("y")) + 14;
        
        //Update Tooltip Position & value
        d3.select("#tooltip")
            .style("left", xPosition + "px")
            .style("top", yPosition + "px")
            .select("#value")
            .text(d.value);
        d3.select("#tooltip").classed("hidden", false)
    })
    .on("mouseout", function() {
        //Remove the tooltip
        d3.select("#tooltip").classed("hidden", true);
    })  ;

//Create labels
svg.selectAll("text")
   .data(dataset, key)
   .enter()
   .append("text")
   .text(function(d) {
        return d.value;
   })
   .attr("text-anchor", "middle")
   .attr("x", function(d, i) {
        return xScale(i) + xScale.rangeBand() / 2;
   })
   .attr("y", function(d) {
        return h - yScale(d.value) + 14;
   })
   .attr("font-family", "sans-serif") 
   .attr("font-size", "11px")
   .attr("fill", "white");


svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate("+margin.left+","+ height+")")        
    .call(xAxis);

svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate("+margin.left+",0)")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Number");

var sortOrder = false;
var sortBars = function () {
    sortOrder = !sortOrder;
    
    sortItems = function (a, b) {
        if (sortOrder) {
            return a.value - b.value;
        }
        return b.value - a.value;
    };

    svg.selectAll("rect")
        .sort(sortItems)
        .transition()
        .delay(function (d, i) {
        return i * 50;
    })
        .duration(1000)
        .attr("x", function (d, i) {
        return xScale(i);
    });

    svg.selectAll('text')
        .sort(sortItems)
        .transition()
        .delay(function (d, i) {
        return i * 50;
    })
        .duration(1000)
        .text(function (d) {
        return d.value;
    })
        .attr("text-anchor", "middle")
        .attr("x", function (d, i) {
        return xScale(i) + xScale.rangeBand() / 2;
    })
        .attr("y", function (d) {
        return h - yScale(d.value) + 14;
    });
};
// Add the onclick callback to the button
d3.select("#sort").on("click", sortBars);
d3.select("#reset").on("click", reset);
function randomSort() {

    
    svg.selectAll("rect")
        .sort(sortItems)
        .transition()
        .delay(function (d, i) {
        return i * 50;
    })
        .duration(1000)
        .attr("x", function (d, i) {
        return xScale(i);
    });

    svg.selectAll('text')
        .sort(sortItems)
        .transition()
        .delay(function (d, i) {
        return i * 50;
    })
        .duration(1000)
        .text(function (d) {
        return d.value;
    })
        .attr("text-anchor", "middle")
        .attr("x", function (d, i) {
        return xScale(i) + xScale.rangeBand() / 2;
    })
        .attr("y", function (d) {
        return h - yScale(d.value) + 14;
    });
}
function reset() {
    svg.selectAll("rect")
        .sort(function(a, b){
            return a.key - b.key;
        })
        .transition()
        .delay(function (d, i) {
        return i * 50;
        })
        .duration(1000)
        .attr("x", function (d, i) {
        return xScale(i);
        });
        
    svg.selectAll('text')
        .sort(function(a, b){
            return a.key - b.key;
        })
        .transition()
        .delay(function (d, i) {
        return i * 50;
    })
        .duration(1000)
        .text(function (d) {
        return d.value;
    })
        .attr("text-anchor", "middle")
        .attr("x", function (d, i) {
        return xScale(i) + xScale.rangeBand() / 2;
    })
        .attr("y", function (d) {
        return h - yScale(d.value) + 14;
    });
};




}






// var w = 600;
// var h = 250;

// var dataset = [ 
//     { key: 0, value: 5 },
//     { key: 1, value: 10 },
//     { key: 2, value: 13 },
//     { key: 3, value: 19 },
//     { key: 4, value: 21 },
//     { key: 5, value: 25 },
//     { key: 6, value: 22 },
//     { key: 7, value: 18 },
//     { key: 8, value: 15 },
//     { key: 9, value: 13 },
//     { key: 10, value: 11 },
//     { key: 11, value: 12 },
//     { key: 12, value: 15 },
//     { key: 13, value: 20 },
//     { key: 14, value: 18 },
//     { key: 15, value: 17 },
//     { key: 16, value: 16 },
//     { key: 17, value: 18 },
//     { key: 18, value: 23 },
//     { key: 19, value: 25 } ];

// var xScale = d3.scale.ordinal()
//                 .domain(d3.range(dataset.length))
//                 .rangeRoundBands([0, w], 0.05); 

// var yScale = d3.scale.linear()
//                 .domain([0, d3.max(dataset, function(d) {return d.value;})])
//                 .range([0, h]);

// var key = function(d) {
//     return d.key;
// };

// //Create SVG element
// var svg = d3.select("body")
//             .append("svg")
//             .attr("width", w)
//             .attr("height", h);

// //Create bars
// svg.selectAll("rect")
//    .data(dataset, key)
//    .enter()
//    .append("rect")
//    .attr("x", function(d, i) {
//         return xScale(i);
//    })
//    .attr("y", function(d) {
//         return h - yScale(d.value);
//    })
//    .attr("width", xScale.rangeBand())
//    .attr("height", function(d) {
//         return yScale(d.value);
//    })
//    .attr("fill", function(d) {
//         return "rgb(0, 0, " + (d.value * 10) + ")";
//    })

//     //Tooltip
//     .on("mouseover", function(d) {
//         //Get this bar's x/y values, then augment for the tooltip
//         var xPosition = parseFloat(d3.select(this).attr("x")) + xScale.rangeBand() / 2;
//         var yPosition = parseFloat(d3.select(this).attr("y")) + 14;
        
//         //Update Tooltip Position & value
//         d3.select("#tooltip")
//             .style("left", xPosition + "px")
//             .style("top", yPosition + "px")
//             .select("#value")
//             .text(d.value);
//         d3.select("#tooltip").classed("hidden", false)
//     })
//     .on("mouseout", function() {
//         //Remove the tooltip
//         d3.select("#tooltip").classed("hidden", true);
//     })  ;

// //Create labels
// svg.selectAll("text")
//    .data(dataset, key)
//    .enter()
//    .append("text")
//    .text(function(d) {
//         return d.value;
//    })
//    .attr("text-anchor", "middle")
//    .attr("x", function(d, i) {
//         return xScale(i) + xScale.rangeBand() / 2;
//    })
//    .attr("y", function(d) {
//         return h - yScale(d.value) + 14;
//    })
//    .attr("font-family", "sans-serif") 
//    .attr("font-size", "11px")
//    .attr("fill", "white");
   
// var sortOrder = false;
// var sortBars = function () {
//     sortOrder = !sortOrder;
    
//     sortItems = function (a, b) {
//         if (sortOrder) {
//             return a.value - b.value;
//         }
//         return b.value - a.value;
//     };

//     svg.selectAll("rect")
//         .sort(sortItems)
//         .transition()
//         .delay(function (d, i) {
//         return i * 50;
//     })
//         .duration(1000)
//         .attr("x", function (d, i) {
//         return xScale(i);
//     });

//     svg.selectAll('text')
//         .sort(sortItems)
//         .transition()
//         .delay(function (d, i) {
//         return i * 50;
//     })
//         .duration(1000)
//         .text(function (d) {
//         return d.value;
//     })
//         .attr("text-anchor", "middle")
//         .attr("x", function (d, i) {
//         return xScale(i) + xScale.rangeBand() / 2;
//     })
//         .attr("y", function (d) {
//         return h - yScale(d.value) + 14;
//     });
// };
// // Add the onclick callback to the button
// d3.select("#sort").on("click", sortBars);
// d3.select("#reset").on("click", reset);
// function randomSort() {

    
//     svg.selectAll("rect")
//         .sort(sortItems)
//         .transition()
//         .delay(function (d, i) {
//         return i * 50;
//     })
//         .duration(1000)
//         .attr("x", function (d, i) {
//         return xScale(i);
//     });

//     svg.selectAll('text')
//         .sort(sortItems)
//         .transition()
//         .delay(function (d, i) {
//         return i * 50;
//     })
//         .duration(1000)
//         .text(function (d) {
//         return d.value;
//     })
//         .attr("text-anchor", "middle")
//         .attr("x", function (d, i) {
//         return xScale(i) + xScale.rangeBand() / 2;
//     })
//         .attr("y", function (d) {
//         return h - yScale(d.value) + 14;
//     });
// }
// function reset() {
//     svg.selectAll("rect")
//         .sort(function(a, b){
//             return a.key - b.key;
//         })
//         .transition()
//         .delay(function (d, i) {
//         return i * 50;
//         })
//         .duration(1000)
//         .attr("x", function (d, i) {
//         return xScale(i);
//         });
        
//     svg.selectAll('text')
//         .sort(function(a, b){
//             return a.key - b.key;
//         })
//         .transition()
//         .delay(function (d, i) {
//         return i * 50;
//     })
//         .duration(1000)
//         .text(function (d) {
//         return d.value;
//     })
//         .attr("text-anchor", "middle")
//         .attr("x", function (d, i) {
//         return xScale(i) + xScale.rangeBand() / 2;
//     })
//         .attr("y", function (d) {
//         return h - yScale(d.value) + 14;
//     });
// };







// // Generate a Bates distribution of 10 random variables.
// var values = d3.range(1000).map(d3.random.bates(10));

// // A formatter for counts.
// var formatCount = d3.format(",.0f");

// var margin = {top: 10, right: 30, bottom: 30, left: 30},
//     width = 960 - margin.left - margin.right,
//     height = 500 - margin.top - margin.bottom;

// var x = d3.scale.linear()
//     .domain([0, 1])
//     .range([0, width]);

// // Generate a histogram using twenty uniformly-spaced bins.
// var data = d3.layout.histogram()
//     .bins(x.ticks(20))
//     (values);

// var y = d3.scale.linear()
//     .domain([0, d3.max(data, function(d) { return d.y; })])
//     .range([height, 0]);

// var xAxis = d3.svg.axis()
//     .scale(x)
//     .orient("bottom");

// var svg = d3.select("#selfChart").append("svg")
//     .attr("width", width + margin.left + margin.right)
//     .attr("height", height + margin.top + margin.bottom)
//   .append("g")
//     .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// var bar = svg.selectAll(".bar")
//     .data(data)
//   .enter().append("g")
//     .attr("class", "bar")
//     .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

// bar.append("rect")
//     .attr("x", 1)
//     .attr("width", x(data[0].dx) - 1)
//     .attr("height", function(d) { return height - y(d.y); });

// bar.append("text")
//     .attr("dy", ".75em")
//     .attr("y", 6)
//     .attr("x", x(data[0].dx) / 2)
//     .attr("text-anchor", "middle")
//     .text(function(d) { return formatCount(d.y); });

// svg.append("g")
//     .attr("class", "x axis")
//     .attr("transform", "translate(0," + height + ")")
//     .call(xAxis);
