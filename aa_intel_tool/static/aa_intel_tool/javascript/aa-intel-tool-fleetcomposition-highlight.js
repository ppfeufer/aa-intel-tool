/* jshint -W097 */
'use strict';

/* Highlighting similar table rows on mouse over and click for d-scans
------------------------------------------------------------------------------------- */

const elementShipClassTable = $('table.aa-intel-dscan-ship-classes');
const elementShipTypeTable = $('table.aa-intel-dscan-ship-types');
const elementFleetcompTable = $('table.aa-intel-fleetcomp-pilot-ships-list');


/**
 * Determine if we can remove all sticky states for this corporation
 *
 * @param {string} by_data The table data attribute for which this function is triggered
 * @param {element} table_row The table row that is to be changed
 * @returns {boolean}
 */
const removeFleetcompositionShiptypeStickyComplete = (by_data, table_row) => {
    let removeSticky = true;

    elementShipClassTable.find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`).each((i, el) => {
        if (by_data === 'shiptype' && !$(el).hasClass('aa-intel-highlight-sticky')) {
            removeSticky = false;
        } else if (by_data === 'shipclass' && $(el).hasClass('aa-intel-highlight-sticky')) {
            removeSticky = false;
        }
    });

    return removeSticky;
};


/**
 * Add highlight to other tables
 *
 * @param {string} by_data The table data attribute for which this function is triggered
 * @param {element} table_row The table row that is to be changed
 */
const addFleetcompositionHightlight = (by_data, table_row) => { // eslint-disable-line no-unused-vars
    elementShipClassTable
        .find(`tr[data-${by_data}-id="${table_row.data(`${by_data}-id`)}"]`)
        .addClass('aa-intel-highlight');

    elementShipTypeTable
        .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
        .addClass('aa-intel-highlight');

    elementFleetcompTable
        .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
        .addClass('aa-intel-highlight');
};


/**
 * Add highlight to other tables
 *
 * @param {string} by_data The table data attribute for which this function is triggered
 * @param {element} table_row The table row that is to be changed
 */
const removeFleetcompositionHightlight = (by_data, table_row) => { // eslint-disable-line no-unused-vars
    elementShipClassTable
        .find(`tr[data-${by_data}-id="${table_row.data(`${by_data}-id`)}"]`)
        .removeClass('aa-intel-highlight');

    elementShipTypeTable
        .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
        .removeClass('aa-intel-highlight');

    elementFleetcompTable
        .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
        .removeClass('aa-intel-highlight');
};


/**
 * Add sticky highlight to other tables
 *
 * @param {string} by_data The table data attribute for which this function is triggered
 * @param {element} table_row The table row that is to be changed
 */
const addFleetcompositionSticky = (by_data, table_row) => {
    table_row.addClass('aa-intel-highlight-sticky');

    if (by_data === 'shiptype') {
        elementShipClassTable
            .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
            .addClass('aa-intel-highlight-sticky');

        elementShipTypeTable
            .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
            .addClass('aa-intel-highlight-sticky');

        elementFleetcompTable
            .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
            .addClass('aa-intel-highlight-sticky');
    }

    if (by_data === 'shipclass') {
        elementShipClassTable
            .find(`tr[data-shipclass-id="${table_row.data('shipclass-id')}"]`)
            .addClass('aa-intel-highlight-sticky');

        elementShipTypeTable
            .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
            .addClass('aa-intel-highlight-sticky');

        elementFleetcompTable
            .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
            .addClass('aa-intel-highlight-sticky');
    }
};


/**
 * Remove sticky highlight to other tables
 *
 * @param {string} by_data The table data attribute for which this function is triggered
 * @param {element} table_row The table row that is to be changed
 */
const removeFleetcompositionSticky = (by_data, table_row) => {
    table_row.removeClass('aa-intel-highlight-sticky');

    if (by_data === 'shiptype') {
        elementShipClassTable
            .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
            .removeClass('aa-intel-highlight-sticky');

        elementShipTypeTable
            .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
            .removeClass('aa-intel-highlight-sticky');

        elementFleetcompTable
            .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
            .removeClass('aa-intel-highlight-sticky');
    }

    if (by_data === 'shipclass') {
        elementShipClassTable
            .find(`tr[data-shipclass-id="${table_row.data('shipclass-id')}"]`)
            .removeClass('aa-intel-highlight-sticky');

        elementFleetcompTable
            .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
            .removeClass('aa-intel-highlight-sticky');

        if (removeFleetcompositionShiptypeStickyComplete(by_data, table_row) === true) {
            elementShipTypeTable
                .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
                .removeClass('aa-intel-highlight-sticky');
        }
    }
};


/**
 * Change the status of the sticky highlight
 *
 * @param {string} by_data The table data attribute for which this function is triggered
 * @param {element} table_row The table row that is to be changed
 */
const changeFleetcompositionStickyHighlight = (by_data, table_row) => { // eslint-disable-line no-unused-vars
    if (
        (
            by_data === 'shiptype' && table_row.hasClass('aa-intel-highlight-sticky') === true
            && removeFleetcompositionShiptypeStickyComplete(by_data, table_row) === true // jshint ignore:line
        )
        || (by_data === 'shipclass' && table_row.hasClass('aa-intel-highlight-sticky') === true) // jshint ignore:line
    ) {
        removeFleetcompositionSticky(by_data, table_row);
    } else {
        addFleetcompositionSticky(by_data, table_row);
    }
};
