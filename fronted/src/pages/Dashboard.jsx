import { useState } from "react";
import API from "../services/api";

function Dashboard() {

    const [prompt, setPrompt] = useState("");
    const [result, setResult] = useState(null);

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

        } catch (error) {

            console.log(error);

        }
    };

    return (

        <div className="min-h-screen bg-slate-900 text-white p-10">

            <h1 className="text-4xl font-bold mb-8">
                SentinelOps Dashboard
            </h1>

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

                        <p>
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

        </div>
    );
}

export default Dashboard;