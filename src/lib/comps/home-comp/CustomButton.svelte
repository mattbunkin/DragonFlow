<script>
// custom button text and functionality component made by Andrey..
let { buttonText, buttonFunc } = $props();
</script>

<!-- svelte-ignore event_directive_deprecated -->
<button class="glow bg-gradient-to-r
    from-cyan-400 to-sky-500 text-stone-100 text-xl
    font-semibold px-6 py-3 rounded-3xl mt-10 block m-auto" 
    on:click={buttonFunc}>
        {buttonText}
</button>


<style>
.glow {
    transform: scale(1);
    transition: transform 0.3s ease-in-out;
}
.glow:hover {
    box-shadow: 0 0 9px 2px rgba(102, 191, 255, 0.7);
    transform: scale(105%); 
    transition: transform 0.3s ease-in-out;
} 
</style>