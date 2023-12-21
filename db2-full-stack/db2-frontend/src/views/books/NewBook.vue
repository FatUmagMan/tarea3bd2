<script setup lang="ts">
import { IColumn, IContainer, IRow } from '@inkline/inkline'
import { reactive } from 'vue'
import { useRouter } from 'vue-router'

import { getAuthors, getCategories, postBook } from '@/api'
import { Author, Book, Category } from '@/interfaces.ts'

import BookForm from '@/components/forms/BookForm.vue'

const router = useRouter()
const book: Book = reactive({
  title: '',
  description: '',
  language: '',
  isbn: '',
  year: null,
  authorId: null,
  categories: []
})
const authors: Author[] = reactive([])
const categories: Category[] = reactive([])

const loadAuthors = async () => {
  Object.assign(authors, await getAuthors())
}
const loadCategories = async () => {
  Object.assign(categories, await getCategories())
}
const saveBook = async (updatedBook: Book) => {
  Object.assign(book, updatedBook)
  book.year = parseInt(String(book.year))
  // book.categories = book.categories.map((categoryId: ) => category.id)
  await postBook(book)
  await router.push({ name: 'ListBooks' })
}

loadAuthors()
loadCategories()
</script>

<template>
  <IContainer>
    <IRow around>
      <IColumn md="8" lg="6">
        <h1 class="_color:primary">Nuevo Libro</h1>
        <BookForm
          :authors="authors"
          :categories="categories"
          @save-book="saveBook"
          @cancel="router.push({ name: 'ListBooks' })"
        ></BookForm>
      </IColumn>
    </IRow>
  </IContainer>
</template>
