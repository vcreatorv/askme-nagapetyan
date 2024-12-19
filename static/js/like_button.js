console.log("loaded")

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


const questionLike = () => {
    const cards = document.querySelectorAll('.question-card')
    for (const card of cards) {
        const likeButton = card.querySelector('.like-button')
        const likeCount = card.querySelector('.like-count')

        const questionId = card.dataset.questionId

        const isLiked = card.dataset.isLiked === 'True';
        if (isLiked) {
            likeButton.classList.add('liked');
        }

        likeButton.addEventListener('click', () => {
            console.log('clicked')
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

document.addEventListener('DOMContentLoaded', questionLike);