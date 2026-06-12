import { defineConfig } from 'vite'

export default defineConfig({
  root: 'src',
  base: './',

  build: {
    outDir: '../dist',
    assetsDir: 'assets',
    assetsInlineLimit: 1000000,
  },
})
