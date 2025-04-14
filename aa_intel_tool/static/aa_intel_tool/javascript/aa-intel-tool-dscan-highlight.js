/* jshint -W097 */
'use strict';

/* Highlighting similar table rows on mouse over and click for d-scans
------------------------------------------------------------------------------------- */

const elementShipClassTable = $('table.aa-intel-dscan-ship-classes');
const elementShipTypeTable = $('table.aa-intel-dscan-ship-types');


/**
 * Determine if we can remove all sticky states for this corporation
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {element} tableRow The table row that is to be changed
 * @returns {boolean}
 */
const removeDscanShiptypeStickyComplete = (byData, tableRow) => {
    let removeSticky = true;

    elementShipClassTable.find(`tr[data-shiptype-id="${tableRow.data('shiptype-id')}"]`).each((i, el) => {
        if (byData === 'shiptype' && !$(el).hasClass('aa-intel-highlight-sticky')) {
            removeSticky = false;
        } else if (byData === 'shipclass' && $(el).hasClass('aa-intel-highlight-sticky')) {
            removeSticky = false;
        }
    });

    return removeSticky;
};


/**
 * Add highlight to other tables
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {element} tableRow The table row that is to be changed
 */
const addDscanHighlight = (byData, tableRow) => { // eslint-disable-line no-unused-vars
    elementShipClassTable
        .find(`tr[data-${byData}-id="${tableRow.data(`${byData}-id`)}"]`)
        .addClass('aa-intel-highlight');

    elementShipTypeTable
        .find(`tr[data-shiptype-id="${tableRow.data('shiptype-id')}"]`)
        .addClass('aa-intel-highlight');
};


/**
 * Add highlight to other tables
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {element} tableRow The table row that is to be changed
 */
const removeDscanHighlight = (byData, tableRow) => { // eslint-disable-line no-unused-vars
    elementShipClassTable
        .find(`tr[data-${byData}-id="${tableRow.data(`${byData}-id`)}"]`)
        .removeClass('aa-intel-highlight');

    elementShipTypeTable
        .find(`tr[data-shiptype-id="${tableRow.data('shiptype-id')}"]`)
        .removeClass('aa-intel-highlight');
};


/**
 * Add sticky highlight to other tables
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {element} tableRow The table row that is to be changed
 */
const addDscanSticky = (byData, tableRow) => {
    tableRow.addClass('aa-intel-highlight-sticky');

    if (byData === 'shiptype') {
        elementShipClassTable
            .find(`tr[data-shiptype-id="${tableRow.data('shiptype-id')}"]`)
            .addClass('aa-intel-highlight-sticky');
    }

    if (byData === 'shipclass') {
        elementShipClassTable
            .find(`tr[data-shipclass-id="${tableRow.data('shipclass-id')}"]`)
            .addClass('aa-intel-highlight-sticky');

        elementShipTypeTable
            .find(`tr[data-shiptype-id="${tableRow.data('shiptype-id')}"]`)
            .addClass('aa-intel-highlight-sticky');
    }
};


/**
 * Remove sticky highlight to other tables
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {element} tableRow The table row that is to be changed
 */
const removeDscanSticky = (byData, tableRow) => {
    tableRow.removeClass('aa-intel-highlight-sticky');

    if (byData === 'shiptype') {
        elementShipClassTable
            .find(`tr[data-shiptype-id="${tableRow.data('shiptype-id')}"]`)
            .removeClass('aa-intel-highlight-sticky');
    }

    if (byData === 'shipclass') {
        elementShipClassTable
            .find(`tr[data-shipclass-id="${tableRow.data('shipclass-id')}"]`)
            .removeClass('aa-intel-highlight-sticky');

        if (removeDscanShiptypeStickyComplete(byData, tableRow) === true) {
            elementShipTypeTable
                .find(`tr[data-shiptype-id="${tableRow.data('shiptype-id')}"]`)
                .removeClass('aa-intel-highlight-sticky');
        }
    }
};


/**
 * Change the status of the sticky highlight
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {element} tableRow The table row that is to be changed
 */
const changeDscanStickyHighlight = (byData, tableRow) => { // eslint-disable-line no-unused-vars
    if (
        (
            byData === 'shiptype' && tableRow.hasClass('aa-intel-highlight-sticky') === true
            && removeDscanShiptypeStickyComplete(byData, tableRow) === true
        ) || (byData === 'shipclass' && tableRow.hasClass('aa-intel-highlight-sticky') === true)
    ) {
        removeDscanSticky(byData, tableRow);
    } else {
        addDscanSticky(byData, tableRow);
    }
};
