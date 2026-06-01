import { useState, useEffect } from "react";

import API from "../services/api";
import { fetchAnalytics } from "../services/analytics";
import { fetchLogs } from "../services/logs";

function Dashboard() {

    const [prompt, setPrompt] = useState("");
    const [result, setResult] = useState(null);

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

    return (

        <div className="min-h-screen bg-slate-900 text-white p-10">

            <h1 className="text-4xl font-bold mb-8">
                SentinelOps Dashboard
            </h1>

            <div className="grid grid-cols-3 gap-4 mb-8">

                <div className="bg-slate-800 p-6 rounded-xl">

                    <h2 className="text-xl font-bold">
                        Threats Blocked
                    </h2>

                    <p className="text-3xl text-red-500 mt-2">
                        {analytics?.blocked_prompts || 0}
                    </p>

                </div>

                <div className="bg-slate-800 p-6 rounded-xl">

                    <h2 className="text-xl font-bold">
                        Safe Prompts
                    </h2>

                    <p className="text-3xl text-green-500 mt-2">
                        {analytics?.safe_prompts || 0}
                    </p>

                </div>

                <div className="bg-slate-800 p-6 rounded-xl">

                    <h2 className="text-xl font-bold">
                        Total Prompts
                    </h2>

                    <p className="text-3xl text-yellow-400 mt-2">
                        {analytics?.total_prompts || 0}
                    </p>

                </div>

            </div>

            <div className="bg-slate-800 p-6 rounded-xl shadow-lg max-w-3xl">

                <textarea
                    rows="6"
                    placeholder="Enter Prompt..."
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    className="w-full p-4 rounded-lg bg-slate-700 text-white border border-slate-600"
                />

                <button
                    onClick={scanPrompt}
                    className="mt-4 bg-red-600 hover:bg-red-700 px-6 py-3 rounded-lg font-semibold"
                >
                    Scan Prompt
                </button>

            </div>

            {result && (

                <div className="mt-10 bg-slate-800 p-6 rounded-xl shadow-lg max-w-3xl">

                    <h2 className="text-2xl font-bold mb-4">
                        Scan Result
                    </h2>

                    <div className="space-y-3">

                        <p>
                            <strong>Safe:</strong> {String(result.safe)}
                        </p>

                        <p className={getThreatColor()}>
                            <strong>Threat Level:</strong> {result.threat_level}
                        </p>

                        <p>
                            <strong>Score:</strong> {result.score}
                        </p>

                        <p>
                            <strong>Reason:</strong> {result.reason}
                        </p>

                        <p>
                            <strong>Recommendation:</strong> {result.recommendation}
                        </p>

                    </div>

                </div>

            )}

            <div className="mt-10">

                <h2 className="text-2xl font-bold mb-4">
                    Threat Logs
                </h2>

                <div className="overflow-x-auto">

                    <table className="w-full bg-slate-800 rounded-xl overflow-hidden">

                        <thead className="bg-slate-700">

                            <tr>

                                <th className="p-4 text-left">
                                    Prompt
                                </th>

                                <th className="p-4 text-left">
                                    Status
                                </th>

                                <th className="p-4 text-left">
                                    Reason
                                </th>

                            </tr>

                        </thead>

                        <tbody>

                            {logs.map((log) => (

                                <tr
                                    key={log.id}
                                    className="border-t border-slate-700"
                                >

                                    <td className="p-4">
                                        {log.prompt}
                                    </td>

                                    <td className="p-4">
                                        {log.status}
                                    </td>

                                    <td className="p-4">
                                        {log.reason}
                                    </td>

                                </tr>

                            ))}

                        </tbody>

                    </table>

                </div>

            </div>

        </div>
    );
}

<div className="mb-8 bg-gradient-to-r from-slate-800 to-slate-700 p-6 rounded-2xl shadow-xl">
    <h2 className="text-3xl font-bold mb-2">
        SeninelOps Security Center
    </h2>

    <p className="text-green-400 font-semibold">
        System Status: SECURE
    </p>

    <div className="grid grid-cols-3 gap-4 mt-4">
        <div className="bg-slate-900 p-4 rounded-lg">
            <p className="text-gray-400">Requests</p>
            <h3 className="text-2xl font-bold">
                {analytics?.total_prompts || 0}
            </h3>
        </div>

        <div className="bg-slate-900 p-4 rounded-lg">
            <p className="text-gray-400">Blocked</p>
            <h3 className="text-2xl font-bold text-red-500">
                {analytics?.blocked_prompts || 0}
            </h3>
        </div>

        <div className="bg-slate-900 p-4 rounded-lg">
            <p className="text-gray-400">High Threats</p>
            <h3 className="text-2xl font-bold text-yellow-400">
                {analytics?.high_threats || 0}
            </h3>
        </div>
    </div>
</div>


export default Dashboard;