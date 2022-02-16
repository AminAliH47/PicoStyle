function brand() {
    // Brand

    let id_brand = document.getElementById("id_brand");

    let input = id_brand.getElementsByTagName("input");
    let brandDP = document.getElementById("brandDP");
    let brand = document.getElementById("brand");
    for (let i = 0; i < input.length; i++) {
        if (input[i].checked) {
            brandDP.innerHTML = `${input[i].labels[0].innerText}`;
            brand.innerHTML += `
                <input type="radio" class="remove-filter mr-3"
                value="" name="brand" onchange="this.form.submit()">
                `;
        }
    }
}

brand();

function status() {
    // Status

    let id_status = document.getElementById("id_status");

    let input = id_status.getElementsByTagName("input");
    let statusDP = document.getElementById("statusDP");
    let status = document.getElementById("status");
    for (let i = 0; i < input.length; i++) {
        if (input[i].checked) {
            statusDP.innerHTML = `${input[i].labels[0].innerText}`;
            status.innerHTML += `
                <input type="radio" class="remove-filter mr-3"
                value="" name="status" onchange="this.form.submit()">
                `;
        }
    }
}

status();