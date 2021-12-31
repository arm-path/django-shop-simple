let methodGet = document.getElementById('id_method_get'),
    pickupPoint = document.getElementById('id_pickup_point'),
    deliveryAddress = document.getElementById('id_delivery_address')

const methodDelivery = () => {
    pickupPoint.classList.add('visually-hidden')
    pickupPoint.value = ''
    document.querySelector(`[for="${pickupPoint.id}"]`).classList.add('visually-hidden')
    deliveryAddress.classList.remove('visually-hidden')
    document.querySelector(`[for="${deliveryAddress.id}"]`).classList.remove('visually-hidden')
}

const methodGetPickup = () => {
    deliveryAddress.classList.add('visually-hidden')
    deliveryAddress.value = ''
    document.querySelector(`[for="${deliveryAddress.id}"]`).classList.add('visually-hidden')
    pickupPoint.classList.remove('visually-hidden')
    document.querySelector(`[for="${pickupPoint.id}"]`).classList.remove('visually-hidden')
}

if (methodGet === 'delivery') {
    methodDelivery()
} else {
    methodGetPickup()
}

methodGet.addEventListener('change', (event) => {
    if (event.target.value === 'delivery') {
        methodDelivery()
    } else {
        methodGetPickup()
    }
})