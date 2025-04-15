<script lang="ts">
    import * as Sidebar from "$lib/components/ui/sidebar/index.js";
    import AppSidebar from "$lib/components/app-sidebar.svelte";
    import CustomDropdown from "$lib/comps/algo-comp/CustomDropdown.svelte";
    let { children } = $props();
    // place holder for dummy data inside dropdown
    let options: string[] = ["Fall 24-25", "Winter 24-25", "Spring 24-25", "Summer 24-25"];
    let viewOptions: string[] = ["List View", "Calendar View"];
    // track selected values
    let selectedQuarter = $state("Fall 24-25");
    let selectedView = $state("List View");
  </script>
  
  <div class="flex">
    <!-- Sidebar section - only visible on md and up -->
    <div class="hidden md:block">
      <Sidebar.Provider>
        <AppSidebar />
        <Sidebar.Trigger />
      </Sidebar.Provider>
    </div>
    
 <!-- main content section always visible -->
    <main class="flex-1">
 <!--Main content wrapper with consistent padding-->
 <div class="p-6 flex flex-col space-y-6">
   <!--Main header-->
   <div class="flex items-center justify-between shadow-md shadow-stone-200 rounded-lg p-6">
     <div class="flex-col mr-5">
        <h1 class="text-4xl font-medium">Term Scheduler</h1>
       <p class="text-left text-black text-opacity-60">plan out your term</p>
     </div>
     <!---Quarter Selection and View Type Components-->
     <div class="flex">
       <CustomDropdown
         dropDownHeader="Fall 2025-2025"
         dropDownSubHeader="Select Your Quarter"
         dropDownOptions={options}
         styling="w-[180px] h-[40px]"
         bind:selected={selectedQuarter}
       />
       <CustomDropdown
         dropDownHeader={"List View"}
         dropDownSubHeader="Select Your View Type"
         dropDownOptions={viewOptions}
         styling="ml-5 w-[120px] h-[40px]"
         bind:selected={selectedView}
       />
     </div>
      </div>
      
   <!-- Render children (page content) directly without extra padding -->
        {@render children?.()}
      </div>
    </main>
 </div>
 <style>
 </style>