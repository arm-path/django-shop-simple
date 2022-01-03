let url,
    changePickupPoint = document.getElementById('changePickupPoint'),
    deletePickupPoint = document.getElementById('deletePickupPoint')

changePickupPoint.addEventListener('click', () => {
    if (document.getElementById('choicePickupPoint').value !== 'Выберите пункт') {
        url = document.getElementById(document.getElementById('choicePickupPoint').value).getAttribute('data-change')
        window.location.href = url
    }
})

deletePickupPoint.addEventListener('click', () => {
    if (document.getElementById('choicePickupPoint').value !== 'Выберите пункт') {
        url = document.getElementById(document.getElementById('choicePickupPoint').value).getAttribute('data-delete')
        window.location.href = url
    }
})