/* global eveIntelToolL10n */

jQuery(document).ready(function($) {
    'use strict';

    /**
     * Array of all data tables on the current page
     *
     * @type array
     */
    const dataTables = $('.table-sortable');
    dataTables.each(function() {
        let dataTableOptions;

        // build options
        if(typeof ($(this).data('haspaging')) !== 'undefined' && $(this).data('haspaging') === 'no') {
            dataTableOptions = {
                language: eveIntelToolL10n.dataTables.translation,
                paging: false,
                lengthChange: false,
                dom:
                    '<\'row\'<\'col-sm-12\'f>>' +
                    '<\'row\'<\'col-sm-12\'tr>>' +
                    '<\'row\'<\'col-sm-12\'i>>'
            };
        } else {
            dataTableOptions = {
                language: eveIntelToolL10n.dataTables.translation
            };
        }

        // initialize the table
        $(this).DataTable(dataTableOptions);
    });

    /**
     * Highlighting similar table rows on mouse over and click
    --------------------------------------------------------------------------------- */

    /**
     * Determine if we can remove all sticky states for this corporation
     *
     * @param {type} element
     * @returns {Boolean}
     */
    const removeCorporationStickyComplete = (function (element) {
        let removeCorporationSticky = true;

        $('table.aa-intel-pilot-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each(function () {
            if ($(this).hasClass('dataHighlightSticky')) {
                removeCorporationSticky = false;
            }
        });

        return removeCorporationSticky;
    });

    /**
     * Determine if we can remove all sticky states for his alliance
     *
     * @param {type} element
     * @returns {Boolean}
     */
    const removeAllianceStickyComplete = (function (element) {
        let removeAllianceSticky = true;

        $('table.aa-intel-pilot-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each(function () {
            if ($(this).hasClass('dataHighlightSticky')) {
                removeAllianceSticky = false;
            }
        });

        return removeAllianceSticky;
    });

    const allianceTableAddStickyByAllianceId = (function (element) {
        $('table.aa-intel-alliance-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each(function () {
            $(this).addClass('dataHighlightSticky');
        });
    });

    const allianceTableAddHighlightByAllianceId = (function (element) {
        $('table.aa-intel-alliance-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each(function () {
            $(this).addClass('dataHighlight');
        });
    });

    const allianceTableRemoveStickyByAllianceId = (function (element) {
        $('table.aa-intel-alliance-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each(function () {
            $(this).removeClass('dataHighlightSticky');
        });
    });

    const allianceTableRemoveHighlightByAllianceId = (function (element) {
        $('table.aa-intel-alliance-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each(function () {
            $(this).removeClass('dataHighlight');
        });
    });

    const corporationTableAddStickyByCorporationId = (function (element) {
        $('table.aa-intel-corporation-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each(function () {
            $(this).addClass('dataHighlightSticky');
        });
    });

    const corporationTableAddHighlightByCorporationId = (function (element) {
        $('table.aa-intel-corporation-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each(function () {
            $(this).addClass('dataHighlight');
        });
    });

    const corporationTableAddStickyByAllianceId = (function (element) {
        $('table.aa-intel-corporation-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each(function () {
            $(this).addClass('dataHighlightSticky');
        });
    });

    const corporationTableAddHighlightByAllianceId = (function (element) {
        $('table.aa-intel-corporation-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each(function () {
            $(this).addClass('dataHighlight');
        });
    });

    const corporationTableRemoveStickyByCorporationId = (function (element) {
        $('table.aa-intel-corporation-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each(function () {
            $(this).removeClass('dataHighlightSticky');
        });
    });

    const corporationTableRemoveHighlightByCorporationId = (function (element) {
        $('table.aa-intel-corporation-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each(function () {
            $(this).removeClass('dataHighlight');
        });
    });

    const corporationTableRemoveStickyByAllianceId = (function (element) {
        $('table.aa-intel-corporation-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each(function () {
            $(this).removeClass('dataHighlightSticky');
        });
    });

    const corporationTableRemoveHighlightByAllianceId = (function (element) {
        $('table.aa-intel-corporation-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each(function () {
            $(this).removeClass('dataHighlight');
        });
    });

    const pilotTableAddStickyByCorporationId = (function (element) {
        $('table.aa-intel-pilot-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each(function () {
            $(this).addClass('dataHighlightSticky');
        });
    });

    const pilotTableAddHighlightByCorporationId = (function (element) {
        $('table.aa-intel-pilot-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each(function () {
            $(this).addClass('dataHighlight');
        });
    });

    const pilotTableAddStickyByAllianceId = (function (element) {
        $('table.aa-intel-pilot-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each(function () {
            $(this).addClass('dataHighlightSticky');
        });
    });

    const pilotTableAddHighlightByAllianceId = (function (element) {
        $('table.aa-intel-pilot-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each(function () {
            $(this).addClass('dataHighlight');
        });
    });

    const pilotTableRemoveStickyByCorporationId = (function (element) {
        $('table.aa-intel-pilot-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each(function () {
            $(this).removeClass('dataHighlightSticky');
        });
    });

    const pilotTableRemoveHighlightByCorporationId = (function (element) {
        $('table.aa-intel-pilot-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each(function () {
            $(this).removeClass('dataHighlight');
        });
    });

    const pilotTableRemoveStickyByAllianceId = (function (element) {
        $('table.aa-intel-pilot-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each(function () {
            $(this).removeClass('dataHighlightSticky');
        });
    });

    const pilotTableRemoveHighlightByAllianceId = (function (element) {
        $('table.aa-intel-pilot-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each(function () {
            $(this).removeClass('dataHighlight');
        });
    });

    // hover and sticky on alliance table
    $('table.aa-intel-alliance-participation-list tr.aa-intel-alliance-participation-item').each(function() {
        // hover …
        $(this).on('mouseenter', function() {
            $(this).addClass('dataHighlight');

            corporationTableAddHighlightByAllianceId($(this));
            pilotTableAddHighlightByAllianceId($(this));
        }).on('mouseleave', function() {
            $(this).removeClass('dataHighlight');

            corporationTableRemoveHighlightByAllianceId($(this));
            pilotTableRemoveHighlightByAllianceId($(this));
        });

        // sticky
        $(this).on('click', function() {
            if($(this).hasClass('dataHighlightSticky')) {
                $(this).removeClass('dataHighlightSticky');

                corporationTableRemoveStickyByAllianceId($(this));
                pilotTableRemoveStickyByAllianceId($(this));
            } else {
                $(this).addClass('dataHighlightSticky');

                corporationTableAddStickyByAllianceId($(this));
                pilotTableAddStickyByAllianceId($(this));
            }
        }).on('click', '.aa-intel-information-link', function(e) {
            e.stopPropagation();
        });
    });

    // hover and sticky on corporation table
    $('table.aa-intel-corporation-participation-list tr.aa-intel-corporation-participation-item').each(function() {
        // hover
        $(this).on('mouseenter', function() {
            $(this).addClass('dataHighlight');

            allianceTableAddHighlightByAllianceId($(this));
            pilotTableAddHighlightByCorporationId($(this));
        }).on('mouseleave', function() {
            $(this).removeClass('dataHighlight');

            allianceTableRemoveHighlightByAllianceId($(this));
            pilotTableRemoveHighlightByCorporationId($(this));
        });

        // sticky
        $(this).on('click', function() {
            if($(this).hasClass('dataHighlightSticky')) {
                $(this).removeClass('dataHighlightSticky');

                pilotTableRemoveStickyByCorporationId($(this));

                if(removeAllianceStickyComplete($(this)) === true) {
                    allianceTableRemoveStickyByAllianceId($(this));
                }
            } else {
                $(this).addClass('dataHighlightSticky');

                allianceTableAddStickyByAllianceId($(this));
                pilotTableAddStickyByCorporationId($(this));
            }
        }).on('click', '.aa-intel-information-link', function(e) {
            e.stopPropagation();
        });
    });

    // hover and sticky on pilot table
    $('table.aa-intel-pilot-participation-list tr.aa-intel-pilot-participation-item').each(function() {
        // hover
        $(this).on('mouseenter', function() {
            $(this).addClass('dataHighlight');

            allianceTableAddHighlightByAllianceId($(this));
            corporationTableAddHighlightByCorporationId($(this));
        }).on('mouseleave', function() {
            $(this).removeClass('dataHighlight');

            allianceTableRemoveHighlightByAllianceId($(this));
            corporationTableRemoveHighlightByCorporationId($(this));
        });

        // sticky
        $(this).on('click', function() {
            if($(this).hasClass('dataHighlightSticky')) {
                $(this).removeClass('dataHighlightSticky');

                if(removeCorporationStickyComplete($(this)) === true) {
                    corporationTableRemoveStickyByCorporationId($(this));
                }

                if(removeAllianceStickyComplete($(this)) === true) {
                    allianceTableRemoveStickyByAllianceId($(this));
                }
            } else {
                $(this).addClass('dataHighlightSticky');

                allianceTableAddStickyByAllianceId($(this));
                corporationTableAddStickyByCorporationId($(this));
            }
        }).on('click', '.aa-intel-information-link', function(e) {
            e.stopPropagation();
        });
    });

    // hover and sticky on d-scans and fleet scans
    $('tr[data-highlight]').each(function() {
        // hover
        $(this).on('mouseenter', function() {
            $('tr[data-highlight="' + $(this).data('highlight') + '"]').each(function() {
                $(this).addClass('dataHighlight');
            });
        }).on('mouseleave', function() {
            $('tr[data-highlight="' + $(this).data('highlight') + '"]').each(function() {
                $(this).removeClass('dataHighlight');
            });
        });

        // sticky
        $(this).on('click', function() {
            $('tr[data-highlight="' + $(this).data('highlight') + '"]').each(function() {
                $(this).toggleClass('dataHighlightSticky');
            });
        }).on('click', '.aa-intel-information-link', function(e) {
            e.stopPropagation();
        });
    });
});
