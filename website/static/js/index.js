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