<script>
    import { RadioButtonGroup, Tabs, Tab, Image } from "smelte";
    let showDialog2 = false;
    let loading = false;

</script>

<div
    class="relative lg:max-w-3xl mx-auto mb-10 mt-24 md:max-w-md md:px-3"
>
<h1>Route1!</h1>
<!-- check rollup.config.js for available color -->
<RadioButtonGroup
  name="Colored test"
  color="blue"
  disabled={false}
  classes='inline'
  items={[{ value: 1, label: 'One' }, { value: 2, label: 'Two' }]} />

  <RadioButtonGroup
  name="Colored test"
  color="secondary"
  disabled={false}
  items={[{ value: 1, label: 'One' }, { value: 2, label: 'Two' }]} />

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
