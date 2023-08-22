'use strict';

/* Highlighting similar table rows on mouse over and click for d-scans
--------------------------------------------------------------------------------- */

const elementShipClassTable = $('table.aa-intel-dscan-ship-classes');
const elementShipTypeTable = $('table.aa-intel-dscan-ship-types');

/**
 * Add highlight to other tables
 *
 * @param by_table {string} The table from which this function is triggered
 * @param table_row {element} The table row that is to be changed
 */
const addHightlight = (by_table, table_row) => { // eslint-disable-line no-unused-vars
    elementShipClassTable
        .find(`tr[data-${by_table}-id="${table_row.data(`${by_table}-id`)}"]`)
        .addClass('aa-intel-highlight');

    elementShipTypeTable
        .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
        .addClass('aa-intel-highlight');
}


/**
 * Add highlight to other tables
 *
 * @param by_table {string} The table from which this function is triggered
 * @param table_row {element} The table row that is to be changed
 */
const removeHightlight = (by_table, table_row) => { // eslint-disable-line no-unused-vars
    elementShipClassTable
        .find(`tr[data-${by_table}-id="${table_row.data(`${by_table}-id`)}"]`)
        .removeClass('aa-intel-highlight');

    elementShipTypeTable
        .find(`tr[data-shiptype-id="${table_row.data('shiptype-id')}"]`)
        .removeClass('aa-intel-highlight');
}
