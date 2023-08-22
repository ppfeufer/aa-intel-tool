'use strict';

/* Highlighting similar table rows on mouse over and click
--------------------------------------------------------------------------------- */

/**
 * Determine if we can remove all sticky states for this corporation
 *
 * @param element
 * @returns {boolean}
 */
const removeCorporationStickyComplete = (element) => {
    let removeCorporationSticky = true;

    $('table.aa-intel-pilot-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each((i, el) => {
        if ($(el).hasClass('aa-intel-highlight-sticky')) {
            removeCorporationSticky = false;
        }
    });

    return removeCorporationSticky;
};


/**
 * Determine if we can remove all sticky states for this alliance
 *
 * @param element
 * @returns {boolean}
 */
const removeAllianceStickyComplete = (element) => {
    let removeAllianceSticky = true;

    $('table.aa-intel-pilot-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each((i, el) => {
        if ($(el).hasClass('aa-intel-highlight-sticky')) {
            removeAllianceSticky = false;
        }
    });

    return removeAllianceSticky;
};


/**
 * Helper function
 *
 * @param element
 */
const allianceTableAddStickyByAllianceId = (element) => {
    $('table.aa-intel-alliance-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]')
        .addClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * @param element
 */
const allianceTableAddHighlightByAllianceId = (element) => {
    $('table.aa-intel-alliance-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]')
        .addClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * @param element
 */
const allianceTableRemoveStickyByAllianceId = (element) => {
    $('table.aa-intel-alliance-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]')
        .removeClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * @param element
 */
const allianceTableRemoveHighlightByAllianceId = (element) => {
    $('table.aa-intel-alliance-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]')
        .removeClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * @param element
 */
const corporationTableAddStickyByCorporationId = (element) => {
    $('table.aa-intel-corporation-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]')
        .addClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * @param element
 */
const corporationTableAddHighlightByCorporationId = (element) => {
    $('table.aa-intel-corporation-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]')
        .addClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * @param element
 */
const corporationTableAddStickyByAllianceId = (element) => {
    $('table.aa-intel-corporation-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]')
        .addClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * @param element
 */
const corporationTableAddHighlightByAllianceId = (element) => {
    $('table.aa-intel-corporation-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]')
        .addClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * @param element
 */
const corporationTableRemoveStickyByCorporationId = (element) => {
    $('table.aa-intel-corporation-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]')
        .removeClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *aa-intel-tool-highlight
 * @param element
 */
const corporationTableRemoveHighlightByCorporationId = (element) => {
    $('table.aa-intel-corporation-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]')
        .removeClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * @param element
 */
const corporationTableRemoveStickyByAllianceId = (element) => {
    $('table.aa-intel-corporation-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]')
        .removeClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * @param element
 */
const corporationTableRemoveHighlightByAllianceId = (element) => {
    $('table.aa-intel-corporation-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]')
        .removeClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * @param element
 */
const pilotTableAddStickyByCorporationId = (element) => {
    $('table.aa-intel-pilot-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]')
        .addClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * @param element
 */
const pilotTableAddHighlightByCorporationId = (element) => {
    $('table.aa-intel-pilot-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]')
        .addClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * @param element
 */
const pilotTableAddStickyByAllianceId = (element) => {
    $('table.aa-intel-pilot-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]')
        .addClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * @param element
 */
const pilotTableAddHighlightByAllianceId = (element) => {
    $('table.aa-intel-pilot-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]')
        .addClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * @param element
 */
const pilotTableRemoveStickyByCorporationId = (element) => {
    $('table.aa-intel-pilot-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]')
        .removeClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * @param element
 */
const pilotTableRemoveHighlightByCorporationId = (element) => {
    $('table.aa-intel-pilot-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]')
        .removeClass('aa-intel-highlight');
};


/**
 * Helper function
 *
 * @param element
 */
const pilotTableRemoveStickyByAllianceId = (element) => {
    $('table.aa-intel-pilot-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]')
        .removeClass('aa-intel-highlight-sticky');
};


/**
 * Helper function
 *
 * @param element
 */
const pilotTableRemoveHighlightByAllianceId = (element) => {
    $('table.aa-intel-pilot-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]')
        .removeClass('aa-intel-highlight');
};


/**
 * Add highlight to other tables from alliance table
 *
 * @param by_table {string} The table from which this function is triggered
 * @param table_row {element} The table row that is to be changed
 */
const addHightlight = (by_table, table_row) => { // eslint-disable-line no-unused-vars
    table_row.addClass('aa-intel-highlight');

    if (by_table === 'alliance') {
        corporationTableAddHighlightByAllianceId(table_row);
        pilotTableAddHighlightByAllianceId(table_row);
    }

    if (by_table === 'corporation') {
        allianceTableAddHighlightByAllianceId(table_row);
        pilotTableAddHighlightByCorporationId(table_row);
    }

    if (by_table === 'pilot') {
        allianceTableAddHighlightByAllianceId(table_row)
        corporationTableAddHighlightByCorporationId(table_row);
    }
}


/**
 * Add sticky highlight to other tables from alliance table
 *
 * @param by_table {string} The table from which this function is triggered
 * @param table_row {element} The table row that is to be changed
 */
const addSticky = (by_table, table_row) => {
    table_row.addClass('aa-intel-highlight-sticky');

    if (by_table === 'alliance') {
        corporationTableAddStickyByAllianceId(table_row);
        pilotTableAddStickyByAllianceId(table_row);
    }

    if (by_table === 'corporation') {
        allianceTableAddStickyByAllianceId(table_row);
        pilotTableAddStickyByCorporationId(table_row);
    }

    if (by_table === 'pilot') {
        allianceTableAddStickyByAllianceId(table_row);
        corporationTableAddStickyByCorporationId(table_row);
    }
}


/**
 * Remove highlight to other tables from alliance table
 *
 * @param by_table {string} The table from which this function is triggered
 * @param table_row {element} The table row that is to be changed
 */
const removeHightlight = (by_table, table_row) => { // eslint-disable-line no-unused-vars
    table_row.removeClass('aa-intel-highlight');

    if (by_table === 'alliance') {
        corporationTableRemoveHighlightByAllianceId(table_row);
        pilotTableRemoveHighlightByAllianceId(table_row);
    }

    if (by_table === 'corporation') {
        allianceTableRemoveHighlightByAllianceId(table_row);
        pilotTableRemoveHighlightByCorporationId(table_row);
    }

    if (by_table === 'pilot') {
        allianceTableRemoveHighlightByAllianceId(table_row);
        corporationTableRemoveHighlightByCorporationId(table_row);
    }
}


/**
 * Remove sticky highlight to other tables from alliance table
 *
 * @param by_table {string} The table from which this function is triggered
 * @param table_row {element} The table row that is to be changed
 */
const removeSticky = (by_table, table_row) => {
    table_row.removeClass('aa-intel-highlight-sticky');

    if (by_table === 'alliance') {
        corporationTableRemoveStickyByAllianceId(table_row);
        pilotTableRemoveStickyByAllianceId(table_row);
    }

    if (by_table === 'corporation') {
        pilotTableRemoveStickyByCorporationId(table_row);

        if (removeAllianceStickyComplete(table_row) === true) {
            allianceTableRemoveStickyByAllianceId(table_row);
        }
    }

    if (by_table === 'pilot') {
        if (removeCorporationStickyComplete(table_row) === true) {
            corporationTableRemoveStickyByCorporationId(table_row);
        }

        if (removeAllianceStickyComplete(table_row) === true) {
            allianceTableRemoveStickyByAllianceId(table_row);
        }
    }
}


/**
 * Change the status of the sticky highlight
 *
 * @param by_table {string} The table from which this function is triggered
 * @param table_row {element} The table row that is to be changed
 */
const changeStickyHighlight = (by_table, table_row) => { // eslint-disable-line no-unused-vars
    if (table_row.hasClass('aa-intel-highlight-sticky')) {
        removeSticky(by_table, table_row);
    } else {
        addSticky(by_table, table_row);
    }
}
