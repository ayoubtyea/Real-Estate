document.addEventListener('DOMContentLoaded', function () {
    const burger = document.querySelector('.navbar-burger');
    const menu = document.querySelector('.navbar-menu');
    const close = document.querySelector('.navbar-close');
    const backdrop = document.querySelector('.navbar-backdrop');

    burger.addEventListener('click', function () {
        menu.classList.toggle('hidden');
        backdrop.classList.toggle('hidden');
    });

    close.addEventListener('click', function () {
        menu.classList.add('hidden');
        backdrop.classList.add('hidden');
    });

    backdrop.addEventListener('click', function () {
        menu.classList.add('hidden');
        backdrop.classList.add('hidden');
    });
});

// Cards 
const state = {};
const carouselList = document.querySelector('.carousel__list');
const carouselItems = document.querySelectorAll('.carousel__item');
const elems = Array.from(carouselItems);

carouselList.addEventListener('click', function (event) {
    var newActive = event.target;
    var isItem = newActive.closest('.carousel__item');

    if (!isItem || newActive.classList.contains('carousel__item_active')) {
        return;
    };

    update(newActive);
});

const update = function (newActive) {
    const newActivePos = newActive.dataset.pos;

    const current = elems.find((elem) => elem.dataset.pos == 0);
    const prev = elems.find((elem) => elem.dataset.pos == -1);
    const next = elems.find((elem) => elem.dataset.pos == 1);
    const first = elems.find((elem) => elem.dataset.pos == -2);
    const last = elems.find((elem) => elem.dataset.pos == 2);

    current.classList.remove('carousel__item_active');

    [current, prev, next, first, last].forEach(item => {
        var itemPos = item.dataset.pos;

        item.dataset.pos = getPos(itemPos, newActivePos)
    });
};

const getPos = function (current, active) {
    const diff = current - active;

    if (Math.abs(current - active) > 2) {
        return -current
    }

    return diff;
}


// SLIDE PAGE
function toggleSlideover() {
    document.getElementById('slideover-container').classList.toggle('invisible');
    document.getElementById('slideover-bg').classList.toggle('opacity-0');
    document.getElementById('slideover-bg').classList.toggle('opacity-50');
    document.getElementById('slideover').classList.toggle('translate-x-full');
}


document.addEventListener("DOMContentLoaded", function () {
    const carouselItems = document.querySelectorAll('.carousel__item');
    carouselItems.forEach((item, index) => {
        setTimeout(() => {
            item.classList.add('animate-move-up');
        }, index * 500);
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const carouselItem = document.querySelector('.carousel__item');
    carouselItem.classList.add('animate-move-right');
});

$(document).ready(function () {
    $('select').change(function () {
        var bedrooms = $('select:eq(0)').val();
        var bathrooms = $('select:eq(1)').val();
        var floors = $('select:eq(2)').val();
        var waterfront = $('select:eq(3)').val();

        $.ajax({
            url: '/predict',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                bedrooms: bedrooms,
                bathrooms: bathrooms,
                floors: floors,
                waterfront: waterfront
            }),
            success: function (response) {
                $('.price button').text(response.predicted_price.toFixed(2) + ' $');
            }
        });
    });
});

// Drop DOWN 

function toggleDropdown() {
    document.getElementById('dropdownMenu').classList.toggle('hidden');
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('.relative button')) {
        var dropdowns = document.getElementsByClassName('dropdown-content');
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (!openDropdown.classList.contains('hidden')) {
                openDropdown.classList.add('hidden');
            }
        }
    }
}


// who we are image handle 
document.addEventListener('DOMContentLoaded', function () {
    const menuIcon = document.getElementById('menu-icon');
    const closeMenu = document.getElementById('close-menu');
    const mobileMenu = document.getElementById('mobile-menu');

    menuIcon.addEventListener('click', function () {
        mobileMenu.style.display = 'flex';
    });

    closeMenu.addEventListener('click', function () {
        mobileMenu.style.display = 'none';
    });
});

let text = new SplitType('#text');
let characters = document.querySelectorAll('.char');

for (i = 0; i < characters.length; i++) {
    characters[i].classList.add('translate-y-full');
}
gsap.to('.char', {
    y: 0,
    stagger: 0.05,
    delay: 0.01,
    duration: 0.5
});


// search for offers 

document.getElementById('category-filter').addEventListener('change', function () {
    const selectedCategory = this.value;
    const propertyCards = document.querySelectorAll('.property-card');

    propertyCards.forEach(card => {
        const cardCategory = card.getAttribute('data-category');
        if (selectedCategory === 'all' || cardCategory === selectedCategory) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});


// request button 
document.addEventListener('DOMContentLoaded', function () {
    const requestButton = document.querySelector('#request-property-button'); // Make sure this ID matches your button
    const ordersTableBody = document.querySelector('#orders-table-body');

    requestButton.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the form from submitting

        // Gather property information
        const propertyTitle = "{{ property.title }}";
        const propertyId = "{{ property.id }}"; // Assuming you have the property ID
        const propertyPrice = "{{ property.current_price }}";
        const propertyLocation = "{{ property.location }}";
        const propertyCategory = "{{ property.category }}";

        // Create a new table row
        const newRow = document.createElement('tr');

        newRow.innerHTML = `
            <td class="py-4 px-6">
                <div class="flex items-center">
                    <img src="{{ url_for('static', filename='images/Dash.png') }}" alt="Property Icon" class="h-8 w-8 mr-2">
                </div>
            </td>
            <td class="py-4 px-6">${propertyTitle}</td>
            <td class="py-4 px-6">${propertyId}</td>
            <td class="py-4 px-6">$${propertyPrice}</td>
            <td class="py-4 px-6">${propertyLocation}</td>
            <td class="py-4 px-6">${propertyCategory}</td>
        `;

        // Append the new row to the table body
        ordersTableBody.appendChild(newRow);

        // Optionally, make the #orders-form visible
        const ordersForm = document.querySelector('#orders-form');
        ordersForm.classList.remove('hidden'); // Remove the hidden class
    });
});

// showing profile form 
function showForm(formId) {
    const forms = document.querySelectorAll('#form-container form');
    forms.forEach(form => {
        form.classList.add('slide-out-right');
        form.classList.add('hidden');
    });

    const selectedForm = document.getElementById(`${formId}-form`);
    selectedForm.classList.remove('slide-out-right');
    selectedForm.classList.remove('hidden');
    selectedForm.classList.add('slide-in-right');

    // Special handling for orders form to show it
    if (formId === 'orders') {
        const ordersForm = document.getElementById('orders-form');
        ordersForm.classList.remove('hidden');
    } else {
        const ordersForm = document.getElementById('orders-form');
        ordersForm.classList.add('hidden');
    }
}

function toggleDropdown() {
    document.getElementById('dropdownMenu').classList.toggle('hidden');
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('.relative button')) {
        var dropdowns = document.getElementsByClassName('dropdown-content');
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (!openDropdown.classList.contains('hidden')) {
                openDropdown.classList.add('hidden');
            }
        }
    }
    // flash meessage 
    document.addEventListener('DOMContentLoaded', (event) => {
        const flashMessages = document.querySelectorAll('.flash-message');
        flashMessages.forEach((msg) => {
            setTimeout(() => {
                msg.classList.add('hide');
                setTimeout(() => {
                    msg.remove();
                }, 500); // Wait for the transition to complete before removing the element
            }, 3000); // 3 seconds before fade out
        });
    });
}

// request informations 
function validateForm() {
    let name = document.getElementById("name").value.trim();
    let email = document.getElementById("email").value.trim();
    let message = document.getElementById("message").value.trim();

    if (name === "" || email === "" || message === "") {
        alert("Please fill out all fields before submitting.");
        return false;
    }

    // Email pattern validation
    let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        alert("Please enter a valid email address.");
        return false;
    }

    return true;  // Allow form submission
}

// manage properties smothly hidden 
function openModal() {
    document.getElementById('addHouseModal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('addHouseModal').classList.add('hidden');
}


// const form = document.getElementById('ai-form');
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('ai-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default form submission

        const formData = new FormData(form);
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                if (result.price) {
                    // Update the price input field
                    document.getElementById('predicted-price').value = result.price.toFixed(2) + ' $';

                    // Scroll smoothly to the AI section to avoid any jump
                    document.getElementById('ai').scrollIntoView({ behavior: 'smooth' });
                } else if (result.error) {
                    console.error('Prediction error:', result.error);
                }
            } else {
                console.error('Failed to fetch prediction');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
});
