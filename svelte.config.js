import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  kit: {
    adapter: adapter(),
    alias: {
      '$lib': './src/lib',
      '$lib/components': './src/lib/components',
      '$lib/utils': './src/lib/utils',
      '$lib/hooks': './src/lib/hooks',
      '$lib/components/ui': './src/lib/components/ui'
    }
  },
  preprocess: vitePreprocess(),
  // Add this section
  vitePlugin: {
    experimental: {
      optimizeDeps: {
        include: ['lucide-svelte']
      }
    }
  }

};

export default config;