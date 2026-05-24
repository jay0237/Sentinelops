import API from "./api";

export const fetchAnalytics = async () => {

    const response = await API.get(
        "/analytics",
        {
            headers:{
                "x-api-key": "Sentinelops-secret-key"
            }
        }
    );

    return response.data;
}