import API from "./api";

export const fetchAnalytics = async () => {

    const response = await API.get(
        "/analytics",
        {
            headers:{
                "x-api-key": "sentinelops-secret-key"
            }
        }
    );

    return response.data;
}