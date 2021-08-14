  <script>
    import { Button, Dialog, TextField, Tabs, Tab, Image } from "smelte";
    let showDialog2 = false;
    let loading = false;

    import FilePond, { registerPlugin } from 'svelte-filepond';
    import FilePondPluginImageExifOrientation from 'filepond-plugin-image-exif-orientation'
    import FilePondPluginImagePreview from 'filepond-plugin-image-preview'
    registerPlugin(FilePondPluginImageExifOrientation, FilePondPluginImagePreview);
    // a reference to the component, used to call FilePond methods
    // for example `pond.getFiles()` will return the active files
    let pond;
    // the name to use for the internal file input
    let name = 'filepond';
    // handle filepond events
    function handleInit() {
      console.log('FilePond has initialised');
    }
    function handleAddFile(err, fileItem) {
      console.log('A file has been added', fileItem);
    }
</script>

<div
    class="relative lg:max-w-3xl mx-auto mb-10 mt-24 md:max-w-md md:px-3"
>
<h1>Upload</h1>

<TextField prepend="file_upload" outlined type="file" />


<FilePond bind:this={pond} {name}
    server="/api/v1/upload/"
    credits=""
    allowMultiple={true}
    instantUpload={false}
    oninit={handleInit}
    onaddfile={handleAddFile}/>

</div>

<style global>
    @import 'filepond/dist/filepond.css';
    @import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css';
  </style>
  