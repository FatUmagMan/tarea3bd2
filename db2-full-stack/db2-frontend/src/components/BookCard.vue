<script setup lang="ts">
import { IBadge, IButton, ICard } from '@inkline/inkline'

import { Book } from '@/interfaces.ts'

defineProps<{
  book: Book
}>()
</script>

<template>
  <ICard>
    <div class="_display:flex">
      <div class="_flex-grow:1">
        <h2 class="_color:primary!">
          {{ book.title }}
        </h2>
      </div>
      <div>
        <IButton outline color="primary" :to="{ name: 'ViewBook', params: { id: book.id } }">
          <FontAwesomeIcon icon="circle-info" class="_margin-right:1/2" />
          Detalles
        </IButton>
      </div>
    </div>
    <h5>{{ book.author?.name }}</h5>
    <div class="_display:flex">
      <div class="_flex-grow:1">
        <p class="_color:gray! _margin-bottom:1/2">{{ book.description }}</p>
      </div>
      <div class="no-wrap">
        <div class="_margin-bottom:1/2">
          <IBadge v-for="category in book.categories" :key="category.id" class="_margin-x:1/4">
            {{ category.name }}
          </IBadge>
        </div>
        <div class="_text-align:right">Disponibles: {{ book.copiesAvailable }}</div>
      </div>
    </div>
  </ICard>
</template>

<style scoped>
.no-wrap {
  flex-shrink: 0;
}
</style>
