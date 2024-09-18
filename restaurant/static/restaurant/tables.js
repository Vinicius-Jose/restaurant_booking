document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("tables_4_seats").addEventListener('change', (event) => verify_tables(event));
    document.getElementById("tables_8_seats").addEventListener('change', (event) => verify_tables(event));
    document.getElementById("num_tables").addEventListener('change', (event) => enable_fields_generated(event));
    document.getElementById("auto_generate").addEventListener('click', (event) => {
        document.getElementById("auto_tables").removeAttribute("hidden");
        document.getElementById("custom_table_div").setAttribute("hidden", "");
    });
    document.getElementById("add").addEventListener('click', (event) => create_fields_table(event));
    document.getElementById("remove").addEventListener('click', (event) => remove_table(event));
    document.getElementById("custom").addEventListener('click', (event) => {
        document.getElementById("custom_table_div").removeAttribute("hidden");
        document.getElementById("auto_tables").setAttribute("hidden", "");
    })
    document.getElementById("save_generate").addEventListener('click', (event) => save_generate_tables(event));
    document.getElementById("save_custom").addEventListener('click', (event) => save_custom(event));


})


function verify_tables(event) {
    const num_tables = document.getElementById("num_tables");
    const tables_4_seats = document.getElementById("tables_4_seats");
    const tables_8_seats = document.getElementById("tables_8_seats");
    const sum = parseFloat(tables_4_seats.value) + parseFloat(tables_8_seats.value);
    const message = document.getElementById("message");
    const button = document.getElementById("save_generate");
    if (sum != parseFloat(num_tables.value)) {
        message.innerHTML = 'The number of tables with 4 seats and 8 seats together must be equals the number of total seats';
        message.removeAttribute("hidden");
        button.setAttribute("disabled", "")
    }
    else {
        message.setAttribute("hidden", "");
        button.removeAttribute("disabled")
    }

}


function enable_fields_generated(event) {
    const tables_4_seats = document.getElementById("tables_4_seats");
    const tables_8_seats = document.getElementById("tables_8_seats");
    if (parseFloat(event.target.value) > 0) {
        tables_4_seats.removeAttribute("disabled");
        tables_8_seats.removeAttribute("disabled");
    } else {
        tables_4_seats.setAttribute("disabled", "");
        tables_8_seats.setAttribute("disabled", "");
    }

}


function create_fields_table(event) {
    const custom_tables = document.getElementById("custom_tables");
    const num_custom_tables = document.getElementById("num_custom_tables");
    const current_table = parseFloat(num_custom_tables.textContent.split(': ')[1]) + 1;
    num_custom_tables.textContent = `Number of tables: ${current_table}`;
    const div_input = document.createElement("div")
    const id_table = document.createElement("h4")
    id_table.innerText = `Table nº: ${current_table}`;
    div_input.setAttribute("id", current_table);
    div_input.setAttribute("class", "mt-4");
    const select = document.createElement("select");

    select.setAttribute("id", `table_${current_table}`);
    select.setAttribute("class", "form-select mt-2")
    const option_1 = document.createElement("option");
    option_1.setAttribute("value", "4");
    option_1.innerHTML = "4 seats";
    const option_2 = document.createElement("option");
    option_2.setAttribute("value", "8");
    option_2.innerHTML = "8 seats";

    select.appendChild(option_1);
    select.appendChild(option_2);

    div_input.appendChild(id_table)
    div_input.appendChild(select)

    custom_tables.appendChild(div_input)

}


function remove_table(event) {
    const num_custom_tables = document.getElementById("num_custom_tables");
    let current_table = num_custom_tables.textContent.split(': ')[1];

    const table = document.getElementById(current_table);
    table.remove();
    current_table = parseFloat(current_table) - 1;

    num_custom_tables.textContent = `Number of tables: ${current_table}`;
}

function save_generate_tables(event) {
    event.preventDefault();
    const num_tables = parseInt(document.getElementById("num_tables").value);
    const tables_4_seats = parseInt(document.getElementById("tables_4_seats").value);
    const tables_8_seats = parseInt(document.getElementById("tables_8_seats").value);
    let tables = [];
    for (let i = 1; i <= num_tables; i++) {
        let table = { "number": i }
        if (i <= tables_4_seats) {
            table["seats"] = 4;
        } else {
            table["seats"] = 8;
        }
        tables.push(table);
    }
    save_tables(tables);
}


function save_custom(event) {
    event.preventDefault();
    const num_tables = parseFloat(num_custom_tables.textContent.split(': ')[1]);

    let tables = [];
    for (let i = 1; i <= num_tables; i++) {
        let table = { "number": i, "seats": document.getElementById(`table_${i}`).value };

        tables.push(table);
    }
    save_tables(tables);
}


function save_tables(tables) {
    data = { "tables": tables };
    const csrftoken = getCookie('csrftoken');
    fetch(`/tables/${document.getElementById("restaurant_id").value}`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 'X-CSRFToken': csrftoken }
    }).then(response => response.json()).then(response => window.location.href = "/");
}

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