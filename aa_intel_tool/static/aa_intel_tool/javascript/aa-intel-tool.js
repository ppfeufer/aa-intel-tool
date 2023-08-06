jQuery(document).ready(($) => { // eslint-disable-line no-unused-vars
    'use strict';

    /**
     * Prevent double form submits
     */
    document.querySelectorAll('form').forEach((form) => {
        'use strict';

        form.addEventListener('submit', (e) => {
            // Prevent if already submitting
            if (form.classList.contains('is-submitting')) {
                e.preventDefault();
            }

            // Add class to hook our visual indicator on
            form.classList.add('is-submitting');
        });
    });
});
