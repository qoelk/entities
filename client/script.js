// set the dimensions and margins of the graph
let documentId = new URLSearchParams(window.location.search).get('document_id')
const httpRequest = new XMLHttpRequest()
httpRequest.open('GET', `http://127.0.0.1:8000/documents/${documentId}`, true)
httpRequest.send()
httpRequest.onreadystatechange = function () {
    if (httpRequest.readyState === XMLHttpRequest.DONE) {
        if (httpRequest.status === 200) {
            let data = JSON.parse(httpRequest.responseText)
            document.querySelector('#text').textContent = data.document.text
        }
    }
}
console.log(documentId)
let nodes
let edges
let margin = document.querySelector('#margin').value
let charge = document.querySelector('#charge').value
let center = document.querySelector('#center').value
let collision = document.querySelector('#collision').value
let simulation
d3.json(`http://127.0.0.1:8000/documents/${documentId}/graph`, ForceGraph)

const refresh = (e) => {
    console.log(e.target.name, e.target.value)
    const value = e.target.value
    const name = e.target.name
    if (name === 'margin') {
        margin = value
    } else if (name === 'charge') {
        charge = value
        simulation.force('charge', null).force('charge', d3.forceManyBody().strength(value))
    } else if (name === 'center') {
        simulation.force('center', d3.forceCenter(value, value))
        center = value
    } else if (name === 'collision') {
        simulation.force('collision', d3.forceCollide().radius(value))
        collision = value
    }
    console.log(simulation)
    simulation.alpha(1)
}
const paramsInputs = document.querySelectorAll('.params__input')
paramsInputs.forEach(input => {
    input.addEventListener('input', refresh)
})

function ForceGraph(data) {
    nodes = data.nodes
    edges = data.links
    initSimulation()

}

let svg = d3.select("dataviz_area")

function ticked() {
    d3.select('#dataviz_area').selectAll('line').data(edges).enter()
        .append("line")
        .style("stroke", "#aaa")
        .attr("x1", function (d) {
            return d.source.x + margin;
        })
        .attr("y1", function (d) {
            return d.source.y + margin;
        })
        .attr("x2", function (d) {
            return d.target.x + margin;
        })
        .attr("y2", function (d) {
            return d.target.y + margin;
        });
    d3.select('#dataviz_area').selectAll('circle').data(nodes).enter()
        .append('circle')
        .attr('r', 8)
        .style("fill", "#69b3a2")
        .attr('cx', (d) => d.x + margin)
        .attr('cy', (d) => d.y + margin)

    d3.select("#dataviz_area").selectAll('text').data(nodes).enter()
        .append('text')
        .attr("x", function (d) {
            return d.x + margin;
        })
        .attr("y", function (d) {
            return d.y + margin;
        })
        .text(function (d) {
            return d.name
        })
        .attr("font-family", "sans-serif")
        .attr("font-size", "14px")
        .attr("fill", "black");
}

function initSimulation() {
    simulation = d3.forceSimulation(nodes)
        .force('charge', d3.forceManyBody().strength(charge))
        .force('center', d3.forceCenter(center, center))
        .force("link", d3.forceLink()                               // This force provides links between nodes
            .id(function (d) {
                return d.id;
            })                     // This provide  the id of a node
            .links(edges)                                    // and this the list of links
        )
        .force('collision', d3.forceCollide().radius(collision))
        .on('tick', ticked)

}