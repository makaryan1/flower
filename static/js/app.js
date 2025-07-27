
// Обработка ошибок JavaScript
window.addEventListener('unhandledrejection', function(event) {
    console.warn('Unhandled promise rejection:', event.reason);
    event.preventDefault();
});

// Добавляем обработчики для формы оформления заказа
document.addEventListener('DOMContentLoaded', function() {
    // Обработка способа оплаты
    const paymentMethodSelect = document.querySelector('select[name="payment"]');
    const bankSelect = document.querySelector('select[name="bank"]');
    const bankGroup = document.querySelector('.bank-group');

    if (paymentMethodSelect && bankSelect && bankGroup) {
        function toggleBankSelect() {
            if (paymentMethodSelect.value === 'online') {
                bankGroup.style.display = 'block';
                bankSelect.required = true;
            } else {
                bankGroup.style.display = 'none';
                bankSelect.required = false;
                bankSelect.value = '';
            }
        }

        paymentMethodSelect.addEventListener('change', toggleBankSelect);
        toggleBankSelect(); // Вызываем при загрузке страницы
    }

    // Обработка способа доставки
    const deliveryMethodSelect = document.querySelector('select[name="delivery"]');
    const districtGroup = document.querySelector('.district-group');

    if (deliveryMethodSelect && districtGroup) {
        function toggleDistrictSelect() {
            if (deliveryMethodSelect.value === 'pickup') {
                districtGroup.style.display = 'none';
            } else {
                districtGroup.style.display = 'block';
            }
        }

        deliveryMethodSelect.addEventListener('change', toggleDistrictSelect);
        toggleDistrictSelect();
    }

    // Обработка изменения количества в корзине
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.value < 1) {
                this.value = 1;
            }
        });
    });

    // Подтверждение очистки корзины
    const clearCartButton = document.querySelector('.clear-cart-btn');
    if (clearCartButton) {
        clearCartButton.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите очистить корзину?')) {
                e.preventDefault();
            }
        });
    }

    // Подтверждение удаления товара
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите удалить этот элемент?')) {
                e.preventDefault();
            }
        });
    });
});
