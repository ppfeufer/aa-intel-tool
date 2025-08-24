/* global _getAaIntelToolJsSettings, ClipboardJS, bootstrap, addFleetcompositionHighlight, removeFleetcompositionHighlight, changeFleetcompositionStickyHighlight, addDscanHighlight, removeDscanHighlight, changeDscanStickyHighlight, addChatscanHighlight, removeChatscanHighlight, changeChatscanStickyHighlight */

/* jshint -W097 */
'use strict';

const aaIntelToolJsSettings = _getAaIntelToolJsSettings();

/**
 * Toggle sticky highlight for scan results
 *
 * @param {jQuery|Element} element The element to attach the events to
 * @param {string} type The type of the element (shipclass or shiptype)
 * @param {string} scanType The scan type (fleetcomposition, dscan, or chatscan)
 * @param {string} [excludeLinkElement=aa-intel-information-link] The class of the element to exclude from sticky toggle
 * @param {boolean} [highlightOnly=false] Omit sticky toggle, only highlight on hover
 * @private
 */
const _toggleScanStickyHighlight = ({element, type, scanType, excludeLinkElement = 'aa-intel-information-link', highlightOnly = false}) => {
    // Function name mappings for different scan types
    const functionMappings = {
        fleetcomposition: {
            add: typeof addFleetcompositionHighlight === 'function' ? addFleetcompositionHighlight : null,
            remove: typeof removeFleetcompositionHighlight === 'function' ? removeFleetcompositionHighlight : null,
            change: typeof changeFleetcompositionStickyHighlight === 'function' ? changeFleetcompositionStickyHighlight : null
        },
        dscan: {
            add: typeof addDscanHighlight === 'function' ? addDscanHighlight : null,
            remove: typeof removeDscanHighlight === 'function' ? removeDscanHighlight : null,
            change: typeof changeDscanStickyHighlight === 'function' ? changeDscanStickyHighlight : null
        },
        chatscan: {
            add: typeof addChatscanHighlight === 'function' ? addChatscanHighlight : null,
            remove: typeof removeChatscanHighlight === 'function' ? removeChatscanHighlight : null,
            change: typeof changeChatscanStickyHighlight === 'function' ? changeChatscanStickyHighlight : null
        }
    };

    const functions = functionMappings[scanType];

    // Highlight
    const highlightHandler = highlightOnly
        ? (element) => element.addClass('aa-intel-highlight') // jshint ignore:line
        : (element) => functions.add(type, element);

    const unhighlightHandler = highlightOnly
        ? (element) => element.removeClass('aa-intel-highlight') // jshint ignore:line
        : (element) => functions.remove(type, element);

    element.mouseenter((event) => {
        highlightHandler($(event.currentTarget));
    }).mouseleave((event) => {
        unhighlightHandler($(event.currentTarget));
    });

    // Sticky
    if (!highlightOnly) {
        element.click((event) => {
            if (!$(event.target).hasClass(excludeLinkElement)) {
                functions.change(type, $(event.currentTarget));
            } else {
                event.stopPropagation();
            }
        });
    }
};

/**
 * Toggle sticky highlight for Fleet Composition
 *
 * @param {Object} params Parameters
 * @param {jQuery|Element} params.element The element to attach the events to
 * @param {string} params.type The type of the element (shipclass or shiptype)
 * @param {string} [params.excludeLinkElement=aa-intel-information-link] The class of the element to exclude from sticky toggle
 * @param {boolean} [params.highlightOnly=false] Omit sticky toggle, only highlight on hover
 * @returns {void}
 * @private
 */
const _toggleFleetcompStickyHighlight = (params) => { // eslint-disable-line no-unused-vars
    _toggleScanStickyHighlight({...params, scanType: 'fleetcomposition'});
};

/**
 * Toggle sticky highlight for D-Scans
 *
 * @param {Object} params Parameters
 * @param {jQuery|Element} params.element The element to attach the events to
 * @param {string} params.type The type of the element (shipclass or shiptype)
 * @param {string} [params.excludeLinkElement=aa-intel-information-link] The class of the element to exclude from sticky toggle
 * @param {boolean} [params.highlightOnly=false] Omit sticky toggle, only highlight on hover
 * @returns {void}
 * @private
 */
const _toggleDscanStickyHighlight = (params) => { // eslint-disable-line no-unused-vars
    _toggleScanStickyHighlight({...params, scanType: 'dscan'});
};

/**
 * Toggle sticky highlight for Chat Scans
 *
 * @param {Object} params Parameters
 * @param {jQuery|Element} params.element The element to attach the events to
 * @param {string} params.type The type of the element (shipclass or shiptype)
 * @param {string} [params.excludeLinkElement=aa-intel-information-link] The class of the element to exclude from sticky toggle
 * @param {boolean} [params.highlightOnly=false] Omit sticky toggle, only highlight on hover
 * @returns {void}
 * @private
 */
const _toggleChatscanStickyHighlight = (params) => { // eslint-disable-line no-unused-vars
    _toggleScanStickyHighlight({...params, scanType: 'chatscan'});
};

/**
 * Number formatter
 *
 * @param {number} value The number to format
 * @return {string} The formatted number
 * @private
 */
const _numberFormatter = (value) => { // eslint-disable-line no-unused-vars
    return new Intl.NumberFormat(aaIntelToolJsSettings.language.django).format(value);
};

/**
 * Bootstrap tooltip
 *
 * @param {string} [selector=body] Selector for the tooltip elements, defaults to 'body'
 *                                 to apply to all elements with the data-bs-tooltip attribute.
 *                                 Example: 'body', '.my-tooltip-class', '#my-tooltip-id'
 *                                 If you want to apply it to a specific element, use that element's selector.
 *                                 If you want to apply it to all elements with the data-bs-tooltip attribute,
 *                                 use 'body' or leave it empty.
 * @param {string} [namespace=aa-intel-tool] Namespace for the tooltip
 * @returns {void}
 */
const bootstrapTooltip = ({selector = 'body', namespace = 'aa-intel-tool'}) => { // eslint-disable-line no-unused-vars
    document.querySelectorAll(`${selector} [data-bs-tooltip="${namespace}"]`)
        .forEach((tooltipTriggerEl) => {
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
 *
 * Get the link HTML for external services
 *
 * @param {string} href
 * @param {string} serviceName
 * @returns {string} HTML string for external link
 * @private
 */
const _externalLinkHtml = (href, serviceName) => {
    return `<a class="aa-intel-information-link" href="${href}" target="_blank" rel="noopener noreferer">${serviceName}</a>`;
};

/**
 * Get the link HTML to EveWho for a pilot
 *
 * @param {string} href
 * @returns {string} HTML string for EveWho link
 */
const eveWhoLinkHtml = (href) => _externalLinkHtml(href, 'evewho');

/**
 * Get the link HTML to zKillboard
 *
 * @param {string} href
 * @returns {string} HTML string for zKillboard link
 */
const zkillboardLinkHtml = (href) => _externalLinkHtml(href, 'zkillboard');

/**
 * Get the link HTML to dotlan
 *
 * @param {string} href
 * @returns {string} HTML string for dotlan link
 */
const dotlanLinkHtml = (href) => _externalLinkHtml(href, 'dotlan');

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

$(document).ready(() => {
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
