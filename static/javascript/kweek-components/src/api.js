import axios from "axios"

const baseURL = location.href.indexOf("localhost") < 0 ? "https://prod.kweek.africa/store/" : "http://localhost:8000/store/";


const api = axios.create({
    baseURL,
});

export default api;
