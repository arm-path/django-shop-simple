let productInCart = document.getElementById('productInCart'),
    cartSum = document.getElementById('cartSum'),
    includeIdFormDelete = 'productDelete_',
    includeIDProductInCart = 'productInCart_'

// Функция: Изменяет количество товара в корзине.
productInCart.addEventListener("change", (event) => {
    if (event.target.getAttribute('data-count') &&
        event.target.getAttribute('data-cart') &&
        event.target.getAttribute('data-url')) {
        let url = event.target.getAttribute('data-url'),
            productInCartID = event.target.getAttribute('data-count'),
            cartID = event.target.getAttribute('data-cart'),
            productInCartCount = event.target.value,
            changeTotal = event.target.parentElement.parentElement.parentElement.querySelector('.js-total')
        sendOnCheck
        (
            url,
            {'product_in_cart': productInCartID, 'quantity': productInCartCount, 'cart': cartID},
            changeTotal
        )
    }
})

// Функция: Удаляет товар из корзины.
productInCart.addEventListener('submit', (event) => {
    event.preventDefault()
    if (event.target.id) {
        if (event.target.id.toString().includes(includeIdFormDelete) && event.target.id.toString().indexOf(includeIdFormDelete) === 0) {
            let idProductsInCart = event.target.id.toString().substr(includeIdFormDelete.length)
            if (idProductsInCart && !isNaN(idProductsInCart)) {
                if (event.target.action) {
                    let url = event.target.action
                    sendOnCheck(url, {'idProductsInCart': idProductsInCart})
                } else console.log('No url')
            } else console.log('Not found ID')
        } else console.log('ID not include "productDelete_"')
    } else console.log('Form not include ID')
})

// Функция: Удаляет элемент таблицы и меняет сумму товаров в корзине.
const ProductInCartDelete = (id, cartSumProduct) => {
    let idProductInCartDelete = includeIDProductInCart + id
    let productInCartDelete = document.getElementById(idProductInCartDelete)
    if (productInCartDelete) {
        document.getElementById(idProductInCartDelete).remove()
        cartSum.textContent = cartSumProduct.toString() + ',00'
    }
    if (document.getElementsByClassName('jsBtnOrder').length === 0) {
        document.getElementById('btnOrder').classList.add('visually-hidden')
    }
}

const sendOnCheck = async (url, data, changeTotal = '') => {
    try {
        axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
        axios.defaults.xsrfCookieName = 'csrftoken'
        response = await axios.post(url, data)
        if (response.status === 200) {
            if (response.data.price && response.data.sum) {
                changeTotal.textContent = response.data.price
                cartSum.textContent = response.data.sum + ',00'
            }
            if (response.data.product_removed && (response.data.cart_sum_product || response.data.cart_sum_product === 0)) {
                ProductInCartDelete(response.data.product_removed, response.data.cart_sum_product)
            }
            if (response.data.errors) console.log(response.data.errors)
        } else console.log(response)
    } catch (e) {
        console.log(e)
    }

}

