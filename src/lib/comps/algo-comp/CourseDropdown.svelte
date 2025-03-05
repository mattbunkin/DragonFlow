<script lang="ts">
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
    import { buttonVariants } from "$lib/components/ui/button/index.js";
    
    // opens towards the bottom 
    let position = $state("bottom");

    // binding values of courses to easily access them 
</script>
    
   <DropdownMenu.Root>
    <DropdownMenu.Trigger class="{buttonVariants({ variant: "outline" })} w-[200px]" 
     >Select a Course</DropdownMenu.Trigger
    >
    <DropdownMenu.Content class="w-56">
     <DropdownMenu.Group>
      <DropdownMenu.GroupHeading>Supported CCI Courses</DropdownMenu.GroupHeading>
      <DropdownMenu.Separator />
      <DropdownMenu.RadioGroup bind:value={position}>
       <DropdownMenu.RadioItem value="CS164">CS164</DropdownMenu.RadioItem>
       <DropdownMenu.RadioItem value="CS171">CS171</DropdownMenu.RadioItem>
       <DropdownMenu.RadioItem value="CS172">CS172</DropdownMenu.RadioItem>
       <DropdownMenu.RadioItem value="CS265">CS265</DropdownMenu.RadioItem>
       <DropdownMenu.RadioItem value="CS260">CS260</DropdownMenu.RadioItem>
       <DropdownMenu.RadioItem value="CS270">CS270</DropdownMenu.RadioItem>
      </DropdownMenu.RadioGroup>
     </DropdownMenu.Group>
    </DropdownMenu.Content>
   </DropdownMenu.Root>