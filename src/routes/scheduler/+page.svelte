<script lang="ts">
   import Progress from "$lib/components/ui/progress/progress.svelte";
   import NumberInput from "$lib/comps/personalize-comp/NumberInput.svelte";
   import TextInput from "$lib/comps/personalize-comp/textInput.svelte";
   import { ExternalLink } from 'lucide-svelte';
   import { Search } from 'lucide-svelte';
   import { CircleX } from 'lucide-svelte';
   import { Meh } from 'lucide-svelte';
   import { ThumbsUp } from 'lucide-svelte';
   import { ThumbsDown } from 'lucide-svelte';


   // save all data to this JS object pass into model.py
   interface Instructor {
      name: string
   }
   interface Days {
      day: string
   }
   
   // define explicit types for the course object 
   interface Course {
      subject_code: string;
      course_number: string;
      instructors: Instructor[];
      course_title: string;
      crn: number;

      // extra data 
      days: Days[]
      instruction_type: string;
      start_time: string;
      end_time: string;
   }

   // Define interface for RMP data
  interface RMPData {
    avgRating: number;
    link: string;
    department: string;
  }
  
  // Store professor ratings
  let professorRatings = $state<Record<string, RMPData>>({});
  

   // data to send to flask api with default values
   let courseData = {
       gpa: 0,
       course: ""
   }

   // store response data from API
   let courseSlots = $state<Course[]>([]);
   let successPercent = $state<number>(1) 

   // track if loading data
   let isLoading = $state(false)

      // Create a derived value for display (so it reacts to successPercent changes)
   let progressValue = $derived(successPercent);


   // send course data to scheduler endpoint
   async function sendCourseData(){
     try {
      isLoading = true;

      // ensure all types of data is correct
      const dataToSend = {
         // ensure gpa is a number type
         gpa: Number(courseData.gpa), 

         // remove any whitespace and turn all letters upper case
         course: (courseData.course.trim()).toUpperCase() 
      };


        const response = await fetch("http://127.0.0.1:5000/auth/course-retriever",
           {
              method: "POST",
              headers: {
                 "Content-Type": "application/json",
               //   "Authorization": `Bearer ${localStorage.getItem("access_token")}`
              },
              // always include cookies for Flask's login/session based authentication
              credentials: "include",

              //payload/data to send to flask endpoint
              body: JSON.stringify(dataToSend)
           }
        )
        // display error here later to user
        if (!response.ok){
            const errorText = await response.text();
            console.error("API Error Response:", errorText);

            // make empty list if error
            courseSlots = []
            throw new Error(`HTTP error. Status ${response.status}`);
        }
      
      // if the data was received successfully 
      else if (response.ok){
         const responseData = await response.json()
         if (responseData.course_data) {
            courseSlots = responseData.course_data
            successPercent = responseData.probability_score

            console.log("Set prob to:", successPercent)
               
         }
         // set empty if other error
         else {
            courseSlots = []
         }
      }
     }
     catch(error){
        console.error(`Failed to retrieve course data from data.json: ${error}`)
     }

     // whether error or success this gets executed
     finally {
      isLoading = false;
     }
   }



  // Function to fetch professor rating from your Flask proxy endpoint
  async function fetchProfessorRating(professorName: string) {
   // api request to flask proxy endpoint
    try {
      const response = await fetch(`http://127.0.0.1:5000/auth/professor-rating?name=${encodeURIComponent(professorName)}`);
      // basic error handling 
      if (!response.ok) {
        throw new Error(`Error fetching professor rating: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`Failed to fetch professor rating: ${error}`);
      return null;
    }
  }
  
  // Load professor ratings when course data changes; reactive once courseSlots var filled
  $effect(() => {
    if (courseSlots.length > 0) {
      // Get all unique professor names
      const uniqueProfessors = [...new Set(
        courseSlots.flatMap(course => 
          course.instructors.map(instructor => instructor.name)
        )
      )];
      
      // Fetch ratings for each professor
      uniqueProfessors.forEach(async (profName) => {
        if (!professorRatings[profName]) {
          const rating = await fetchProfessorRating(profName);
          if (rating && !rating.error) {
            professorRatings[profName] = rating;
          }
        }
      });
    }
  });

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
         bind:studentInput={courseData.gpa}
      />

     <!-- Find courses via search bar  -->
      <div class="flex grow justify-between mb-2">
        <TextInput 
        inputHeader="Search Courses by Course Code and Number"
        inputPlaceholder="CS171"
        textStyling="md:mt-2 lg:mt-3 xl:mt-3 text-medium sm:text-lg w-full mr-2"
        bind:studentInput={courseData.course}
        />

        <!--Sends course data moment button is clicked -->
        <button 
         onclick={sendCourseData}
         disabled={isLoading}
        >
        {#if isLoading}
            <span class="animate-pulse">Loading...</span>
         {:else}
           <Search class="mb-7 ml-5"/>
         {/if}
         </button>
      </div>

      <!--Display course cards when button is clicked -->
      {#if courseSlots.length > 0}
      <div>
         {#each courseSlots as course, i}
         <!--Styling for course card-->
          <div class="p-4 text-lg border rounded-sm shadow-sm mb-6">

            <!--course subject code+name, and course crn-->
            <div class="flex items-center justify-between w-full">
               <h3 class="font-medium">
                  {course.subject_code + course.course_number || `Course ${i+1}`}
               </h3>
               <h3 class="font-medium">
                  {course.crn || 'Course CRN'}
               </h3>
            </div>
            
            <!--course name and time slot-->
            <div class="flex items-center justify-between w-full">
               <p class="text-black text-opacity-60">
                  {course.course_title}
               </p>
               <p class="text-black text-opacity-70 text-sm">
                  {course.instruction_type}:
                  <!--could have a course with multiple days -->
                  {#each course.days as day}
                  <!-- add space between days if more than one day-->
                     {#if course.days.length > 1}
                        {`${day} `}
                     {:else}
                        {day}
                     {/if}
                  {/each}
               </p>
            </div>
         
            <div class="flex items-center justify-between w-full">
               <p class="text-sm text-black text-opacity-60">
                  {(course.instructors)[0].name || 'Course details'}
                </p>
               
                <!--If we found a RMP link and name/rating -->
               {#if professorRatings[(course.instructors)[0].name]}
                  <div class="flex items-center ml-2">
                     <!--Determine the color of the rating based of actual rating-->
                     {#if professorRatings[(course.instructors)[0].name].avgRating >= 3.5}
                        <span class="text-emerald-400 font-medium text-sm mt-1 mr-1">
                           {professorRatings[(course.instructors)[0].name].avgRating.toFixed(2)} <ThumbsUp class="inline-block mb-2"/>
                        </span>
                     
                     <!--Meh rating case-->
                     {:else if  professorRatings[(course.instructors)[0].name].avgRating < 3.5 && professorRatings[(course.instructors)[0].name].avgRating > 2.5}
                     <span class="text-yellow-400 font-medium text-sm mt-1 mr-1">
                        {professorRatings[(course.instructors)[0].name].avgRating.toFixed(2)} <Meh class="inline-block mb-1"/>
                     </span>

                     <!--bad rating case-->
                     {:else}
                     <span class="text-red-400 font-medium text-sm mt-1 mr-1">
                        {professorRatings[(course.instructors)[0].name].avgRating.toFixed(2)} <ThumbsDown class="inline-block"/>
                     </span>
                     {/if}
                     <p>
                        
                     </p>

                     <!--Link to direct to professor-->
                     <a 
                     href={professorRatings[(course.instructors)[0].name].link} 
                     target="_blank" 
                     rel="noopener noreferrer"
                     >
                     <ExternalLink class="text-blue-500 text-opacity-80 ml-1 w-4 h-4"/>
                     </a>
                  </div>
               {:else}
                  <!-- Default link when rating is not available -->
                  <a 
                     href={`https://www.ratemyprofessors.com/search/teachers?query=${encodeURIComponent((course.instructors)[0].name)}`} 
                     target="_blank" 
                     rel="noopener noreferrer"
                  >
                     <ExternalLink class="text-blue-500 text-opacity-80 ml-1 w-4 h-4"/>
                  </a>
               {/if}
            </div>

            <div class="flex items-center justify-between w-full mt-1">
               <Progress value={progressValue} max={100} class="w-[90%] mt-3 inline-block"/>
               <p class="inline-block text-sm">
                  {progressValue}%
               </p>
            </div>
              
      

          </div>

        {/each}
      </div>

      <!--If data is loading for course-->
      {:else if isLoading}
      <div class="mt-4 p-4 text-center">
         <p>Loading courses...</p>
      </div>

      <!--If there is no courses at all found-->
      {:else if courseData.course}
      <div class="flex flex-col items-center justify-center mt-4 p-4 text-center text-zinc-800">
         <p class="text-xl">No courses found. Try a different search.</p>
         <CircleX class="text-red-400 w-10 h-10 mt-2"/>
       </div>
      {/if}
   

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