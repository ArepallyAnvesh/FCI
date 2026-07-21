// ==========================================================
// Farmer Consumer Interaction (FCI) - script.js
// Handles: mobile nav toggle, image preview on add/edit product,
// simple client-side form validation, delete confirmation.
// ==========================================================

document.addEventListener('DOMContentLoaded', function () {

    // ---------- Mobile nav toggle ----------
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function () {
            navLinks.classList.toggle('open');
        });
    }

    // ---------- Image preview for Add/Edit Product forms ----------
    const imageInput = document.getElementById('productImage');
    const imagePreview = document.getElementById('imagePreview');
    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function () {
            const file = imageInput.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // ---------- Delete confirmation ----------
    document.querySelectorAll('.confirm-delete').forEach(function (link) {
        link.addEventListener('click', function (e) {
            const ok = confirm('Are you sure you want to delete this product? This cannot be undone.');
            if (!ok) {
                e.preventDefault();
            }
        });
    });

    // ---------- Simple password match / required validation ----------
    const regForm = document.getElementById('registerForm');
    if (regForm) {
        regForm.addEventListener('submit', function (e) {
            const password = regForm.querySelector('[name="password"]');
            if (password && password.value.length < 4) {
                e.preventDefault();
                alert('Password must be at least 4 characters long.');
            }
        });
    }

    // ---------- Highlight active nav link ----------
    const currentPage = window.location.pathname.split('/').pop();
    document.querySelectorAll('.nav-links a').forEach(function (link) {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
});
