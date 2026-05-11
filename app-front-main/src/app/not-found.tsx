import Link from 'next/link'
import { Button, Typography, Container, Box } from '@mui/material'
import { Home as HomeIcon, SearchOff as SearchOffIcon } from '@mui/icons-material'

export default function NotFoundPage() {
  return (
    <Container maxWidth="md" className="flex flex-col items-center justify-center min-h-screen text-center">
      <Box className="mb-6 text-gray-400">
        <SearchOffIcon sx={{ fontSize: 100 }} />
      </Box>

      <Typography variant="h1" className="text-6xl font-bold text-gray-800 mb-4">
        404
      </Typography>

      <Typography variant="h5" className="mb-2">
        Página não encontrada
      </Typography>
      <Typography variant="body1" color="text.secondary" className="mb-6 max-w-md">
        Desculpe, não conseguimos encontrar a página que você procurava. Verifique o endereço ou volte para a página
        inicial.
      </Typography>

      <Button variant="contained" startIcon={<HomeIcon />} className="px-6 py-2" LinkComponent={Link} href="/">
        Voltar para o início
      </Button>
    </Container>
  )
}
