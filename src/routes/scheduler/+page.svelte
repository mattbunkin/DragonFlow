<script lang="ts">
    import CourseDropdown from "$lib/comps/algo-comp/CourseDropdown.svelte";
    import Progress from "$lib/components/ui/progress/progress.svelte";
    import { onMount } from "svelte";

    // save all data to this JS object pass into model.py
    let scheduleData = {
        gpa: 0
    }

    // color for text to be reactive dependent on calculated percent 
    let successPercent: number = 10 // 30 placeholder for now
    
    // script for the success bar
    let value = $state(0);
    onMount(() => {
        const timer = setTimeout(() => (value = successPercent), 500);
        return () => clearTimeout(timer);
    });


</script>
    <div class="grid grid-cols-1 lg:grid-cols-2 px-5">

        <div class="flex flex-col items-center">

            <!-- For the Model to process and grab data like CRN and GPA -->
            <p class="font-medium text-center text-lg">Last term's GPA</p>
            <label class="input input-bordered flex items-center h-8 mb-5">
            <input bind:value={scheduleData.gpa} type="number" class="grow" placeholder="" />
            </label>

            <h1 class="font-medium text-lg mb-3">
                Choose a course for the term
            </h1>
            <CourseDropdown />
        </div>

        <div class="flex flex-col content-center mt-12 lg:mt-0">
            <h1 class="font-medium text-center text-lg mb-3">
               Put into current term?
            </h1>

            <div class="flex">
                <button class="text-stone-100 text-lg
                bg-emerald-400 hover:bg-emerald-300 font-semibold px-6
                 py-3 rounded-3xl m-auto">
                   Confirm
               </button>
               <button class="text-stone-100 text-lg
                font-semibold px-6 bg-red-500 hover:bg-red-400
                 py-3 rounded-3xl m-auto">
                    Cancel
               </button>
            </div>
    

        </div>
        
    </div>

    <!-- Bottom section of ML-model page-->
    <div class="flex flex-col justify-center mt-10">
        <h1 class="font-medium mt-5 text-3xl text-center">
            Based off our AI model you have
        </h1>
        <Progress {value} max={100} class="w-[75%] block m-auto mt-3 mb-5"/>
        <h1 class="text-center text-lg">
            <p class="inline-block">
                {successPercent}%
            </p> 
        chance of succeeding
        </h1>
    </div>

<style>


</style>