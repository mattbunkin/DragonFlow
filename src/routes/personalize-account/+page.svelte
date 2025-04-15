<script lang="ts">
import { Asterisk } from 'lucide-svelte';
import DrexelDate from '$lib/comps/personalize-comp/DrexelDate.svelte';
import TextInput from '$lib/comps/personalize-comp/textInput.svelte';
import NumberInput from '$lib/comps/personalize-comp/NumberInput.svelte';
import CustomButton from '$lib/comps/home-comp/CustomButton.svelte';
import { goto } from '$app/navigation';

/* 
    Explanation of default data types:
    - minor and concentrations can be empty
    strings if student doesn't have any; can't be 
    empty if minor/concentration needed is true.

    - undergrad is false whenever its a grad student
    - coop_type is true if it is the 5 year, 3 coops program
    (most popular), false if it is 4 year, 1 coop program.
    - calendar_type is true if a student goes by quarter system but false
    if student goes by semester system
*/

let studentData = $state({
    major: "",
    minor: "",
    concentrations: "",

    // can't be nullable, user must input these
    enrollment_date: "",
    graduation_date: "",
    minor_needed: false,
    concentration_needed: false,
    undergrad: true,
    coop_type: true,
    calendar_type: true,

    // numerical inputs 
    gpa: 0,
    min_credits: 0,
    min_gpa: 0,

    // could be nullable 
    time_preference: "",
})

// send student data; since student is logged-in must include authentication!
async function sendStudentData(){
    try {
      // go to this endpoint to perform some operation
      const response = await fetch("http://127.0.0.1:5000/auth/personalize-account",
        {
          // define operation we want to perform
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`
          },
          // always include cookies for Flask's session based authentication
          credentials: "include",

          // payload/data to send to endpoint 
          body: JSON.stringify(studentData)
        }
      )
      // if something we wrong fetching flask endpoint then show error
      if (!response.ok){
        throw new Error(`HTTP error. Status: ${response.status}`)
      }

      else if (response.ok){
        const responseData = await response.json()

        // store access token 
        localStorage.setItem("access_token", responseData.user_access_token)

        // redirect user to main scheduler 
        await goto("/scheduler")
      }

    }
    
    // initial error catch for fetch; display error on browser console 
    catch(error){
      console.error(`Failed to fetch data from client: ${error}`)
    }

}

</script>


<div class="flex flex-col items-center min-h-screen p-10 mt-5">

  <h1 class="text-4xl text-center mt-8 mb-2 font-medium inline-flex animate-shine bg-[linear-gradient(110deg,#656565,45%,#1e2631,55%,#656565)] bg-[length:200%_100%] text-transparent bg-clip-text">
    Let's Personalize Your Course Scheduling Experience.
  </h1>   
  <p class="mb-10 text-zinc-600">
    Its ok to leave inputs empty for questions that don't 
    apply to you!
</p>

  <!-- Card component containing all inputs -->
  <div class="card flex flex-col gap-2 shadow-lg py-7 px-5 sm:w-[90%] md:w-[28rem] lg:w-[32rem] xl:w-[38rem]">

    <!-- Student must input (or leave empty) all info here -->
    <TextInput
      inputHeader={"What are your major(s)?"}
      inputPlaceholder={"e.g. Biology, Computer Science"}
      textStyling={"font-semibold text-lg mb-2"}
      bind:studentInput={studentData.major}
    />

    <TextInput
      inputHeader="What's your minor(s) (optional)"
      inputPlaceholder="e.g. Chemistry"
      textStyling="font-semibold text-lg mb-2"
      bind:studentInput={studentData.minor}
    />

    <TextInput
      inputHeader={"Any concentrations? (optional)"}
      inputPlaceholder={"e.g. Algorithm Design, Artificial Intelligence"}
      textStyling={"font-semibold text-lg mb-2"}
      bind:studentInput={studentData.concentrations}
    />

    <!-- Student required info to be inputted! (Some errors with using on-click for divs so used comments to ignore errors..)-->
    <!-- Student Type Selection - Segmented Toggle -->
    <p class="font-semibold text-lg mb-2 text-zinc-700">What type of student are you?  <Asterisk class="inline-block text-red-500"/></p>
    <div class="bg-gray-100 p-1 rounded-xl flex mb-7">
      <!-- svelte-ignore event_directive_deprecated -->
      <button 
        class="w-1/2 py-3 rounded-lg transition-all duration-300 {studentData.undergrad ? 'bg-white shadow-md text-sky-500' : 'text-gray-500 hover:text-gray-700'}"
        on:click={() => studentData.undergrad = true}
      >
        Undergraduate
      </button>
      <!-- svelte-ignore event_directive_deprecated -->
      <button 
        class="w-1/2 py-3 rounded-lg transition-all duration-300 {!studentData.undergrad ? 'bg-white shadow-md text-sky-500' : 'text-gray-500 hover:text-gray-700'}"
        on:click={() => studentData.undergrad = false}
      >
        Graduate
      </button>
    </div>

    <!-- Student required info to be inputted! (Some errors with using on-click for divs so used comments to ignore errors..)-->
    <!-- Student Type Selection - Segmented Toggle -->
    <p class="font-semibold text-lg mb-2 text-zinc-700">Does your major need a minor?<Asterisk class="inline-block text-red-500"/></p>
    <div class="bg-gray-100 p-1 rounded-xl flex mb-7">
      <!-- svelte-ignore event_directive_deprecated -->
      <button 
        class="w-1/2 py-3 rounded-lg transition-all duration-300 {studentData.minor_needed ? 'bg-white shadow-md text-emerald-500' : 'text-gray-500 hover:text-gray-700'}"
        on:click={() => studentData.minor_needed = true}
      >
        Yes
      </button>
      <!-- svelte-ignore event_directive_deprecated -->
      <button 
        class="w-1/2 py-3 rounded-lg transition-all duration-300 {!studentData.minor_needed ? 'bg-white shadow-md text-red-500' : 'text-gray-500 hover:text-gray-700'}"
        on:click={() => studentData.minor_needed = false}
      >
        No
      </button>
    </div>

    <!-- Student required info to be inputted! (Some errors with using on-click for divs so used comments to ignore errors..)-->
    <!-- Student Type Selection - Segmented Toggle -->
    <p class="font-semibold text-lg mb-2 text-zinc-700">Does your major need concentrations? <Asterisk class="inline-block text-red-500"/></p>
    <div class="bg-gray-100 p-1 rounded-xl flex mb-7">
      <!-- svelte-ignore event_directive_deprecated -->
      <button 
        class="w-1/2 py-3 rounded-lg transition-all duration-300 {studentData.concentration_needed ? 'bg-white shadow-md text-emerald-500' : 'text-gray-500 hover:text-gray-700'}"
        on:click={() => studentData.concentration_needed = true}
      >
        Yes
      </button>
      <!-- svelte-ignore event_directive_deprecated -->
      <button 
        class="w-1/2 py-3 rounded-lg transition-all duration-300 {!studentData.concentration_needed ? 'bg-white shadow-md text-red-500' : 'text-gray-500 hover:text-gray-700'}"
        on:click={() => studentData.concentration_needed = false}
      >
        No
      </button>
    </div>

    


    <!-- student selects calendar type -->
    <p class="font-semibold text-lg mb-2 text-zinc-700">Select your academic calendar  <Asterisk class="inline-block text-red-500"/></p>
    <div class="grid grid-cols-1 gap-4 mb-7">

      <!-- svelte-ignore a11y_click_events_have_key_events -->
      <!-- svelte-ignore a11y_no_static_element_interactions -->
      <!-- svelte-ignore event_directive_deprecated -->
      <div 
        class="p-4 rounded-xl border-2 transition-all cursor-pointer {studentData.calendar_type ? 'border-sky-400 bg-blue-50' : 'border-gray-200 hover:border-gray-300'}"
        on:click={() => studentData.calendar_type = true}
      >
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-base font-medium">Quarter System</h3>
            <p class="text-gray-500 text-sm mt-1">Drexel's three 10-week terms per year</p>
          </div>
          <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center {studentData.calendar_type ? 'border-blue-500 bg-white' : 'border-gray-300'}">
            {#if studentData.calendar_type}
              <div class="w-2.5 h-2.5 rounded-full bg-blue-500"></div>
            {/if}
          </div>
        </div>
      </div>
      <!-- svelte-ignore a11y_click_events_have_key_events -->
      <!-- svelte-ignore a11y_no_static_element_interactions -->
      <!-- svelte-ignore event_directive_deprecated -->
      <div 
        class="p-4 rounded-xl border-2 transition-all cursor-pointer {!studentData.calendar_type ? 'border-sky-400 bg-blue-50' : 'border-gray-200 hover:border-gray-300'}"
        on:click={() => studentData.calendar_type = false}
      >
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-base font-medium">Semester System</h3>
            <p class="text-gray-500 text-sm mt-1">Drexel's two 15-week terms per year</p>
          </div>
          <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center {!studentData.calendar_type ? 'border-blue-500 bg-white' : 'border-gray-300'}">
            {#if !studentData.calendar_type}
              <div class="w-2.5 h-2.5 rounded-full bg-blue-500"></div>
            {/if}
          </div>
        </div>
      </div>
    </div>

    <!-- student selects co-op type via calendar switch -->
    <p class="font-semibold text-lg mb-2 text-zinc-700">Select Co-op Type  <Asterisk class="inline-block text-red-500"/></p>
    <label class="flex items-center justify-between w-full p-4 bg-white rounded-xl border border-gray-200 mb-7">
      <span class="text-gray-700">5-year Co-op cycle</span>
      <div class="relative inline-block w-12 h-6 transition duration-200 ease-in-out">
        <input 
          type="checkbox"
          bind:checked={studentData.coop_type}
          class="peer sr-only"
        />
        <span class="absolute top-0 left-0 right-0 bottom-0 rounded-full bg-gray-300 transition-all duration-300 before:absolute before:h-4 before:w-4 before:left-1 before:bottom-1 before:bg-white before:rounded-full before:transition-all before:duration-300 peer-checked:bg-blue-500 peer-checked:before:translate-x-6"></span>
      </div>
    </label>

    <!-- enrollmentDate and graduationDate are -->
    <DrexelDate 
    bind:enrollmentDate={studentData.enrollment_date} 
    bind:graduationDate={studentData.graduation_date} 
    />

    <!-- numerical inputs from student -->
    <NumberInput
      inputHeader={"What's your cumulative GPA so far?"}
      customStep={0.1}
      textStyling="font-semibold text-lg mb-2"
      bind:studentInput={studentData.gpa}
    />

    <NumberInput
      inputHeader={"What's your major's minimum GPA for graduation?"}
      customStep={0.1}
      textStyling="font-semibold text-lg mb-2 "
      bind:studentInput={studentData.min_gpa}
    />

    <NumberInput
      inputHeader={"What's your major's minimum credits for graduation?"}
      customStep={1}
      textStyling="font-semibold text-lg mb-2"
      bind:studentInput={studentData.min_credits}
    />

    <!-- Extra info to personalize the scheduling experience to be added later -->
     
    <!-- <TextInput 
      inputHeader={"When do you prefer to have your classes?"}
      inputPlaceholder={"Morning"}
      bind:studentInput={studentData.time_preference}
    /> -->


  </div>
  <!-- Card containing all inputs ends here-->
  <CustomButton 
    buttonText={"Try Out Scheduler"}
    buttonFunc={sendStudentData}
  />



</div>



<style>
  .card{
    border-color: rgba(210, 210, 210, 0.357);
    border-width: 2px;
    margin-bottom: 1rem;
  }  
</style>