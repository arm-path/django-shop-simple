create_specification = document.getElementById('create_specification')

create_specification.addEventListener('click', () => {
    container_create_specification = document.getElementById('container_create_specification')
    title = document.getElementById('id_title_specification')
    unit = document.getElementById('id_unit')
    use_filters = document.getElementById('id_use_filters')
    type_filter = document.getElementById('id_type_filter')
    console.log(title, unit, use_filters, type_filter)
})