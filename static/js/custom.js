function material() {
    // Material

    let id_material = document.getElementById("id_material");

    let input = id_material.getElementsByTagName("input");
    let materialDP = document.getElementById("materialDP");
    let material = document.getElementById("material");
    for (let i = 0; i < input.length; i++) {
        if (input[i].checked) {
            materialDP.innerHTML = `${input[i].labels[0].innerText}`;
            material.innerHTML += `
                <input type="radio" class="remove-filter mr-3"
                value="" id="hello" name="material" onchange="this.form.submit()">
                `;
        }
    }
}

material();

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

function sort() {
    // Sort by

    let id_sort = document.getElementById("id_sort");

    let input = id_sort.getElementsByTagName("input");
    let sortDP = document.getElementById("sortDP");
    let sort = document.getElementById("sort");
    for (let i = 0; i < input.length; i++) {
        if (input[i].checked) {
            sortDP.innerHTML = `${input[i].labels[0].innerText}`;
            sort.innerHTML += `
                <input type="radio" class="remove-filter mr-3"
                value="" name="sort" onchange="this.form.submit()">
                `;
        }
    }
}

sort();

// function brand() {
//     // Brand
//
//     let id_brand = document.getElementById("id_brand");
//
//     let input = id_brand.getElementsByTagName("input");
//     let brandDP = document.getElementById("brandDP");
//     let brand = document.getElementById("brand");
//     for (let i = 0; i < input.length; i++) {
//         if (input[i].checked) {
//             brandDP.innerHTML = `${input[i].labels[0].innerText}`;
//             brand.innerHTML += `
//                 <input type="radio" class="remove-filter mr-3"
//                 value="" name="brand" onchange="this.form.submit()">
//                 `;
//         }
//     }
// }
//
// brand();
