// Compute available pixel height for the info panels
function getInfoMaxHeight() {
  var sidebar = document.getElementById('sidebar');
  var infoBody = document.querySelector('.card-body.text-white');
  var bottom = document.querySelector('[style*="flex-shrink: 0"]');
  if (!sidebar || !infoBody) return 200;
  var sidebarBottom = sidebar.getBoundingClientRect().bottom;
  var infoBodyTop = infoBody.getBoundingClientRect().top;
  var bottomHeight = bottom ? bottom.getBoundingClientRect().height : 0;
  return Math.max(80, sidebarBottom - infoBodyTop - bottomHeight - 20);
}

// Re-apply height to whichever tooltip is currently visible
function refreshInfoHeight() {
  var maxH = getInfoMaxHeight();
  var div1 = document.getElementById('div1');
  var div2 = document.getElementById('div2');
  if (div1 && div1.style.display !== 'none') {
    div1.style.maxHeight = maxH + 'px';
  }
  if (div2 && div2.style.display !== 'none') {
    div2.style.maxHeight = maxH + 'px';
  }
}
// Display edge infos
function edgeinfo(e) {
  var maxH = getInfoMaxHeight();
  var div1 = document.getElementById('div1');
  div1.style.display = 'block';
  div1.style.opacity = '0.9';
  div1.style.overflow = 'hidden';
  div1.style.maxHeight = maxH + 'px';
  div1.style.display = 'flex';
  div1.style.flexDirection = 'column';

  // Clickable node names that navigate to their info
  var srcLabel = "<span onclick='_showNodeInfo(\"" + e.source.label + "\")' style='cursor:pointer; text-decoration:underline; color:#DEB887;'>" + e.source.label + "</span>";
  var tgtLabel = "<span onclick='_showNodeInfo(\"" + e.target.label + "\")' style='cursor:pointer; text-decoration:underline; color:#DEB887;'>" + e.target.label + "</span>";

  var edge_info = "<h5 class=\"text-white card-title\" style=\"margin-bottom:0; flex-shrink:0;\">" + srcLabel + " i " + tgtLabel + "</h5>";
  edge_info += "<div style=\"flex: 1 1 auto; overflow-y: auto; overflow-x: hidden; padding-right: 5px; margin-top: 10px; min-height: 0;\"><p class=\"text-white card-text\">";
  if (e.place !== "") {
    edge_info += "<b>Lloc: </b>" + e.place + "<br/>";
  }
  if (e.year !== "" || e.month != ""){
    var monthNames = ["", "Gener", "Febrer", "Mar\u00e7", "Abril", "Maig", "Juny", "Juliol", "Agost", "Setembre", "Octubre", "Novembre", "Desembre"];
    var monthStr = (e.month >= 1 && e.month <= 12) ? monthNames[e.month] : "";
    edge_info += "<b>Data: </b>" + monthStr + (monthStr === "" ? "" : " ") + e.year + "<br/>";
  }
  if (e.comments !== "") edge_info += "<b>Comentaris: </b>" + e.comments + "<br/>";
  var tipusMap = {1: 'Lio', 2: 'Manual', 3: 'Oral', 5: 'Complet'};
  var tipusLabel = tipusMap[e.weight] || e.weight;
  edge_info += "<b>Tipus: </b>" + tipusLabel + "<br/>";
  edge_info += "<b>Relaci\u00f3: </b>" + e.relationship + "<br/>";
  edge_info += "</p></div>";

  div1.innerHTML = edge_info;
  document.getElementById('div2').style.display = 'none';
};

// Helper: find node object by label and show node info
function _showNodeInfo(label) {
  var node = null;
  for (var i = 0; i < nodes.length; i++) {
    if (nodes[i].label === label) { node = nodes[i]; break; }
  }
  if (node) {
    nodeinfo(node);
    if (typeof nodeF === 'function') nodeF(node);
  }
}

// Helper: show edge info by index in the global edges array
function _showEdgeFromIdx(idx) {
  var edge = edges[idx];
  if (!edge) return;
  edgeinfo(edge);
  if (typeof window.edgeF === 'function') window.edgeF(edge);
}

// Display info about node
function nodeinfo(e){
  var maxH = getInfoMaxHeight();
  var div2 = document.getElementById('div2');
  div2.style.display = 'block';
  div2.style.opacity = '0.9';
  div2.style.overflowY = 'auto';
  div2.style.maxHeight = maxH + 'px';

  var node_info = "<h5 class=\"text-white card-title\" style=\"margin-bottom:0;\">" + e.label +"</h5>";
  node_info += "<b>Sexe: </b>" + e.gender + "<br/>";
  node_info += "<b>Any: </b>" + e.year + "<br/>";
  node_info += "<b>CFIS: </b>" + e.cfis + "<br/>";
  node_info += "<b>Arestes: </b>" + e.degree + "<br/>";
  node_info += "<b>Points: </b>" + e.points + "<br/>";
  node_info += "<b>Average: </b>" + e.average + "<br/>";

  // Build neighbour list
  var neighbours = edges.filter(function(edge) {
    return edge.source === e || edge.target === e;
  });
  if (neighbours.length > 0) {
    node_info += "<hr style='border-color: rgba(255,255,255,0.2); margin: 8px 0;'/>";
    node_info += "<b style='font-size:13px;'>Ve\u00efns:</b><ul style='padding-left:16px; margin: 4px 0; list-style: disc;'>";
    neighbours.forEach(function(edge) {
      var neighbour = edge.source === e ? edge.target : edge.source;
      // Store edge index for onclick access
      var edgeIdx = edges.indexOf(edge);
      node_info += "<li><span onclick='_showEdgeFromIdx(" + edgeIdx + ")' style='cursor:pointer; text-decoration:underline; color:#DEB887;'>" + neighbour.label + "</span></li>";
    });
    node_info += "</ul>";
  }

  div2.innerHTML = node_info;
  document.getElementById('div1').style.display = 'none';
}

// Display menu
function menu(val){
  if(val == "not_choosen"){
    document.getElementById("no_choose").style.display="block";
    document.getElementById("rank_p").style.display="none";
    document.getElementById("rank_a").style.display="none";
    document.getElementById("rank_m").style.display="none";
  }
  if(val == "ranking_p"){
    document.getElementById("no_choose").style.display="none";
    document.getElementById("rank_p").style.display="block";
    document.getElementById("rank_a").style.display="none";
    document.getElementById("rank_m").style.display="none";

        var rank1_p = "<b>1r: </b>" + nodes[pnt_rank_id[0]].label + " (" +  nodes[pnt_rank_id[0]].points + ") <br/>";
        var rank2_p = "<b>2n: </b>" + nodes[pnt_rank_id[1]].label + " (" +  nodes[pnt_rank_id[1]].points + ") <br/>";
        var rank3_p = "<b>3r: </b>" + nodes[pnt_rank_id[2]].label + " (" +  nodes[pnt_rank_id[2]].points + ") <br/>";
        var rank4_p = "<b>4t: </b>" + nodes[pnt_rank_id[3]].label + " (" +  nodes[pnt_rank_id[3]].points + ") <br/>";
        var rank5_p = "<b>5è: </b>" + nodes[pnt_rank_id[4]].label + " (" +  nodes[pnt_rank_id[4]].points + ") <br/>";
      console.log(rank1_p)
      d3.select("#rank_1_p").html(rank1_p)
      d3.select("#rank_2_p").html(rank2_p)
      d3.select("#rank_3_p").html(rank3_p)
      d3.select("#rank_4_p").html(rank4_p)
      d3.select("#rank_5_p").html(rank5_p)
  }
  if(val == "ranking_a"){
    document.getElementById("no_choose").style.display="none";
    document.getElementById("rank_p").style.display="none";
    document.getElementById("rank_a").style.display="block";
    document.getElementById("rank_m").style.display="none";

    var rank1_a = "<b>1r: </b>" + nodes[deg_rank_id[0]].label + " (" +  nodes[deg_rank_id[0]].degree + ")";
    var rank2_a = "<b>2n: </b>" + nodes[deg_rank_id[1]].label + " (" +  nodes[deg_rank_id[1]].degree + ") ";
    var rank3_a = "<b>3r: </b>" + nodes[deg_rank_id[2]].label + " (" +  nodes[deg_rank_id[2]].degree + ") ";
    var rank4_a = "<b>4t: </b>" + nodes[deg_rank_id[3]].label + " (" +  nodes[deg_rank_id[3]].degree + ") ";
    var rank5_a = "<b>5è: </b>" + nodes[deg_rank_id[4]].label + " (" +  nodes[deg_rank_id[4]].degree + ") ";

  d3.select("#rank_1_a").html(rank1_a)
  d3.select("#rank_2_a").html(rank2_a)
  d3.select("#rank_3_a").html(rank3_a)
  d3.select("#rank_4_a").html(rank4_a)
  d3.select("#rank_5_a").html(rank5_a)
  }
  if(val == "ranking_m"){
    document.getElementById("no_choose").style.display="none";
    document.getElementById("rank_p").style.display="none";
    document.getElementById("rank_m").style.display="block";
    document.getElementById("rank_a").style.display="none";

    var rank1_m = "<b>1r: </b>" + nodes[avg_rank_id[0]].label + " (" +  nodes[avg_rank_id[0]].average + ")";
    var rank2_m = "<b>2n: </b>" + nodes[avg_rank_id[1]].label + " (" +  nodes[avg_rank_id[1]].average + ") ";
    var rank3_m = "<b>3r: </b>" + nodes[avg_rank_id[2]].label + " (" +  nodes[avg_rank_id[2]].average + ") ";
    var rank4_m = "<b>4t: </b>" + nodes[avg_rank_id[3]].label + " (" +  nodes[avg_rank_id[3]].average + ") ";
    var rank5_m = "<b>5è: </b>" + nodes[avg_rank_id[4]].label + " (" +  nodes[avg_rank_id[4]].average + ") ";

  d3.select("#rank_1_m").html(rank1_m)
  d3.select("#rank_2_m").html(rank2_m)
  d3.select("#rank_3_m").html(rank3_m)
  d3.select("#rank_4_m").html(rank4_m)
  d3.select("#rank_5_m").html(rank5_m)
  }
}
