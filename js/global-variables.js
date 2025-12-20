// ### GRAPH ###

// Map of node info throw its label
var nodeHash = {};

// Lists of nodes and edges (only important info for the network construction)
var nodes = [];
var edges = [];

var darkmode = false;

var color_t = "#000000"
var color_n = "black"

// ### COLORS ###
// Color mapping by year - add new years here
var colors = {
  "2017": "#E57373",
  "2018": "#66BB6A",
  "2019": "#42A5F5",
  "2020": "#FFFF99",
  "2021": "#FF9933",
  "2022": "#666633",
  "2023": "#FF7F50", 
  "2024": "#999966",
  "2025": "#9966CC",
  "2026": "#FF6B6B",
  "2027": "#4ECDC4",
  "2028": "#FFE66D",
  "2029": "#95E1D3", 
  "2030": "#F38181",  
  "OTHER": "#660000"  // Fallback for unknown years
};

// ### RANKINGS ###

var avg_rank_id = [];
var pnt_rank_id = [];
var deg_rank_id = [];

// ### MAX DEGREE ###

var max_degree = [];
