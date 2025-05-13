<script lang="ts">
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
    import { buttonVariants } from "$lib/components/ui/button/index.js";
    
    // opens towards the bottom 
    let position = $state("bottom");


    // Properties with default values
    let {
      dropDownHeader,
      dropDownSubHeader, 
      dropDownOptions, 
      styling,
      // Add a bind:selected prop to allow parent components to access the selected value
      selected = $bindable("")
    } = $props();

   // Watch for position changes and update selected value
    $effect(() => {
      if (position && dropDownOptions.includes(position)) {
        selected = position;
      }
    });
</script>
    
   <DropdownMenu.Root>
    <DropdownMenu.Trigger class="{buttonVariants({ variant: "outline" })} {styling}" 
     >{selected || dropDownHeader}</DropdownMenu.Trigger
    >
    <DropdownMenu.Content class="w-56">
     <DropdownMenu.Group>
      <DropdownMenu.GroupHeading>{dropDownSubHeader}</DropdownMenu.GroupHeading>
      <DropdownMenu.Separator />
      <DropdownMenu.RadioGroup bind:value={selected}>
        {#each dropDownOptions as option}
            <!-- svelte-ignore attribute_quoted -->
            <DropdownMenu.RadioItem 
              value="{option}"
              >
              <!--Display option in component-->
              {option}
            </DropdownMenu.RadioItem>
        {/each}
      </DropdownMenu.RadioGroup>
     </DropdownMenu.Group>
    </DropdownMenu.Content>
   </DropdownMenu.Root>