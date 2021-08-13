<script>
    import { Button, Dialog, TextField, Tabs, Tab, Image } from "smelte";
    let showDialog2 = false;
    let loading = false;

</script>

<div
    class="relative lg:max-w-3xl mx-auto mb-10 mt-24 md:max-w-md md:px-3"
>
<h1>Route1!</h1>
<Dialog persistent bind:value={showDialog2}>
    <h5 slot="title">Do you think you can close me by clicking outside?</h5>
    <div class="text-gray-700 dark:text-gray-100">Doubt it.</div>
    <div slot="actions">
      <Button text on:click={() => (showDialog2 = false)}>Yes</Button>
      <Button text on:click={() => (showDialog2 = false)}>No</Button>
    </div>
  </Dialog>
  <TextField label="Label" placeholder="Input here" prepend="whatshot" outlined />

<Button color="alert" on:click={() => (showDialog2 = true)}>Show modal</Button>

<Tabs
    selected="1"
    class="bg-black shadow-sm mt-6 text-white rounded-t-lg"
    color="yellow-a200"
    let:selected={selected}
    {loading}
    items={[
      { id: "1", text: 'Cats', icon: 'alarm_on' },
      { id: "2", text: 'Kittens', icon: 'bug_report' },
      { id: "3", text: 'Dog', icon: 'eject' },
    ]}>
    <div
      slot="content"
      class="flex items-center content-center overflow-hidden w-full bg-gray-900 h-full"
      style="height: 350px"
    >
      <Tab id="1" {selected}>
        <Image
          alt="kitten 1"
          class="w-full"
          src="https://placekitten.com/400/250"
          width="400"
          height="350"
        />
      </Tab>
      <Tab id="2" {selected}>
        <Image
          alt="kitten 1"
          class="w-full"
          src="https://placekitten.com/400/251"
          width="400"
          height="350"
        />
      </Tab>
      <Tab id="3" {selected}>
        <Image
          alt="Dog"
          class="w-full"
          src="static/images/cocker-spaniel-2785074_640.jpg"
          width="400"
          height="350"
        />
      </Tab>
    </div>
  </Tabs>
</div>
