// TODO: substituir por objeto?
export enum MediaTypeEnum {
  IMAGE = 'photo',
  VIDEO = 'video',
  AUDIO = 'audio',
}

export type Paginated<T> = {
  data: T
  total: number
  page: number
  limit: number
  total_pages: number
}

export type PaginationParams = {
  page: number
  limit: number
}

export type Headers = {
  'x-turnstile-token'?: string
}
