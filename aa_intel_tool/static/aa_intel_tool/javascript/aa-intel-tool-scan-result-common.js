/* global aaIntelToolJsL10n, ClipboardJS */

'use strict';

/**
 * Fetch data from an ajax URL
 *
 * @param {string} url
 * @returns {Promise<any>}
 */
const fetchAjaxData = async (url) => { // eslint-disable-line no-unused-vars
    return await fetch(url)
        .then(response => {
            if (response.ok) {
                return Promise.resolve(response);
            } else {
                return Promise.reject(new Error('Failed to load'));
            }
        })
        .then(response => response.json())
        .then(tableData => {
            return tableData;
        })
        .catch(function (error) {
            console.log(`Error: ${error.message}`);
        });
};


/**
 * Pilot info element in datatable
 *
 * @param {Object} pilotData
 * @returns {string}
 */
const pilotInfoPanel = (pilotData) => { // eslint-disable-line no-unused-vars
    let html_logo = '' +
        '<span class="aa-intel-pilot-avatar-wrapper">\n' +
        '    <img ' +
        '        class="eve-image" ' +
        '        data-eveid="' + pilotData.id + '" ' +
        '        src="' + pilotData.portrait + '" ' +
        '        alt="' + pilotData.name + '" ' +
        '        title="' + pilotData.name + '" ' +
        '        width="32" ' +
        '        height="32">\n' +
        '</span>';

    let html_info = '' +
        '<span class="aa-intel-pilot-information-wrapper">\n' +
        '    <span class="aa-intel-pilot-name-wrapper">\n' +
        '        ' + pilotData.name + '\n' +
        '    </span>\n';

    html_info += '' +
        '    <span class="aa-intel-pilot-links-wrapper">\n' +
        '        <small>\n' +
        '            <a ' +
        '                class="aa-intel-information-link" ' +
        '                href="' + pilotData.evewho + '" ' +
        '                target="_blank" ' +
        '                rel="noopener noreferer"' +
        '            >' +
        '               evewho <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
        '            </a> |\n' +

        '            <a ' +
        '                class="aa-intel-information-link" ' +
        '                href="' + pilotData.zkillboard + '" ' +
        '                target="_blank" rel="noopener noreferer"' +
        '            >' +
        '                zkillboard <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
        '            </a>\n' +
        '        </small>\n' +
        '    </span>\n';

    return html_logo + html_info;
};


/**
 * Corporation info element in datatable
 *
 * @param {Object} corporationData
 * @param {boolean} logoOnly Returns only the corporation logo
 * @returns {string}
 */
const corporationInfoPanel = (corporationData, logoOnly = false) => { // eslint-disable-line no-unused-vars
    let html_logo = '' +
        '<span class="aa-intel-corporation-logo-wrapper">\n' +
        '    <img ' +
        '        class="eve-image" ' +
        '        data-eveid="' + corporationData.id + '" ' +
        '        src="' + corporationData.logo + '" ' +
        '        alt="' + corporationData.name + '" ' +
        '        title="' + corporationData.name + '" ' +
        '        width="32" ' +
        '        height="32">\n' +
        '</span>';

    let html_info = '' +
        '<span class="aa-intel-corporation-information-wrapper">\n' +
        '    <span class="aa-intel-corporation-name-wrapper">\n' +
        '        ' + corporationData.name + '\n' +
        '    </span>\n';

    html_info += '' +
        '    <span class="aa-intel-corporation-links-wrapper">\n' +
        '        <small>\n';

    if ((1000000 <= corporationData.id) && corporationData.id <= 2000000) {
        html_info += '' +
            '            (' + aaIntelToolJsL10n.scanData.npcCorp + ')';
    } else {
        html_info += '' +
            '            <a ' +
            '                class="aa-intel-information-link" ' +
            '                href="' + corporationData.dotlan + '" ' +
            '                target="_blank" ' +
            '                rel="noopener noreferer"' +
            '            >' +
            '               dotlan <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
            '            </a> |\n' +

            '            <a ' +
            '                class="aa-intel-information-link" ' +
            '                href="' + corporationData.zkillboard + '" ' +
            '                target="_blank" rel="noopener noreferer"' +
            '            >' +
            '                zkillboard <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
            '            </a>\n' +
            '        </small>\n' +
            '    </span>\n';
    }

    html_info += '' +
        '</span>';

    if (logoOnly) {
        return html_logo;
    }

    return html_logo + html_info;
};


/**
 * Alliance info element in datatable
 *
 * @param {Object} allianceData {object}
 * @param {boolean} logoOnly Returns only the alliance logo
 * @returns {string}
 */
const allianceInfoPanel = (allianceData, logoOnly = false) => { // eslint-disable-line no-unused-vars
    if (allianceData.name === '') {
        allianceData.name = aaIntelToolJsL10n.scanData.empty;
    }

    let html_logo = '' +
        '<span class="aa-intel-alliance-logo-wrapper alliance-id-' + allianceData.id + '">\n' +
        '    <img ' +
        '        class="eve-image" ' +
        '        data-eveid="' + allianceData.id + '" ' +
        '        src="' + allianceData.logo + '" ' +
        '        alt="' + allianceData.name + '" ' +
        '        title="' + allianceData.name + '" ' +
        '        width="32" ' +
        '        height="32">\n' +
        '</span>';

    let html_info = '' +
        '<span class="aa-intel-alliance-information-wrapper">\n' +
        '    <span class="aa-intel-alliance-name-wrapper">\n' +
        '        ' + allianceData.name + '\n' +
        '    </span>\n';

    if (allianceData.id > 1) {
        html_info += '' +
            '    <span class="aa-intel-alliance-links-wrapper">\n' +
            '        <small>\n' +
            '            <a ' +
            '                class="aa-intel-information-link" ' +
            '                href="' + allianceData.dotlan + '" ' +
            '                target="_blank" ' +
            '                rel="noopener noreferer"' +
            '            >' +
            '               dotlan <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
            '            </a> |\n' +

            '            <a ' +
            '                class="aa-intel-information-link" ' +
            '                href="' + allianceData.zkillboard + '" ' +
            '                target="_blank" rel="noopener noreferer"' +
            '            >' +
            '                zkillboard <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
            '            </a>\n' +
            '        </small>\n' +
            '    </span>\n';
    }

    html_info += '' +
        '</span>';

    if (logoOnly) {
        if (allianceData.id === 1) {
            return '';
        }

        return html_logo;
    }

    return html_logo + html_info;
};


/**
 * Ship/Item info element in datatable
 *
 * @param {Object} shipData
 * @returns {string}
 */
const shipInfoPanel = (shipData) => { // eslint-disable-line no-unused-vars
    let html_logo = '' +
        '<span class="aa-intel-ship-image-wrapper">\n' +
        '    <img ' +
        '        class="eve-image" ' +
        '        data-eveid="' + shipData.id + '" ' +
        '        src="' + shipData.image + '" ' +
        '        alt="' + shipData.name + '" ' +
        '        title="' + shipData.name + '" ' +
        '        width="32" ' +
        '        height="32">\n' +
        '</span>';

    let html_info = '' +
        '<span class="aa-intel-ship-information-wrapper">\n' +
        '    <span class="aa-intel-ship-name-wrapper">\n' +
        '        ' + shipData.name + '\n' +
        '    </span>\n' +
        '</span>\n';

    return html_logo + html_info;
};


jQuery(document).ready(($) => {
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
     * @param {string} elementId The HTML-element ID
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
