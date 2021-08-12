
<script>
    import { onMount } from "svelte";
    import { LeafletMap, TileLayer } from "svelte-leafletjs";
    import { Button, Icon, Dialog, TextField } from "smelte";

    export  let name;

    let map;
    let showDialog2 = false;

    const mapOptions = {
        center: [14.6419083, 121.04793075343855],
        zoom: 11,
        // work around for safari
        // https://github.com/domoritz/leaflet-locatecontrol/issues/280
        // https://github.com/Leaflet/Leaflet/issues/7255
        tap: false,
    };

    //const tileUrl = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
    const tileUrl =
        "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png";
    const tileLayerOptions = {
        minZoom: 0,
        maxZoom: 20,
        maxNativeZoom: 19,
        // attribution: "© OpenStreetMap contributors",
        attribution: `&copy;<a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>,
          &copy;<a href="https://carto.com/attributions" target="_blank">CARTO</a>`,
    };


    function boundsCheck(e) {
        // alert(map.getMap().getBounds());
        console.log("bounds", map.getMap().getBounds());
    }

    onMount(async () => {
        if (map) {
            console.log("map bounds and invalidate size");
            console.log("bounds", map.getMap().getBounds());
            map.getMap().invalidateSize();
        }
    });
</script>
<main
class="relative lg:max-w-3xl mx-auto mb-10 mt-24 md:max-w-md md:px-3"
>
<h1>Hello {name}!</h1>
<Dialog persistent bind:value={showDialog2}>
    <h5 slot="title">Do you think you can close me by clicking outside?</h5>
    <div class="text-gray-700 dark:text-gray-100">Doubt it.</div>
    <div slot="actions">
      <Button text on:click={() => (showDialog2 = false)}>Yes</Button>
      <Button text on:click={() => (showDialog2 = false)}>No</Button>
    </div>
  </Dialog>
<Button color="alert" on:click={() => (showDialog2 = true)}>Show modal</Button>
<TextField label="Number only" prepend="search" outlined type="number" min="10" max="100" />
<TextField label="Label" placeholder="Input here" prepend="whatshot" outlined />
<TextField prepend="file_upload" outlined type="file" />
<p>
    Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn
    how to build Svelte apps.
</p>
<h1>Leaflet</h1>
<div class="mt-24" style="height: 300px;">
<LeafletMap
    options={mapOptions}
    bind:this={map}
    events={["dragend"]}
    on:dragend={boundsCheck}
>
    <TileLayer url={tileUrl} options={tileLayerOptions} />
</LeafletMap>
</div>

</main>


<style>
main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
}

h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4em;
    font-weight: 100;
}

@media (min-width: 640px) {
    main {
        max-width: none;
    }
}
</style>
