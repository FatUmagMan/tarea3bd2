<script setup lang="ts">
import {
  IButton,
  IButtonGroup,
  ICheckboxGroup,
  IForm,
  IFormGroup,
  IFormLabel,
  IInput,
  INumberInput,
  ISelect,
  ITextarea
} from '@inkline/inkline'
import { Ref, computed, onMounted, reactive, ref, watch } from 'vue'

import { Author, Book, Category } from '@/interfaces'

interface Props {
  inputBook?: Book | null
  authors: Author[]
  categories: Category[]
}

const props = withDefaults(defineProps<Props>(), {
  inputBook: null
})

const emit = defineEmits<{
  saveBook: [book: Book]
  cancel: []
}>()

const book: Book = reactive({
  title: '',
  description: '',
  language: '',
  isbn: '',
  year: null,
  authorId: null,
  categories: [],
  copies: []
})
const selectedCategories: Ref<number[]> = ref([])

const authorOptions = computed(() => {
  return props.authors.map((x) => ({ id: x.id, label: x.name }))
})
const categoryOptions = computed(() => {
  return props.categories.map((x) => ({ id: x.id, label: x.name }))
})

watch(
  () => props.inputBook,
  () => {
    if (props.inputBook !== null) {
      Object.assign(book, props.inputBook)
      selectedCategories.value = props.inputBook.categories.map((x) => x.id as number)
    }
  }
)

const saveBook = () => {
  // update book.categories based on selectedCategories
  book.categories = props.categories
    .filter((x) => selectedCategories.value.includes(x.id as number))
    .map((x) => ({ id: x.id }))

  emit('saveBook', book)
}
</script>

<template>
  <IForm>
    <IFormGroup>
      <IFormLabel>Título</IFormLabel>
      <IInput v-model="book.title"></IInput>
    </IFormGroup>
    <IFormGroup>
      <IFormLabel>Descripción</IFormLabel>
      <ITextarea v-model="book.description"></ITextarea>
    </IFormGroup>
    <IFormGroup>
      <IFormLabel>Idioma</IFormLabel>
      <IInput v-model="book.language"></IInput>
    </IFormGroup>
    <IFormGroup>
      <IFormLabel>ISBN</IFormLabel>
      <IInput v-model="book.isbn"></IInput>
    </IFormGroup>
    <IFormGroup>
      <IFormLabel>Año</IFormLabel>
      <INumberInput v-model="book.year"></INumberInput>
    </IFormGroup>
    <IFormGroup>
      <IFormLabel>Autor</IFormLabel>
      <ISelect v-model="book.authorId" :options="authorOptions"></ISelect>
    </IFormGroup>
    <IFormGroup>
      <IFormLabel>Categorías</IFormLabel>
      <ICheckboxGroup
        v-model="selectedCategories"
        inline
        :options="categoryOptions"
      ></ICheckboxGroup>
    </IFormGroup>
    <IFormGroup class="_margin-top:3!">
      <IButtonGroup block>
        <IButton color="primary" @click="saveBook">Guardar</IButton>
        <IButton color="gray" @click="emit('cancel')">Cancelar</IButton>
      </IButtonGroup>
    </IFormGroup>
  </IForm>
</template>

<style scoped></style>
