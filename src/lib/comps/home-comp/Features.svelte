<script lang="ts">
    import { onMount } from "svelte";
    import { Sparkle } from "lucide-svelte"
    import { Progress } from "$lib/components/ui/progress/index.js";
    import { CalendarSearch } from "lucide-svelte";
    import { Smile } from "lucide-svelte";

    // script for the success bar
    let value = $state(13);
    onMount(() => {
        const timer = setTimeout(() => (value = 66), 500);
        return () => clearTimeout(timer);
    });

</script>


<div class="grid grid-cols-1 md:grid-cols-2 p-5 mb-10 mt-10">

    <div class="flex flex-col content-center ml-8">

        <!-- Main Header for Features-->
        <h1 class="font-light text-4xl mt-8 mb-10">
            We'll do all the heavy lifting for you.
        </h1>
        
        <!-- Cards for info -->
        <div
        class="inline-flex animate-shine max-w-[475px] w-full 
        items-center rounded-xl text-sm border border-black/10
         bg-white bg-[length:200%_100%] px-4 py-5 transition-colors">

        <div class="flex flex-col gap-2 justify-center">
          <h3 class="text-xl font-semibold text-black">
            Easily Plan Your Term <CalendarSearch class="inline-block ml-1 mb-1"/> 
        </h3>

          <p class="text-sm leading-[1.5] text-neutral-950">
            Our algorithms will immediately plan out your term based on the courses you're interested in and your major requirements. 
            We make sure that each recommendation is valid and correct per Drexel's term master schedule and your needs.
          </p>

        </div>
      </div>
      <div
        class="inline-flex mt-10 animate-shine max-w-[475px] w-full 
        items-center justify-center rounded-xl text-sm border
         border-black/10 bg-white bg-[length:200%_100%] 
         px-4 py-5 transition-colors">
        <div class="flex flex-col gap-2">
          <h3 class="text-xl font-semibold text-black">
            Input Your Interests  <Smile class="inline-block ml-1 mb-1"/> 
        </h3>

          <p class="text-sm leading-[1.5] text-neutral-950">
            Everyone has different preferences, our algorithms account for that. Whether it'd be classes at a certain time frame or with a specific professor, we've got you covered.
          </p>

        </div>
      </div>


        <!-- Final Left Side Column Text-->
        <h1 class="font-light text-4xl mt-8 mb-10">
            Succeed with 
            <p class="gradtext inline-block">AI</p>
            <Sparkle class="text-sky-400 inline-block relative bottom-3 right-2"/>
             <p class="relative lg:right-3 inline-block">based</p> 
             course
            recommendations.
        </h1>
    </div>
    

    <!--The Column on the right-->
    <div class="flex flex-col content-center md:ml-8 md:mt-32">

      <!-- The Class Table Demo -->
      <div class="overflow-x-auto">
        <table class="table">
          <!-- head -->
          <thead>
            <tr>
              <th></th>
              <th>Prof.</th>
              <th>Time</th>
              <th>Dates</th>
            </tr>
          </thead>
          <tbody>
            <!-- row 1 -->
            <tr>
              <th>ENGL101</th>
              <td>Cy Ganderton</td>
              <td>10:00 PM - 11:50 AM</td>
              <td>M W F</td>
            </tr>
            <!-- row 2 -->
            <tr>
              <th>MATH121</th>
              <td>Hart Hagerty</td>
              <td>12:00 PM - 12:50 PM </td>
              <td>M T W</td>
            </tr>
            <!-- row 3 -->
            <tr>
              <th>ECON101</th>
              <td>Marvin Reyes</td>
              <td>9:00 AM - 9:50 AM</td>
              <td>F</td>
            </tr>
            <!-- row 4 -->
            <tr>
              <th>UNIVCI101</th>
              <td>Brice Swyre</td>
              <td>9:00 AM - 9:50 AM</td>
              <td>T TH</td>
            </tr><!-- row 5 -->
            <tr>
              <th>CI101</th>
              <td>Daniel Mark</td>
              <td>3:00 PM - 4:45 PM</td>
              <td>T</td>
            </tr><!-- row 6 -->
            <tr>
              <th>CS164</th>
              <td>Brian Smith</td>
              <td>1:00 PM - 2:50 PM</td>
              <td>W TH</td>
            </tr>
          </tbody>
        </table>
      </div>


        <!-- Bottom Success Bar -->
        <h1 class="text-md text-center lg:mt-24 mt-10"> We predict you have a 
            <p class="text-emerald-400 inline-block">60%</p> 
            chance of success with this schedule </h1>
        <Progress {value} max={100} class="w-[60%] block m-auto mt-3 mb-10" />
    </div>

</div>



<style>

    .gradtext{
        background: -webkit-linear-gradient(#46c5fb, #3e8bce);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

</style>