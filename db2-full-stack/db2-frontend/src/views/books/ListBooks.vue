<script setup lang="ts">
import { IButton, IColumn, IContainer, IIcon, ILoader, IRow } from '@inkline/inkline'
import { reactive, ref } from 'vue'

import { getBooks } from '@/api'
import { Book } from '@/interfaces.ts'

import BookCard from '@/components/BookCard.vue'

const books: Book[] = reactive([])
const loading = ref(false)

const loadBooks = async () => {
  loading.value = true
  Object.assign(books, await getBooks())
  loading.value = false
}

loadBooks()
</script>

<template>
  <IContainer>
    <IRow>
      <IColumn class="_display:flex! _justify-content:end!">
        <IButton color="primary" :to="{ name: 'NewBook' }">
          <template #icon>
            <IIcon name="ink-plus" />
          </template>
          Nuevo libro
        </IButton>
      </IColumn>
    </IRow>
    <IRow class="_margin-top:2!">
      <div v-if="loading" class="_margin-x:auto _margin-top:5">
        <ILoader />
      </div>
      <template v-else>
        <IColumn v-for="book in books" :key="book.id" xs="12" md="6" class="_margin-bottom:2!">
          <BookCard :book="book" />
        </IColumn>
      </template>
    </IRow>
  </IContainer>
</template>
