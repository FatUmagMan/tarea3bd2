<script setup lang="ts">
import { IColumn, IContainer, IRow } from '@inkline/inkline'
import { Ref, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { getAuthors, getBook, getCategories, updateBook } from '@/api'
import { Author, Book, Category } from '@/interfaces.ts'

import BookForm from '@/components/forms/BookForm.vue'

const route = useRoute()
const router = useRouter()
const book: Ref<Book | null> = ref(null)
const authors: Author[] = reactive([])
const categories: Category[] = reactive([])

const loadBook = async () => {
  book.value = await getBook(route.params.id as string)
}
const loadAuthors = async () => {
  Object.assign(authors, await getAuthors())
}
const loadCategories = async () => {
  Object.assign(categories, await getCategories())
}

const saveBook = async (book: Book) => {
  book.year = Number(book.year)
  await updateBook(book)
  await router.push({ name: 'ViewBook', params: { id: book.id } })
}

loadBook()
loadAuthors()
loadCategories()
</script>

<template>
  <IContainer>
    <IRow around>
      <IColumn md="8" lg="6">
        <h1 class="_color:primary">Editar {{ book?.title }}</h1>
        <BookForm
          :input-book="book"
          :categories="categories"
          :authors="authors"
          @save-book="saveBook"
          @cancel="router.push({ name: 'ViewBook', params: { id: book?.id } })"
        ></BookForm>
      </IColumn>
    </IRow>
  </IContainer>
</template>

<style scoped></style>
