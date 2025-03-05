import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  optimizeDeps: {
    exclude: ['@floating-ui/dom', 'bits-ui', 'svelte-motion', 'lucide-svelte'],
  },
  build: {
    commonjsOptions: {
      include: [/node_modules/]
    }
  },
  ssr: {
    noExternal: ['svelte-motion', 'bits-ui']
  }
});