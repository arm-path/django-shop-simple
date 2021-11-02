let create_specification = document.getElementById('create_specification')

create_specification.addEventListener('click', () => {
    let id_form_specification = document.getElementById('id_form_specification')
    id_form_specification.addEventListener('submit', event => {
        event.preventDefault()
        let title = document.getElementById('id_title_specification'),
            unit = document.getElementById('id_unit'),
            use_filters = document.getElementById('id_use_filters'),
            type_filter = document.getElementById('id_type_filter'),
            category = document.getElementById('id_category_specification')
        let data = {}
        data.title = title.value
        data.unit = unit.value
        data.use_filters = use_filters.checked
        data.type_filter = type_filter.value
        data.category = category.value
        send_on_check(data)
    })
})

// Функция передачи данных на сервер.
const send_on_check = async data => {
    try {
        // Определение данных для передачи на червер через axios.
        const url = `/specification-create/${data.category}/`
        console.log(url)
        axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
        axios.defaults.xsrfCookieName = 'csrftoken'
        let response = await axios.post(url, data)
        console.log(response)
    } catch (e) {
        // Выполнение условия при отрицательном ответе от сервера.
        let error = document.getElementById('responseSRV')
        error.textContent = 'Произошла не предвиденная ошибка, комментарий не был добавлен'
        error.classList.add('text-danger')
    }
}

