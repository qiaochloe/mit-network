import ForceGraph from 'force-graph';

fetch("./data/data.json")
.then((res) => res.json())
.then((data) => {
  const Graph = ForceGraph()(document.getElementById("graph"))
    .nodeId("course_code")
    .nodeRelSize(6)
    .nodeLabel(data => data.course_code + " " + data.course_title)
    .nodeAutoColorBy("course_department")
    .nodeVal("val") 
    .linkSource("course_code")
    .linkTarget("prereq_code")
    // .linkDirectionalArrowLength(6);
    .graphData(data)
    .zoom(1, 0)
});
