<script lang="ts">
    import '../app.css';
    import { onMount } from 'svelte';
    import { initAuthentication, isAuthenticated } from '../tools/token-service';
    import { goto } from '$app/navigation';
    import { page } from '$app/state';
    
    // path configs
    const publicRoutes = ["/", "/login", "/sign-up"];
    const privateRoutes = ["/scheduler", "/personalize-account", "/dashboard"];
    
    // init auth on mount
    onMount(() => {
        initAuthentication();
    })
    
    // handling route protection - improved version
    $effect(() => {
        const path = page.url.pathname;
        
        // Only redirect from private routes if not authenticated
        if (privateRoutes.some(route => path === route || path.startsWith(route + "/")) && !$isAuthenticated) {
            // go to login if user tried to access protected route
            goto("/login");
        }
        
        // Only redirect from login/signup pages if already authenticated
        // Don't redirect from home page regardless of auth status
        if ((path === "/login" || path === "/sign-up") && $isAuthenticated) {
            goto("/scheduler");
        }
    });
    
    let { children } = $props();
</script>

{@render children()}
