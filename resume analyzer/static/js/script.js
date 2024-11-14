document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[type="file"]');
    const uploadForm = document.querySelector('form');
    const feedback = document.createElement('p');
    feedback.style.color = 'red';
    feedback.style.display = 'none';
    uploadForm.appendChild(feedback);

    // Validate file type
    fileInput.addEventListener('change', function() {
        const file = fileInput.files[0];
        if (file && !['application/pdf', 'application/msword'].includes(file.type)) {
            feedback.textContent = "Please upload a PDF or DOC file.";
            feedback.style.display = 'block';
            fileInput.value = '';  // Clear the invalid file
        } else {
            feedback.style.display = 'none';
        }
    });

    // Show loading message on form submit
    uploadForm.addEventListener('submit', function() {
        const loadingMessage = document.createElement('p');
        loadingMessage.textContent = "Analyzing your resume, please wait...";
        loadingMessage.style.color = 'blue';
        uploadForm.appendChild(loadingMessage);
    });
});
