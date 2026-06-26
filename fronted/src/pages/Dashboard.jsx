import { useState, useEffect } from "react";

import API from "../services/api";
import { fetchAnalytics } from "../services/analytics";
import { fetchLogs } from "../services/logs";

function Dashboard({ theme, setTheme }) {

    const [prompt, setPrompt] = useState("");
    const [result, setResult] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [fileResult, setFileResult] = useState(null);


    const [analytics, setAnalytics] = useState(null);

    const [logs, setLogs] = useState([]);

    const isDark = theme === "dark";

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

    const cardBaseClass = isDark
        ? "bg-gradient-to-br from-slate-800 to-slate-750 border border-slate-700"
        : "bg-white border border-slate-200";

    const panelClass = isDark
        ? "bg-slate-900 border-l-4 border-cyan-500"
        : "bg-slate-50 border-l-4 border-cyan-600";

    const headingTextClass = isDark ? "text-white" : "text-slate-900";
    const mutedTextClass = isDark ? "text-slate-400" : "text-slate-600";
    const tableMutedClass = isDark ? "text-slate-300" : "text-slate-700";
    const tableDividerClass = isDark ? "divide-slate-700" : "divide-slate-200";
    const tableRowHoverClass = isDark ? "hover:bg-slate-700/50" : "hover:bg-slate-50";
    const sectionBorderClass = isDark ? "border-slate-700" : "border-slate-200";

    const toggleTheme = () => {
        setTheme((current) => (current === "dark" ? "light" : "dark"));
    };

    return (

        <div className={
            isDark
                ? "min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white"
                : "min-h-screen bg-gradient-to-br from-slate-100 via-sky-50 to-white text-slate-900"
        }>

            <div className={`p-8 border-b ${sectionBorderClass}`}>
                <div className="flex flex-wrap items-start justify-between gap-4">
                    <div>
                        <h1 className="text-5xl font-bold bg-gradient-to-r from-cyan-500 to-blue-600 bg-clip-text text-transparent">
                            SentinelOps
                        </h1>
                        <p className={`${mutedTextClass} mt-2`}>AI Prompt Security & Threat Detection</p>
                    </div>

                    <button
                        onClick={toggleTheme}
                        className={
                            isDark
                                ? "px-4 py-2 rounded-lg font-semibold bg-slate-700 text-slate-100 border border-slate-600 hover:bg-slate-600 transition-colors"
                                : "px-4 py-2 rounded-lg font-semibold bg-white text-slate-900 border border-slate-300 hover:bg-slate-100 transition-colors"
                        }
                    >
                        {isDark ? "Switch to Light" : "Switch to Dark"}
                    </button>
                </div>
            </div>

            <div className="p-8">

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">

                    <div className={
                        isDark
                            ? "bg-gradient-to-br from-red-900/30 to-red-800/10 border border-red-700/50 p-6 rounded-2xl hover:shadow-lg hover:shadow-red-500/20 transition-all"
                            : "bg-gradient-to-br from-red-100 to-red-50 border border-red-200 p-6 rounded-2xl hover:shadow-lg hover:shadow-red-200 transition-all"
                    }>
                        <div className="flex items-center justify-between">
                            <div>
                                <h2 className={`${isDark ? "text-slate-300" : "text-slate-700"} font-semibold mb-2`}>Threats Blocked</h2>
                                <p className="text-4xl font-bold text-red-400">
                                    {analytics?.blocked_prompts || 0}
                                </p>
                            </div>
                            <div className="text-5xl opacity-30">⚠</div>
                        </div>
                    </div>

                    <div className={
                        isDark
                            ? "bg-gradient-to-br from-green-900/30 to-green-800/10 border border-green-700/50 p-6 rounded-2xl hover:shadow-lg hover:shadow-green-500/20 transition-all"
                            : "bg-gradient-to-br from-green-100 to-green-50 border border-green-200 p-6 rounded-2xl hover:shadow-lg hover:shadow-green-200 transition-all"
                    }>
                        <div className="flex items-center justify-between">
                            <div>
                                <h2 className={`${isDark ? "text-slate-300" : "text-slate-700"} font-semibold mb-2`}>Safe Prompts</h2>
                                <p className="text-4xl font-bold text-green-400">
                                    {analytics?.safe_prompts || 0}
                                </p>
                            </div>
                            <div className="text-5xl opacity-30">OK</div>
                        </div>
                    </div>

                    <div className={
                        isDark
                            ? "bg-gradient-to-br from-blue-900/30 to-blue-800/10 border border-blue-700/50 p-6 rounded-2xl hover:shadow-lg hover:shadow-blue-500/20 transition-all"
                            : "bg-gradient-to-br from-blue-100 to-blue-50 border border-blue-200 p-6 rounded-2xl hover:shadow-lg hover:shadow-blue-200 transition-all"
                    }>
                        <div className="flex items-center justify-between">
                            <div>
                                <h2 className={`${isDark ? "text-slate-300" : "text-slate-700"} font-semibold mb-2`}>Total Scanned</h2>
                                <p className="text-4xl font-bold text-blue-400">
                                    {analytics?.total_prompts || 0}
                                </p>
                            </div>
                            <div className="text-5xl opacity-30">#</div>
                        </div>
                    </div>

                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-10">

                    <div className={`lg:col-span-2 p-8 rounded-2xl shadow-xl ${cardBaseClass}`}>
                        <h2 className={`text-2xl font-bold mb-6 flex items-center gap-3 ${headingTextClass}`}>
                            <span>Scan Prompt</span>
                        </h2>
                        
                        <textarea
                            rows="6"
                            placeholder="Enter your AI prompt here to scan for security threats..."
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                            className={
                                isDark
                                    ? "w-full p-4 rounded-lg bg-slate-900 text-white border border-slate-600 focus:border-cyan-500 focus:outline-none transition-colors placeholder-slate-500"
                                    : "w-full p-4 rounded-lg bg-white text-slate-900 border border-slate-300 focus:border-cyan-600 focus:outline-none transition-colors placeholder-slate-500"
                            }
                        />

                        <button
                            onClick={scanPrompt}
                            className="mt-6 w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 px-8 py-3 rounded-lg font-semibold text-lg transition-all transform hover:scale-105 shadow-lg"
                        >
                            Scan for Threats
                        </button>
                    </div>

                    <div className={`p-8 rounded-2xl shadow-xl ${cardBaseClass}`}>
                        <h2 className={`text-2xl font-bold mb-6 flex items-center gap-3 ${headingTextClass}`}>
                            <span>File Scan</span>
                        </h2>

                        <div className={
                            isDark
                                ? "border-2 border-dashed border-slate-600 rounded-lg p-6 text-center hover:border-cyan-500 transition-colors mb-4"
                                : "border-2 border-dashed border-slate-300 rounded-lg p-6 text-center hover:border-cyan-600 transition-colors mb-4"
                        }>
                            <input
                                type="file"
                                onChange={(e) => setSelectedFile(e.target.files[0])}
                                className="hidden" 
                                id="file-input"
                            />
                            <label htmlFor="file-input" className="cursor-pointer block">
                                <p className="text-2xl mb-2">File</p>
                                <p className={tableMutedClass}>Click or drag file</p>
                                <p className={`text-xs mt-1 ${mutedTextClass}`}>{selectedFile?.name || "No file selected"}</p>
                            </label>
                        </div>

                        <button
                            onClick={scanFile}
                            disabled={!selectedFile}
                            className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 disabled:from-slate-600 disabled:to-slate-700 disabled:cursor-not-allowed px-8 py-3 rounded-lg font-semibold text-lg transition-all transform hover:scale-105 shadow-lg"
                        >
                            Analyze File
                        </button>
                    </div>

                </div>

            {fileResult && (

                (() => {
                    const scanResult = fileResult.result || fileResult.scan_result;
                    const isThreatenening = scanResult.threat_level === "high" || scanResult.threat_level === "critical";

                    return (

                <div className={`p-8 rounded-2xl shadow-xl mb-8 ${cardBaseClass}`}>

                    <h2 className={`text-2xl font-bold mb-6 flex items-center gap-3 ${headingTextClass}`}>
                        <span>File Scan Result</span>
                    </h2>

                    <div className={`${panelClass} p-6 rounded-lg space-y-4`}>
                        <div className="flex items-center justify-between">
                            <p className={tableMutedClass}><strong>File:</strong></p>
                            <p className="font-mono text-cyan-400 text-sm">{fileResult.filename}</p>
                        </div>

                        <div className="flex items-center justify-between">
                            <p className={tableMutedClass}><strong>Threat Level:</strong></p>
                            <p className={`font-bold text-lg ${isThreatenening ? 'text-red-400' : 'text-green-400'}`}>
                                {scanResult.threat_level?.toUpperCase()}
                            </p>
                        </div>

                        <div className="flex items-center justify-between">
                            <p className={tableMutedClass}><strong>Status:</strong></p>
                            <p className={`font-semibold ${isThreatenening ? 'text-red-400' : 'text-green-400'}`}>
                                {isThreatenening ? "THREAT DETECTED" : "SAFE"}
                            </p>
                        </div>

                        <div className={`pt-4 border-t ${sectionBorderClass}`}>
                            <p className={tableMutedClass}><strong>Reason:</strong></p>
                            <p className={`${mutedTextClass} mt-2`}>{scanResult.reason}</p>
                        </div>
                    </div>

                </div>

                    );
                })()

            )}

            {result && (        

                <div className={`p-8 rounded-2xl shadow-xl mb-8 ${cardBaseClass}`}>

                    <h2 className={`text-2xl font-bold mb-6 flex items-center gap-3 ${headingTextClass}`}>
                        <span>Scan Result</span>
                    </h2>

                    <div className={`${panelClass} p-6 rounded-lg space-y-4`}>

                        <div className="flex items-center justify-between">
                            <p className={tableMutedClass}><strong>Status:</strong></p>
                            <p className={`px-4 py-1 rounded-full font-semibold ${result.safe ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                                {result.safe ? "SAFE" : "THREAT"}
                            </p>
                        </div>

                        <div className="flex items-center justify-between">
                            <p className={tableMutedClass}><strong>Threat Level:</strong></p>
                            <p className={`${getThreatColor()} font-semibold text-lg`}>
                                {result.threat_level?.toUpperCase() || 'N/A'}
                            </p>
                        </div>

                        {result.score && (
                            <div className="flex items-center justify-between">
                                <p className={tableMutedClass}><strong>Risk Score:</strong></p>
                                <div className={
                                    isDark
                                        ? "w-32 h-2 bg-slate-700 rounded-full overflow-hidden"
                                        : "w-32 h-2 bg-slate-300 rounded-full overflow-hidden"
                                }>
                                    <div className={`h-full ${result.score > 0.7 ? 'bg-red-500' : result.score > 0.4 ? 'bg-yellow-500' : 'bg-green-500'}`} 
                                         style={{width: `${result.score * 100}%`}}></div>
                                </div>
                            </div>
                        )}

                        <div className={`pt-4 border-t ${sectionBorderClass}`}>
                            <p className={tableMutedClass}><strong>Reason:</strong></p>
                            <p className={`${mutedTextClass} mt-2`}>{result.reason}</p>
                        </div>

                        {result.recommendation && (
                            <div className={`pt-4 border-t ${sectionBorderClass}`}>
                                <p className={tableMutedClass}><strong>Recommendation:</strong></p>
                                <p className={`${mutedTextClass} mt-2`}>{result.recommendation}</p>
                            </div>
                        )}

                    </div>

                </div>

            )}

            <div className={`p-8 rounded-2xl shadow-xl ${cardBaseClass}`}>

                <h2 className={`text-2xl font-bold mb-6 flex items-center gap-3 ${headingTextClass}`}>
                    <span>Recent Threat Logs</span>
                </h2>

                <div className="overflow-x-auto">

                    <table className="w-full">

                        <thead>

                            <tr className={`border-b-2 ${sectionBorderClass}`}>

                                <th className={`p-4 text-left font-semibold ${tableMutedClass}`}>
                                    Prompt
                                </th>

                                <th className={`p-4 text-left font-semibold ${tableMutedClass}`}>
                                    Status
                                </th>

                                <th className={`p-4 text-left font-semibold ${tableMutedClass}`}>
                                    Reason
                                </th>

                            </tr>

                        </thead>

                        <tbody className={`divide-y ${tableDividerClass}`}>

                            {logs && logs.length > 0 ? (
                                logs.map((log) => (

                                    <tr
                                        key={log.id}
                                        className={`${tableRowHoverClass} transition-colors`}
                                    >

                                        <td className={`p-4 truncate max-w-xs ${tableMutedClass}`}>
                                            {log.prompt}
                                        </td>

                                        <td className="p-4">
                                            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                                                log.status === 'blocked' ? 'bg-red-500/20 text-red-500' : 'bg-green-500/20 text-green-600'
                                            }`}>
                                                {log.status === 'blocked' ? 'Blocked' : 'Safe'}
                                            </span>
                                        </td>

                                        <td className={`p-4 ${tableMutedClass}`}>
                                            {log.reason}
                                        </td>

                                    </tr>

                                ))
                            ) : (
                                <tr>
                                    <td colSpan="3" className={`p-8 text-center ${mutedTextClass}`}>
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