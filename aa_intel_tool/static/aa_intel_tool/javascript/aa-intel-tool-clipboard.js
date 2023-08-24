/* global aaIntelToolJsL10n, ClipboardJS */

jQuery(document).ready(($) => {
    'use strict';

    const elementCopyToClipboard = $('button#btn-copy-permalink-to-clipboard');


    /**
     * Remove copy buttons if the browser doesn't support it
     */
    if (!ClipboardJS.isSupported()) {
        elementCopyToClipboard.remove();
    }


    /**
     * Closing the message
     *
     * @param {string} element
     * @param {int} closeAfter Close Message after given time in seconds (Default: 10)
     */
    const closeMessageElement = (element, closeAfter = 10) => {
        $(element).fadeTo(closeAfter * 1000, 500).slideUp(500, (elm) => {
            $(elm).slideUp(500, (el) => {
                $(el).remove();
            });
        });
    };


    /**
     * Show a message when copy action was successful
     *
     * @param {string} message
     * @param {string} element
     */
    const showSuccess = (message, element) => {
        $(element).html(
            '<div class="alert alert-success alert-dismissable alert-message-success">' +
            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + message +
            '</div>'
        );

        closeMessageElement('.alert-message-success');
    };


    /**
     * Show a message when copy action was not successful
     *
     * @param {string} message
     * @param {string} element
     */
    const showError = (message, element) => {
        $(element).html(
            '<div class="alert alert-danger alert-dismissable alert-message-error">' +
            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + message +
            '</div>'
        );

        closeMessageElement('.alert-message-error', 9999);
    };


    /**
     * Copy the scan link to clipboard
     *
     * @param elementId {string}
     */
    const copyScanLink = (elementId) => {
        /**
         * Copy text to clipboard
         *
         * @type Clipboard
         */
        const clipboardScanLink = new ClipboardJS(elementId);

        /**
         * Copy success
         *
         * @param {type} e
         */
        clipboardScanLink.on('success', (e) => {
            showSuccess(
                aaIntelToolJsL10n.copyToClipboard.permalink.text.success,
                '.aa-intel-copy-result'
            );

            e.clearSelection();
            clipboardScanLink.destroy();
        });

        /**
         * Copy error
         */
        clipboardScanLink.on('error', () => {
            showError(
                aaIntelToolJsL10n.copyToClipboard.permalink.text.error,
                '.aa-intel-copy-result'
            );

            clipboardScanLink.destroy();
        });
    };


    /**
     * Copy ping text
     */
    elementCopyToClipboard.click(() => {
        copyScanLink('#' + elementCopyToClipboard.attr('id'));
    });
});
