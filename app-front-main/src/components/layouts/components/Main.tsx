import { PropsWithChildren } from 'react'

export const Main = ({ children }: PropsWithChildren) => {
  return <main className="overflow-auto  bg-[#F1F5F9] p-4">{children}</main>
}
