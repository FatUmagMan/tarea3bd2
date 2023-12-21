import { camelCase } from 'change-case/keys'

const BASE_URL = 'http://127.0.0.1:8000'

export async function apiFetch<T>(
  url: string,
  method = 'GET',
  body: BodyInit | null | undefined = undefined,
  headers: HeadersInit | Record<string, never> = {},
  camelCaseDepth: number = 5
): Promise<T> {
  url = new URL(url, BASE_URL).href

  const response = await fetch(url, { method, body, headers })
  if (!response.ok) {
    const text = await response.text()
    let detail: string

    // get error detail from response body
    try {
      const json = JSON.parse(text)
      detail = json.detail
    } catch (error) {
      detail = await response.text()
    }

    throw { status: response.status, message: detail }
  }
  return camelCase(await response.json(), camelCaseDepth) as T
}
