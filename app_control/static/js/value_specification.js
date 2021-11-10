let url = null, data=null, slug_specification,
    id_errors_value_specification = document.getElementById('id_errors_value_specification'),
    table_value_specification = document.getElementById('table_value_specification'),
    create_value_specification = document.getElementById("create_value_specification"),
    id_form_value_specification = document.getElementById("id_form_value_specification"),
    id_submit_value_specification= document.getElementById('id_submit_value_specification'),
    create_change_value_specification_label = document.getElementById("create_change_value_specification_label"),
    modal_specification = document.querySelector('.modal-js[data-modal]')

// Функция: Создает значение характеристики.
create_value_specification.addEventListener("click", (event) => {
    create_change_value_specification_label.textContent = "Добавление значения"
    id_submit_value_specification.textContent = 'Добавить'
    document.getElementById('id_value').value = ''
    id_errors_value_specification.innerHTML = ''
    url = create_value_specification.getAttribute('data-action')
    data = {'value': document.getElementById('id_value').value}
})

// Функция: Изменяет значение характеристики.
table_value_specification.addEventListener('click', (event) => {
    if (event.target.getAttribute('data-change')) {
        create_change_value_specification_label.textContent = 'Изменение Характеристики'
        id_submit_value_specification.textContent = 'Изменить'
        id_errors_value_specification.innerHTML = ''
        url = event.target.closest('button').getAttribute('data-action')
        data = {'value': document.getElementById('id_value').value}
        new bootstrap.Modal(modal_specification).show()
        get_value_specification(url)
    }
})

// Функция: Отправляет форму.
id_form_value_specification.addEventListener('submit', (event) => {
    event.preventDefault()
    if (url !== null && data !== null) send_on_check(url, data)
})

// Функция: Получает значения характеристик.
const get_value_specification = async url => {
    response = await axios.get(url)
    if (response.status === 200) {
        document.getElementById('id_value').value = response.data.value_specification.value
    }
}

// Функция: Отправляет данные на сервер, получает и обрабатывает результаты.
const send_on_check = async (url, data) => {
    try {
        axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
        axios.defaults.xsrfCookieName = 'csrftoken'
        response = await axios.post(url, data)
        console.log(response)
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
            }else{
                window.location.reload()
            }
        }
    } catch (e) {
        console.log('Error', e)
    }
}