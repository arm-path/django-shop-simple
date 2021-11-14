let html_specification_select,
    select_value = document.getElementById('id_category').value,
    id_slug = document.getElementById('id_slug').textContent,
    id_specifications = document.getElementById('id_specifications')

document.getElementById('id_category').addEventListener('change', (event) => {
    if (confirm('Вы уверены что хотите изменить категори? При изменении категории будут получены новые характеристики из данной категории.')) {
        select_value = document.getElementById('id_category').value
        html_specification_select = ''
        send_on_check_(`/control/specification-for-product/${id_slug}/${select_value}/`)
    } else {
        document.getElementById('id_category').value = select_value
    }
})


const send_on_check_ = async (url) => {
    try {
        axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
        axios.defaults.xsrfCookieName = 'csrftoken'
        response = await axios.get(url)
        console.log(response)
        if (response.status === 200) {
            if (response.data.category_specification) {
                response.data.category_specification.forEach((specification) => {
                    html_specification_select += `
                    <div class="row"> <div class="col-md-4 mt-2">${specification.title}</div>
                    <div class="col-md-3 mt-2">
                    <select id="id_select_${specification.pk}" name="id_specification_${specification.pk}" class="form-select" 
                    aria-label="Default select example">
                    <option value="0" ${select = specification.select ? 'selected' : null}>-------</option>
                    `
                    html_value_option = ''
                    specification.values.forEach((value) => {
                        html_value_option += `
                            <option value="${value.pk}" ${select = specification.select === value.pk ? 'selected' : null}>
                                ${value.value}
                            </option>
                        `
                    })
                    html_specification_select += html_value_option
                    html_specification_select += `
                       </select> </div> 
                       <div class="col-md-3 mt-2">
                       <button type="button" class="btn btn-success" data-add-value="add-value-btn" 
                               data-action="/control/specification/${specification.slug}/value-create/" 
                               data-get-select="id_select_${specification.pk}">
                       <i class="bi bi-plus-circle" data-add-value="add-value-btn"></i>
                       </button></div></div>`
                }) // TODO: Изменить получение url в data-action.
                id_specifications.innerHTML = html_specification_select
            }
        }
    } catch (e) {
        console.log('Error', e)
    }
}