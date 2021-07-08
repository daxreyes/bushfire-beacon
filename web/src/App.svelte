<script>
    import { onMount } from "svelte";
    import { LeafletMap, TileLayer } from "svelte-leafletjs";
    import { Spacer, AppBar, Tabs, Button, Icon } from "smelte";
    export let name;

    let map;

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

    const topMenu = [
        { to: "/", text: "Home" },
        { to: "/components", text: "Components" },
        { to: "/typography", text: "Typography" },
        { to: "/color", text: "Color" },
    ];

    $: path = document.location.pathname;

    function boundsCheck(e) {
        // alert(map.getMap().getBounds());
        console.log("bounds", map.getMap().getBounds());
    }

    onMount(async () => {
        if (map) {
            console.log("map bounds and invalidate size");
            console.log("bounds", map.getMap().getBounds());
            // map.getMap().invalidateSize();
        }
    });
</script>

<AppBar  class={i => i.replace('primary-300', 'dark-600')}>
    <a href="." class="px-2 md:px-8 flex items-center">
        <!-- https://freesvg.org/fire-1 -->
        <img src="/fire1.svg" alt="fire logo" width="44" />
        <h6 class="pl-3 text-white tracking-widest font-thin text-lg">
            BEACON
        </h6>
    </a>
    <Spacer />
    <Tabs
        navigation
        items={topMenu}
    />
</AppBar>

<main
    class="relative p-8 lg:max-w-3xl mx-auto mb-10 mt-24 md:ml-64 md:pl-16
md:max-w-md md:px-3"
>
    <h1>Hello {name}!</h1>
    <Button>test</Button>
    <p>
        Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn
        how to build Svelte apps.
    </p>
</main>

<h1>Leaflet</h1>
<div class="leaflet-map" style="width: 100%; height: 90%;">
    <LeafletMap
        options={mapOptions}
        bind:this={map}
        events={["dragend"]}
        on:dragend={boundsCheck}
    >
        <TileLayer url={tileUrl} options={tileLayerOptions} />
    </LeafletMap>
</div>

<style>
    main {
        text-align: center;
        padding: 1em;
        max-width: 240px;
        margin: 0 auto;
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
