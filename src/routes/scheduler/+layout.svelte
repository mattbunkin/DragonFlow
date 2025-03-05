<script lang="ts">
    import * as Sidebar from "$lib/components/ui/sidebar/index.js";
    import AppSidebar from "$lib/components/app-sidebar.svelte";
    let { children } = $props();
  </script>
  
  <div class="flex">
    <!-- Sidebar section - only visible on md and up -->
    <div class="hidden md:block">
      <Sidebar.Provider>
        <AppSidebar />
        <Sidebar.Trigger />
      </Sidebar.Provider>
    </div>
    
    <!-- main content section  always visible -->
    <main class="flex-1">
      <div class="p-6 text-center">
        <h1 class="text-4xl font-medium">Term Scheduler</h1>
        <p class="font-light text-lg">plan out your term</p>
      </div>
      
      <!-- Render children (page content) here -->
      <div class="p-6">
        {@render children?.()}
      </div>
    </main>
  </div>