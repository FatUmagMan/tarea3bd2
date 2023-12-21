<script setup lang="ts">
import { ILayout, ILayoutContent, ILayoutHeader } from '@inkline/inkline'

import Header from '@/components/base/Header.vue'
</script>

<template>
  <ILayout>
    <ILayoutHeader>
      <Header></Header>
    </ILayoutHeader>
    <ILayoutContent class="_padding-top:2!">
      <RouterView></RouterView>
    </ILayoutContent>
  </ILayout>
</template>

<style scoped></style>
