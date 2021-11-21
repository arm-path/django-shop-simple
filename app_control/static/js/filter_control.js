let id_category = document.getElementById('id_category')
let id_specifications = document.getElementById('id_specification')

id_category.addEventListener('change', (event) => {
    if (id_category.getAttribute('data-action')) {
        url = id_category.getAttribute('data-action')
        url += `?category=${event.target.value}`
        send_on_check(url)
    }
})


// Функция: Отправляет данные на сервер, получает и обрабатывает результаты.
const send_on_check = async (url) => {
    response = await axios.get(url)
    if (response.status === 200) {
        if (response.data.specifications) {
            id_specifications.innerHTML = '<option value="0" selected>-------</option>'
            response.data.specifications.forEach((obj)=>{
                id_specifications.append(new Option(`${obj.title}`, `${obj.slug}`))
            })
        } else {

        }
    } else {
        console.log(response)
    }
}

