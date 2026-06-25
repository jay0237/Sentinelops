import { useState, useEffect } from "react";

import API from "../services/api";
import { fetchAnalytics } from "../services/analytics";
import { fetchLogs } from "../services/logs";

function Dashboard() {

    const [prompt, setPrompt] = useState("");
    const [result, setResult] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [fileResult, setFileResult] = useState(null);


    const [analytics, setAnalytics] = useState(null);

    const [logs, setLogs] = useState([]);

    const getThreatColor = () => {

        if (!result) return "";

        if (result.threat_level === "high") {
            return "text-red-500";
        }

        if (result.threat_level === "medium") {
            return "text-yellow-400";
        }

        return "text-green-400";
    };

    const scanPrompt = async () => {

        try {

            const response = await API.post(
                "/scan",
                {
                    text: prompt
                },
                {
                    headers: {
                        "x-api-key": "sentinelops-secret-key"
                    }
                }
            );

            setResult(response.data);

            loadAnalytics();
            loadLogs();

        } catch (error) {

            console.log(error);

        }
    };

    useEffect(() => {

        loadAnalytics();
        loadLogs();

    }, []);

    const loadAnalytics = async () => {

        try {

            const data = await fetchAnalytics();

            setAnalytics(data);

        } catch (error) {

            console.log(error);

        }
    };

    const loadLogs = async () => {

        try {

            const data = await fetchLogs();

            setLogs(data);

        } catch (error) {

            console.log(error);

        }
    };

    const scanFile = async () => {

        if (!selectedFile) return;

        const formData = new FormData();

        formData.append("file", selectedFile);

        try {

            const response = await API.post(
                "/scan-file",
                formData,
                {
                    headers: {
                        "x-api-key": "sentinelops-secret-key"
                    }
                }
            );

            setFileResult(response.data);

        } catch (error) {

            console.log(error);

        }
    };

    return (

        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">

            <div className="p-8 border-b border-slate-700">
                <h1 className="text-5xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                    🛡️ SentinelOps
                </h1>
                <p className="text-slate-400 mt-2">AI Prompt Security & Threat Detection</p>
            </div>

            <div className="p-8">

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">

                    <div className="bg-gradient-to-br from-red-900/30 to-red-800/10 border border-red-700/50 p-6 rounded-2xl hover:shadow-lg hover:shadow-red-500/20 transition-all">
                        <div className="flex items-center justify-between">
                            <div>
                                <h2 className="text-slate-300 font-semibold mb-2">Threats Blocked</h2>
                                <p className="text-4xl font-bold text-red-400">
                                    {analytics?.blocked_prompts || 0}
                                </p>
                            </div>
                            <div className="text-5xl opacity-20">⚠️</div>
                        </div>
                    </div>

                    <div className="bg-gradient-to-br from-green-900/30 to-green-800/10 border border-green-700/50 p-6 rounded-2xl hover:shadow-lg hover:shadow-green-500/20 transition-all">
                        <div className="flex items-center justify-between">
                            <div>
                                <h2 className="text-slate-300 font-semibold mb-2">Safe Prompts</h2>
                                <p className="text-4xl font-bold text-green-400">
                                    {analytics?.safe_prompts || 0}
                                </p>
                            </div>
                            <div className="text-5xl opacity-20">✅</div>
                        </div>
                    </div>

                    <div className="bg-gradient-to-br from-blue-900/30 to-blue-800/10 border border-blue-700/50 p-6 rounded-2xl hover:shadow-lg hover:shadow-blue-500/20 transition-all">
                        <div className="flex items-center justify-between">
                            <div>
                                <h2 className="text-slate-300 font-semibold mb-2">Total Scanned</h2>
                                <p className="text-4xl font-bold text-blue-400">
                                    {analytics?.total_prompts || 0}
                                </p>
                            </div>
                            <div className="text-5xl opacity-20">📊</div>
                        </div>
                    </div>

                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-10">

                    <div className="lg:col-span-2 bg-gradient-to-br from-slate-800 to-slate-750 border border-slate-700 p-8 rounded-2xl shadow-xl">
                        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
                            <span>🔍</span> Scan Prompt
                        </h2>
                        
                        <textarea
                            rows="6"
                            placeholder="Enter your AI prompt here to scan for security threats..."
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                            className="w-full p-4 rounded-lg bg-slate-900 text-white border border-slate-600 focus:border-cyan-500 focus:outline-none transition-colors placeholder-slate-500"
                        />

                        <button
                            onClick={scanPrompt}
                            className="mt-6 w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 px-8 py-3 rounded-lg font-semibold text-lg transition-all transform hover:scale-105 shadow-lg"
                        >
                            🛡️ Scan for Threats
                        </button>
                    </div>

                    <div className="bg-gradient-to-br from-slate-800 to-slate-750 border border-slate-700 p-8 rounded-2xl shadow-xl">
                        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
                            <span>📁</span> File Scan
                        </h2>

                        <div className="border-2 border-dashed border-slate-600 rounded-lg p-6 text-center hover:border-cyan-500 transition-colors mb-4">
                            <input
                                type="file"
                                onChange={(e) => setSelectedFile(e.target.files[0])}
                                className="hidden" 
                                id="file-input"
                            />
                            <label htmlFor="file-input" className="cursor-pointer block">
                                <p className="text-2xl mb-2">📄</p>
                                <p className="text-slate-300">Click or drag file</p>
                                <p className="text-xs text-slate-500 mt-1">{selectedFile?.name || 'No file selected'}</p>
                            </label>
                        </div>

                        <button
                            onClick={scanFile}
                            disabled={!selectedFile}
                            className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 disabled:from-slate-600 disabled:to-slate-700 disabled:cursor-not-allowed px-8 py-3 rounded-lg font-semibold text-lg transition-all transform hover:scale-105 shadow-lg"
                        >
                            📊 Analyze File
                        </button>
                    </div>

                </div>

            {fileResult && (

                (() => {
                    const scanResult = fileResult.result || fileResult.scan_result;
                    const isThreatenening = scanResult.threat_level === "high" || scanResult.threat_level === "critical";

                    return (

                <div className="bg-gradient-to-br from-slate-800 to-slate-750 border border-slate-700 p-8 rounded-2xl shadow-xl mb-8">

                    <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
                        <span>📄</span> File Scan Result
                    </h2>

                    <div className="bg-slate-900 p-6 rounded-lg space-y-4 border-l-4 border-cyan-500">
                        <div className="flex items-center justify-between">
                            <p className="text-slate-300"><strong>File:</strong></p>
                            <p className="font-mono text-cyan-400 text-sm">{fileResult.filename}</p>
                        </div>

                        <div className="flex items-center justify-between">
                            <p className="text-slate-300"><strong>Threat Level:</strong></p>
                            <p className={`font-bold text-lg ${isThreatenening ? 'text-red-400' : 'text-green-400'}`}>
                                {scanResult.threat_level?.toUpperCase()}
                            </p>
                        </div>

                        <div className="flex items-center justify-between">
                            <p className="text-slate-300"><strong>Status:</strong></p>
                            <p className={`font-semibold ${isThreatenening ? 'text-red-400' : 'text-green-400'}`}>
                                {isThreatenening ? '🚨 THREAT DETECTED' : '✅ SAFE'}
                            </p>
                        </div>

                        <div className="pt-4 border-t border-slate-700">
                            <p className="text-slate-300"><strong>Reason:</strong></p>
                            <p className="text-slate-400 mt-2">{scanResult.reason}</p>
                        </div>
                    </div>

                </div>

                    );
                })()

            )}

            {result && (        

                <div className="bg-gradient-to-br from-slate-800 to-slate-750 border border-slate-700 p-8 rounded-2xl shadow-xl mb-8">

                    <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
                        <span>📋</span> Scan Result
                    </h2>

                    <div className="bg-slate-900 p-6 rounded-lg space-y-4 border-l-4 border-cyan-500">

                        <div className="flex items-center justify-between">
                            <p className="text-slate-300"><strong>Status:</strong></p>
                            <p className={`px-4 py-1 rounded-full font-semibold ${result.safe ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                                {result.safe ? '✅ SAFE' : '⚠️ THREAT'}
                            </p>
                        </div>

                        <div className="flex items-center justify-between">
                            <p className="text-slate-300"><strong>Threat Level:</strong></p>
                            <p className={`${getThreatColor()} font-semibold text-lg`}>
                                {result.threat_level?.toUpperCase() || 'N/A'}
                            </p>
                        </div>

                        {result.score && (
                            <div className="flex items-center justify-between">
                                <p className="text-slate-300"><strong>Risk Score:</strong></p>
                                <div className="w-32 h-2 bg-slate-700 rounded-full overflow-hidden">
                                    <div className={`h-full ${result.score > 0.7 ? 'bg-red-500' : result.score > 0.4 ? 'bg-yellow-500' : 'bg-green-500'}`} 
                                         style={{width: `${result.score * 100}%`}}></div>
                                </div>
                            </div>
                        )}

                        <div className="pt-4 border-t border-slate-700">
                            <p className="text-slate-300"><strong>Reason:</strong></p>
                            <p className="text-slate-400 mt-2">{result.reason}</p>
                        </div>

                        {result.recommendation && (
                            <div className="pt-4 border-t border-slate-700">
                                <p className="text-slate-300"><strong>Recommendation:</strong></p>
                                <p className="text-slate-400 mt-2">{result.recommendation}</p>
                            </div>
                        )}

                    </div>

                </div>

            )}

            <div className="bg-gradient-to-br from-slate-800 to-slate-750 border border-slate-700 p-8 rounded-2xl shadow-xl">

                <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
                    <span>📋</span> Recent Threat Logs
                </h2>

                <div className="overflow-x-auto">

                    <table className="w-full">

                        <thead>

                            <tr className="border-b-2 border-slate-700">

                                <th className="p-4 text-left text-slate-300 font-semibold">
                                    Prompt
                                </th>

                                <th className="p-4 text-left text-slate-300 font-semibold">
                                    Status
                                </th>

                                <th className="p-4 text-left text-slate-300 font-semibold">
                                    Reason
                                </th>

                            </tr>

                        </thead>

                        <tbody className="divide-y divide-slate-700">

                            {logs && logs.length > 0 ? (
                                logs.map((log) => (

                                    <tr
                                        key={log.id}
                                        className="hover:bg-slate-700/50 transition-colors"
                                    >

                                        <td className="p-4 text-slate-300 truncate max-w-xs">
                                            {log.prompt}
                                        </td>

                                        <td className="p-4">
                                            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                                                log.status === 'blocked' ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'
                                            }`}>
                                                {log.status === 'blocked' ? '🚨 Blocked' : '✅ Safe'}
                                            </span>
                                        </td>

                                        <td className="p-4 text-slate-300">
                                            {log.reason}
                                        </td>

                                    </tr>

                                ))
                            ) : (
                                <tr>
                                    <td colSpan="3" className="p-8 text-center text-slate-400">
                                        No logs yet. Scan a prompt to get started.
                                    </td>
                                </tr>
                            )}

                        </tbody>

                    </table>

                </div>

            </div>

        </div>
    );
}

export default Dashboard;