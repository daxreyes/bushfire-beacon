<script>
    import Router from "svelte-spa-router";
    import { location } from "svelte-spa-router";
    import { Spacer, AppBar, Tabs, Tab, Button, Icon, Dialog, TextField } from "smelte";

    import Home from "./Home.svelte";
    import Route1 from "./Route1.svelte";


    const topMenu = [
        { to: "#/", text: "Home" },
        { to: "#/route1", text: "Route1" },
        // { to: "/route2", text: "Route2" },
    ];

    const routes = {
    "/": Home,
    "/route1": Route1,
    }

    $: path = document.location.pathname;

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

<Router {routes} />