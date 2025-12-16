import os
from pathlib import Path

# Path: src folder
BASE_DIR = Path("src")

print("🚀 AGENT 50: Writing COMPLETE Dashboard Files (With CSS)...")

if not BASE_DIR.exists():
    print("❌ Error: 'src' folder nahi mila! Sahi folder mein script chalayen.")
    exit()

# ==========================================
# 1. CSS FILE (index.css) - YE MISSING THI!
# ==========================================
css_content = r'''@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  background-color: #030712;
  color: #ffffff;
}
'''

# ==========================================
# 2. MAIN ENTRY (main.tsx)
# ==========================================
main_content = r'''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css' 

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
'''

# ==========================================
# 3. APP (App.tsx)
# ==========================================
app_content = r'''import Dashboard from './pages/Dashboard';

function App() {
  return (
    <Dashboard />
  );
}

export default App;
'''

# ==========================================
# 4. DASHBOARD (With Animations)
# ==========================================
dash_content = r'''import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const Dashboard = () => {
  const [cpu, setCpu] = useState(12);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setCpu(prev => Math.floor(Math.random() * (30 - 10 + 1) + 10));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen p-6 bg-gray-950 text-white">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* HEADER */}
        <header className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600">
              AGENT 50 SUPREME
            </h1>
            <p className="text-gray-400 text-sm tracking-widest mt-1">CLOUD COMMAND CENTER</p>
          </div>
          <div className="flex items-center gap-3">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
            </span>
            <span className="font-mono text-green-400">SYSTEM ACTIVE</span>
          </div>
        </header>

        {/* METRICS */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <motion.div 
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
            className="p-6 rounded-2xl border border-gray-800 bg-gray-900/50 backdrop-blur-xl"
          >
            <h3 className="text-gray-400 text-sm font-mono mb-2">CPU LOAD</h3>
            <div className="flex items-end gap-2">
              <span className="text-5xl font-bold text-blue-400">{cpu}%</span>
            </div>
            <div className="w-full bg-gray-800 h-1 mt-4 rounded-full"><div className="bg-blue-500 h-full transition-all duration-500" style={{ width: `${cpu}%` }}></div></div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
            className="p-6 rounded-2xl border border-gray-800 bg-gray-900/50 backdrop-blur-xl"
          >
            <h3 className="text-gray-400 text-sm font-mono mb-2">MEMORY</h3>
            <div className="flex items-end gap-2">
              <span className="text-5xl font-bold text-purple-400">2.4</span>
              <span className="text-sm text-gray-500 mb-2">GB</span>
            </div>
            <div className="w-full bg-gray-800 h-1 mt-4 rounded-full"><div className="bg-purple-500 h-full" style={{ width: '30%' }}></div></div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
            className="p-6 rounded-2xl border border-gray-800 bg-gray-900/50 backdrop-blur-xl"
          >
            <h3 className="text-gray-400 text-sm font-mono mb-2">STATUS</h3>
            <div className="flex items-end gap-2">
              <span className="text-5xl font-bold text-emerald-400">GOOD</span>
            </div>
            <div className="w-full bg-gray-800 h-1 mt-4 rounded-full"><div className="bg-emerald-500 h-full" style={{ width: '100%' }}></div></div>
          </motion.div>
        </div>

        {/* CONSOLE */}
        <motion.div 
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }}
          className="mt-8 border border-gray-800 rounded-xl overflow-hidden bg-black font-mono text-sm"
        >
          <div className="bg-gray-900/50 px-4 py-2 border-b border-gray-800 text-gray-500 text-xs">agent50-console — bash</div>
          <div className="p-4 text-gray-300 space-y-2 h-48">
            <p>➜ <span className="text-blue-400">~</span> initializing styles...</p>
            <p>➜ <span className="text-blue-400">~</span> applying framer-motion animations...</p>
            <p>➜ <span className="text-blue-400">~</span> system online.</p>
            <p className="animate-pulse">_</p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard;
'''

# FILES MAPPING
files_to_fill = {
    "index.css": css_content, # ✅ YE LINE AB ADD HO GAYI HAI
    "main.tsx": main_content,
    "App.tsx": app_content,
    "pages/Dashboard.tsx": dash_content
}

# WRITE FILES
for path, content in files_to_fill.items():
    full_path = BASE_DIR / path
    if not full_path.parent.exists():
         full_path.parent.mkdir(parents=True, exist_ok=True)
         
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Repaired: {path}")

print("\n🎉 DONE! SERVER RESTART KARNA ZAROORI HAI!")