
async function navigatecq(id) {
    sessionStorage.setItem("qid", id)
    window.location.href = `http://127.0.0.1:8000/getcq/${id}`

}

    async function navigatedq(id) {
        sessionStorage.setItem("qid", id)
            window.location.href = `http://127.0.0.1:8000/getdq/${id}`

}

    async function navigatewq(id) {
        sessionStorage.setItem("qid", id)
            window.location.href = `http://127.0.0.1:8000/getwq/${id}`

        }