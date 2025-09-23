import './App.css'
import Navbar from './components/navbar'
import PlayerInfoCard from './components/player-info-card'
import PlayerTabs from './components/player-tabs'

function App() {
  return (
    <>
      <Navbar />
      <div className="content">
        <div>
          <PlayerInfoCard
            name="Lionel Messi"
            club="Inter Miami"
            height="1.70 m"
            foot="Left"
            dob="1987-06-24"
            imageUrl="https://images.playground.com/2e920f23e0764132842b1868477a568c.jpeg"
          />
          <PlayerTabs />
        </div>
      </div>
    </>
  );
}

export default App
