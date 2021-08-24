<script>
  import { onMount } from "svelte";
  import { Vega, VegaLite } from "svelte-vega";

  const data = {
    table: [
      { category: "A", amount: 28 },
      { category: "B", amount: 55 },
      { category: "C", amount: 43 },
      { category: "D", amount: 91 },
      { category: "E", amount: 81 },
      { category: "F", amount: 53 },
      { category: "G", amount: 19 },
      { category: "H", amount: 87 },
    ],
  };

  let viewVL;
  let specVL = {
    $schema: "https://vega.github.io/schema/vega-lite/v5.json",
    description: "A simple bar chart with embedded data.",
    data: {
      name: "table",
    },
    mark: "bar",
    encoding: {
      x: { field: "category", type: "nominal" },
      y: { field: "amount", type: "quantitative" },
    },
  };
  let viewV;
  const specV = {
    $schema: "https://vega.github.io/schema/vega/v5.json",
    width: 400,
    height: 200,
    padding: { left: 5, right: 5, top: 5, bottom: 5 },
    data: [
      {
        name: "table",
      },
    ],
    signals: [
      {
        name: "tooltip",
        value: {},
        on: [
          { events: "rect:mouseover", update: "datum" },
          { events: "rect:mouseout", update: "{}" },
        ],
      },
    ],
    scales: [
      {
        name: "xscale",
        type: "band",
        domain: { data: "table", field: "category" },
        range: "width",
      },
      {
        name: "yscale",
        domain: { data: "table", field: "amount" },
        nice: true,
        range: "height",
      },
    ],
    axes: [
      { orient: "bottom", scale: "xscale" },
      { orient: "left", scale: "yscale" },
    ],
    marks: [
      {
        type: "rect",
        from: { data: "table" },
        encode: {
          enter: {
            x: { scale: "xscale", field: "category", offset: 1 },
            width: { scale: "xscale", band: 1, offset: -1 },
            y: { scale: "yscale", field: "amount" },
            y2: { scale: "yscale", value: 0 },
          },
          update: {
            fill: { value: "steelblue" },
          },
          hover: {
            fill: { value: "red" },
          },
        },
      },
      {
        type: "text",
        encode: {
          enter: {
            align: { value: "center" },
            baseline: { value: "bottom" },
            fill: { value: "#333" },
          },
          update: {
            x: { scale: "xscale", signal: "tooltip.category", band: 0.5 },
            y: { scale: "yscale", signal: "tooltip.amount", offset: -2 },
            text: { signal: "tooltip.amount" },
            fillOpacity: [
              { test: "datum === tooltip", value: 0 },
              { value: 1 },
            ],
          },
        },
      },
    ],
  };

  let viewVTree;
  const specVTree = {
    "$schema": "https://vega.github.io/schema/vega/v5.json",
    "description": "An example of treemap layout for hierarchical data.",
    "width": 960,
    "height": 500,
    "padding": 2.5,
    "autosize": "none",

    "signals": [
      {
        "name": "layout", "value": "squarify",
        "bind": {
          "input": "select",
          "options": [
            "squarify",
            "binary",
            "slicedice"
          ]
        }
      },
      {
        "name": "aspectRatio", "value": 1.6,
        "bind": {"input": "range", "min": 1, "max": 5, "step": 0.1}
      }
    ],

    "data": [
      {
        "name": "tree",
        "url": "data/flare.json",
        "transform": [
          {
            "type": "stratify",
            "key": "id",
            "parentKey": "parent"
          },
          {
            "type": "treemap",
            "field": "size",
            "sort": {"field": "value"},
            "round": true,
            "method": {"signal": "layout"},
            "ratio": {"signal": "aspectRatio"},
            "size": [{"signal": "width"}, {"signal": "height"}]
          }
        ]
      },
      {
        "name": "nodes",
        "source": "tree",
        "transform": [{ "type": "filter", "expr": "datum.children" }]
      },
      {
        "name": "leaves",
        "source": "tree",
        "transform": [{ "type": "filter", "expr": "!datum.children" }]
      }
    ],

    "scales": [
      {
        "name": "color",
        "type": "ordinal",
        "domain": {"data": "nodes", "field": "name"},
        "range": [
          "#3182bd", "#6baed6", "#9ecae1", "#c6dbef", "#e6550d",
          "#fd8d3c", "#fdae6b", "#fdd0a2", "#31a354", "#74c476",
          "#a1d99b", "#c7e9c0", "#756bb1", "#9e9ac8", "#bcbddc",
          "#dadaeb", "#636363", "#969696", "#bdbdbd", "#d9d9d9"
        ]
      },
      {
        "name": "size",
        "type": "ordinal",
        "domain": [0, 1, 2, 3],
        "range": [256, 28, 20, 14]
      },
      {
        "name": "opacity",
        "type": "ordinal",
        "domain": [0, 1, 2, 3],
        "range": [0.15, 0.5, 0.8, 1.0]
      }
    ],

    "marks": [
      {
        "type": "rect",
        "from": {"data": "nodes"},
        "interactive": false,
        "encode": {
          "enter": {
            "fill": {"scale": "color", "field": "name"}
          },
          "update": {
            "x": {"field": "x0"},
            "y": {"field": "y0"},
            "x2": {"field": "x1"},
            "y2": {"field": "y1"}
          }
        }
      },
      {
        "type": "rect",
        "from": {"data": "leaves"},
        "encode": {
          "enter": {
            "stroke": {"value": "#fff"}
          },
          "update": {
            "x": {"field": "x0"},
            "y": {"field": "y0"},
            "x2": {"field": "x1"},
            "y2": {"field": "y1"},
            "fill": {"value": "transparent"}
          },
          "hover": {
            "fill": {"value": "red"}
          }
        }
      },
      {
        "type": "text",
        "from": {"data": "nodes"},
        "interactive": false,
        "encode": {
          "enter": {
            "font": {"value": "Helvetica Neue, Arial"},
            "align": {"value": "center"},
            "baseline": {"value": "middle"},
            "fill": {"value": "#000"},
            "text": {"field": "name"},
            "fontSize": {"scale": "size", "field": "depth"},
            "fillOpacity": {"scale": "opacity", "field": "depth"}
          },
          "update": {
            "x": {"signal": "0.5 * (datum.x0 + datum.x1)"},
            "y": {"signal": "0.5 * (datum.y0 + datum.y1)"}
          }
        }
      }
    ]
  }

  $: viewVL ? console.log("Vega-Lite view: ", viewVL.data("table")) : "";
  $: viewV ? console.log("Vega view: ", viewV.data("table")) : "";
  $: viewVTree ? console.log("Vega view: ", viewV.data("table")) : "";


</script>

<div
    class="relative lg:max-w-3xl mx-auto mb-10 mt-24 md:max-w-md md:px-3"
>
  <h1>Vega</h1>

  <Vega {data} spec={specV} bind:view={viewV} />
  <VegaLite {data} spec={specVL} bind:view={viewVL} />

  <Vega spec={specVTree} bind:view={viewVTree} />

</div>  