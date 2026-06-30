function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
}

const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.shopping-item-checkbox').forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            const listId = checkbox.dataset.listId;
            const itemId = checkbox.dataset.itemId;
            fetch(`/shopping/${listId}/items/${itemId}/toggle/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
            })
                .then(response => response.json())
                .then(data => {
                    checkbox.checked = data.checked;
                });
        });
    });
});
