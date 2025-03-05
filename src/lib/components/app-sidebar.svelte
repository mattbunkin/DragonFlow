<script lang="ts">
    import * as Sidebar from "$lib/components/ui/sidebar/index.js";
    import Calendar from "lucide-svelte/icons/calendar";
    import House from "lucide-svelte/icons/house";
    import Inbox from "lucide-svelte/icons/inbox";
    import { User } from "lucide-svelte";
    import Settings from "lucide-svelte/icons/settings";
 
  // can customize all settings here 
  const items = [
    {
      title: "Dashboard",
      url: "/",
      icon: House,
    },
    {
      title: "Inbox",
      url: "/",
      icon: Inbox,
    },
    {
      title: "Schedule",
      url: "/",
      icon: Calendar,
    },
    {
      title: "Profile",
      url: "/",
      icon: User,
    },
    {
      title: "Settings",
      url: "/",
      icon: Settings,
    },
  ];
</script>
    
<Sidebar.Root collapsible="icon">
    <Sidebar.Content>
      <Sidebar.Group>
        <Sidebar.GroupLabel>
            <div class="mt-9 text-center">
                <a href="/" class="text-3xl font-medium">
                    DragonFlow
                </a>
            </div>
        </Sidebar.GroupLabel>
        <Sidebar.GroupContent>
          <Sidebar.Menu class="mt-12 gap-2">
            {#each items as item (item.title)}
              <Sidebar.MenuItem>
                <Sidebar.MenuButton class="text-base">
                  {#snippet child({ props })}
                    <a href={item.url} {...props}>
                      <item.icon/>
                      <span>{item.title}</span>
                    </a>
                  {/snippet}
                </Sidebar.MenuButton>
              </Sidebar.MenuItem>
            {/each}
          </Sidebar.Menu>
        </Sidebar.GroupContent>
      </Sidebar.Group>
    </Sidebar.Content>
  </Sidebar.Root>

  