<script lang="ts">
    let {inputHeader, inputPlaceholder, studentInput = $bindable() } = $props();
    import { Asterisk } from "lucide-svelte";
</script>

<!-- input header -->
<p class="font-semibold text-lg mb-2 text-zinc-700">
    {inputHeader} <Asterisk class="inline-block text-red-500"/>
</p>

<label class="input input-bordered flex items-center gap-2 mb-7 min-w-[270px]">
    <input bind:value={studentInput} type="text" class="grow" placeholder={inputPlaceholder}/>
</label>