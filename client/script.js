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
let nodes
let edges
let margin = 100
let charge = -1200
let centerX = document.querySelector('#dataviz_area').clientWidth / 2
let centerY = document.querySelector('#dataviz_area').clientHeight / 2
let collision = 40
let simulation

d3.json(`http://127.0.0.1:8000/documents/${documentId}/graph`, ForceGraph)

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
            return d.source.x
        })
        .attr("y1", function (d) {
            return d.source.y
        })
        .attr("x2", function (d) {
            return d.target.x
        })
        .attr("y2", function (d) {
            return d.target.y
        });
    d3.select('#dataviz_area').selectAll('circle').data(nodes).enter()
        .append('circle')
        .attr('r', 12)
        .style("fill", "#7f8ca1")
        .attr('cx', (d) => d.x)
        .attr('cy', (d) => d.y)

    d3.select("#dataviz_area").selectAll('text').data(nodes).enter()
        .append('text')
        .attr("x", function (d) {
            return d.x
        })
        .attr("y", function (d) {
            return d.y
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
        .force('center', d3.forceCenter(centerX, centerY))
        .force("link", d3.forceLink()                               // This force provides links between nodes
            .id(function (d) {
                return d.id;
            })                     // This provide  the id of a node
            .links(edges)                                    // and this the list of links
        )
        .force('collision', d3.forceCollide().radius(collision))
        .alphaDecay(0.001)
        .on('tick', ticked)

}