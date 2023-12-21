<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { IBadge, IButton, IColumn, IContainer, IRow, ITable } from '@inkline/inkline'
import { Ref, ref } from 'vue'
import { useRoute } from 'vue-router'

import { getBook } from '@/api'
import { Book, BookCopy } from '@/interfaces.ts'

const route = useRoute()
const book: Ref<Book | null> = ref(null)

const loadBook = async () => {
  book.value = await getBook(route.params.id as string)
}

const bookCopyStatus = (bookCopy: BookCopy) => {
  if (bookCopy.isAvailable) {
    return 'Disponible'
  } else {
    return 'Prestado'
  }
}

loadBook()
</script>

<template>
  <IContainer>
    <IRow around>
      <IColumn md="10" lg="8">
        <div class="_clearfix!">
          <div class="_float:right!">
            <IButton :to="{ name: 'EditBook', params: { id: book?.id } }" outline color="primary">
              <FontAwesomeIcon icon="edit" class="_margin-right:1/2"></FontAwesomeIcon>
              Modificar
            </IButton>
          </div>
        </div>

        <h1 class="_color:primary">{{ book?.title }}</h1>
        <p>{{ book?.description }}</p>
      </IColumn>
    </IRow>
    <IRow around>
      <IColumn md="10" lg="8">
        <h3 class="_color:primary">Detalles</h3>
        <ITable border condensed>
          <tbody>
            <tr>
              <th class="_text-align:center">ISBN</th>
              <td class="_text-align:center">{{ book?.isbn }}</td>
            </tr>
            <tr>
              <th class="_text-align:center">Año</th>
              <td class="_text-align:center">{{ book?.year }}</td>
            </tr>
            <tr>
              <th class="_text-align:center">Idioma</th>
              <td class="_text-align:center">{{ book?.language }}</td>
            </tr>
            <tr>
              <th class="_text-align:center">Autor</th>
              <td class="_text-align:center">{{ book?.author?.name }}</td>
            </tr>
            <tr>
              <th class="_text-align:center">Categorías</th>
              <td class="_text-align:center">
                <IBadge
                  v-for="category in book?.categories"
                  :key="category?.id"
                  class="_margin-x:1/4"
                >
                  {{ category.name }}
                </IBadge>
              </td>
            </tr>
          </tbody>
        </ITable>
      </IColumn>
    </IRow>
    <IRow around>
      <IColumn md="10" lg="8">
        <h3 class="_color:primary">Copias</h3>
        <ITable v-if="book?.copies.length > 0" border condensed>
          <thead>
            <tr>
              <th class="_text-align:center!">Serie</th>
              <th class="_text-align:center!">Estado</th>
              <th class="_text-align:center!"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="bookCopy in book?.copies" :key="bookCopy.id">
              <td class="_text-align:center!">{{ bookCopy.serialNumber }}</td>
              <td class="_text-align:center!">{{ bookCopyStatus(bookCopy) }}</td>
              <td class="_text-align:center!">
                <RouterLink v-if="bookCopy.isAvailable" to="#">Préstamo</RouterLink>
              </td>
            </tr>
          </tbody>
        </ITable>
        <template v-else>
          <p>No existen copias de este libro.</p>
        </template>
      </IColumn>
    </IRow>
  </IContainer>
</template>

<style scoped></style>
