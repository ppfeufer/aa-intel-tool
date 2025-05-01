/* global aaIntelToolJsSettings, ClipboardJS, bootstrap */

/* jshint -W097 */
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
 * Bootstrap tooltip
 *
 * @param {string} selector The selector container for the tooltip
 */
const bootstrapTooltip = (selector = 'body') => { // eslint-disable-line no-unused-vars
    // Initialize Bootstrap tooltips
    [].slice.call(document.querySelectorAll(`${selector} [data-bs-tooltip="aa-intel-tool"]`))
        .map((tooltipTriggerEl) => {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
};


/**
 * Get the image HTML string for an Eve portrait or logo
 *
 * @param {int} eveId
 * @param {string} eveName
 * @param {string} imageSource
 * @param {int} imageSize
 * @returns {`<img class='eve-image rounded' data-eveid='${int}' src='${string}' alt='${string}' title='${string}' data-bs-tooltip='aa-intel-tool' loading='lazy' width='${int}' height='${int}'>`}
 */
const eveImageHtml = (eveId, eveName, imageSource, imageSize = 32) => {
    return `<img class="eve-image rounded" data-eveid="${eveId}" src="${imageSource}" alt="${eveName}" title="${eveName}" data-bs-tooltip="aa-intel-tool" loading="lazy" width="${imageSize}" height="${imageSize}">`;
};


/**
 * Get the link HTML to EveWho for a pilot
 *
 * @param {string} href
 * @returns {`<a class='aa-intel-information-link' href='${string}' target='_blank' rel='noopener noreferer'>evewho <sup><small><i class='fa-solid fa-external-link-alt' aria-hidden='true'></i></small></sup></a>`}
 */
const eveWhoLinkHtml = (href) => {
    return `<a class="aa-intel-information-link" href="${href}" target="_blank" rel="noopener noreferer">evewho <sup><small><i class="fa-solid fa-external-link-alt" aria-hidden="true"></i></small></sup></a>`;
};


/**
 * Get the link HTML to zKillboard
 *
 * @param {string} href
 * @returns {`<a class='aa-intel-information-link' href='${string}' target='_blank' rel='noopener noreferer'>zkillboard <sup><small><i class='fa-solid fa-external-link-alt' aria-hidden='true'></i></small></sup></a>`}
 */
const zkillboardLinkHtml = (href) => {
    return `<a class="aa-intel-information-link" href="${href}" target="_blank" rel="noopener noreferer">zkillboard <sup><small><i class="fa-solid fa-external-link-alt" aria-hidden="true"></i></small></sup></a>`;
};


/**
 * Get the link HTML to dotlan
 *
 * @param {string} href
 * @returns {`<a class='aa-intel-information-link' href='${string}' target='_blank' rel='noopener noreferer'>dotlan <sup><small><i class='fa-solid fa-external-link-alt' aria-hidden='true'></i></small></sup></a>`}
 */
const dotlanLinkHtml = (href) => {
    return `<a class="aa-intel-information-link" href="${href}" target="_blank" rel="noopener noreferer">dotlan <sup><small><i class="fa-solid fa-external-link-alt" aria-hidden="true"></i></small></sup></a>`;
};

/**
 * Info panel for the datatable
 *
 * @param {string} imageData
 * @param {string} eveData
 * @param {string} additionalInfo
 * @param {boolean} logoOnly Returns only the logo
 * @returns {string} HTML construct for the info panel
 */
const infoPanel = (
    imageData,
    eveData,
    additionalInfo = '',
    logoOnly = false
) => {
    const imageDataHtml = `<span class="aa-intel-eve-image-wrapper">${imageData}</span>`;

    if (logoOnly) {
        return imageDataHtml;
    }

    let eveDataHtml = `<span class="aa-intel-eve-information-wrapper"><span class="aa-intel-eve-name-wrapper">${eveData}</span>`;

    if (additionalInfo) {
        eveDataHtml += `<span class="aa-intel-additional-information-wrapper"><small>${additionalInfo}</small></span>`;
    } else {
        eveDataHtml += `</span>`;
    }

    return imageDataHtml + eveDataHtml;
};

/**
 * Pilot info element in datatable
 *
 * @param {Object} pilotData
 * @returns {string} HTML construct for the pilot info
 */
const pilotInfoPanel = (pilotData) => { // eslint-disable-line no-unused-vars
    const imageData = eveImageHtml(pilotData.id, pilotData.name, pilotData.portrait);
    const eveData = pilotData.name;
    const additionalInfo = `${eveWhoLinkHtml(pilotData.evewho)} | ${zkillboardLinkHtml(pilotData.zkillboard)}`;

    return infoPanel(imageData, eveData, additionalInfo);
};


/**
 * Corporation info element in datatable
 *
 * @param {Object} corporationData
 * @param {boolean} logoOnly Returns only the corporation logo
 * @returns {string} HTML construct for the corporation info
 */
const corporationInfoPanel = (corporationData, logoOnly = false) => { // eslint-disable-line no-unused-vars
    const imageData = eveImageHtml(corporationData.id, corporationData.name, corporationData.logo);
    const eveData = corporationData.name;
    let additionalInfo = '';

    if ((1000000 <= corporationData.id) && corporationData.id <= 2000000) {
        additionalInfo = `(${aaIntelToolJsSettings.translation.scanData.npcCorp})`;
    } else {
        additionalInfo = `${dotlanLinkHtml(corporationData.dotlan)} | ${zkillboardLinkHtml(corporationData.zkillboard)}`;
    }

    return infoPanel(imageData, eveData, additionalInfo, logoOnly);
};


/**
 * Alliance info element in datatable
 *
 * @param {Object} allianceData {object}
 * @param {boolean} logoOnly Returns only the alliance logo
 * @returns {string} HTML construct for the alliance info
 */
const allianceInfoPanel = (allianceData, logoOnly = false) => { // eslint-disable-line no-unused-vars
    if (allianceData.name === '') {
        allianceData.name = aaIntelToolJsSettings.translation.scanData.unaffiliated;
    }

    const imageData = eveImageHtml(allianceData.id, allianceData.name, allianceData.logo);
    const eveData = allianceData.name;
    let additionalInfo = aaIntelToolJsSettings.translation.scanData.noAlliance;

    if (allianceData.id > 1) {
        additionalInfo = `${dotlanLinkHtml(allianceData.dotlan)} | ${zkillboardLinkHtml(allianceData.zkillboard)}`;
    }

    if (logoOnly) {
        if (allianceData.id === 1) {
            return '';
        }
    }

    return infoPanel(imageData, eveData, additionalInfo, logoOnly);
};


/**
 * Ship/Item info element in datatable
 *
 * @param {Object} shipData
 * @returns {string} HTML construct for the ship info
 */
const shipInfoPanel = (shipData) => { // eslint-disable-line no-unused-vars
    const imageData = eveImageHtml(shipData.id, shipData.name, shipData.image);
    const eveData = shipData.name;

    return infoPanel(imageData, eveData);
};


$(() => {
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
        $(element).fadeTo(closeAfter * 1000, 500).slideUp(500, () => {
            $(element).remove();
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
            `<div class="alert alert-success alert-dismissible alert-message-success d-flex align-items-center fade show">${message}<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`
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
            `<div class="alert alert-danger alert-dismissible alert-message-error d-flex align-items-center fade show">${message}<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`
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
                aaIntelToolJsSettings.translation.copyToClipboard.permalink.text.success,
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
                aaIntelToolJsSettings.translation.copyToClipboard.permalink.text.error,
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
