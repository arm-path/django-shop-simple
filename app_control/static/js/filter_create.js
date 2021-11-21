let data = {}, response, response_filter_one, response_filter_two,
    url = window.location.pathname,
    form_filter_one = document.getElementById('form_filter_one'),
    error_filter_one = document.getElementById('error_filter_one'),
    tbody_filter_one = document.getElementById('tbody_filter_one'),

    form_filter_two = document.getElementById('form_filter_two'),
    tbody_filter_two = document.getElementById('tbody_filter_two'),
    error_filter_two = document.getElementById('error_filter_two')

// Функция: создает фильтр №1.
form_filter_one.addEventListener('submit', (event) => {
    event.preventDefault()
    let id_lessOrEqual = document.getElementById('id_lessOrEqual'),
        id_moreOrEqual = document.getElementById('id_moreOrEqual')
    if ((!isNaN(id_lessOrEqual.value) || id_lessOrEqual.value === '') && (!isNaN(id_moreOrEqual.value) || id_moreOrEqual.value === '')) {
        if (id_lessOrEqual.value === '' && id_moreOrEqual.value === '') {
            error_filter_one.classList.add('alert', 'alert-danger', 'text-center')
            error_filter_one.textContent = 'Должно быть заполнено по крайне мере одно поле!'
        } else {
            error_filter_one.classList.remove('alert', 'alert-danger', 'text-center')
            error_filter_one.textContent = ''
            data = {'type': 'filter_one', 'lessOrEqual': id_lessOrEqual.value, 'moreOrEqual': id_moreOrEqual.value}
            send_on_check(url, data, error_filter_one)
        }
    } else {
        error_filter_one.classList.add('alert', 'alert-danger', 'text-center')
        error_filter_one.textContent = 'Поля должны содержать число!'
    }
})

// Функция: создает фильтр №2.
form_filter_two.addEventListener('submit', (event) => {
    event.preventDefault()
    let id_from_digit = document.getElementById('id_from_digit'),
        id_before_digit = document.getElementById('id_before_digit')
    if (!isNaN(id_from_digit.value) && !isNaN(id_before_digit.value)) {
        error_filter_two.classList.remove('alert', 'alert-danger', 'text-center')
        error_filter_two.textContent = ''
        data = {'type': 'filter_two', 'from_digit': id_from_digit.value, 'before_digit': id_before_digit.value}
        send_on_check(url, data, error_filter_two)

    } else {
        error_filter_two.classList.add('alert', 'alert-danger', 'text-center')
        error_filter_two.textContent = 'Поля должны содержать число!'
    }
})

// Функция: Создает элемент таблицы для фильтра №1 и фильтра №2
let create_tbody_element = (obj_td1, obj_td2, obj_td3, type) => {
    let row = document.createElement('TR'),
        td1 = document.createElement('TD'),
        td2 = document.createElement('TD'),
        td3 = document.createElement('TD')

    td1.appendChild(document.createTextNode(obj_td1))
    td2.appendChild(document.createTextNode(obj_td2))
    if (type === 'filter_one') {
        row.id = `tr_filter_one_${obj_td3}`
        td3.innerHTML = ` <form data-delete="${obj_td3}" action="" method="POST"> <button type="submit" class="btn btn-danger">
                            <i class="bi bi-trash"></i></button></form>`
    }
    if (type === 'filter_two') {
        row.id = `tr_filter_two_${obj_td3}`
        td3.innerHTML = `<form data-delete="${obj_td3}" action="" method="POST"><button type="submit" class="btn btn-danger">
                            <i class="bi bi-trash"></i></button></form>`
    }

    row.classList.add('text-center')
    row.appendChild(td1)
    row.appendChild(td2)
    row.appendChild(td3)
    if (type === 'filter_one') {
        tbody_filter_one.appendChild(row)
    }
    if (type === 'filter_two') {
        tbody_filter_two.appendChild(row)
    }
}

// Функция: Удаляет фильтр №1.
tbody_filter_one.addEventListener('submit', (event) => {
    event.preventDefault()
    let id_filter_one = event.target.getAttribute('data-delete')
    if (!isNaN(id_filter_one)) {
        data = {'type': 'delete_filter_one', 'pk': id_filter_one}
        send_on_check(url, data, error_filter_one)
    }
})

// Функция: Удаляет фильтр №2.
tbody_filter_two.addEventListener('submit', (event) => {
    event.preventDefault()
    let id_filter_two = event.target.getAttribute('data-delete')
    if (!isNaN(id_filter_two)) {
        data = {'type': 'delete_filter_two', 'pk': id_filter_two}
        send_on_check(url, data, error_filter_two)
    }
})

// Функция: Отправляет данные на сервер, получает и обрабатывает результаты.
const send_on_check = async (url, data, error_filter) => {
    try {
        axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
        axios.defaults.xsrfCookieName = 'csrftoken'
        response = await axios.post(url, data)
        console.log(response)
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
            if (response.data.filter_one) {
                response_filter_one = response.data.filter_one
                create_tbody_element(response_filter_one.lessOrEqual, response_filter_one.moreOrEqual, response_filter_one.id, 'filter_one')
                document.getElementById('id_lessOrEqual').value = ''
                document.getElementById('id_moreOrEqual').value = ''
            }
            if (response.data.filter_two) {
                response_filter_two = response.data.filter_two
                create_tbody_element(response_filter_two.from_digit, response_filter_two.before_digit, response_filter_two.id, 'filter_two')
                document.getElementById('id_from_digit').value = ''
                document.getElementById('id_before_digit').value = ''
            }
            if (response.data.delete_filter_one) {
                tbody_filter_one.removeChild(document.getElementById(`tr_filter_one_${response.data.delete_filter_one}`))
            }
            if (response.data.delete_filter_two) {
                tbody_filter_two.removeChild(document.getElementById(`tr_filter_two_${response.data.delete_filter_two}`))
            }
        } else {
            console.log(response.status)
        }
    } catch (e) {
        console.log(e)
    }

}