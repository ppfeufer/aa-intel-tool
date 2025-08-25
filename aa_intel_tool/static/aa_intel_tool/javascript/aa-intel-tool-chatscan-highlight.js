/* jshint -W097 */
'use strict';

/**
 * Determine if we can remove all sticky states for elements matching the selector.
 *
 * @param {string} selector CSS selector for elements to check
 * @returns {boolean} True if no elements have the sticky class, false otherwise
 */
const canRemoveStickyHighlight = (selector) => {
    return !$(selector).hasClass('aa-intel-highlight-sticky');
};

/**
 * Determine if we can remove all sticky states for this corporation.
 *
 * @param {jQuery|Element} element The jQuery element to check
 * @returns {boolean} True if no elements have the sticky class, false otherwise
 */
const removeCorporationStickyComplete = (element) => {
    return canRemoveStickyHighlight(`table.aa-intel-pilot-participation-list tr[data-corporation-id="${element.data('corporationId')}"]`);
};

/**
 * Determine if we can remove all sticky states for this alliance.
 *
 * @param {jQuery|Element} element
 * @returns {boolean} True if no elements have the sticky class, false otherwise
 */
const removeAllianceStickyComplete = (element) => {
    return canRemoveStickyHighlight(`table.aa-intel-pilot-participation-list tr[data-alliance-id="${element.data('allianceId')}"]`);
};

/**
 * Generic helper function to manipulate table row classes
 *
 * @param {string} tableClass The table CSS class
 * @param {string} dataAttribute The data attribute name ('alliance-id' or 'corporation-id')
 * @param {string} dataValue The data attribute value
 * @param {string} cssClass The CSS class to add/remove
 * @param {string} action The action to perform ('add' or 'remove')
 * @return {void}
 */
const manipulateTableHighlight = ({
    tableClass,
    dataAttribute,
    dataValue,
    cssClass,
    action
}) => {
    const selector = `table.${tableClass} tr[data-${dataAttribute}="${dataValue}"]`;
    const elements = $(selector);

    if (action === 'add') {
        elements.addClass(cssClass);
    } else if (action === 'remove') {
        elements.removeClass(cssClass);
    }
};

/**
 * Add a highlight to other tables from alliance table
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {jQuery|HTMLElement} tableRow The table row that is to be changed
 * @return {void}
 */
const addChatscanHighlight = (byData, tableRow) => { // eslint-disable-line no-unused-vars
    tableRow.addClass('aa-intel-highlight');

    if (byData === 'alliance') {
        // corporationTableAddHighlightByAllianceId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-corporation-participation-list',
            dataAttribute: 'alliance-id',
            dataValue: tableRow.data('allianceId'),
            cssClass: 'aa-intel-highlight',
            action: 'add'
        });
        // pilotTableAddHighlightByAllianceId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-pilot-participation-list',
            dataAttribute: 'alliance-id',
            dataValue: tableRow.data('allianceId'),
            cssClass: 'aa-intel-highlight',
            action: 'add'
        });
    }

    if (byData === 'corporation') {
        // allianceTableAddHighlightByAllianceId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-alliance-participation-list',
            dataAttribute: 'alliance-id',
            dataValue: tableRow.data('allianceId'),
            cssClass: 'aa-intel-highlight',
            action: 'add'
        });
        // pilotTableAddHighlightByCorporationId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-pilot-participation-list',
            dataAttribute: 'corporation-id',
            dataValue: tableRow.data('corporationId'),
            cssClass: 'aa-intel-highlight',
            action: 'add'
        });
    }

    if (byData === 'pilot') {
        // allianceTableAddHighlightByAllianceId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-alliance-participation-list',
            dataAttribute: 'alliance-id',
            dataValue: tableRow.data('allianceId'),
            cssClass: 'aa-intel-highlight',
            action: 'add'
        });
        // corporationTableAddHighlightByCorporationId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-corporation-participation-list',
            dataAttribute: 'corporation-id',
            dataValue: tableRow.data('corporationId'),
            cssClass: 'aa-intel-highlight',
            action: 'add'
        });
    }
};

/**
 * Add sticky highlight to other tables from alliance table
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {jQuery|HTMLElement} tableRow The table row that is to be changed
 * @return {void}
 */
const addChatscanSticky = (byData, tableRow) => {
    tableRow.addClass('aa-intel-highlight-sticky');

    if (byData === 'alliance') {
        // corporationTableAddStickyByAllianceId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-corporation-participation-list',
            dataAttribute: 'alliance-id',
            dataValue: tableRow.data('allianceId'),
            cssClass: 'aa-intel-highlight-sticky',
            action: 'add'
        });
        // pilotTableAddStickyByAllianceId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-pilot-participation-list',
            dataAttribute: 'alliance-id',
            dataValue: tableRow.data('allianceId'),
            cssClass: 'aa-intel-highlight-sticky',
            action: 'add'
        });
    }

    if (byData === 'corporation') {
        // allianceTableAddStickyByAllianceId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-alliance-participation-list',
            dataAttribute: 'alliance-id',
            dataValue: tableRow.data('allianceId'),
            cssClass: 'aa-intel-highlight-sticky',
            action: 'add'
        });
        // pilotTableAddStickyByCorporationId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-pilot-participation-list',
            dataAttribute: 'corporation-id',
            dataValue: tableRow.data('corporationId'),
            cssClass: 'aa-intel-highlight-sticky',
            action: 'add'
        });
    }

    if (byData === 'pilot') {
        // allianceTableAddStickyByAllianceId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-alliance-participation-list',
            dataAttribute: 'alliance-id',
            dataValue: tableRow.data('allianceId'),
            cssClass: 'aa-intel-highlight-sticky',
            action: 'add'
        });
        // corporationTableAddStickyByCorporationId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-corporation-participation-list',
            dataAttribute: 'corporation-id',
            dataValue: tableRow.data('corporationId'),
            cssClass: 'aa-intel-highlight-sticky',
            action: 'add'
        });
    }
};

/**
 * Remove highlight to other tables from alliance table
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {jQuery|HTMLElement} tableRow The table row that is to be changed
 * @return {void}
 */
const removeChatscanHighlight = (byData, tableRow) => { // eslint-disable-line no-unused-vars
    tableRow.removeClass('aa-intel-highlight');

    if (byData === 'alliance') {
        // corporationTableRemoveHighlightByAllianceId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-corporation-participation-list',
            dataAttribute: 'alliance-id',
            dataValue: tableRow.data('allianceId'),
            cssClass: 'aa-intel-highlight',
            action: 'remove'
        });
        // pilotTableRemoveHighlightByAllianceId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-pilot-participation-list',
            dataAttribute: 'alliance-id',
            dataValue: tableRow.data('allianceId'),
            cssClass: 'aa-intel-highlight',
            action: 'remove'
        });
    }

    if (byData === 'corporation') {
        // allianceTableRemoveHighlightByAllianceId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-alliance-participation-list',
            dataAttribute: 'alliance-id',
            dataValue: tableRow.data('allianceId'),
            cssClass: 'aa-intel-highlight',
            action: 'remove'
        });
        // pilotTableRemoveHighlightByCorporationId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-pilot-participation-list',
            dataAttribute: 'corporation-id',
            dataValue: tableRow.data('corporationId'),
            cssClass: 'aa-intel-highlight',
            action: 'remove'
        });
    }

    if (byData === 'pilot') {
        // allianceTableRemoveHighlightByAllianceId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-alliance-participation-list',
            dataAttribute: 'alliance-id',
            dataValue: tableRow.data('allianceId'),
            cssClass: 'aa-intel-highlight',
            action: 'remove'
        });
        // corporationTableRemoveHighlightByCorporationId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-corporation-participation-list',
            dataAttribute: 'corporation-id',
            dataValue: tableRow.data('corporationId'),
            cssClass: 'aa-intel-highlight',
            action: 'remove'
        });
    }
};

/**
 * Remove sticky highlight to other tables from alliance table
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {jQuery|HTMLElement} tableRow The table row that is to be changed
 * @return {void}
 */
const removeChatscanSticky = (byData, tableRow) => {
    tableRow.removeClass('aa-intel-highlight-sticky');

    if (byData === 'alliance') {
        // corporationTableRemoveStickyByAllianceId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-corporation-participation-list',
            dataAttribute: 'alliance-id',
            dataValue: tableRow.data('allianceId'),
            cssClass: 'aa-intel-highlight-sticky',
            action: 'remove'
        });
        // pilotTableRemoveStickyByAllianceId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-pilot-participation-list',
            dataAttribute: 'alliance-id',
            dataValue: tableRow.data('allianceId'),
            cssClass: 'aa-intel-highlight-sticky',
            action: 'remove'
        });
    }

    if (byData === 'corporation') {
        // pilotTableRemoveStickyByCorporationId(tableRow);
        manipulateTableHighlight({
            tableClass: 'aa-intel-pilot-participation-list',
            dataAttribute: 'corporation-id',
            dataValue: tableRow.data('corporationId'),
            cssClass: 'aa-intel-highlight-sticky',
            action: 'remove'
        });

        if (removeAllianceStickyComplete(tableRow) === true) {
            // allianceTableRemoveStickyByAllianceId(tableRow);
            manipulateTableHighlight({
                tableClass: 'aa-intel-alliance-participation-list',
                dataAttribute: 'alliance-id',
                dataValue: tableRow.data('allianceId'),
                cssClass: 'aa-intel-highlight-sticky',
                action: 'remove'
            });
        }
    }

    if (byData === 'pilot') {
        if (removeCorporationStickyComplete(tableRow) === true) {
            // corporationTableRemoveStickyByCorporationId(tableRow);
            manipulateTableHighlight({
                tableClass: 'aa-intel-corporation-participation-list',
                dataAttribute: 'corporation-id',
                dataValue: tableRow.data('corporationId'),
                cssClass: 'aa-intel-highlight-sticky',
                action: 'remove'
            });
        }

        if (removeAllianceStickyComplete(tableRow) === true) {
            // allianceTableRemoveStickyByAllianceId(tableRow);
            manipulateTableHighlight({
                tableClass: 'aa-intel-alliance-participation-list',
                dataAttribute: 'alliance-id',
                dataValue: tableRow.data('allianceId'),
                cssClass: 'aa-intel-highlight-sticky',
                action: 'remove'
            });
        }
    }
};

/**
 * Change the status of the sticky highlight
 *
 * @param {string} byData The table data attribute for which this function is triggered
 * @param {jQuery|HTMLElement} tableRow The table row that is to be changed
 * @return {void}
 */
const changeChatscanStickyHighlight = (byData, tableRow) => { // eslint-disable-line no-unused-vars
    if (tableRow.hasClass('aa-intel-highlight-sticky')) {
        removeChatscanSticky(byData, tableRow);
    } else {
        addChatscanSticky(byData, tableRow);
    }
};
