let data = {}, response, response_filter_one,
    url = window.location.pathname,
    form_filter = document.getElementById('form_filter'),
    error_filter = document.getElementById('error_filter'),
    tbody_filter = document.getElementById('tbody_filter')

// Функция: создает фильтр.
form_filter.addEventListener('submit', (event) => {
    event.preventDefault()
    let id_lessOrEqual = document.getElementById('id_lessOrEqual'),
        id_moreOrEqual = document.getElementById('id_moreOrEqual')
    if ((!isNaN(id_lessOrEqual.value) || id_lessOrEqual.value === '') && (!isNaN(id_moreOrEqual.value) || id_moreOrEqual.value === '')) {
        if (id_lessOrEqual.value === '' && id_moreOrEqual.value === '') {
            error_filter.classList.add('alert', 'alert-danger', 'text-center')
            error_filter.textContent = 'Должно быть заполнено по крайне мере одно поле!'
        } else {
            error_filter.classList.remove('alert', 'alert-danger', 'text-center')
            error_filter.textContent = ''
            data = {'type': 'create_filter', 'lessOrEqual': id_lessOrEqual.value, 'moreOrEqual': id_moreOrEqual.value}
            send_on_check(url, data, error_filter)
        }
    } else {
        error_filter.classList.add('alert', 'alert-danger', 'text-center')
        error_filter.textContent = 'Поля должны содержать число!'
    }
})

// Функция: Создает элемент таблицы для фильтра.
let create_tbody_element = (obj_td1, obj_td2, obj_td3) => {
    let row = document.createElement('TR'),
        td1 = document.createElement('TD'),
        td2 = document.createElement('TD'),
        td3 = document.createElement('TD')

    td1.appendChild(document.createTextNode(obj_td1))
    td2.appendChild(document.createTextNode(obj_td2))
    row.id = `tr_filter_${obj_td3}`
    td3.innerHTML = ` <form data-delete="${obj_td3}" action="" method="POST"> <button type="submit" class="btn btn-danger">
                      <i class="bi bi-trash"></i></button></form>`
    row.classList.add('text-center')
    row.appendChild(td1)
    row.appendChild(td2)
    row.appendChild(td3)
    tbody_filter.appendChild(row)
}

// Функция: Удаляет фильтр.
tbody_filter.addEventListener('submit', (event) => {
    event.preventDefault()
    let id_filter = event.target.getAttribute('data-delete')
    if (!isNaN(id_filter)) {
        data = {'type': 'delete_filter', 'pk': id_filter}
        send_on_check(url, data, error_filter)
    }
})

// Функция: Отправляет данные на сервер, получает и обрабатывает результаты.
const send_on_check = async (url, data, error_filter) => {
    try {
        axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
        axios.defaults.xsrfCookieName = 'csrftoken'
        response = await axios.post(url, data)
        if (response.status === 200) {
            if (response.data.errors) {
                error_filter.classList.add('alert', 'alert-danger', 'text-center')
                if (response.data.errors.__all__) {
                    response.data.errors.__all__.forEach((obj) => {
                        error_filter.innerHTML += `<div>${obj}</div>`
                    })
                } else console.log(reponse.data.errors)
            } else {
                error_filter.classList.remove('alert', 'alert-danger', 'text-center')
            }
            if (response.data.create_filter) {
                response_filter = response.data.create_filter
                create_tbody_element(response_filter.lessOrEqual, response_filter.moreOrEqual, response_filter.id)
                document.getElementById('id_lessOrEqual').value = ''
                document.getElementById('id_moreOrEqual').value = ''
            }

            if (response.data.delete_filter) {
                tbody_filter.removeChild(document.getElementById(`tr_filter_${response.data.delete_filter}`))
            }

        } else {
            console.log(response.status)
        }
    } catch (e) {
        console.log(e)
    }

}