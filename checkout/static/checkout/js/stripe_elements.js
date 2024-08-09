/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit
var form = document.getElementById('payment-form');

// Ensure all fields are accessed correctly
var firstName = form.querySelector('input[name="first_name"]');
var lastName = form.querySelector('input[name="last_name"]');
var email = form.querySelector('input[name="email"]');
var phoneNumber = form.querySelector('input[name="phone_number"]');
var country = form.querySelector('select[name="country"]');  // Country is a select element
var postcode = form.querySelector('input[name="postcode"]');
var townOrCity = form.querySelector('input[name="town_or_city"]');
var streetAddress1 = form.querySelector('input[name="street_address1"]');
var streetAddress2 = form.querySelector('input[name="street_address2"]');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);

    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    var url = '/checkout/cache_checkout_data/';

    $.post(url, postData).done(function () {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(firstName.value) + ' ' + $.trim(lastName.value),
                    phone: $.trim(phoneNumber.value),
                    email: $.trim(email.value),
                    address: {
                        line1: $.trim(streetAddress1.value),
                        line2: $.trim(streetAddress2.value),
                        city: $.trim(townOrCity.value),
                        country: $.trim(country.value),  // Access country value properly
                        postal_code: $.trim(postcode.value),
                    }
                }
            },
            shipping: {
                name: $.trim(firstName.value) + ' ' + $.trim(lastName.value),
                phone: $.trim(phoneNumber.value),
                address: {
                    line1: $.trim(streetAddress1.value),
                    line2: $.trim(streetAddress2.value),
                    city: $.trim(townOrCity.value),
                    country: $.trim(country.value),  // Access country value properly
                    postal_code: $.trim(postcode.value),
                }
            },
        }).then(function(result) {
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                card.update({ 'disabled': false});
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function () {
        // just reload the page, the error will be in django messages
        location.reload();
    });
});



// var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
// var clientSecret = $('#id_client_secret').text().slice(1, -1);
// var stripe = Stripe(stripePublicKey);
// var elements = stripe.elements();
// var style = {
//     base: {
//         color: '#000',
//         fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
//         fontSmoothing: 'antialiased',
//         fontSize: '16px',
//         '::placeholder': {
//             color: '#aab7c4'
//         }
//     },
//     invalid: {
//         color: '#dc3545',
//         iconColor: '#dc3545'
//     }
// };
// var card = elements.create('card', {style: style});
// card.mount('#card-element');

// // Handle realtime validation errors on the card element
// card.addEventListener('change', function (event) {
//     var errorDiv = document.getElementById('card-errors');
//     if (event.error) {
//         var html = `
//             <span class="icon" role="alert">
//                 <i class="fas fa-times"></i>
//             </span>
//             <span>${event.error.message}</span>
//         `;
//         $(errorDiv).html(html);
//     } else {
//         errorDiv.textContent = '';
//     }
// });

// // Handle form submit
// var form = document.getElementById('payment-form');

// form.addEventListener('submit', function(ev) {
//     ev.preventDefault();
//     card.update({ 'disabled': true});
//     $('#submit-button').attr('disabled', true);
    

//     var saveInfo = Boolean($('#id-save-info').attr('checked'));
//     // From using {% csrf_token %} in the form
//     var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
//     var postData = {
//         'csrfmiddlewaretoken': csrfToken,
//         'client_secret': clientSecret,
//         'save_info': saveInfo,
//     };
//     var url = '/checkout/cache_checkout_data/';
    
//     $.post(url, postData).done(function () {
//         stripe.confirmCardPayment(clientSecret, {
//             payment_method: {
//                 card: card,
//                 billing_details: {
//                     name: $.trim(form.full_name.value),
//                     phone: $.trim(form.phone_number.value),
//                     email: $.trim(form.email.value),
//                     address:{
//                         line1: $.trim(form.street_address1.value),
//                         line2: $.trim(form.street_address2.value),
//                         city: $.trim(form.town_or_city.value),
//                         country: $.trim(form.country.value),
//                         state: $.trim(form.county.value),
//                     }
//                 }
//             },
//             shipping: {
//                 name: $.trim(form.full_name.value),
//                 phone: $.trim(form.phone_number.value),
//                 address: {
//                     line1: $.trim(form.street_address1.value),
//                     line2: $.trim(form.street_address2.value),
//                     city: $.trim(form.town_or_city.value),
//                     country: $.trim(form.country.value),
//                     postal_code: $.trim(form.postcode.value),
//                     state: $.trim(form.county.value),
//                 }
//             },
//         }).then(function(result) {
//             if (result.error) {
//                 var errorDiv = document.getElementById('card-errors');
//                 var html = `
//                     <span class="icon" role="alert">
//                     <i class="fas fa-times"></i>
//                     </span>
//                     <span>${result.error.message}</span>`;
//                 $(errorDiv).html(html);
//                 card.update({ 'disabled': false});
//                 $('#submit-button').attr('disabled', false);
//             } else {
//                 if (result.paymentIntent.status === 'succeeded') {
//                     form.submit();
//                 }
//             }
//         });
//     }).fail(function () {
//         // just reload the page, the error will be in django messages
//         location.reload();
//     })
// });