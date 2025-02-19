<script lang="ts">

    import { goto } from "$app/navigation"

    // these functions will automatically be called once button clicked
    function goToLogin(){
        goto("/login");
    }

    function goToSignUp(){
        goto("/sign-up");
    }

</script>

    <!--Sticky means the header stays on top-->
    <div class="flex pl-5 pt-10 pb-5 pr-5 z-10 justify-between sticky">

        <div class="ml-4 mt-2">
            <a href="/" class="font-semibold text-4xl">
                DragonFlow
            </a>
        </div>

        <!--Buttons on the corner of header-->
        <div class="">
            <button class="rounded-3xl bg-black text-stone-200 px-8 py-3 font-semibold text-lg mr-3" 
            on:click={goToLogin}>
                Login
            </button>

            <button class="rounded-3xl bg-black text-stone-200 text-lg px-8 py-3 font-semibold"
             on:click={goToSignUp}>
                Sign Up
            </button>
        </div>
        
    </div>

<style>

</style>