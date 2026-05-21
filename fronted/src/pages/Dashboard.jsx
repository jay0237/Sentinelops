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

            console.log(response.data);

        } catch (error) {

            console.log(error);

        }
    };

    return (

        <div style={{ padding: "40px" }}>

            <h1>SentinelOps Dashboard</h1>

            <textarea
                rows="6"
                cols="60"
                placeholder="Enter Prompt...."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
            />

            <br />
            <br />

            <button onClick={scanPrompt}>
                Scan Prompt
            </button>

            {result && (

                <div
                    style={{
                        marginTop: "30px",
                        padding: "20px",
                        border: "1px solid black",
                        borderRadius: "10px",
                        backgroundColor: "#f5f5f5"
                    }}
                >

                    <h2>Scan Result</h2>

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
                        <strong>Alert:</strong> {result.alert}
                    </p>

                </div>

            )}

        </div>
    );
}

export default Dashboard;