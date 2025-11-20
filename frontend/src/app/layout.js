import './globals.css'

export const metadata = {
  title: 'Anime Picker | AI-Powered Recommendations',
  description: 'Discover your next favorite anime with our AI-powered semantic search engine.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
