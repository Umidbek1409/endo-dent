/**
 * Dental Clinic - Admin Image Preview
 *
 * This script adds live image preview functionality to all file input
 * fields in the Django admin panel. When a user selects an image file,
 * a preview thumbnail appears directly below the input field.
 *
 * Loaded via the Media class in each ModelAdmin that has image fields.
 */

// Wait for the DOM to be fully loaded before attaching event listeners
document.addEventListener('DOMContentLoaded', function () {
    /**
     * Find all file input fields that are used for image uploads in the admin.
     * These inputs typically have a change event we can listen to.
     */
    var fileInputs = document.querySelectorAll('input[type="file"][accept*="image"], input[type="file"]');

    /**
     * Loop through each file input and attach a change event listener.
     * The listener reads the selected file and displays a preview image.
     */
    fileInputs.forEach(function (input) {
        /**
         * When the user selects a new file, this function is triggered.
         * It reads the file using FileReader and creates a preview <img> element.
         */
        input.addEventListener('change', function (e) {
            // Get the first selected file from the input
            var file = e.target.files[0];

            // If no file is selected (user cancelled), remove any existing preview
            if (!file) {
                removePreview(input);
                return;
            }

            // Check if the selected file is an image type
            if (!file.type.startsWith('image/')) {
                return; // Skip non-image files
            }

            // Create a FileReader to read the file as a data URL
            var reader = new FileReader();

            /**
             * When the file is successfully read, this callback creates
             * an <img> element and inserts it below the file input.
             */
            reader.onload = function (event) {
                // Remove any existing preview for this input first
                removePreview(input);

                // Create a new <img> element for the preview
                var img = document.createElement('img');
                // Set the image source to the data URL read by FileReader
                img.src = event.target.result;
                // Style the preview image with appropriate sizing and rounded corners
                img.style.cssText = 'max-width: 200px; max-height: 200px; margin-top: 10px; border-radius: 8px; border: 2px solid #e2e8f0; display: block;';
                // Add a class for potential CSS targeting
                img.className = 'admin-image-preview';

                // Insert the preview image directly after the file input element
                input.parentNode.insertBefore(img, input.nextSibling);
            };

            // Read the file as a Data URL (base64-encoded string)
            reader.readAsDataURL(file);
        });
    });

    /**
     * Helper function: removes any existing preview image associated with a file input.
     * Looks for the next sibling <img> element with the preview class and removes it.
     *
     * @param {HTMLElement} input - The file input element
     */
    function removePreview(input) {
        // Check if the next sibling is an existing preview image
        var nextEl = input.nextElementSibling;
        // If it's an img with our preview class, remove it from the DOM
        if (nextEl && nextEl.tagName === 'IMG' && nextEl.classList.contains('admin-image-preview')) {
            nextEl.parentNode.removeChild(nextEl);
        }
    }
});
