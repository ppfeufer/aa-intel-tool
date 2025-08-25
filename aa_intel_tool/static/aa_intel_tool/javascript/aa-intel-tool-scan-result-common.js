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
 * @returns {void}
 * @private
 */
const _toggleScanStickyHighlight = ({
    element,
    type,
    scanType,
    excludeLinkElement = 'aa-intel-information-link',
    highlightOnly = false
}) => {
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

    element
        .mouseenter((event) => {
            highlightHandler($(event.currentTarget));
        })
        .mouseleave((event) => {
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
 * @param {int} eveId Eve ID of the entity
 * @param {string} eveName Name of the entity
 * @param {string} imageSource URL of the image
 * @param {int} [imageSize=32] Size of the image (width and height)
 * @returns {`<img class='eve-image rounded' data-eveid='${int}' src='${string}' alt='${string}' title='${string}' data-bs-tooltip='aa-intel-tool' loading='lazy' width='${int}' height='${int}'>`}
 * @private
 */
const _eveImageHtml = ({eveId, eveName, imageSource, imageSize = 32}) => {
    return `<img class="eve-image rounded" data-eveid="${eveId}" src="${imageSource}" alt="${eveName}" title="${eveName}" data-bs-tooltip="aa-intel-tool" loading="lazy" width="${imageSize}" height="${imageSize}">`;
};

/**
 *
 * Get the link HTML for external services
 *
 * @param {string} serviceName Name of the external service
 * @param {string} href URL of the external service
 * @returns {`<a class='aa-intel-information-link' href='${string}' target='_blank' rel='noopener noreferer'>${string}</a>`} HTML string for the external service link
 * @private
 */
const _externalLinkHtml = ({serviceName, href}) => {
    return `<a class="aa-intel-information-link" href="${href}" target="_blank" rel="noopener noreferer">${serviceName}</a>`;
};

/**
 * Get the link HTML to EveWho for a pilot
 *
 * @param {string} href URL of the external service
 * @returns {`<a class='aa-intel-information-link' href='${string}' target='_blank' rel='noopener noreferer'>evewho</a>`} HTML string for the EveWho link
 * @private
 */
const _eveWhoLinkHtml = (href) => _externalLinkHtml({
    serviceName: 'evewho',
    href: href
});

/**
 * Get the link HTML to zKillboard
 *
 * @param {string} href URL of the external service
 * @returns {`<a class='aa-intel-information-link' href='${string}' target='_blank' rel='noopener noreferer'>zkillboard</a>`} HTML string for the zKillboard link
 * @private
 */
const _zkillboardLinkHtml = (href) => _externalLinkHtml({
    serviceName: 'zkillboard',
    href: href
});

/**
 * Get the link HTML to dotlan
 *
 * @param {string} href URL of the external service
 * @returns {`<a class='aa-intel-information-link' href='${string}' target='_blank' rel='noopener noreferer'>dotlan</a>`} HTML string for the dotlan link
 * @private
 */
const _dotlanLinkHtml = (href) => _externalLinkHtml({
    serviceName: 'dotlan',
    href: href
});

/**
 * Info panel for the datatable
 *
 * @param {string} imageData HTML for the image
 * @param {string} eveData Name of the entity
 * @param {string} [additionalInfo=''] Additional information (links etc.)
 * @param {boolean} [logoOnly=false] Returns only the logo
 * @returns {`<span class='aa-intel-eve-image-wrapper'>${string}</span>`|`<span class='aa-intel-eve-image-wrapper'>${string}</span><span class='aa-intel-eve-information-wrapper'><span class='aa-intel-eve-name-wrapper'>${string}</span><span class='aa-intel-additional-information-wrapper'><small>${string}</small></span></span>|<span class='aa-intel-eve-image-wrapper'>${string}</span>`} HTML construct for the info panel
 * @private
 */
const _infoPanel = ({imageData, eveData, additionalInfo = '', logoOnly = false}) => {
    const imageDataHtml = `<span class="aa-intel-eve-image-wrapper">${imageData}</span>`;

    if (logoOnly) {
        return imageDataHtml;
    }

    const nameWrapper = `<span class="aa-intel-eve-name-wrapper">${eveData}</span>`;
    const additionalWrapper = additionalInfo
        ? `<span class="aa-intel-additional-information-wrapper"><small>${additionalInfo}</small></span>` // jshint ignore:line
        : '';

    return `${imageDataHtml}<span class="aa-intel-eve-information-wrapper">${nameWrapper}${additionalWrapper}</span>`;
};

/**
 * Pilot info element in datatable
 *
 * @param {Object} pilotData Pilot data
 * @param {int} pilotData.id Pilot ID
 * @param {string} pilotData.name Pilot name
 * @param {string} pilotData.portrait URL of the pilot portrait
 * @param {string} pilotData.evewho URL to EveWho
 * @param {string} pilotData.zkillboard URL to zKillboard
 * @returns {`<span class='aa-intel-eve-image-wrapper'>${string}</span><span class='aa-intel-eve-information-wrapper'><span class='aa-intel-eve-name-wrapper'>${string}</span><span class='aa-intel-additional-information-wrapper'><small>${string} | ${string}</small></span></span>`} HTML construct for the pilot info
 */
const pilotInfoPanel = (pilotData) => { // eslint-disable-line no-unused-vars
    const imageData = _eveImageHtml({
        eveId: pilotData.id,
        eveName: pilotData.name,
        imageSource: pilotData.portrait
    });
    const additionalInfo = `${_eveWhoLinkHtml(pilotData.evewho)} | ${_zkillboardLinkHtml(pilotData.zkillboard)}`;

    return _infoPanel({
        imageData: imageData,
        eveData: pilotData.name,
        additionalInfo: additionalInfo
    });
};

/**
 * Corporation info element in datatable
 *
 * @param {Object} corporationData Corporation data
 * @param {int} corporationData.id Corporation ID
 * @param {string} corporationData.name Corporation name
 * @param {string} corporationData.logo URL of the corporation logo
 * @param {string} corporationData.dotlan URL to dotlan
 * @param {string} corporationData.zkillboard URL to zKillboard
 * @param {boolean} logoOnly Returns only the corporation logo
 * @returns {`<span class='aa-intel-eve-image-wrapper'>${string}</span><span class='aa-intel-eve-information-wrapper'><span class='aa-intel-eve-name-wrapper'>${string}</span><span class='aa-intel-additional-information-wrapper'><small>${string}</small></span></span>|<span class='aa-intel-eve-image-wrapper'>${string}</span>`} HTML construct for the corporation info
 */
const corporationInfoPanel = (corporationData, logoOnly = false) => { // eslint-disable-line no-unused-vars
    const imageData = _eveImageHtml({
        eveId: corporationData.id,
        eveName: corporationData.name,
        imageSource: corporationData.logo
    });

    const isNpcCorp = corporationData.id >= 1000000 && corporationData.id <= 2000000;
    const additionalInfo = isNpcCorp
        ? `(${aaIntelToolJsSettings.translation.scanData.npcCorp})` // jshint ignore:line
        : `${_dotlanLinkHtml(corporationData.dotlan)} | ${_zkillboardLinkHtml(corporationData.zkillboard)}`;

    return _infoPanel({
        imageData: imageData,
        eveData: corporationData.name,
        additionalInfo: additionalInfo,
        logoOnly: logoOnly
    });
};

/**
 * Alliance info element in datatable
 *
 * @param {Object} allianceData Alliance data
 * @param {int} allianceData.id Alliance ID
 * @param {string} allianceData.name Alliance name
 * @param {string} allianceData.logo URL of the alliance logo
 * @param {string} allianceData.dotlan URL to dotlan
 * @param {string} allianceData.zkillboard URL to zKillboard
 * @param {boolean} logoOnly Returns only the alliance logo
 * @returns {'' | `<span class='aa-intel-eve-image-wrapper'>${string}</span><span class='aa-intel-eve-information-wrapper'><span class='aa-intel-eve-name-wrapper'>${string}</span><span class='aa-intel-additional-information-wrapper'><small>${string}</small></span></span>|<span class='aa-intel-eve-image-wrapper'>${string}</span>`} HTML construct for the alliance info
 */
const allianceInfoPanel = (allianceData, logoOnly = false) => { // eslint-disable-line no-unused-vars
    const name = allianceData.name || aaIntelToolJsSettings.translation.scanData.unaffiliated;

    if (logoOnly && allianceData.id === 1) {
        return '';
    }

    const imageData = _eveImageHtml({
        eveId: allianceData.id,
        eveName: name,
        imageSource: allianceData.logo
    });
    const additionalInfo = allianceData.id > 1
        ? `${_dotlanLinkHtml(allianceData.dotlan)} | ${_zkillboardLinkHtml(allianceData.zkillboard)}` // jshint ignore:line
        : aaIntelToolJsSettings.translation.scanData.noAlliance;

    return _infoPanel({
        imageData: imageData,
        eveData: name,
        additionalInfo: additionalInfo,
        logoOnly: logoOnly
    });
};

/**
 * Ship/Item info element in datatable
 *
 * @param {Object} shipData Ship data
 * @param {int} shipData.id Ship ID
 * @param {string} shipData.name Ship name
 * @param {string} shipData.image URL of the ship image
 * @returns {`<span class='aa-intel-eve-image-wrapper'>${string}</span><span class='aa-intel-eve-information-wrapper'><span class='aa-intel-eve-name-wrapper'>${string}</span></span>`} HTML construct for the ship info
 */
const shipInfoPanel = (shipData) => { // eslint-disable-line no-unused-vars
    const imageData = _eveImageHtml({
        eveId: shipData.id,
        eveName: shipData.name,
        imageSource: shipData.image
    });

    return _infoPanel({imageData: imageData, eveData: shipData.name});
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
     * @param {jQuery|HTMLElement} element The element to close
     * @param {int} [closeAfter=10] Close Message after given time in seconds
     * @return {void}
     */
    const closeMessageElement = ({element, closeAfter = 10}) => {
        element.fadeTo(closeAfter * 1000, 500).slideUp(500, () => {
            element.remove();
        });
    };

    /**
     * Show a message (success or error)
     *
     * @param {string} message The message to show
     * @param {jQuery|HTMLElement} element The element to show the message in
     * @param {string} type The message type (e.g.: 'success' or 'error')
     * @return {void}
     */
    const showMessage = ({message, element, type}) => {
        const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
        const messageClass = `alert-message-${type}`;
        const closeAfter = type === 'success' ? 10 : 9999;

        element.html(
            `<div class="alert ${alertClass} alert-dismissible ${messageClass} d-flex align-items-center fade show">${message}<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`
        );

        closeMessageElement({
            element: $(`.${messageClass}`),
            closeAfter: closeAfter
        });
    };

    /**
     * Show a success message
     *
     * @param {string} message The message to show
     * @param {jQuery|HTMLElement} element The element to show the message in
     * @return {void}
     */
    const showSuccess = ({message, element}) => showMessage({
        message: message,
        element: element,
        type: 'success'
    });

    /**
     * Show an error message
     *
     * @param {string} message The message to show
     * @param {jQuery|HTMLElement} element The element to show the message in
     * @return {void}
     */
    const showError = ({message, element}) => showMessage({
        message: message,
        element: element,
        type: 'error'
    });

    /**
     * Copy the scan link to clipboard
     *
     * @param {string} elementId The HTML-element ID
     * @return {void}
     */
    const copyScanLink = (elementId) => {
        /**
         * Copy text to clipboard
         *
         * @type Clipboard
         */
        const clipboardScanLink = new ClipboardJS(elementId);

        /**
         * Handle clipboard operation result
         *
         * @param {boolean} success Whether the operation was successful
         * @param {Event} [e] The event object (for success case)
         * @return {void}
         */
        const handleClipboardResult = ({success, e}) => {
            const messageType = success ? 'success' : 'error';
            const message = aaIntelToolJsSettings.translation.copyToClipboard.permalink.text[messageType];

            (success ? showSuccess : showError)({
                message: message,
                element: $('.aa-intel-copy-result')
            });

            if (success && e) {
                e.clearSelection();
            }

            clipboardScanLink.destroy();
        };

        clipboardScanLink
            .on('success', (e) => handleClipboardResult({success: true, e: e}))
            .on('error', () => handleClipboardResult({success: false}));
    };

    // Copy ping text
    elementCopyToClipboard.click(() => {
        copyScanLink(`#${elementCopyToClipboard.attr('id')}`);
    });
});
