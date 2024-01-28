document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("disease-identification-form");
    const plantDropdown = document.getElementById("plants");
    const fileInput = document.getElementById('file-input');
    const imgView = document.getElementById('img-view');

    // Add event listeners for drag and drop
    imgView.addEventListener('dragover', handleDragOver);
    imgView.addEventListener('drop', handleFileDrop);

    // Add event listener for manual file selection
    fileInput.addEventListener('change', handleFileSelect);

    form.addEventListener("submit", (event) => {
        if (plantDropdown.value === "default") {
            alert("Please select a plant.");
            event.preventDefault();
        }

        if (fileInput.files.length === 0) {
            alert("Please upload an image.");
            event.preventDefault();
        } else {
            const allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
            if (!allowedExtensions.exec(fileInput.value)) {
                alert('Please upload a file with a valid format (PNG or JPG).');
                event.preventDefault();
            }
        }
    });

    // Handle file drag and drop
    function handleDragOver(event) {
        event.preventDefault();
        event.dataTransfer.dropEffect = 'copy';
    }

    function handleFileDrop(event) {
        event.preventDefault();
        const files = event.dataTransfer.files;

        if (files.length > 0) {
            const file = files[0];
            displayImage(file);
            // If you want to submit the form immediately on drop, uncomment the following line:
            form.submit();
        }
    }

    // Handle manual file selection
    function handleFileSelect(event) {
        const files = event.target.files;
        if (files.length > 0) {
            const file = files[0];
            displayImage(file);
        }
    }

    // Display the dropped or selected image
    function displayImage(file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.classList.add('avatar-icon');
            imgView.innerHTML = ''; // Clear previous content
            imgView.appendChild(img);
        };

        reader.readAsDataURL(file);
    }
});