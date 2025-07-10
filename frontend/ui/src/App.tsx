import { NavBar } from "./components/NavBar";
import { ChatPane } from "./components/ChatPane";
import { Box } from "@mui/material";
import { PDBViewer } from "./components/PDBViewer";
import { useState } from "react";

function App() {
  const [pdbContent, setPdbContent] = useState<string | null>(null);

  return (
    <div>
      <header>
        <NavBar />
      </header>
      <Box
        sx={{
          padding: "1rem",
          display: "flex",
          height: "calc(100vh - 64px)",
          overflow: "hidden",
        }}
      >
        <Box sx={{ flex: 4, transition: "flex 0.5s ease" }}>
          <ChatPane setPdbContent={setPdbContent} />
        </Box>
        <Box
          sx={{
            flex: pdbContent ? 2 : 0,
            transition: "flex 0.8s ease, opacity 0.8s ease",
            opacity: pdbContent ? 1 : 0,
            paddingLeft: pdbContent ? "1rem" : 0,
            overflow: "hidden",
          }}
        >
          {pdbContent && <PDBViewer pdbData={pdbContent} />}
        </Box>
      </Box>
    </div>
  );
}

export default App;
