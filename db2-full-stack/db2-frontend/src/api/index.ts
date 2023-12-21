import { snakeCase } from 'change-case/keys'

import { Author, Book, Category } from '../interfaces.ts'
import { apiFetch } from './utilities.ts'

async function getBooks(): Promise<Book[]> {
  return apiFetch<Book[]>('/books')
}

async function getBook(bookId: number | string): Promise<Book> {
  return apiFetch<Book>(`/books/${bookId}`)
}

async function postBook(book: Book) {
  return apiFetch<Book>('/books', 'POST', JSON.stringify(snakeCase(book)))
}

async function updateBook(book: Book) {
  return apiFetch<Book>(`/books/${book.id}`, 'PATCH', JSON.stringify(snakeCase(book)))
}

async function getAuthors(): Promise<Author[]> {
  return apiFetch<Author[]>('/authors')
}

async function postAuthor(author: Author) {
  return apiFetch<Author>('/authors', 'POST', JSON.stringify(snakeCase(author)))
}

async function getCategories() {
  return apiFetch<Category[]>('/categories')
}

export { getBooks, getBook, postBook, updateBook, getAuthors, postAuthor, getCategories }
