document.addEventListener('DOMContentLoaded', () => {
    document.getElementById("date").addEventListener('click', function () {
        document.getElementById("times").parentElement.removeAttribute('hidden');
        document.getElementById("times").parentElement.removeAttribute('hidden');
        document.getElementById("save_booking").setAttribute("hidden", "");
        document.getElementById("not_found_message").setAttribute("hidden", "");
    });
    document.getElementsByName("btnradio").forEach(btnradio => btnradio.addEventListener('click', (event) => get_bookings_available(event)));
    document.querySelectorAll("#cancel").forEach(cancel => {
        cancel.addEventListener('click', (event) => update_status_booking(event))
    });
    document.querySelectorAll("#confirm").forEach(confirm => {
        confirm.addEventListener('click', (event) => update_status_booking(event))
    });

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

function get_bookings_available(event) {
    const tables = document.getElementById("tables");
    tables.innerHTML = ""
    tables.parentElement.removeAttribute("hidden")
    const time = event.target.getAttribute("id")
    const date = document.getElementById("date").value
    const restaurant_id = document.getElementById("restaurant_id").value
    const csrftoken = getCookie('csrftoken');
    const message = document.getElementById("not_found_message")
    message.removeAttribute("hidden")
    fetch(`/booking/${restaurant_id}?date=${date}-${time}`, {
        method: 'GET',
        headers: { 'X-CSRFToken': csrftoken }
    }).then(response => response.json()).then(response => response.tables.forEach(table => {
        message.setAttribute("hidden", "");
        const input = document.createElement("input");
        input.setAttribute("id", table.number);
        input.setAttribute("type", "radio");
        input.setAttribute("class", "btn-check");
        input.setAttribute("name", "btnradio2");
        input.setAttribute("value", table.id);
        input.setAttribute("autocomplete", "off");

        const label = document.createElement("label")
        label.setAttribute("class", "btn btn-outline-primary");
        label.setAttribute("for", table.number);
        label.innerHTML = `Table ${table.number}: <br> N Seats: ${table.seats}`

        input.addEventListener('click', function () {
            document.getElementById("save_booking").removeAttribute("hidden");
        })

        tables.appendChild(input);
        tables.appendChild(label);

    }));
}
