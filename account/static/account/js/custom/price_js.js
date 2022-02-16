let exwPriceEL = document.getElementById('id_exw_price');
let exwPrice;
let discountEl = document.getElementById('id_discount');
let discount = 0;
let w_discount = parseInt(document.getElementById("id_w_discount").value);
let r_discount = parseInt(document.getElementById("id_r_discount").value);

let wholesalePrice = document.getElementById('id_wholesale_price');
let retailerPriceUSD = document.getElementById('id_retail_price_USD');
// Currency section
let currenciesEL = document.getElementById('id_currency');
let currency;
let retail_percent = parseInt(document.getElementById('retail_percent').value);
let wholesale_percent = parseInt(document.getElementById('wholesale_percent').value);

function separate(Number) {
    Number += '';
    Number = Number.replace(',', '');
    let x = Number.split('.');
    let y = x[0];
    let z = x.length > 1 ? '.' + x[1] : '';
    let rgx = /(\d+)(\d{3})/;
    while (rgx.test(y))
        y = y.replace(rgx, '$1' + ',' + '$2');
    return y + z;
}

function calPrice() {
    const reg = new RegExp('^[0-9]+$');
    let p = exwPriceEL.value.replace(/,/g, '');

    if (p.match(reg)) {
        exwPrice = parseInt(p);
    } else {
        exwPriceEL.value = "";
    }

    let wPrice = document.getElementById('id_wPrice');
    let rPrice = document.getElementById('id_rPrice');
    let wP;
    if (currency === "USD") {

    } else if (currency === "EUR") {
        exwPrice = exwPrice / 0.87;

    } else if (currency === "RUB") {
        exwPrice = exwPrice / 72.78;

    } else if (currency === "SAR") {
        exwPrice = exwPrice / 200000;

    } else {
        document.getElementById('currency_error').classList.remove('d-none');
    }

    wP = ((exwPrice) * (1 - (discount / 100)) * (1 + (wholesale_percent / 100)));
    wP = parseFloat(wP.toFixed(2));


    wholesalePrice.value = `${separate((wP * (1 - (w_discount / 100))).toFixed(2))} $`;
    wPrice.value = `${separate((wP* (1 - (w_discount / 100))).toFixed(2))} $`;

    let r_price = (wP * (1 + (retail_percent / 100))) * (1 - (r_discount / 100));
    rPrice.value = `${separate(r_price.toFixed(2))} $`;
    retailerPriceUSD.value = `${separate(r_price.toFixed(2))} $`;

    document.getElementById('id_discount1').value = discount;
}

window.addEventListener('load', () => {
    document.querySelectorAll('input[name="currency"]').forEach((item) => {
        if (item.checked) {
            switch (item.id) {
                case 'id_currency_0':
                    currency = "USD";
                    break;
                case 'id_currency_1':
                    currency = "SAR";
                    break;
                case 'id_currency_2':
                    currency = "RUB";
                    break;
                case 'id_currency_3':
                    currency = "EUR";
                    break;
            }
        }
    })
    discount = parseInt(discountEl.value);
    calPrice();
})


exwPriceEL.setAttribute('onkeyup', 'javascript:document.getElementById("id_exw_price_num").innerText = (parseFloat(this.value).toLocaleString())');

currenciesEL.addEventListener('change', () => {
    document.getElementById('currency_error').classList.add('d-none');
    document.querySelectorAll('input[name="currency"]').forEach((item) => {
        if (item.checked) {
            switch (item.id) {
                case 'id_currency_0':
                    currency = "USD";
                    break;
                case 'id_currency_1':
                    currency = "SAR";
                    break;
                case 'id_currency_2':
                    currency = "RUB";
                    break;
                case 'id_currency_3':
                    currency = "EUR";
                    break;
            }
        }
    })
    calPrice();
})


exwPriceEL.addEventListener('focusout', (el) => {
    calPrice();
})

discountEl.addEventListener('focusout', (el) => {
    if (el.target.value > 100) {
        el.target.value = "";
        document.getElementById('discount_error').classList.remove('d-none')
    } else {
        discount = parseInt(el.target.value);
        document.getElementById('discount_error').classList.add('d-none')
    }

    calPrice();
})