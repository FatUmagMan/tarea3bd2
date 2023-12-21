import type { UserOptions } from '@inkline/plugin'
import inkline from '@inkline/plugin/vite'
import vue from '@vitejs/plugin-vue'
import { URL, fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'

const inklineConfig: UserOptions = {
  outputDir: 'src/css/variables'
}

export default defineConfig({
  plugins: [inkline(inklineConfig), vue()],
  resolve: {
    alias: [{ find: '@', replacement: fileURLToPath(new URL('./src', import.meta.url)) }]
  }
})
