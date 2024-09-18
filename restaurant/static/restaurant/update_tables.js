document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("#remove").forEach(element => {
        element.addEventListener('click', (event) => remove_existing_table(event));
    });
    document.getElementById("add").addEventListener('click', (event) => create_fields_table(event));
    document.getElementById("save_custom").addEventListener('click', (event) => save(event));

})


function remove_existing_table(event) {
    event.preventDefault();
    const num_custom_tables = document.getElementById("num_custom_tables");
    let num_table = num_custom_tables.textContent.split(': ')[1];
    const id = event.target.dataset.tableId
    const table = document.getElementById(id);
    const csrftoken = getCookie('csrftoken');
    fetch(`/tables/${document.getElementById("restaurant_id").value}`, {
        method: 'DELETE',
        body: JSON.stringify({ "id": id }),
        headers: { 'X-CSRFToken': csrftoken }
    }).then(response => response.json()).then(() => {
        const body = document.getElementById("body");
        body.setAttribute("class", "")
        body.setAttribute("style", "")
        document.querySelector(".modal-backdrop").remove();
        table.remove();
        current_table = parseFloat(num_table) - 1;
        num_custom_tables.textContent = `Number of tables: ${current_table}`;
    });
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


function create_fields_table(event) {
    const custom_tables = document.getElementById("custom_tables");
    const num_custom_tables = document.getElementById("num_custom_tables");
    const current_table = parseFloat(num_custom_tables.textContent.split(': ')[1]) + 1;
    num_custom_tables.textContent = `Number of tables: ${current_table}`;
    const div_input = document.createElement("div")
    const id_table = document.createElement("h4")


    div_input.setAttribute("class", "mt-4");
    const select = document.createElement("select");
    const num_table = parseInt(custom_tables.lastElementChild.dataset.tableNumber) + 1
    div_input.setAttribute("data-table-number", num_table)
    id_table.innerText = `Table nº: ${num_table}`;
    div_input.setAttribute("id", `table_new_${num_table}`);


    select.setAttribute("id", `select_${num_table}`);
    select.setAttribute("class", "form-select mt-2")
    const option_1 = document.createElement("option");
    option_1.setAttribute("value", "4");
    option_1.innerHTML = "4 seats";
    const option_2 = document.createElement("option");
    option_2.setAttribute("value", "8");
    option_2.innerHTML = "8 seats";


    const remove_button = document.createElement("button")
    remove_button.setAttribute("class", "btn btn-light mt-2")
    remove_button.innerText = "Remove"
    remove_button.addEventListener('click', (event) => remove_new_table(event))

    select.appendChild(option_1);
    select.appendChild(option_2);

    div_input.appendChild(id_table);
    div_input.appendChild(select);
    div_input.appendChild(remove_button);

    custom_tables.appendChild(div_input);

}


function remove_new_table(event) {
    event.preventDefault();
    const num_custom_tables = document.getElementById("num_custom_tables");
    let current_table = num_custom_tables.textContent.split(': ')[1];


    event.target.parentElement.remove()
    current_table = parseFloat(current_table) - 1;

    num_custom_tables.textContent = `Number of tables: ${current_table}`;
}



function save(event) {
    event.preventDefault();
    const num_tables = parseFloat(num_custom_tables.textContent.split(': ')[1]);

    const custom_tables = document.getElementById("custom_tables");
    let tables = [];
    document.querySelectorAll('[data-table-number]').forEach(node => {
        const table_number = node.dataset.tableNumber
        let table = { "number": table_number, "seats": document.getElementById(`select_${table_number}`).value };
        if (!node.getAttribute("id").includes("table_new")) {
            table["id"] = node.getAttribute("id")
        }
        tables.push(table);
    });

    update_tables(tables);
}

function update_tables(tables) {
    data = { "tables": tables };
    const csrftoken = getCookie('csrftoken');
    fetch(`/tables/${document.getElementById("restaurant_id").value}`, {
        method: 'PUT',
        body: JSON.stringify(data),
        headers: { 'X-CSRFToken': csrftoken }
    }).then(response => response.json()).then(response => window.location.href = "/");
}
