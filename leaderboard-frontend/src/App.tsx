import './App.css'
import { AuthProvider } from './context/AuthContext'
import Navbar from './components/navbar'
import PlayerInfoCard from './components/player-info-card'
import PlayerTabs from './components/player-tabs'

function App() {
  return (
    <AuthProvider>
      <Navbar />
      <div className="content">
        <div>
          <PlayerInfoCard />
          <PlayerTabs />
        </div>
      </div>
    </AuthProvider>
  );
}

export default App
