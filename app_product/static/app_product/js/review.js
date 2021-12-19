let review, url,
    reviewCreateForm = document.getElementById('reviewCreateForm'),
    reviewList = document.getElementById('reviewList'),
    reviewCreateFormError = document.getElementById('reviewCreateFormError'),
    csrf_token = document.getElementsByName('csrfmiddlewaretoken')

// Функция: Создает отзыв.
reviewCreateForm.addEventListener('submit', (event) => {
    event.preventDefault()
    reviewCreateFormError.textContent = ''
    let rating = document.querySelector('input[name="rating"]:checked')
    if (rating && rating.getAttribute('value')) {
        if (rating.value in [1, 2, 3, 4, 5, 6]) {
            rating = rating.value
        } else rating = 0
    } else rating = 0
    let reviewText = document.getElementById('reviewText')
    if (reviewText) {
        review = reviewText.value
    } else review = ''
    if (reviewCreateForm.getAttribute('action')) {
        url = reviewCreateForm.action
        data = {'rating': rating, 'review': review}
        clearForm()
        sendOnCheck(url, data)
    }
})

// Функция: Очищает данные в форме.
const clearForm = () => {
    if (document.querySelector('input[name="rating"]:checked')) {
        document.querySelector('input[name="rating"]:checked').checked = false
    }
    document.getElementById('reviewText').value = ''
}

// Функция: Удаляет отзыв.
reviewList.addEventListener('submit', (event) => {
    event.preventDefault()
    if (event.target.id && event.target.action) {
        if (event.target.id.lastIndexOf('_') !== -1) {
            let reviewDeleteFormID = event.target.id.substr(event.target.id.lastIndexOf('_') + 1)
            if (!isNaN(reviewDeleteFormID)) {
                data = {'review': reviewDeleteFormID}
                url = event.target.action
                sendOnCheck(url, data)
            }
        }
    }

})

const sendOnCheck = async (url, data) => {
    try {
        axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
        axios.defaults.xsrfCookieName = 'csrftoken'
        response = await axios.post(url, data)
        if (response.status === 200) {
            if (response.data.review) {
                let review_response = response.data.review
                reviewCreateFormError.textContent = ''
                reviewList.insertAdjacentHTML('afterbegin', `
                <div id="reviewDetail_${review_response.id}" class="mt-2">
                    <div><b class="review-user">${review_response.customer}</b>
                    <i class="bi bi-star"></i> ${review_response.rating}</div>
                    <small style="color: #5d5d64"><i>Только что</i></small>
                    <div><b>Отзыв: </b>${review_response.review}</div>
                    <form id="reviewDeleteForm_${review_response.id}" action="/review/delete/" method="POST">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_token[0].value}">
                        <button type="submit" class="review-delete-link ">Удалить</button>
                    </form>
                </div>
                `)
                clearForm()
            }
            if (response.data.error_review) {
                reviewCreateFormError.textContent = `${response.data.error_review}`
            }
            if (response.data.review_delete) {
                let reviewDetailID = document.getElementById(`reviewDetail_${response.data.review_delete}`)
                if (reviewDetailID) {
                    reviewList.removeChild(reviewDetailID)
                }
            }
            if (response.data.errors) console.log(response.data.errors)
        } else console.log(response.status)
    } catch (e) {
        console.log(e)
    }

}
