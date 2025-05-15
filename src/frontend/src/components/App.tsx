import React from "react";
import { AgentPreview } from "./agents/AgentPreview";
import { ThemeProvider } from "./core/theme/ThemeProvider";

const App: React.FC = () => {
  // Sample agent details - in a real application, this would come from an API
  const mockAgentDetails = {
    id: "sample-agent-1",
    name: "Sample AI Agent",
    description: "A helpful AI assistant",
    logo: "Avatar_Default.svg",
  };

  return (
    <ThemeProvider>
      <div className="app-container">
        <AgentPreview
          resourceId="sample-resource-id"
          agentDetails={mockAgentDetails}
        />
      </div>
    </ThemeProvider>
  );
};

export default App;
