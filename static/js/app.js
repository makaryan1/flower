
// FlowerShop Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavbar();
    initCart();
    initForms();
    initModals();
    initAnimations();
});

// Navbar functionality
function initNavbar() {
    const navbar = document.querySelector('.modern-nav');
    if (!navbar) return;

    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Mobile menu handling
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            const navbarCollapse = document.querySelector('.navbar-collapse');
            if (navbarCollapse) {
                navbarCollapse.classList.toggle('show');
            }
        });
    }
}

// Cart functionality
function initCart() {
    // Update cart count
    updateCartCount();
    
    // Cart quantity controls
    const quantityControls = document.querySelectorAll('.quantity-control');
    quantityControls.forEach(control => {
        control.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input[type="number"]');
            const action = this.dataset.action;
            let currentValue = parseInt(input.value) || 0;
            
            if (action === 'increase') {
                input.value = currentValue + 1;
            } else if (action === 'decrease' && currentValue > 1) {
                input.value = currentValue - 1;
            }
            
            // Auto-submit form after change
            const form = input.closest('form');
            if (form) {
                form.submit();
            }
        });
    });
}

// Update cart count in navbar
function updateCartCount() {
    const cartItems = JSON.parse(sessionStorage.getItem('cart_items') || '{}');
    const cartCount = Object.values(cartItems).reduce((total, qty) => total + qty, 0);
    const cartBadge = document.querySelector('.cart-count');
    if (cartBadge) {
        cartBadge.textContent = cartCount;
        cartBadge.style.display = cartCount > 0 ? 'inline' : 'none';
    }
}

// Form enhancements
function initForms() {
    // Add form validation feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Пожалуйста, заполните все обязательные поля', 'error');
            }
        });
    });

    // Auto-format phone numbers
    const phoneInputs = document.querySelectorAll('input[type="tel"], input[name*="phone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.startsWith('995')) {
                value = '+' + value;
            }
            this.value = value;
        });
    });

    // Checkout form enhancements
    const checkoutForm = document.getElementById('checkout-form');
    if (checkoutForm) {
        const districtSelect = checkoutForm.querySelector('[name="district"]');
        const paymentMethodSelect = checkoutForm.querySelector('[name="payment"]');
        const bankSelect = checkoutForm.querySelector('[name="bank"]');

        if (districtSelect) {
            districtSelect.addEventListener('change', updateDeliveryPrice);
        }

        if (paymentMethodSelect && bankSelect) {
            paymentMethodSelect.addEventListener('change', function() {
                const bankGroup = bankSelect.closest('.form-group, .mb-3');
                if (this.value === 'online') {
                    bankGroup.style.display = 'block';
                    bankSelect.setAttribute('required', 'required');
                } else {
                    bankGroup.style.display = 'none';
                    bankSelect.removeAttribute('required');
                }
            });
        }
    }
}

// Update delivery price based on district
function updateDeliveryPrice() {
    const districtSelect = document.querySelector('[name="district"]');
    const priceElement = document.getElementById('delivery-price');
    const finalPriceElement = document.getElementById('final-price');
    
    if (!districtSelect || !priceElement) return;
    
    const selectedOption = districtSelect.options[districtSelect.selectedIndex];
    const price = selectedOption.text.includes('5₾') ? 5 : 10;
    
    priceElement.textContent = `₾${price}`;
    
    // Update final price
    if (finalPriceElement) {
        const basePrice = parseFloat(finalPriceElement.dataset.basePrice || 0);
        finalPriceElement.textContent = `₾${basePrice + price}`;
    }
}

// Modal functionality
function initModals() {
    // Product quick view modals
    const quickViewButtons = document.querySelectorAll('[data-bs-toggle="modal"]');
    quickViewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            if (productId) {
                loadProductModal(productId);
            }
        });
    });
}

// Load product data into modal
function loadProductModal(productId) {
    fetch(`/api/product/${productId}`)
        .then(response => response.json())
        .then(data => {
            const modal = document.getElementById('productModal');
            if (modal) {
                modal.querySelector('.product-name').textContent = data.name;
                modal.querySelector('.product-description').textContent = data.description;
                modal.querySelector('.product-price').textContent = `₾${data.price}`;
                const img = modal.querySelector('.product-image');
                if (img && data.image_url) {
                    img.src = data.image_url;
                    img.alt = data.name;
                }
            }
        })
        .catch(error => {
            console.error('Error loading product:', error);
            showNotification('Ошибка загрузки товара', 'error');
        });
}

// Animations and effects
function initAnimations() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Fade in animation for cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card, .product-card').forEach(card => {
        observer.observe(card);
    });
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show notification`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to page
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(notification, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Search functionality
function initSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchButton = document.querySelector('.search-button');
    
    if (searchInput && searchButton) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                performSearch(this.value);
            }
        });
        
        searchButton.addEventListener('click', function() {
            performSearch(searchInput.value);
        });
    }
}

function performSearch(query) {
    if (query.trim()) {
        window.location.href = `/catalog?search=${encodeURIComponent(query)}`;
    }
}

// Language switcher
function switchLanguage(lang) {
    fetch(`/set_language/${lang}`)
        .then(() => {
            window.location.reload();
        })
        .catch(error => {
            console.error('Error switching language:', error);
        });
}

// Export functions for global use
window.FlowerShop = {
    showNotification,
    updateCartCount,
    switchLanguage,
    performSearch
};
