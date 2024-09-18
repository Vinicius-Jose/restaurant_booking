document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll("#cancel").forEach(cancel => {
        cancel.addEventListener('click', (event) => update_status_booking(event))
    });
    document.querySelectorAll("#confirm").forEach(confirm => {
        confirm.addEventListener('click', (event) => update_status_booking(event))
    });

    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
    try {
        document.getElementById("date").addEventListener("change", function (event) {
            const date = event.target.value;
            const restaurant_id = document.getElementById("restaurant_id").value
            window.location.href = `/bookings/${restaurant_id}/0?date=${date}`

        });
    } catch (error) {

    }

})

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function update_status_booking(event) {
    const csrftoken = getCookie('csrftoken');
    fetch(`/booking`, {
        method: 'PUT',
        body: JSON.stringify({ "booking": event.target.dataset.booking, "status": event.target.dataset.status }),
        headers: { 'X-CSRFToken': csrftoken }
    }).then(response => response.json()).then(response => { event.target.parentElement.parentElement.remove() });
}

