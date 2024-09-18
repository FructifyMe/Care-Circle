// Add any client-side JavaScript functionality here
console.log('Care Circle application loaded');

// Add date picker functionality to date input fields
document.addEventListener('DOMContentLoaded', function() {
    const dateInputs = document.querySelectorAll('input[type="datetime-local"]');
    dateInputs.forEach(input => {
        // You can add a date picker library here if needed
        console.log('Date input initialized:', input);
    });

    // Image preview functionality
    const imageInput = document.querySelector('input[type="file"]');
    const imagePreview = document.createElement('img');
    imagePreview.style.display = 'none';
    imagePreview.style.maxWidth = '100%';
    imagePreview.style.marginTop = '10px';
    
    if (imageInput) {
        imageInput.parentNode.insertBefore(imagePreview, imageInput.nextSibling);

        imageInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                }
                reader.readAsDataURL(file);
            } else {
                imagePreview.style.display = 'none';
            }
        });
    }
});
