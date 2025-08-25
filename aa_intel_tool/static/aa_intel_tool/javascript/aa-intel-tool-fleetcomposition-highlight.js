/* jshint -W097 */
'use strict';

const tables = {
    shipClass: $('table.aa-intel-dscan-ship-classes'),
    shipType: $('table.aa-intel-dscan-ship-types'),
    fleetComp: $('table.aa-intel-fleetcomp-pilot-ships-list')
};

/**
 * Apply or remove CSS class from matching table rows
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {jQuery|HTMLElement} tableRow The table row that is to be changed
 * @param {string} className The CSS class to add or remove
 * @param {boolean} add Whether to add (true) or remove (false) the class
 * @returns {void}
 */
const manipulateTableHighlight = ({byData, tableRow, className, add}) => {
    const action = add ? 'addClass' : 'removeClass';
    const shiptypeId = tableRow.data('shiptype-id');
    const dataId = tableRow.data(`${byData}-id`);

    // Apply to ship class table with appropriate data attribute
    tables.shipClass
        .find(`tr[data-${byData}-id="${dataId}"]`)[action](className);

    // Apply to ship type and fleet comp tables using shiptype-id
    tables.shipType
        .find(`tr[data-shiptype-id="${shiptypeId}"]`)[action](className);

    tables.fleetComp
        .find(`tr[data-shiptype-id="${shiptypeId}"]`)[action](className);
};

/**
 * Determine if we can remove all sticky states for this shiptype
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {jQuery|HTMLElement} tableRow The table row that is to be changed
 * @returns {boolean}
 */
const removeFleetcompositionShiptypeStickyComplete = (byData, tableRow) => {
    let removeSticky = true;

    tables.shipClass.find(`tr[data-shiptype-id="${tableRow.data('shiptype-id')}"]`).each((i, el) => {
        const hasSticky = $(el).hasClass('aa-intel-highlight-sticky');

        if ((byData === 'shiptype' && !hasSticky) || (byData === 'shipclass' && hasSticky)) {
            removeSticky = false;
        }
    });

    return removeSticky;
};

/**
 * Add highlight to other tables
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {jQuery|HTMLElement} tableRow The table row that is to be changed
 * @returns {void}
 */
const addFleetcompositionHighlight = (byData, tableRow) => { // eslint-disable-line no-unused-vars
    manipulateTableHighlight({
        byData: byData,
        tableRow: tableRow,
        className: 'aa-intel-highlight',
        add: true
    });
};

/**
 * Remove highlight from other tables
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {jQuery|HTMLElement} tableRow The table row that is to be changed
 * @returns {void}
 */
const removeFleetcompositionHighlight = (byData, tableRow) => { // eslint-disable-line no-unused-vars
    manipulateTableHighlight(byData, tableRow, 'aa-intel-highlight', false);
};

/**
 * Add sticky highlight to other tables
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {jQuery|HTMLElement} tableRow The table row that is to be changed
 * @returns {void}
 */
const addFleetcompositionSticky = (byData, tableRow) => {
    tableRow.addClass('aa-intel-highlight-sticky');

    manipulateTableHighlight({
        byData: byData,
        tableRow: tableRow,
        className: 'aa-intel-highlight',
        add: false
    });
};

/**
 * Remove sticky highlight from other tables
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {jQuery|HTMLElement} tableRow The table row that is to be changed
 * @returns {void}
 */
const removeFleetcompositionSticky = (byData, tableRow) => {
    tableRow.removeClass('aa-intel-highlight-sticky');

    if (byData === 'shiptype') {
        manipulateTableHighlight({
            byData: byData,
            tableRow: tableRow,
            className: 'aa-intel-highlight-sticky',
            add: false
        });
    } else if (byData === 'shipclass') {
        // Remove from ship class and fleet comp tables
        const shipclassId = tableRow.data('shipclass-id');
        const shiptypeId = tableRow.data('shiptype-id');

        tables.shipClass
            .find(`tr[data-shipclass-id="${shipclassId}"]`)
            .removeClass('aa-intel-highlight-sticky');

        tables.fleetComp
            .find(`tr[data-shiptype-id="${shiptypeId}"]`)
            .removeClass('aa-intel-highlight-sticky');

        // Only remove from ship type table if conditions are met
        if (removeFleetcompositionShiptypeStickyComplete(byData, tableRow)) {
            tables.shipType
                .find(`tr[data-shiptype-id="${shiptypeId}"]`)
                .removeClass('aa-intel-highlight-sticky');
        }
    }
};

/**
 * Change the status of the sticky highlight
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {jQuery|HTMLElement} tableRow The table row that is to be changed
 * @returns {void}
 */
const changeFleetcompositionStickyHighlight = (byData, tableRow) => { // eslint-disable-line no-unused-vars
    if (
        (
            byData === 'shiptype' && tableRow.hasClass('aa-intel-highlight-sticky') === true
            && removeFleetcompositionShiptypeStickyComplete(byData, tableRow) === true // jshint ignore:line
        )
        || (byData === 'shipclass' && tableRow.hasClass('aa-intel-highlight-sticky') === true) // jshint ignore:line
    ) {
        removeFleetcompositionSticky(byData, tableRow);
    } else {
        addFleetcompositionSticky(byData, tableRow);
    }
};
