import os
from pathlib import Path

# Path: src folder
BASE_DIR = Path("src")

print("🔗 AGENT 50: Connecting Brain to Dashboard...")

if not BASE_DIR.exists():
    print("❌ Error: 'src' folder nahi mila! 'agent 50-console' mein run karein.")
    exit()

# ==========================================
# REAL DASHBOARD (Connects to Port 5000)
# ==========================================
dash_content = r'''import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const Dashboard = () => {
  const [stats, setStats] = useState({
    cpu: 0,
    memory: 0,
    status: 'CONNECTING...',
    projects: 0
  });
  
  const [logs, setLogs] = useState<string[]>([]);

  const addLog = (msg: string) => {
    setLogs(prev => [`> ${msg}`, ...prev].slice(0, 5));
  };

  // Connect to Backend (Brain)
  useEffect(() => {
    addLog("Initializing connection to Neural Core...");
    
    const fetchData = async () => {
      try {
        // Asli Backend se baat karein
        const res = await fetch('http://localhost:5000/api/v1/system/status');
        const data = await res.json();
        
        if (data.status === 'success') {
          setStats({
            cpu: data.system.cpu_percentage || 15,
            memory: data.system.memory_usage_mb || 1024,
            status: 'ONLINE',
            projects: data.system.active_projects || 3
          });
        }
      } catch (error) {
        // Agar Backend band ho
        console.error("Brain Connection Failed", error);
        setStats(prev => ({...prev, status: 'OFFLINE (Brain Missing)'}));
      }
    };

    // Har 2 second mein data update karein
    fetchData();
    const interval = setInterval(fetchData, 2000);
    
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen p-6 bg-gray-950 text-white font-sans">
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
            <span className={`relative flex h-3 w-3`}>
              <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${stats.status.includes('ONLINE') ? 'bg-green-400' : 'bg-red-400'}`}></span>
              <span className={`relative inline-flex rounded-full h-3 w-3 ${stats.status.includes('ONLINE') ? 'bg-green-500' : 'bg-red-500'}`}></span>
            </span>
            <span className={`font-mono ${stats.status.includes('ONLINE') ? 'text-green-400' : 'text-red-400'}`}>
              SYSTEM {stats.status}
            </span>
          </div>
        </header>

        {/* METRICS */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* CPU Card */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="p-6 rounded-2xl border border-gray-800 bg-gray-900/50 backdrop-blur-xl">
            <h3 className="text-gray-400 text-sm font-mono mb-2">CPU LOAD</h3>
            <div className="flex items-end gap-2">
              <span className="text-5xl font-bold text-blue-400">{stats.cpu}%</span>
            </div>
            <div className="w-full bg-gray-800 h-1 mt-4 rounded-full">
              <div className="bg-blue-500 h-full transition-all duration-500" style={{ width: `${stats.cpu}%` }}></div>
            </div>
          </motion.div>

          {/* Memory Card */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="p-6 rounded-2xl border border-gray-800 bg-gray-900/50 backdrop-blur-xl">
            <h3 className="text-gray-400 text-sm font-mono mb-2">MEMORY</h3>
            <div className="flex items-end gap-2">
              <span className="text-5xl font-bold text-purple-400">{stats.memory}</span>
              <span className="text-sm text-gray-500 mb-2">MB</span>
            </div>
            <div className="w-full bg-gray-800 h-1 mt-4 rounded-full">
              <div className="bg-purple-500 h-full" style={{ width: '40%' }}></div>
            </div>
          </motion.div>

          {/* Projects Card */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="p-6 rounded-2xl border border-gray-800 bg-gray-900/50 backdrop-blur-xl">
            <h3 className="text-gray-400 text-sm font-mono mb-2">ACTIVE PROJECTS</h3>
            <div className="flex items-end gap-2">
              <span className="text-5xl font-bold text-emerald-400">{stats.projects}</span>
            </div>
            <div className="w-full bg-gray-800 h-1 mt-4 rounded-full">
              <div className="bg-emerald-500 h-full" style={{ width: '100%' }}></div>
            </div>
          </motion.div>
        </div>

        {/* CONSOLE LOGS */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }} className="mt-8 border border-gray-800 rounded-xl overflow-hidden bg-black font-mono text-sm">
          <div className="bg-gray-900/50 px-4 py-2 border-b border-gray-800 text-gray-500 text-xs">agent50-console — live-connection</div>
          <div className="p-4 text-gray-300 space-y-2 h-48 overflow-hidden">
            {logs.map((log, i) => (
              <p key={i} className="animate-fade-in"><span className="text-green-400">➜</span> {log}</p>
            ))}
            <p className="animate-pulse">_</p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard;
'''

# WRITE FILE
file_path = BASE_DIR / "pages/Dashboard.tsx"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(dash_content)

print(f"✅ CONNECTED! Dashboard ab Port 5000 se baat karega.")