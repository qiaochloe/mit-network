import ForceGraph from 'force-graph';

fetch("./data/data.json")
.then((res) => res.json())
.then((data) => {
  const Graph = ForceGraph()(document.getElementById("graph"))
    .nodeId("course_code")
    .nodeRelSize(6)
    .nodeLabel(data => data.course_code + " " + data.course_title)
    // .nodeAutoColorBy("group")
    // .nodeVal("val") 
    .linkSource("course")
    .linkTarget("prereq")
    // .linkDirectionalArrowLength(6);
    .graphData(data)
});
