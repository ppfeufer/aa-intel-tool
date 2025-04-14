/* jshint -W097 */
'use strict';

/* Highlighting similar table rows on mouse over and click for chat scans
--------------------------------------------------------------------------------- */

/**
 * Determine if we can remove all sticky states for this corporation.
 *
 * @param element
 * @returns {boolean}
 */
const removeCorporationStickyComplete = (element) => {
    let removeCorporationSticky = true;

    $(`table.aa-intel-pilot-participation-list tr[data-corporation-id="${element.data('corporationId')}"]`).each((i, el) => {
        if ($(el).hasClass('aa-intel-highlight-sticky')) {
            removeCorporationSticky = false;
        }
    });

    return removeCorporationSticky;
};


/**
 * Determine if we can remove all sticky states for this alliance.
 *
 * @param element
 * @returns {boolean}
 */
const removeAllianceStickyComplete = (element) => {
    let removeAllianceSticky = true;

    $(`table.aa-intel-pilot-participation-list tr[data-alliance-id="${element.data('allianceId')}"]`).each((i, el) => {
        if ($(el).hasClass('aa-intel-highlight-sticky')) {
            removeAllianceSticky = false;
        }
    });

    return removeAllianceSticky;
};


/**
 * Helper function
 *
 * Add a sticky highlight to the alliance table by alliance ID.
 *
 * @param element
 */
const allianceTableAddStickyByAllianceId = (element) => {
    $(`table.aa-intel-alliance-participation-list tr[data-alliance-id="${element.data('allianceId')}"]`)
        .addClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * Add a highlight to the alliance table by alliance ID.
 *
 * @param element
 */
const allianceTableAddHighlightByAllianceId = (element) => {
    $(`table.aa-intel-alliance-participation-list tr[data-alliance-id="${element.data('allianceId')}"]`)
        .addClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * Remove a sticky highlight from the alliance table by alliance ID.
 *
 * @param element
 */
const allianceTableRemoveStickyByAllianceId = (element) => {
    $(`table.aa-intel-alliance-participation-list tr[data-alliance-id="${element.data('allianceId')}"]`)
        .removeClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * Remove a highlight from the alliance table by alliance ID.
 *
 * @param element
 */
const allianceTableRemoveHighlightByAllianceId = (element) => {
    $(`table.aa-intel-alliance-participation-list tr[data-alliance-id="${element.data('allianceId')}"]`)
        .removeClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * Add a sticky highlight to the corporation table by corporation ID.
 *
 * @param element
 */
const corporationTableAddStickyByCorporationId = (element) => {
    $(`table.aa-intel-corporation-participation-list tr[data-corporation-id="${element.data('corporationId')}"]`)
        .addClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * Add a highlight to the corporation table by corporation ID.
 *
 * @param element
 */
const corporationTableAddHighlightByCorporationId = (element) => {
    $(`table.aa-intel-corporation-participation-list tr[data-corporation-id="${element.data('corporationId')}"]`)
        .addClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * Add a sticky highlight to the corporation table by alliance ID.
 *
 * @param element
 */
const corporationTableAddStickyByAllianceId = (element) => {
    $(`table.aa-intel-corporation-participation-list tr[data-alliance-id="${element.data('allianceId')}"]`)
        .addClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * Add a highlight to the corporation table by alliance ID.
 *
 * @param element
 */
const corporationTableAddHighlightByAllianceId = (element) => {
    $(`table.aa-intel-corporation-participation-list tr[data-alliance-id="${element.data('allianceId')}"]`)
        .addClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * Remove a sticky highlight from the corporation table by corporation ID.
 *
 * @param element
 */
const corporationTableRemoveStickyByCorporationId = (element) => {
    $(`table.aa-intel-corporation-participation-list tr[data-corporation-id="${element.data('corporationId')}"]`)
        .removeClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * Remove a highlight from the corporation table by corporation ID.
 *
 * @param element
 */
const corporationTableRemoveHighlightByCorporationId = (element) => {
    $(`table.aa-intel-corporation-participation-list tr[data-corporation-id="${element.data('corporationId')}"]`)
        .removeClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * Remove a sticky highlight from the corporation table by alliance ID.
 *
 * @param element
 */
const corporationTableRemoveStickyByAllianceId = (element) => {
    $(`table.aa-intel-corporation-participation-list tr[data-alliance-id="${element.data('allianceId')}"]`)
        .removeClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * Remove a highlight from the corporation table by alliance ID.
 *
 * @param element
 */
const corporationTableRemoveHighlightByAllianceId = (element) => {
    $(`table.aa-intel-corporation-participation-list tr[data-alliance-id="${element.data('allianceId')}"]`)
        .removeClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * Add a sticky highlight to the pilot table by corporation ID.
 *
 * @param element
 */
const pilotTableAddStickyByCorporationId = (element) => {
    $(`table.aa-intel-pilot-participation-list tr[data-corporation-id="${element.data('corporationId')}"]`)
        .addClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * Add a highlight to the pilot table by corporation ID.
 *
 * @param element
 */
const pilotTableAddHighlightByCorporationId = (element) => {
    $(`table.aa-intel-pilot-participation-list tr[data-corporation-id="${element.data('corporationId')}"]`)
        .addClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * Add a sticky highlight to the pilot table by alliance ID.
 *
 * @param element
 */
const pilotTableAddStickyByAllianceId = (element) => {
    $(`table.aa-intel-pilot-participation-list tr[data-alliance-id="${element.data('allianceId')}"]`)
        .addClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * Add a highlight to the pilot table by alliance ID.
 *
 * @param element
 */
const pilotTableAddHighlightByAllianceId = (element) => {
    $(`table.aa-intel-pilot-participation-list tr[data-alliance-id="${element.data('allianceId')}"]`)
        .addClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * Remove a sticky highlight from the pilot table by corporation ID.
 *
 * @param element
 */
const pilotTableRemoveStickyByCorporationId = (element) => {
    $(`table.aa-intel-pilot-participation-list tr[data-corporation-id="${element.data('corporationId')}"]`)
        .removeClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * Remove a highlight from the pilot table by corporation ID.
 *
 * @param element
 */
const pilotTableRemoveHighlightByCorporationId = (element) => {
    $(`table.aa-intel-pilot-participation-list tr[data-corporation-id="${element.data('corporationId')}"]`)
        .removeClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * Add a sticky highlight to the pilot table by alliance ID.
 *
 * @param element
 */
const pilotTableRemoveStickyByAllianceId = (element) => {
    $(`table.aa-intel-pilot-participation-list tr[data-alliance-id="${element.data('allianceId')}"]`)
        .removeClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * Add a highlight to the pilot table by alliance ID.
 *
 * @param element
 */
const pilotTableRemoveHighlightByAllianceId = (element) => {
    $(`table.aa-intel-pilot-participation-list tr[data-alliance-id="${element.data('allianceId')}"]`)
        .removeClass('aa-intel-highlight');
};


/**
 * Add a highlight to other tables from alliance table
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {element} tableRow The table row that is to be changed
 */
const addChatscanHighlight = (byData, tableRow) => { // eslint-disable-line no-unused-vars
    tableRow.addClass('aa-intel-highlight');

    if (byData === 'alliance') {
        corporationTableAddHighlightByAllianceId(tableRow);
        pilotTableAddHighlightByAllianceId(tableRow);
    }

    if (byData === 'corporation') {
        allianceTableAddHighlightByAllianceId(tableRow);
        pilotTableAddHighlightByCorporationId(tableRow);
    }

    if (byData === 'pilot') {
        allianceTableAddHighlightByAllianceId(tableRow);
        corporationTableAddHighlightByCorporationId(tableRow);
    }
};


/**
 * Add sticky highlight to other tables from alliance table
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {element} tableRow The table row that is to be changed
 */
const addChatscanSticky = (byData, tableRow) => {
    tableRow.addClass('aa-intel-highlight-sticky');

    if (byData === 'alliance') {
        corporationTableAddStickyByAllianceId(tableRow);
        pilotTableAddStickyByAllianceId(tableRow);
    }

    if (byData === 'corporation') {
        allianceTableAddStickyByAllianceId(tableRow);
        pilotTableAddStickyByCorporationId(tableRow);
    }

    if (byData === 'pilot') {
        allianceTableAddStickyByAllianceId(tableRow);
        corporationTableAddStickyByCorporationId(tableRow);
    }
};


/**
 * Remove highlight to other tables from alliance table
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {element} tableRow The table row that is to be changed
 */
const removeChatscanHighlight = (byData, tableRow) => { // eslint-disable-line no-unused-vars
    tableRow.removeClass('aa-intel-highlight');

    if (byData === 'alliance') {
        corporationTableRemoveHighlightByAllianceId(tableRow);
        pilotTableRemoveHighlightByAllianceId(tableRow);
    }

    if (byData === 'corporation') {
        allianceTableRemoveHighlightByAllianceId(tableRow);
        pilotTableRemoveHighlightByCorporationId(tableRow);
    }

    if (byData === 'pilot') {
        allianceTableRemoveHighlightByAllianceId(tableRow);
        corporationTableRemoveHighlightByCorporationId(tableRow);
    }
};


/**
 * Remove sticky highlight to other tables from alliance table
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {element} tableRow The table row that is to be changed
 */
const removeChatscanSticky = (byData, tableRow) => {
    tableRow.removeClass('aa-intel-highlight-sticky');

    if (byData === 'alliance') {
        corporationTableRemoveStickyByAllianceId(tableRow);
        pilotTableRemoveStickyByAllianceId(tableRow);
    }

    if (byData === 'corporation') {
        pilotTableRemoveStickyByCorporationId(tableRow);

        if (removeAllianceStickyComplete(tableRow) === true) {
            allianceTableRemoveStickyByAllianceId(tableRow);
        }
    }

    if (byData === 'pilot') {
        if (removeCorporationStickyComplete(tableRow) === true) {
            corporationTableRemoveStickyByCorporationId(tableRow);
        }

        if (removeAllianceStickyComplete(tableRow) === true) {
            allianceTableRemoveStickyByAllianceId(tableRow);
        }
    }
};


/**
 * Change the status of the sticky highlight
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {element} tableRow The table row that is to be changed
 */
const changeChatscanStickyHighlight = (byData, tableRow) => { // eslint-disable-line no-unused-vars
    if (tableRow.hasClass('aa-intel-highlight-sticky')) {
        removeChatscanSticky(byData, tableRow);
    } else {
        addChatscanSticky(byData, tableRow);
    }
};
