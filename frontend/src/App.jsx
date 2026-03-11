import Sidebar from './components/Sidebar'
import GenerateListingPage from './pages/GenerateListingPage'

export default function App() {
  return (
    <div className="h-screen bg-slate-950 flex">
      <Sidebar />
      <main className="flex-1">
        <GenerateListingPage />
      </main>
    </div>
  )
}
