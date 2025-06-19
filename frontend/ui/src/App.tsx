import { NavBar } from "./components/NavBar";
import { ChatPane } from "./components/ChatPane";

function App() {
  return (
    <div>
      <header>
        <NavBar />
      </header>
      <div style={{ padding: "1rem" }}>
        <ChatPane />
      </div>
    </div>
  );
}

export default App;
