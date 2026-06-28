function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
}

const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.completed-checkbox').forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            const planId = checkbox.dataset.planId;
            const entryId = checkbox.dataset.entryId;
            fetch(`/mealplans/${planId}/entries/${entryId}/toggle-completed/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
            })
                .then(response => response.json())
                .then(data => {
                    checkbox.checked = data.completed;
                    const adherenceEl = document.getElementById('adherence-value');
                    if (adherenceEl) {
                        adherenceEl.textContent = data.adherence_pct;
                    }
                });
        });
    });
});
