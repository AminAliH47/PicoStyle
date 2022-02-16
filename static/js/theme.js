// Get products from json url
function searchAutocomplete() {
    var search_box = document.getElementById("search-dropdown");
    $.ajax({
        method: "get",
        dataType: "json",
        url: "/products/autocomplete",
        success: function (response) {
            response = JSON.parse(response)
            response.forEach((item) => {
                const el = document.createElement("a");
                el.href = `/products/d/${item.pk}/${item.fields.slug}`;
                el.classList.add("dropdown-item");
                let cat;
                (item.fields.category == 2) ? cat = "Men" : cat = "Women"
                el.innerText = `${item.fields.title} in ${cat}`;
                search_box.appendChild(el);
            })
        },
        error: function () {
            alert("Something Went wrong")
        }
    })
}

// When the user scrolls the page, execute myFunction
window.onscroll = function () {
    myFunction()
};

// Get the navbar
var navbar = document.getElementById("oper-nav");

// Get the offset position of the navbar
var sticky = navbar.offsetTop;

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
    if (window.pageYOffset >= 75) {
        document.getElementById('go-top').style.visibility = "visible";
        document.getElementById('go-top').style.opacity = "1";
    } else {
        document.getElementById('go-top').style.visibility = "hidden";
        document.getElementById('go-top').style.opacity = "0";
    }
}

function openNav() {
    document.getElementById("mySidenav").style.width = "300px";
    document.getElementById("mySidenav").style.overflow = "visible";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("mySidenav").style.overflow = "hidden";
}

function openCategoryNav() {
    document.getElementById("categorySidenav").style.width = "300px";
    document.getElementById("categorySidenav").style.overflow = "visible";
}

function closeCategoryNav() {
    document.getElementById("categorySidenav").style.width = "0";
    document.getElementById("categorySidenav").style.overflow = "hidden";
}

function openSearch() {
    let el = document.getElementById("search");
    let div = document.getElementById("search-dropdown");
    if (el.value == "") {
        div.style.display = "none";
    } else {
        div.style.display = "block";
    }
    searchAutocomplete();
    document.getElementById("search-overlay").style.visibility = "visible";
    document.getElementById("search-overlay").style.opacity = "1";
}

function closeSearch() {
    document.getElementById("search-overlay").style.visibility = "hidden";
    document.getElementById("search-overlay").style.opacity = "0";
}

document.querySelectorAll("a").forEach((item) => {
    if (item.href == "#") {
        item.dataset.target = "#SoonModal";
        item.dataset.toggle = "modal";
    }
})

// Filter product for auto complete
function filterProduct(el) {
    var input, filter, ul, li, a, i;
    div = document.getElementById("search-dropdown");
    if (el.value == "") {
        div.style.display = "none";
    } else {
        div.style.display = "block";
    }
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
        txtValue = a[i].textContent || a[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}

let cat = "";
window.addEventListener('load', () => {
    let categories = document.querySelectorAll('[name=category]');
    categories.forEach((item) => {
        item.addEventListener('click', (el) => {
            cat = el.target.value;
        })
    })
})

// Create newsletter subscriber
$("#submit-subscriber").click(function () {
    let csrf = document.getElementsByName("csrfmiddlewaretoken")[0];

    $.ajax({
        type: "POST",
        url: '/en/newsletter/create/',
        data: {
            email: $("#newsletter_email").val(),
            full_name: $("#newsletter_full_name").val(),
            category: cat,
            csrfmiddlewaretoken: csrf.value,
        },
        success: function (response) {
            n_email_error = document.getElementById("n-email-error");
            if (response === "created") {
                n_email_error.innerText = "";
                n_email_error.style.display = "none";

                $("#newsletter_full_name").val("");
                $("#newsletter_email").val("");
                let categories = document.querySelectorAll('[name=category]');
                categories.forEach((item) => {
                    item.checked = false;
                })

                $("#newsletter-alert").fadeIn(300);
                setTimeout(function () {
                    $("#newsletter-alert").fadeOut(300);
                }, 3000);
            } else {
                n_email_error.innerText = response;
            }
        },
        error: function () {
            alert("Error");
        },
    });
})

function soonModal() {
    let header = document.getElementById("header");
    let a_h = header.getElementsByTagName("a");
    for (let i = 0; i < a_h.length; i++) {
        if (a_h[i].href.slice(-1) == "" || a_h[i].href.slice(-1) == "#") {
            a_h[i].setAttribute("onClick", "$('#soonModal').modal('show')");
        }
    }
    let footer = document.getElementById("footer");
    let a_f = footer.getElementsByTagName("a");
    for (let i = 0; i < a_f.length; i++) {
        if (a_f[i].href.slice(-4, -1) == "/en" || a_f[i].href.slice(-1) == "#") {
            a_f[i].href = "#";
            a_f[i].setAttribute("onClick", "$('#soonModal').modal('show')");
        }
    }
}

soonModal()

$('#category-tabs li a').click(function () {
    $(this).next('ul').slideToggle('500');
    $(this).find('i').toggleClass('fa-minus fa-plus')
});


