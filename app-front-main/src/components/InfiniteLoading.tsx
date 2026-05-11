import { CircularProgress } from '@mui/material'
import useInfiniteScroll from 'react-infinite-scroll-hook'

type InfiniteLoadingProps = {
  isFetchingNextPage: boolean
  hasNextPage: boolean
  fetchNextPage: VoidFunction
  isError: boolean
  rootMargin?: string
}

export const InfiniteLoading = ({
  isFetchingNextPage,
  hasNextPage,
  fetchNextPage,
  isError,
  rootMargin = '0px 0px 400px 0px',
}: InfiniteLoadingProps) => {
  const [infiniteRef] = useInfiniteScroll({
    loading: isFetchingNextPage,
    hasNextPage,
    onLoadMore: fetchNextPage,
    disabled: isError,
    rootMargin,
  })

  return hasNextPage && <CircularProgress ref={infiniteRef} size="30px" sx={{ justifySelf: 'center', my: '20px' }} />
}
