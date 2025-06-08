import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  // Configure content collection to use root content/ directory
  content: {
    sources: ['content']
  },
  // Base site configuration
  site: 'https://vibe.news',
  base: '/',
  trailingSlash: 'never'
}); 