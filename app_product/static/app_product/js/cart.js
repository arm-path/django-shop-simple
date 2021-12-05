let productInCart = document.getElementById('productInCart'),
    cartSum = document.getElementById('cartSum')

productInCart.addEventListener("change", (event) => {
    if (event.target.getAttribute('data-count') &&
        event.target.getAttribute('data-cart') &&
        event.target.getAttribute('data-url')) {
        let url = event.target.getAttribute('data-url'),
            productInCartID = event.target.getAttribute('data-count'),
            cartID = event.target.getAttribute('data-cart'),
            productInCartCount = event.target.value,
            changeTotal = event.target.parentElement.parentElement.querySelector('.js-total')
        sendOnCheck
        (
            url,
            {'product_in_cart': productInCartID, 'quantity': productInCartCount, 'cart': cartID},
            changeTotal
        )
    }
})


const sendOnCheck = async (url, data, changeTotal) => {
    try {
        axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
        axios.defaults.xsrfCookieName = 'csrftoken'
        response = await axios.post(url, data)
        if (response.status === 200) {
            if (response.data.price && response.data.sum) {
                changeTotal.textContent = response.data.price
                cartSum.textContent = response.data.sum
            }
        } else {
            console.log(response)
        }
    } catch (e) {
        console.log(e)
    }

}

