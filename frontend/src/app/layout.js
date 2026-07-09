import './globals.css'

export const metadata = {
  title: 'Drug Shortage Predictor AI',
  description: 'Predict FDA injectable drug shortages from clinical trial terminations.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
