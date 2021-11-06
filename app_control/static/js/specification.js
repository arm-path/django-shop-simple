let response, url, data = {},
    create_specification = document.getElementById('create_specification'),
    table_specification = document.getElementById('table_specification'),
    modal_specification = document.querySelector('.modal-js[data-modal]'),
    title = document.getElementById('id_title_specification'),
    unit = document.getElementById('id_unit'),
    use_filters = document.getElementById('id_use_filters'),
    type_filter = document.getElementById('id_type_filter'),
    id_form_specification = document.getElementById('id_form_specification'),
    id_btn_specification = document.getElementById('id_btn_specification'),
    create_change_specificationLabel = document.getElementById('createChangeSpecificationLabel')

// Функция: Создать Характеристику.
create_specification.addEventListener('click', () => {
    title.value = ''
    type_filter.value = 'base'
    unit.value = ''
    use_filters.checked = false
    create_change_specificationLabel.textContent = 'Добавление Характеристики'
    id_btn_specification.textContent = 'Добавить'
    id_form_specification.addEventListener('submit', event => {
        event.preventDefault()
        data_form(create_specification.getAttribute('data-action'))
    })
})

// Функция: Изменить данные характеристики.
table_specification.addEventListener('click', (event) => {
    if (event.target.getAttribute('data-change')) {
        url = event.target.closest('button').getAttribute('data-action')
        const modal = new bootstrap.Modal(modal_specification)
        modal.show()
        create_change_specificationLabel.textContent = 'Изменение Характеристики'
        id_btn_specification.textContent = 'Изменить'
        get_specification(url)
        id_form_specification.addEventListener('submit', event => {
            event.preventDefault()
            data_form(url)
        })
    }
})

// Фнукция: Данные из формы.
const data_form = (url) => {
    data.title = title.value
    data.unit = unit.value
    data.use_filters = use_filters.checked
    data.type_filter = type_filter.value
    send_on_check(url, data)
}

// Функция: Получить Характеористику.
const get_specification = async (url, data) => {
    response = await axios.get(url)
    if (response.status === 200) {
        title.value = response.data.specification.title
        type_filter.value = response.data.specification.type_filter
        unit.value = response.data.specification.unit
        use_filters.checked = response.data.specification.use_filters
    }
}

// Функция: Отправить данные на сервер.
const send_on_check = async (url, data) => {
    try {
        axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
        axios.defaults.xsrfCookieName = 'csrftoken'
        response = await axios.post(url, data)
        if (response.status === 200) {
            if (response.data.errors) {
                let id_errors_specification = document.getElementById('id_errors_specification')
                if (response.data.errors.__all__) {
                    response.data.errors.__all__.forEach((item) => {
                        id_errors_specification.innerHTML += `<div class="alert alert-danger m-2 mt-1 mb-1 p-1" 
                                                                   style="text-align: center; font-size: 12px" 
                                                                   role="alert">${item}
                                                              </div>`
                    })
                }
                if (response.data.errors.title) {
                    response.data.errors.title.forEach((item) => {
                        id_errors_specification.innerHTML += `<div class="alert alert-danger m-2 mt-1 mb-1 p-1"
                                                                   style="text-align: center; font-size: 12px"
                                                                   role="alert">Поле "Характеристика": ${item}
                                                              </div>`
                    })
                }
                if (response.data.errors.unit) {
                    response.data.errors.unit.forEach((item) => {
                        id_errors_specification.innerHTML += `<div class="alert alert-danger m-2 mt-1 mb-1 p-1"
                                                                   style="text-align: center; font-size: 12px"
                                                                   role="alert">Поле "Ед. Измерения": ${item}
                                                              </div>`
                    })
                }
                if (response.data.errors.use_filters) {
                    response.data.errors.use_filters.forEach((item) => {
                        id_errors_specification.innerHTML += `<div class="alert alert-danger m-2 mt-1 mb-1 p-1"
                                                                   style="text-align: center; font-size: 12px"
                                                                   role="alert">Поле "Использовать в фильтрах": ${item}
                                                              </div>`
                    })
                }
                if (response.data.errors.type_filter) {
                    response.data.errors.type_filter.forEach((item) => {
                        id_errors_specification.innerHTML = `<div class="alert alert-danger m-2 mt-1 mb-1 p-1"
                                                                   style="text-align: center; font-size: 12px"
                                                                   role="alert">Поле "Тип фильтра": ${item}
                                                              </div>`
                    })
                }
            } else {
                window.location.reload()
            }
        }
    } catch (e) {
        console.log('Error', e)
    }
}

