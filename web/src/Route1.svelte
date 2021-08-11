<script>
    import { Button, Dialog, TextField } from "smelte";
    let showDialog2 = false;

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
</div> 