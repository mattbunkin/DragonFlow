<script lang="ts">
  import { type DateRange, DateRangePicker } from "bits-ui";
  import CalendarBlank from "phosphor-svelte/lib/CalendarBlank";
  import CaretLeft from "phosphor-svelte/lib/CaretLeft";
  import CaretRight from "phosphor-svelte/lib/CaretRight";
  import { cn } from "$lib/utils";
  import type { DateValue } from "@internationalized/date";

  // declare props with the $bindable rune 
  let { enrollmentDate = $bindable(""), graduationDate = $bindable("") } = $props();
  
  // Use $state rune for reactivity w/ explicit DateRange type
  let value = $state<DateRange>({ start: undefined, end: undefined });

  // Use $effect to update the props when dates change
  $effect(() => {
    // if the value being selected is start of date range
      if (value.start) {
          enrollmentDate = formatDate(value.start);
      }
  });
  
  $effect(() => {
    // if the value being selected is end of date range
      if (value.end) {
          graduationDate = formatDate(value.end);
      }
  });
  
  // helper function with proper TypeScript typing
  function formatDate(date: DateValue | undefined): string {
    // if not date type 
      if (!date) return "";
      return `${date.year}-${String(date.month).padStart(2, '0')}`;
  }

</script>

<!-- Picking a date for enrollment and graduation-->
<DateRangePicker.Root
  bind:value
  weekdayFormat="short"
  fixedWeeks={true}
  class="flex w-full flex-col gap-1.5"
>
  <DateRangePicker.Label class="block select-none text-center text-md font-medium text-zinc-700">
    Enrollment & Graduation Dates
  </DateRangePicker.Label>
  
  <div
  class="custom flex h-input w-full select-none items-center justify-center rounded-full border border-gray-300 bg-white px-4 py-3 text-md tracking-[0.01em] text-gray-800 focus-within:shadow-none hover:border-gray-400 mb-10"
>
  <div class="flex flex-1 justify-center">
    {#each ["start", "end"] as const as type}
      <div class="flex items-center justify-center">
        <DateRangePicker.Input {type}>
          {#snippet children({ segments })}
            <div class="flex justify-center">
              {#each segments as { part, value }}
                <div class="inline-block select-none text-center">
                  {#if part === "literal"}
                    <DateRangePicker.Segment
                      {part}
                      class="p-1 text-gray-500 text-center"
                    >
                      {value}
                    </DateRangePicker.Segment>
                  {:else}
                    <DateRangePicker.Segment
                      {part}
                      class="rounded-lg px-1 py-1 hover:bg-gray-100 focus:bg-gray-100 focus:text-gray-800 aria-[valuetext=Empty]:text-gray-500 text-center"
                    >
                      {value}
                    </DateRangePicker.Segment>
                  {/if}
                </div>
              {/each}
            </div>
          {/snippet}
        </DateRangePicker.Input>
      </div>
      {#if type === "start"}
        <div aria-hidden="true" class="px-2 text-gray-500">–⁠⁠⁠⁠⁠</div>
      {/if}
    {/each}
  </div>

  <DateRangePicker.Trigger
    class="ml-auto inline-flex size-8 items-center justify-center rounded-full text-gray-600 transition-all hover:bg-gray-100 active:bg-gray-200"
  >
    <CalendarBlank class="size-5" />
  </DateRangePicker.Trigger>
</div>
  
  <DateRangePicker.Content sideOffset={6} class="z-50">
    <DateRangePicker.Calendar
      class="mt-6 rounded-2xl border border-gray-200 bg-white p-5 shadow-lg"
    >
      {#snippet children({ months, weekdays })}
        <DateRangePicker.Header class="flex items-center justify-between">
          <DateRangePicker.PrevButton
            class="inline-flex size-10 items-center justify-center rounded-full bg-white transition-all hover:bg-gray-100 active:scale-95"
          >
            <CaretLeft class="size-5" />
          </DateRangePicker.PrevButton>
          <DateRangePicker.Heading class="text-lg font-medium" />
          <DateRangePicker.NextButton
            class="inline-flex size-10 items-center justify-center rounded-full bg-white transition-all hover:bg-gray-100 active:scale-95"
          >
            <CaretRight class="size-5" />
          </DateRangePicker.NextButton>
        </DateRangePicker.Header>
        
        <div
          class="flex flex-col space-y-4 pt-4 sm:flex-row sm:space-x-4 sm:space-y-0"
        >
          {#each months as month}
            <DateRangePicker.Grid
              class="w-full border-collapse select-none space-y-1"
            >
              <DateRangePicker.GridHead>
                <DateRangePicker.GridRow
                  class="mb-1 flex w-full justify-between"
                >
                  {#each weekdays as day}
                    <DateRangePicker.HeadCell
                      class="w-10 text-xs !font-normal text-gray-500"
                    >
                      <div>{day.slice(0, 2)}</div>
                    </DateRangePicker.HeadCell>
                  {/each}
                </DateRangePicker.GridRow>
              </DateRangePicker.GridHead>
              
              <DateRangePicker.GridBody>
                {#each month.weeks as weekDates}
                  <DateRangePicker.GridRow class="flex w-full">
                    {#each weekDates as date}
                      <DateRangePicker.Cell
                        {date}
                        month={month.value}
                        class="relative m-0 size-10 overflow-visible !p-0 text-center text-sm focus-within:relative focus-within:z-20"
                      >
                        <DateRangePicker.Day
                          class={cn(
                            "group relative inline-flex size-10 items-center justify-center overflow-visible whitespace-nowrap rounded-full border border-transparent bg-white p-0 text-sm font-normal text-gray-800 transition-all hover:border-gray-300 focus-visible:outline-none data-[disabled]:pointer-events-none data-[outside-month]:pointer-events-none data-[highlighted]:rounded-none data-[selection-end]:rounded-full data-[selection-start]:rounded-full data-[highlighted]:bg-gray-100 data-[selected]:bg-gray-100 data-[selection-end]:bg-gray-800 data-[selection-start]:bg-gray-800 data-[selected]:font-medium data-[selection-end]:font-medium data-[selection-start]:font-medium data-[disabled]:text-gray-300 data-[selected]:text-gray-800 data-[selection-end]:text-white data-[selection-start]:text-white data-[unavailable]:text-gray-400 data-[unavailable]:line-through data-[selection-start]:focus-visible:outline-none data-[selection-start]:focus-visible:ring-0 data-[selected]:[&:not([data-selection-start])]:[&:not([data-selection-end])]:rounded-none data-[selected]:[&:not([data-selection-start])]:[&:not([data-selection-end])]:focus-visible:border-gray-300 data-[selected]:[&:not([data-selection-start])]:[&:not([data-selection-end])]:focus-visible:outline-none"
                          )}
                        >
                          <div
                            class="absolute top-[5px] hidden size-1 rounded-full bg-gray-800 transition-all group-data-[today]:block group-data-[selected]:bg-white"
                          ></div>
                          {date.day}
                        </DateRangePicker.Day>
                      </DateRangePicker.Cell>
                    {/each}
                  </DateRangePicker.GridRow>
                {/each}
              </DateRangePicker.GridBody>
            </DateRangePicker.Grid>
          {/each}
        </div>
      {/snippet}
    </DateRangePicker.Calendar>
  </DateRangePicker.Content>
</DateRangePicker.Root>

<style>
    /* Global style to remove all focus outlines */
    :global(*:focus) {
      outline: none !important;
      box-shadow: none !important;
    }
    
    /* Remove any blue focus rings */
    :global(*:focus-visible) {
      outline: none !important;
      box-shadow: none !important;
      border-color: rgba(210, 210, 210, 0.8) !important;
    }

  </style>