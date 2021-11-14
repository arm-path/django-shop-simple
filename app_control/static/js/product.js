let url = null, select_id = null, newOption
    modal_specification = document.querySelector('.modal-js[data-modal]'),
    id_value = document.getElementById('id_value'),
    id_errors_value_specification = document.getElementById('id_errors_value_specification')

// Функция: Открывает модальное окно.
document.getElementById('id_specifications').addEventListener('click', (event) => {
    if (event.target.getAttribute('data-add-value')) {
        select_id = event.target.closest('button').getAttribute('data-get-select')
        url = event.target.closest('button').getAttribute('data-action')
        id_value.value = ''
        id_errors_value_specification.innerHTML = ''
        new bootstrap.Modal(modal_specification).show()
    }
})

// Функция: Добавляет значение характеристики.
document.getElementById('id_form_value_specification').addEventListener('submit', (event) => {
    event.preventDefault()
    if (select_id !== null && url !== null) {
        let select_values = document.getElementById(select_id)
        select_id = null
        send_on_check(url, {'value': id_value.value}, select_values)
    }
})

// Функция: Отправляет данные на сервер, получает и обрабатывает результаты.
const send_on_check = async (url, data, select_values) => {
    try {
        axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
        axios.defaults.xsrfCookieName = 'csrftoken'
        response = await axios.post(url, data)
        if (response.status === 200) {
            if (response.data.errors) {
                if (response.data.errors.__all__) {
                    response.data.errors.__all__.forEach((item) => {
                        id_errors_value_specification.innerHTML += `<div class="alert alert-danger m-2 mt-1 mb-1 p-1" 
                        style="text-align: center; font-size: 12px" role="alert">${item} </div>`
                    })
                }
                if (response.data.errors.value) {
                    response.data.errors.title.forEach((item) => {
                        id_errors_value_specification.innerHTML += `<div class="alert alert-danger m-2 mt-1 mb-1 p-1"
                        style="text-align: center; font-size: 12px" role="alert">Поле "Значение": ${item} </div>`
                    })
                }
            } else {
                newOption = new Option(response.data.success.value, response.data.success.id)
                document.getElementById(`id_select_${response.data.success.specification}`).append(newOption)
                newOption.selected = true
            }
        }
    } catch (e) {
        console.log('Error', e)
    }
}