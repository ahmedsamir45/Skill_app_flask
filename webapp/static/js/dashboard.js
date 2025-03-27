document.addEventListener("DOMContentLoaded", function() {
    // Initialize modal and cropper
    const imageCropModal = new bootstrap.Modal(document.getElementById('imageCropModal'));
    let cropper;
    
    // Image upload handler
    document.getElementById('imageUpload').addEventListener('change', function(e) {
        const files = e.target.files;
        if (files && files.length > 0) {
            const file = files[0];
            if (!file.type.match('image.*')) {
                alert('Please select an image file (JPEG, PNG, etc.)');
                return;
            }
            
            const reader = new FileReader();
            reader.onload = function(event) {
                document.getElementById('imagePreview').src = event.target.result;
                imageCropModal.show();
                
                // Initialize cropper after modal is shown
                imageCropModal._element.addEventListener('shown.bs.modal', function() {
                    if (cropper) {
                        cropper.destroy();
                    }
                    
                    cropper = new Cropper(document.getElementById('imagePreview'), {
                        aspectRatio: 1,
                        viewMode: 1,
                        autoCropArea: 0.8,
                        responsive: true,
                        rotatable: true,
                        scalable: true,
                        zoomable: true,
                        minContainerWidth: 500,
                        minContainerHeight: 400
                    });
                }, { once: true });
            };
            reader.readAsDataURL(file);
        }
    });
    
    // Crop button handler
    document.getElementById('cropImageBtn').addEventListener('click', function() {
        if (cropper) {
            const canvas = cropper.getCroppedCanvas({
                width: 400,
                height: 400,
                minWidth: 200,
                minHeight: 200,
                fillColor: '#fff',
                imageSmoothingEnabled: true,
                imageSmoothingQuality: 'high'
            });
            
            if (canvas) {
                const croppedImageUrl = canvas.toDataURL('image/jpeg');
                document.getElementById('croppedPreview').src = croppedImageUrl;
                document.getElementById('croppedImageData').value = croppedImageUrl;
                document.getElementById('imagePreviewContainer').style.display = 'block';
                imageCropModal.hide();
                
                // Update the current profile image preview
                document.getElementById('currentProfileImage').src = croppedImageUrl;
            }
        }
    });
    
    // Clean up when modal is closed
    imageCropModal._element.addEventListener('hidden.bs.modal', function() {
        if (cropper) {
            cropper.destroy();
        }
    });
});

console.log('dashboard')




document.addEventListener("DOMContentLoaded", function() {
    // Initialize CKEditor with basic configuration
    CKEDITOR.replace('jobDescription', {
        toolbar: [
            { name: 'basicstyles', items: ['Bold', 'Italic', 'Underline', 'Strike', '-', 'RemoveFormat'] },
            { name: 'paragraph', items: ['NumberedList', 'BulletedList', '-', 'Blockquote'] },
            { name: 'links', items: ['Link', 'Unlink'] },
            { name: 'tools', items: ['Maximize'] }
        ],
        height: 200,
        removeButtons: 'Styles,Font,FontSize',
        disallowedContent: 'script; *[on*]',
        basicEntities: false,
        autoParagraph: false,
        removePlugins: 'flash,iframe,forms'
    });

    // Basic HTML sanitization before form submission
    document.getElementById('jobPostForm').addEventListener('submit', function() {
        var editor = CKEDITOR.instances.jobDescription;
        var html = editor.getData();
        // Simple client-side sanitization (server-side is still required)
        var cleanHtml = html.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
                           .replace(/ on\w+="[^"]*"/g, '')
                           .replace(/javascript:/gi, '');
        editor.setData(cleanHtml);
    });

    // Rest of your existing JavaScript
});