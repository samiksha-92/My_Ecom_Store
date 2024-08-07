console.log("bag.js loaded");

document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.update-form');
    const removeForms = document.querySelectorAll('.remove-form');

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

        // Ensure the quantity input manually changes trigger update
        quantityInput.addEventListener('change', () => {
            updateBag(form);
        });
    });

    removeForms.forEach(form => {
        const removeBtn = form.querySelector('.remove-btn');
        removeBtn.addEventListener('click', () => {
            console.log('Remove button clicked');
            removeFromBag(form);
        });
    });

    function updateBag(form) {
        const formData = new FormData(form);
        const url = form.getAttribute('action');
        const productId = formData.get('product_id');
        console.log('Updating product with ID:', productId);

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Update response:', data);
            console.log('Product ID:', productId);

            const subtotalElement = document.querySelector(`#subtotal-${productId}`);
            console.log('Subtotal element:', subtotalElement);
            if (subtotalElement) {
                subtotalElement.innerText = `$${parseFloat(data.subtotal).toFixed(2)}`;
            } else {
                console.error(`Element with ID #subtotal-${productId} not found`);
            }

            const bagTotalElement = document.getElementById('bag-total');
            if (bagTotalElement) {
                bagTotalElement.innerText = `$${parseFloat(data.total).toFixed(2)}`;
            } else {
                console.error('Element with ID #bag-total not found');
            }

            const grandTotalElement = document.getElementById('grand-total');
            if (grandTotalElement) {
                grandTotalElement.innerText = `$${parseFloat(data.grand_total).toFixed(2)}`;
            } else {
                console.error('Element with ID #grand-total not found');
            }
        })
        .catch(error => {
            console.error('Error updating bag:', error);
        });
    }

    function removeFromBag(form) {
        const formData = new FormData(form);
        const url = form.getAttribute('action');
        const productId = formData.get('product_id');
        console.log('Removing product with ID:', productId);

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Remove response:', data);
            if (data.status === 'success') {
                const itemRow = form.closest('tr');
                if (itemRow) {
                    itemRow.remove();
                }
                const bagTotalElement = document.getElementById('bag-total');
                if (bagTotalElement) {
                    bagTotalElement.innerText = `$${parseFloat(data.total).toFixed(2)}`;
                } else {
                    console.error('Element with ID #bag-total not found');
                }

                const grandTotalElement = document.getElementById('grand-total');
                if (grandTotalElement) {
                    grandTotalElement.innerText = `$${parseFloat(data.grand_total).toFixed(2)}`;
                } else {
                    console.error('Element with ID #grand-total not found');
                }
            } else {
                alert('Failed to remove the item');
            }
        })
        .catch(error => {
            console.error('Error removing from bag:', error);
        });
    }
});
