/* jshint -W097 */
'use strict';

const elementShipClassTable = $('table.aa-intel-dscan-ship-classes');
const elementShipTypeTable = $('table.aa-intel-dscan-ship-types');

/**
 * Determine if we can remove all sticky states for this shiptype
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {jQuery|HTMLElement} tableRow The table row that is to be changed
 * @returns {boolean}
 */
const removeDscanShiptypeStickyComplete = (byData, tableRow) => {
    const shiptypeId = tableRow.data('shiptype-id');
    const relatedElements = elementShipClassTable.find(`tr[data-shiptype-id="${shiptypeId}"]`);

    return relatedElements.toArray().every((el) => {
        const $el = $(el);

        return byData === 'shiptype'
            ? $el.hasClass('aa-intel-highlight-sticky') // jshint ignore:line
            : !$el.hasClass('aa-intel-highlight-sticky');
    });
};

/**
 * Apply or remove CSS class to target elements
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {jQuery|HTMLElement} tableRow The table row that is to be changed
 * @param {string} className The CSS class to add or remove
 * @param {boolean} add Whether to add (true) or remove (false) the class
 */
const manipulateTableHighlight = ({byData, tableRow, className, add}) => {
    const action = add ? 'addClass' : 'removeClass';
    const shiptypeId = tableRow.data('shiptype-id');
    const dataId = tableRow.data(`${byData}-id`);

    if (byData === 'shiptype') {
        elementShipClassTable.find(`tr[data-shiptype-id="${shiptypeId}"]`)[action](className);
    } else if (byData === 'shipclass') {
        elementShipClassTable.find(`tr[data-shipclass-id="${dataId}"]`)[action](className);

        if (add || removeDscanShiptypeStickyComplete(byData, tableRow)) {
            elementShipTypeTable.find(`tr[data-shiptype-id="${shiptypeId}"]`)[action](className);
        }
    }
};

/**
 * Add highlight to other tables
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {jQuery|HTMLElement} tableRow The table row that is to be changed
 */
const addDscanHighlight = (byData, tableRow) => { // eslint-disable-line no-unused-vars
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
 */
const removeDscanHighlight = (byData, tableRow) => { // eslint-disable-line no-unused-vars
    manipulateTableHighlight({
        byData: byData,
        tableRow: tableRow,
        className: 'aa-intel-highlight',
        add: false
    });
};

/**
 * Change the status of the sticky highlight
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {jQuery|HTMLElement} tableRow The table row that is to be changed
 */
const changeDscanStickyHighlight = (byData, tableRow) => { // eslint-disable-line no-unused-vars
    if (
        (
            byData === 'shiptype' && tableRow.hasClass('aa-intel-highlight-sticky') === true
            && removeDscanShiptypeStickyComplete(byData, tableRow) === true // jshint ignore:line
        ) || (byData === 'shipclass' && tableRow.hasClass('aa-intel-highlight-sticky') === true)
    ) {
        manipulateTableHighlight({
            byData: byData,
            tableRow: tableRow,
            className: 'aa-intel-highlight-sticky',
            add: false
        });
    } else {
        manipulateTableHighlight({
            byData: byData,
            tableRow: tableRow,
            className: 'aa-intel-highlight-sticky',
            add: true
        });
    }
};
