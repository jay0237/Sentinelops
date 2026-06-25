import Dashboard from "./pages/Dashboard";
import { useEffect } from "react";

function App(){

  useEffect(() => {
    // Add smooth scrolling
    document.documentElement.style.scrollBehavior = 'smooth';
  }, []);

  return(
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Dashboard />
    </div>
  );
}

export default App;