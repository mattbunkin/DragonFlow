 <script>
    let {inputHeader, customStep, studentInput = $bindable() } = $props();
    import { Asterisk } from "lucide-svelte";

    // stops negative numbers from being inputted
    function handleInput(){
        if (studentInput < 0){
            studentInput = 0;
        }
    }

</script>
 
 <!-- header above the numerical input text box -->
<p class="font-semibold text-lg mb-2 text-zinc-700">
    {inputHeader} <Asterisk class="inline-block text-red-500"/>
</p>

 <label class="input input-bordered flex items-center h-8 mb-5">
 <!-- svelte-ignore event_directive_deprecated -->
 <input bind:value={studentInput} 
    type="number" 
    class="grow" 
    min="0"
    step="{customStep}"
    on:input={handleInput}/>
 </label>