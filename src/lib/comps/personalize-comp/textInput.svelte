<script lang="ts">
    let {inputHeader, inputPlaceholder, textStyling, studentInput = $bindable() } = $props();
    import { Asterisk } from "lucide-svelte";
</script>

<!-- input header -->
<p class="{textStyling} text-zinc-700">
    {inputHeader} <Asterisk class="inline-block text-red-500"/>
</p>

<label class="input input-bordered flex items-center gap-2 mb-7 min-w-[270px]">
    <input bind:value={studentInput} type="text" class="grow" placeholder={inputPlaceholder}/>
</label>