import API from "./api"

export const fetchLogs = async () => {

    const response = await API.get(
        "/logs",
        {
            headers: {
                "x-api-key": "sentinelops-secret-key"
            }
        }
    );
    return response.data;
}