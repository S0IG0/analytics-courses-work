import axios from "axios";

const HOST = "localhost"
const HTTP_API = `http://${HOST}/api`

const $api = axios.create({
    baseURL: HTTP_API
});

export default $api;