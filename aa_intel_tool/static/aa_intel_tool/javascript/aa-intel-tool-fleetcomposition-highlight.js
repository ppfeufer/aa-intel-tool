'use strict';

/* Highlighting similar table rows on mouse over and click for d-scans
------------------------------------------------------------------------------------- */

const elementShipClassTable = $('table.aa-intel-dscan-ship-classes');
const elementShipTypeTable = $('table.aa-intel-dscan-ship-types');
const elementFleetcompTable = $('table.aa-intel-fleetcomp-pilot-ships-list');


/**
 * Determine if we can remove all sticky states for this corporation
 *
 * @param by_table {string} The table from which this function is triggered
 * @param table_row {element} The table row that is to be changed
 * @returns {boolean}
 */
const removeFleetcompositionShiptypeStickyComplete = (by_table, table_row) => {
    let removeSticky = true;

    elementShipClassTable.find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`).each((i, el) => {
        if (by_table === 'shiptype' && !$(el).hasClass('aa-intel-highlight-sticky')) {
            removeSticky = false;
        } else if (by_table === 'shipclass' && $(el).hasClass('aa-intel-highlight-sticky')) {
            removeSticky = false;
        }
    });

    return removeSticky;
};


/**
 * Add highlight to other tables
 *
 * @param by_table {string} The table from which this function is triggered
 * @param table_row {element} The table row that is to be changed
 */
const addFleetcompositionHightlight = (by_table, table_row) => { // eslint-disable-line no-unused-vars
    elementShipClassTable
        .find(`tr[data-${by_table}-id="${table_row.data(`${by_table}-id`)}"]`)
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
 * @param by_table {string} The table from which this function is triggered
 * @param table_row {element} The table row that is to be changed
 */
const removeFleetcompositionHightlight = (by_table, table_row) => { // eslint-disable-line no-unused-vars
    elementShipClassTable
        .find(`tr[data-${by_table}-id="${table_row.data(`${by_table}-id`)}"]`)
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
 * @param by_table {string} The table from which this function is triggered
 * @param table_row {element} The table row that is to be changed
 */
const addFleetcompositionSticky = (by_table, table_row) => {
    table_row.addClass('aa-intel-highlight-sticky');

    if (by_table === 'shiptype') {
        elementShipClassTable
            .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
            .addClass('aa-intel-highlight-sticky');
    }

    if (by_table === 'shipclass') {
        elementShipClassTable
            .find(`tr[data-shipclass-id="${table_row.data('shipclass-id')}"]`)
            .addClass('aa-intel-highlight-sticky');

        elementShipTypeTable
            .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
            .addClass('aa-intel-highlight-sticky');
    }
};


/**
 * Remove sticky highlight to other tables
 *
 * @param by_table {string} The table from which this function is triggered
 * @param table_row {element} The table row that is to be changed
 */
const removeFleetcompositionSticky = (by_table, table_row) => {
    table_row.removeClass('aa-intel-highlight-sticky');

    if (by_table === 'shiptype') {
        elementShipClassTable
            .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
            .removeClass('aa-intel-highlight-sticky');
    }

    if (by_table === 'shipclass') {
        elementShipClassTable
            .find(`tr[data-shipclass-id="${table_row.data('shipclass-id')}"]`)
            .removeClass('aa-intel-highlight-sticky');

        if (removeFleetcompositionShiptypeStickyComplete(by_table, table_row) === true) {
            elementShipTypeTable
                .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
                .removeClass('aa-intel-highlight-sticky');
        }
    }
};


/**
 * Change the status of the sticky highlight
 *
 * @param by_table {string} The table from which this function is triggered
 * @param table_row {element} The table row that is to be changed
 */
const changeFleetcompositionStickyHighlight = (by_table, table_row) => { // eslint-disable-line no-unused-vars
    if (
        (
            by_table === 'shiptype' && table_row.hasClass('aa-intel-highlight-sticky') === true
            && removeFleetcompositionShiptypeStickyComplete(by_table, table_row) === true
        ) || (by_table === 'shipclass' && table_row.hasClass('aa-intel-highlight-sticky') === true)
    ) {
        removeFleetcompositionSticky(by_table, table_row);
    } else {
        addFleetcompositionSticky(by_table, table_row);
    }
};