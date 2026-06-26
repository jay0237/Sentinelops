import Dashboard from "./pages/Dashboard";
import { useEffect, useState } from "react";

function App(){
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem("theme");
    return savedTheme === "light" ? "light" : "dark";
  });

  useEffect(() => {
    document.documentElement.style.scrollBehavior = "smooth";
  }, []);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, []);

  return(
    <div className={
      theme === "dark"
        ? "min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900"
        : "min-h-screen bg-gradient-to-br from-slate-100 via-sky-50 to-white"
    }>
      <Dashboard theme={theme} setTheme={setTheme} />
    </div>
  );
}

export default App;