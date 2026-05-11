import { format as formatFn } from 'date-fns'
import { ptBR } from 'date-fns/locale'

export const format = (date: Date | number | string, formatStr: string): string => {
  let d: Date

  if (typeof date === 'string') {
    const match = date.match(/^(\d{4})-(\d{2})-(\d{2})$/)
    if (match) {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const [_, year, month, day] = match
      d = new Date(Number(year), Number(month) - 1, Number(day))
    } else {
      d = new Date(date)
    }
  } else {
    d = new Date(date)
  }

  return formatFn(d, formatStr, { locale: ptBR })
}
