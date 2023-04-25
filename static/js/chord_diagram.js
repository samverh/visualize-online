
// Gebaseerd op D3 voorbeeld code
// Bron: https://d3-graph-gallery.com/graph/chord_colors.html 


function chordDiagram(matrix, names) {
    // diagram
    const chord = d3.chord()
    .padAngle(0.03)
    .sortSubgroups(d3.ascending)
    const chords = chord(matrix);

    // sizes
    var width = 700;
    var height = 700;
    var innerRadius = width / 2 * 0.7;
    var outerRadius = innerRadius + 5;

    // colormap and gradient
    var color20 = d3.scaleSequential().domain([1, names.length]).interpolator(d3.interpolateRainbow);
    function getGradID(d){ return "linkGrad-" + d.source.index + "-" + d.target.index; }

    // add element
    var svg = d3.select("body")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

    // draw nodes
    var outer_arc = d3.arc()
    .innerRadius(innerRadius)
    .outerRadius(outerRadius);

    var g_outer = svg.append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
    .datum(chords);

    var group = g_outer.append("g")
    .attr("class", "groups")
    .selectAll("g")
    .data(function(chords) { return chords.groups; })
    .enter().append("g");

    // add color
    group.append("path")
    .style("fill", function(d) {
        return color20(d.index);
    })
    .style("stroke", function(d) {
        return color20(d.index);
    })
    .attr("d", outer_arc);

    // add text
    group.append("text")
    .attr("dy", ".35em") //width
    .attr("transform", function(d,i) {
        // tekst tussen begin en eind vd streep zetten
        d.angle = (d.startAngle + d.endAngle) / 2;
        d.name = names[i]; 
        return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")" +
        "translate(" + (outerRadius + 13) + ")" +
        ((d.angle > Math.PI) ? "rotate(180)" : "");
    })
    .attr("text-anchor", d => d.angle > Math.PI ? "end" : null)
    .text(function(d) {
        return d.name;
    });

    // gradient
    const grads = svg.append("defs").selectAll("linearGradient")
    .data(chords)
    .enter().append("linearGradient")
    .attr("id", getGradID)
    .attr("gradientUnits", "userSpaceOnUse")
    .attr("x1", function(d,i) { return innerRadius * Math.cos((d.source.endAngle-d.source.startAngle)/2 + d.source.startAngle - Math.PI/2); })
    .attr("y1", function(d,i) { return innerRadius * Math.sin((d.source.endAngle-d.source.startAngle)/2 + d.source.startAngle - Math.PI/2); })
    .attr("x2", function(d,i) { return innerRadius * Math.cos((d.target.endAngle-d.target.startAngle)/2 + d.target.startAngle - Math.PI/2); })
    .attr("y2", function(d,i) { return innerRadius * Math.sin((d.target.endAngle-d.target.startAngle)/2 + d.target.startAngle - Math.PI/2); })

    // starting color (at 0%)
    grads.append("stop")
    .attr("offset", "0%")
    .attr("stop-color", function(d){ return color20(d.source.index); });

    // ending color (at 100%)
    grads.append("stop")
    .attr("offset", "100%")
    .attr("stop-color", function(d){ return color20(d.target.index); });

    // add chord
    var inner_chord = d3.ribbon()
    .radius(innerRadius - 5);

    // connections
    g_outer.append("g")
    .attr("fill-opacity", .8)
    .attr("class", "ribbons")
    .selectAll("path")
    .data(function(chords) { return chords; })
    .enter().append("path")
    .attr("d", inner_chord)
    .attr("class", "chord")
    .style("fill", function(d){ return "url(#" + getGradID(d) + ")"; })
}