function questionLike() {
    const cards = document.querySelectorAll('.question-card')
    for (const card of cards) {
        const likeButton = card.querySelector('.like-button')
        const likeCount = card.querySelector('.like-count')

        const isLiked = card.dataset.isLiked === 'True';
        if (isLiked) {
            likeButton.classList.add('liked');
        }

        const questionId = card.dataset.questionId
        likeButton.addEventListener('click', () => {
            const request = new Request(`/question_like/${questionId}/`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            fetch(request)
                .then((response) => {
                    if (response.status === 401) {
                        window.location.href = '/login/?continue=' + window.location.pathname;
                    } else {
                        return response.json();
                    }
                })
                .then((data) => {
                    if (data) {
                        likeCount.innerHTML = data.question_likes_count;
                        if (data.liked) {
                            likeButton.classList.add('liked');
                        } else {
                            likeButton.classList.remove('liked');
                        }
                    }
                })
        })
    }
}


function answerLike() {
    const question_id = document.querySelector('.question-card').dataset.questionId
    const cards = document.querySelectorAll('.answer-card')
    for (const card of cards) {
        const likeButton = card.querySelector('.like-button')
        const likeCount = card.querySelector('.like-count')

        const isLiked = card.dataset.isLiked === 'True'
        if (isLiked) {
            likeButton.classList.add('liked')
        }

       const answerId = card.id.split('-')[1]
        likeButton.addEventListener('click', () => {
            const request = new Request(`/answer_like/${answerId}/`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            fetch(request)
                .then((response) => {
                    if (response.status === 401) {
                        window.location.href = '/login/?continue=' + window.location.pathname
                    } else {
                        return response.json()
                    }
                })
                .then((data) => {
                    if (data) {
                        likeCount.innerHTML = data.answer_likes_count
                        if (data.liked) {
                            likeButton.classList.add('liked')
                        } else {
                            likeButton.classList.remove('liked')
                        }
                    }
                })
        })
    }
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function randomTagColor() {
    const tags = document.querySelectorAll('.tag-badge')
    const colors = ['text-bg-secondary', 'text-bg-primary', 'text-bg-success', 'text-bg-danger', 'text-bg-warning', 'text-bg-info', 'text-bg-dark']

    tags.forEach(tag => {
        const randomColor = colors[Math.floor(Math.random() * colors.length)]
        tag.classList.add(randomColor)
    });
}

document.addEventListener('DOMContentLoaded', () => {
    questionLike();
    answerLike();
    randomTagColor();
});
