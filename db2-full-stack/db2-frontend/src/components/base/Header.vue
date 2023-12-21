<script setup lang="ts">
import { INav, INavItem, INavbar, INavbarCollapsible, useInkline } from '@inkline/inkline'
import { computed, toRefs } from 'vue'

const inkline = useInkline()
const colorMode = toRefs(inkline.options).colorMode

const colorModeIcon = computed(() => {
  return colorMode.value === 'light' ? 'moon' : 'sun'
})

const toggleColorMode = () => {
  colorMode.value = colorMode.value === 'light' ? 'dark' : 'light'
}
</script>

<template>
  <INavbar>
    <INavbarCollapsible>
      <INav>
        <INavItem :to="{ name: 'Home' }">Inicio</INavItem>
        <INavItem :to="{ name: 'ListBooks' }">Libros</INavItem>
      </INav>
      <INav>
        <INavItem stop-propagation class="clickable" @click="toggleColorMode">
          <FontAwesomeIcon :icon="colorModeIcon" size="lg" />
        </INavItem>
      </INav>
    </INavbarCollapsible>
  </INavbar>
</template>

<style scoped>
.clickable {
  cursor: pointer;
}
</style>
