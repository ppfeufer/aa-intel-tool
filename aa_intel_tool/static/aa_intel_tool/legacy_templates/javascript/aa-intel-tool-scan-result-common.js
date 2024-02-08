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
 * Get the image HTML string for an Eve portrait or logo
 *
 * @param {int} eveId
 * @param {string} eveName
 * @param {string} imageSource
 * @param {int} imageSize
 * @returns {string} `<img class="eve-image" data-eveid="${eveId}" src="${imageSource}" alt="${eveName}" title="${eveName}" loading="lazy" width="${imageSize}" height="${imageSize}">`
 */
const eveImageHtml = (eveId, eveName, imageSource, imageSize = 32) => {
    return `<img class="eve-image" data-eveid="${eveId}" src="${imageSource}" alt="${eveName}" title="${eveName}" loading="lazy" width="${imageSize}" height="${imageSize}">`;
};


/**
 * Get the link HTML to EveWho for a pilot
 *
 * @param {string} href
 * @returns {string} `<a class="aa-intel-information-link" href="${href}" target="_blank" rel="noopener noreferer">evewho <i class="fas fa-external-link-alt" aria-hidden="true"></i></a>`
 */
const eveWhoLinkHtml = (href) => {
    return `<a class="aa-intel-information-link" href="${href}" target="_blank" rel="noopener noreferer">evewho <i class="fas fa-external-link-alt" aria-hidden="true"></i></a>`;
};


/**
 * Get the link HTML to zKillboard
 *
 * @param {string} href
 * @returns {string} `<a class="aa-intel-information-link" href="${href}" target="_blank" rel="noopener noreferer">zkillboard <i class="fas fa-external-link-alt" aria-hidden="true"></i></a>`
 */
const zkillboardLinkHtml = (href) => {
    return `<a class="aa-intel-information-link" href="${href}" target="_blank" rel="noopener noreferer">zkillboard <i class="fas fa-external-link-alt" aria-hidden="true"></i></a>`;
};


/**
 * Get the link HTML to dotlan
 *
 * @param {string} href
 * @returns {string} `<a class="aa-intel-information-link" href="${href}" target="_blank" rel="noopener noreferer">dotlan <i class="fas fa-external-link-alt" aria-hidden="true"></i></a>`
 */
const dotlanLinkHtml = (href) => {
    return `<a class="aa-intel-information-link" href="${href}" target="_blank" rel="noopener noreferer">dotlan <i class="fas fa-external-link-alt" aria-hidden="true"></i></a>`;
};


/**
 * Pilot info element in datatable
 *
 * @param {Object} pilotData
 * @returns {string}
 */
const pilotInfoPanel = (pilotData) => { // eslint-disable-line no-unused-vars
    const html_logo = `<span class="aa-intel-pilot-avatar-wrapper">${eveImageHtml(pilotData.id, pilotData.name, pilotData.portrait)}</span>`;
    let html_info = `<span class="aa-intel-pilot-information-wrapper"><span class="aa-intel-pilot-name-wrapper">${pilotData.name}</span>`;
    html_info += `<span class="aa-intel-pilot-links-wrapper"><small>${eveWhoLinkHtml(pilotData.evewho)} | ${zkillboardLinkHtml(pilotData.zkillboard)}</small></span>`;

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
    const html_logo = `<span class="aa-intel-corporation-logo-wrapper">${eveImageHtml(corporationData.id, corporationData.name, corporationData.logo)}</span>`;
    let html_info = `<span class="aa-intel-corporation-information-wrapper"><span class="aa-intel-corporation-name-wrapper">${corporationData.name}</span>`;
    html_info += `<span class="aa-intel-corporation-links-wrapper"><small>`;

    if ((1000000 <= corporationData.id) && corporationData.id <= 2000000) {
        html_info += `(${aaIntelToolJsL10n.scanData.npcCorp})`;
    } else {
        html_info += `${dotlanLinkHtml(corporationData.dotlan)} | ${zkillboardLinkHtml(corporationData.zkillboard)}</small></span>`;
    }

    html_info += `</span>`;

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

    const html_logo = `<span class="aa-intel-corporation-logo-wrapper">${eveImageHtml(allianceData.id, allianceData.name, allianceData.logo)}</span>`;
    let html_info = `<span class="aa-intel-alliance-information-wrapper"><span class="aa-intel-alliance-name-wrapper">${allianceData.name}</span>`;

    if (allianceData.id > 1) {
        html_info += `<span class="aa-intel-alliance-links-wrapper"><small>${dotlanLinkHtml(allianceData.dotlan)} | ${zkillboardLinkHtml(allianceData.zkillboard)}</small></span>`;
    }

    html_info += `</span>`;

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
    const html_logo = `<span class="aa-intel-ship-image-wrapper">${eveImageHtml(shipData.id, shipData.name, shipData.image)}</span>`;
    const html_info = `<span class="aa-intel-ship-information-wrapper"><span class="aa-intel-ship-name-wrapper">${shipData.name}</span></span>`;

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
            `<div class="alert alert-success alert-dismissable alert-message-success"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>${message}</div>`
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
            `<div class="alert alert-danger alert-dismissable alert-message-error"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>${message}</div>`
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
