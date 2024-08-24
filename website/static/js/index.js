// admin sidebar showing 

function showForm(formId) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        if (section.id === formId) {
            section.classList.remove('hidden');
            section.classList.add('active');
            section.classList.remove('slide-out-right');
            section.classList.add('slide-in-right');
        } else {
            section.classList.remove('active');
            section.classList.add('slide-out-right');
            section.classList.add('hidden');
        }
    });
}

// open the modal


function openModal() {
    document.getElementById('addHouseModal').classList.remove('hidden');
    document.getElementById('addHouseModal').classList.add('flex');
}

function closeModal() {
    document.getElementById('addHouseModal').classList.add('hidden');
    document.getElementById('addHouseModal').classList.remove('flex');
}

function openEditModal(propertyId) {
    // Optionally set the property ID or other state
    document.getElementById('edit-modal').classList.remove('hidden');
    document.getElementById('edit-modal').classList.add('flex');
}

function closeEditModal() {
    // Clear the form fields
    document.querySelectorAll('#edit-modal input').forEach(input => input.value = '');
    document.querySelectorAll('#edit-modal textarea').forEach(textarea => textarea.value = '');

    // Optionally, clear any state or URL parameters
    history.pushState(null, '', location.pathname);

    document.getElementById('edit-modal').classList.add('hidden');
    document.getElementById('edit-modal').classList.remove('flex');
}
