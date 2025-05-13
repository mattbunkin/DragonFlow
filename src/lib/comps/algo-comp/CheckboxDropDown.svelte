<script lang="ts">
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
    import { buttonVariants } from "$lib/components/ui/button/index.js";

    // Properties with default values
    let {
      dropDownHeader,
      dropDownSubHeader, 
      dropDownOptions, 
      styling,

      // Add a bind:selected prop to allow parent components to access the selected value
      selected = $bindable(<string[]>[])
    } = $props();

    // make object that checks if certain option was checked or not
    const checkedStates = $state<Record<string, boolean>>({});

    // Initialize checked states
    $effect(() => {
        dropDownOptions.forEach((option: string) => {
            checkedStates[option] = selected.includes(option);
        });
    });

    // Function to handle checkbox changes
    function handleCheckboxChange(option: string, isChecked: boolean) {
    if (isChecked) {
        // Add to selected if not already there
        if (!selected.includes(option)) {
        selected = [...selected, option];
        }
    } else {
        // Remove from selected
        selected = selected.filter((item: string) => item !== option);
    }

    // Update the checked state
    checkedStates[option] = isChecked;
    }

    // this function helps so we don't update UI based off the selected options.. but by the header..
    function getDisplayText() {
    // Always show the dropdown header text regardless of selection
    return dropDownHeader;
  }
</script>
    
   <DropdownMenu.Root>
    <DropdownMenu.Trigger class="{buttonVariants({ variant: "outline" })} {styling}" 
     >{getDisplayText()}</DropdownMenu.Trigger
    >
    <DropdownMenu.Content class="w-56">
     <DropdownMenu.Group>
      <DropdownMenu.GroupHeading>{dropDownSubHeader}</DropdownMenu.GroupHeading>
      <DropdownMenu.Separator />
        {#each dropDownOptions as option}
        <!-- place holder we don't actually care if it was checked or not-->
            <DropdownMenu.CheckboxItem 
            checked={checkedStates[option]} 
            onCheckedChange={(isChecked) => handleCheckboxChange(option, isChecked)}
            >
                {option}
            </DropdownMenu.CheckboxItem>
        {/each}
     </DropdownMenu.Group>
    </DropdownMenu.Content>
   </DropdownMenu.Root>