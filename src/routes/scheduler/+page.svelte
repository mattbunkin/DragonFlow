<script lang="ts">
   import CustomDropDown from "$lib/comps/algo-comp/CustomDropDown.svelte";
   import Progress from "$lib/components/ui/progress/progress.svelte";
   import NumberInput from "$lib/comps/personalize-comp/NumberInput.svelte";
   import TextInput from "$lib/comps/personalize-comp/textInput.svelte";
   import { onMount } from "svelte";
   import { Search } from 'lucide-svelte';

   // save all data to this JS object pass into model.py
   let courseData = {
       gpa: 0,
       course: ""
   }

   // color for text to be reactive dependent on calculated percent 
   let successPercent: number = 10 // 30 placeholder for now
   
   // script for the success bar
   let value = $state(0);
   onMount(() => {
       const timer = setTimeout(() => (value = successPercent), 500);
       return () => clearTimeout(timer);
   });


   // send course data to scheduler endpoint
   async function sendCourseData(){
     try {
        const response = await fetch("http://127.0.0.1:5000/auth/course_retriever",
           {
              method: "POST",
              headers: {
                 "Content-Type": "application/json",
                 "Authorization": `Bearer ${localStorage.getItem("access_token")}`
              },
              // always include cookies for Flask's login/session based authentication
              credentials: "include",

              //payload/data to send to flask endpoint
              body: JSON.stringify(courseData)
           }
        )
        // display error here later to user
        if (!response.ok){
           throw new Error(`HTTP error. Status ${response.status}`)
        }
        else if (response.ok){
           const allCourseData = await response.json()
        }
     }
     catch(error){
        console.error(`Failed to retrieve course data from data.json: ${error}`)
     }
   }

</script>
  <!-- Main content sections - use flex-col to stack them without extra padding -->
  <div class="flex flex-col space-y-6">
    <!-- Course selection section -->
    <div class="rounded-lg shadow-md shadow-stone-200 p-6">
       <h1 class="font-semibold text-lg">
        Course Selection
           </h1>
     <hr class="straight-line w-90 mx-auto my-2 bg-gray-200 border-0 md:my-2 dark:bg-zinc-900">
     <NumberInput
        inputHeader="Last Term's GPA"
        customStep={0.1}
        textStyling="mt-5 text-medium"
        studentInput={courseData.gpa}
     />

     <!-- Find courses via search bar  -->
     <div class="flex grow justify-between">
        <TextInput 
        inputHeader="Search Courses by Course Code and Number"
        inputPlaceholder="CS171"
        textStyling="md:mt-2 lg:mt-3 xl:mt-3 text-medium sm:text-lg w-full mr-2"
        studentInput={courseData.course}
        />

        <!--Sends course data moment button is clicked -->
        <button onclick={sendCourseData}>
           <Search class="mb-7 ml-5"/>
              </button>

        <!--Display course cards when button is clicked -->

           </div>
   

     <!-- Courses searched will appear here-->
       
   </div>
    <!-- Schedule section -->
    <div class="rounded-lg shadow-md shadow-stone-200 p-6">
       <h1>Current Schedule</h1>
    </div>
    <!-- Recommendation section -->
    <div class="rounded-lg shadow-md shadow-stone-200 p-6">
       <h1>Input Your Interests</h1>
    </div>
   </div>


<style>
.straight-line{
  height: 2.5px;
}

</style>