

// document.addEventListener('DOMContentLoaded', function() {
//     const forms = document.querySelectorAll('.update-form');

//     forms.forEach(form => {
//         const decrementBtn = form.querySelector('.decrement-btn');
//         const incrementBtn = form.querySelector('.increment-btn');
//         const quantityInput = form.querySelector('.quantity-input');

//         decrementBtn.addEventListener('click', () => {
//             let currentQuantity = parseInt(quantityInput.value);
//             if (currentQuantity > 1) {
//                 quantityInput.value = currentQuantity - 1;
//                 updateBag(form);
//             }
//         });

//         incrementBtn.addEventListener('click', () => {
//             let currentQuantity = parseInt(quantityInput.value);
//             if (currentQuantity < 5) {
//                 quantityInput.value = currentQuantity + 1;
//                 updateBag(form);
//             }
//         });
//     });

//     function updateBag(form) {
//         const formData = new FormData(form);
//         const url = form.getAttribute('action');

//         fetch(url, {
//             method: 'POST',
//             body: formData,
//             headers: {
//                 'X-CSRFToken': formData.get('csrfmiddlewaretoken')
//             }
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.status === 'success') {
//                 // Ensure values are treated as numbers
//                 const subtotal = parseFloat(data.subtotal).toFixed(2);
//                 const total = parseFloat(data.total).toFixed(2);
//                 const grandTotal = parseFloat(data.grand_total).toFixed(2);

//                 // Update subtotal for the current item
//                 const subtotalCell = form.closest('tr').querySelector('.subtotal');
//                 if (subtotalCell) {
//                     subtotalCell.textContent = `$${subtotal}`;
//                 }

//                 // Update total and grand total
//                 const totalElement = document.querySelector('.total');
//                 const grandTotalElement = document.querySelector('.grand-total');
//                 if (totalElement) {
//                     totalElement.textContent = `$${total}`;
//                 }
//                 if (grandTotalElement) {
//                     grandTotalElement.textContent = `$${grandTotal}`;
//                 }
//             } else {
//                 alert('Failed to update the cart');
//             }
//         });
//     }
// });


document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.update-form');

    forms.forEach(form => {
        const decrementBtn = form.querySelector('.decrement-btn');
        const incrementBtn = form.querySelector('.increment-btn');
        const quantityInput = form.querySelector('.quantity-input');

        decrementBtn.addEventListener('click', () => {
            let currentQuantity = parseInt(quantityInput.value);
            if (currentQuantity > 1) {
                quantityInput.value = currentQuantity - 1;
                updateBag(form);
            }
        });

        incrementBtn.addEventListener('click', () => {
            let currentQuantity = parseInt(quantityInput.value);
            if (currentQuantity < 5) {
                quantityInput.value = currentQuantity + 1;
                updateBag(form);
            }
        });
    });

    function updateBag(form) {
        const formData = new FormData(form);
        const url = form.getAttribute('action');

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Ensure values are treated as numbers
                const subtotal = parseFloat(data.subtotal).toFixed(2);
                const total = parseFloat(data.total).toFixed(2);
                const grandTotal = parseFloat(data.grand_total).toFixed(2);

                // Update subtotal for the current item
                const subtotalCell = form.closest('tr').querySelector('.subtotal');
                if (subtotalCell) {
                    subtotalCell.textContent = `$${subtotal}`;
                }

                // Update total and grand total
                const totalElement = document.querySelector('.total');
                const grandTotalElement = document.querySelector('.grand-total');
                const mobileGrandTotalElement = document.getElementById('mobile-grand-total');

                if (totalElement) {
                    totalElement.textContent = `$${total}`;
                }
                if (grandTotalElement) {
                    grandTotalElement.textContent = `$${grandTotal}`;
                }
                if (mobileGrandTotalElement) {
                    mobileGrandTotalElement.textContent = `$${grandTotal}`;
                }
            } else {
                alert('Failed to update the cart');
            }
        });
    }
});
