<script>
  import { onMount } from "svelte";
  import "@carbon/charts/styles.min.css";
  import { BarChartSimple } from "@carbon/charts-svelte";
  import { WordCloudChart } from "@carbon/charts-svelte";

  let chart;
  // click codesandbox to see sample code for wordcloud
  // https://carbon-design-system.github.io/carbon-charts/svelte/?path=/story/simple-charts-word-cloud--word-cloud
  let words = [
  {
    "word": "Lorem",
    "value": 52,
    "group": "Second"
  },
  {
    "word": "ipsum",
    "value": 25,
    "group": "Second"
  },
  {
    "word": "dolor",
    "value": 51,
    "group": "Second"
  },
  {
    "word": "amet",
    "value": 40,
    "group": "First"
  },
  {
    "word": "consectetur",
    "value": 25,
    "group": "Fourth"
  },
];

  function barMouseOver(e) {
    console.log(e.detail);
  }

  onMount(() => {
    return () => {
      if (chart) chart.services.events.removeEventListener("bar-mouseover", barMouseOver);
    };
  });

  $: if (chart) chart.services.events.addEventListener("bar-mouseover", barMouseOver);


</script>

<div
    class="relative lg:max-w-3xl mx-auto mb-10 mt-24 md:max-w-md md:px-3"
>
<h1>Charts</h1>

<BarChartSimple
  bind:chart
  data={[
    { group: "Qty", value: 65000 },
    { group: "More", value: 29123 },
    { group: "Sold", value: 35213 },
    { group: "Restocking", value: 51213 },
    { group: "Misc", value: 16932 },
  ]}
  options={{
    title: "Simple bar (discrete)",
    height: "400px",
    axes: {
      left: { mapsTo: "value" },
      bottom: { mapsTo: "group", scaleType: "labels" },
    },
  }}
/>


<WordCloudChart
  data={words}
  options={{
  "title": "Word cloud",
  "resizable": true,
  "color": {
    "pairing": {
      "option": 3
    }
  },
  "height": "400px"
}}
  />

</div>  