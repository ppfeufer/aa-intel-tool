/* global aaIntelToolJsOptions, aaIntelToolJsL10n */

jQuery(document).ready(($) => {
    'use strict';

    /* Elements
    --------------------------------------------------------------------------------- */
    const elementPilotsTable = $('table.aa-intel-pilot-participation-list');
    const elementCorporationsTable = $('table.aa-intel-corporation-participation-list');
    const elementAlliancesTable = $('table.aa-intel-alliance-participation-list');

    const elementPilotsTotalCount = $('span#aa-intel-pilots-count');
    const elementCorporationsTotalCount = $('span#aa-intel-corporations-count');
    const elementAlliancesTotalCount = $('span#aa-intel-alliances-count');


    /**
     * Corporation info element in datatable
     *
     * @param pilotData
     * @returns {string}
     */
    const pilotInfoPanel = (pilotData) => {
        let html_logo = '' +
            '<span class="aa-intel-pilot-avatar-wrapper">\n' +
            '    <img ' +
            '        class="eve-image" ' +
            '        data-eveid="' + pilotData.id + '" ' +
            '        src="' + pilotData.portrait + '" ' +
            '        alt="' + pilotData.name + '" ' +
            '        title="' + pilotData.name + '" ' +
            '        width="32" ' +
            '        height="32">\n' +
            '</span>';

        let html_info = '' +
            '<span class="aa-intel-pilot-information-wrapper">\n' +
            '    <span class="aa-intel-pilot-name-wrapper">\n' +
            '        ' + pilotData.name + '\n' +
            '    </span>\n';

        html_info += '' +
            '    <span class="aa-intel-corporation-links-wrapper">\n' +
            '        <small>\n';

        html_info += '' +
            '    <span class="aa-intel-pilot-links-wrapper">\n' +
            '        <small>\n' +
            '            <a ' +
            '                class="aa-intel-information-link" ' +
            '                href="' + pilotData.evewho + '" ' +
            '                target="_blank" ' +
            '                rel="noopener noreferer"' +
            '            >' +
            '               evewho <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
            '            </a> |\n' +

            '            <a ' +
            '                class="aa-intel-information-link" ' +
            '                href="' + pilotData.zkillboard + '" ' +
            '                target="_blank" rel="noopener noreferer"' +
            '            >' +
            '                zkillboard <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
            '            </a>\n' +
            '        </small>\n' +
            '    </span>\n';

        return html_logo + html_info;
    };


    /**
     * Corporation info element in datatable
     *
     * @param corporationData
     * @param logoOnly {boolean}
     * @returns {string}
     */
    const corporationInfoPanel = (corporationData, logoOnly) => {
        logoOnly = typeof logoOnly !== 'undefined' ? logoOnly : false;

        let html_logo = '' +
            '<span class="aa-intel-corporation-logo-wrapper">\n' +
            '    <img ' +
            '        class="eve-image" ' +
            '        data-eveid="' + corporationData.id + '" ' +
            '        src="' + corporationData.logo + '" ' +
            '        alt="' + corporationData.name + '" ' +
            '        title="' + corporationData.name + '" ' +
            '        width="32" ' +
            '        height="32">\n' +
            '</span>';

        let html_info = '' +
            '<span class="aa-intel-corporation-information-wrapper">\n' +
            '    <span class="aa-intel-corporation-name-wrapper">\n' +
            '        ' + corporationData.name + '\n' +
            '    </span>\n';

        html_info += '' +
            '    <span class="aa-intel-corporation-links-wrapper">\n' +
            '        <small>\n';

        if((1000000 <= corporationData.id) && corporationData.id <= 2000000) {
            html_info += '' +
                '            (' + aaIntelToolJsL10n.scanData.npcCorp + ')';
        } else {
            html_info += '' +
                '            <a ' +
                '                class="aa-intel-information-link" ' +
                '                href="' + corporationData.dotlan + '" ' +
                '                target="_blank" ' +
                '                rel="noopener noreferer"' +
                '            >' +
                '               dotlan <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
                '            </a> |\n' +

                '            <a ' +
                '                class="aa-intel-information-link" ' +
                '                href="' + corporationData.zkillboard + '" ' +
                '                target="_blank" rel="noopener noreferer"' +
                '            >' +
                '                zkillboard <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
                '            </a>\n' +
                '        </small>\n' +
                '    </span>\n';
        }

        html_info += '' +
            '</span>';

        if (logoOnly) {
            return html_logo;
        }

        return html_logo + html_info;
    };


    /**
     * Alliance info element in datatable
     *
     * @param allianceData
     * @param logoOnly {boolean}
     * @returns {string}
     */
    const allianceInfoPanel = (allianceData, logoOnly) => {
        logoOnly = typeof logoOnly !== 'undefined' ? logoOnly : false;

        if (allianceData.name === '') {
            allianceData.name = aaIntelToolJsL10n.scanData.empty;
        }

        let html_logo = '' +
            '<span class="aa-intel-alliance-logo-wrapper">\n' +
            '    <img ' +
            '        class="eve-image" ' +
            '        data-eveid="' + allianceData.id + '" ' +
            '        src="' + allianceData.logo + '" ' +
            '        alt="' + allianceData.name + '" ' +
            '        title="' + allianceData.name + '" ' +
            '        width="32" ' +
            '        height="32">\n' +
            '</span>';

        let html_info = '' +
            '<span class="aa-intel-alliance-information-wrapper">\n' +
            '    <span class="aa-intel-alliance-name-wrapper">\n' +
            '        ' + allianceData.name + '\n' +
            '    </span>\n';

        if (allianceData.id > 1) {
            html_info += '' +
                '    <span class="aa-intel-alliance-links-wrapper">\n' +
                '        <small>\n' +
                '            <a ' +
                '                class="aa-intel-information-link" ' +
                '                href="' + allianceData.dotlan + '" ' +
                '                target="_blank" ' +
                '                rel="noopener noreferer"' +
                '            >' +
                '               dotlan <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
                '            </a> |\n' +

                '            <a ' +
                '                class="aa-intel-information-link" ' +
                '                href="' + allianceData.zkillboard + '" ' +
                '                target="_blank" rel="noopener noreferer"' +
                '            >' +
                '                zkillboard <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
                '            </a>\n' +
                '        </small>\n' +
                '    </span>\n';
        }

        html_info += '' +
            '</span>';

        if (logoOnly) {
            if (allianceData.id === 1) {
                return '';
            }

            return html_logo;
        }

        return html_logo + html_info;
    };


    /**
     * Datatable Alliances Breakdown
     */
    elementAlliancesTable.DataTable({
        paging: false,
        language: aaIntelToolJsL10n.dataTables.translation,
        lengthChange: false,
        dom:
            '<\'row\'<\'col-sm-12\'f>>' +
            '<\'row\'<\'col-sm-12\'tr>>' +
            '<\'row\'<\'col-sm-12\'i>>',
        ajax: {
            url: aaIntelToolJsOptions.ajax.getAllianceList,
            dataSrc: '',
            cache: true
        },
        columns: [
            {
                data: (data) => {
                    return allianceInfoPanel(data, false);
                }
            },
            {
                data: 'count'
            },
            {
                data: 'ticker'
            }
        ],
        order: [
            [1, 'desc']
        ],
        columnDefs: [
            {
                targets: 1,
                createdCell: (td) => {
                    $(td).addClass('text-right');
                }
            },
            {
                targets: 2,
                visible: false
            }
        ],
        createdRow: (row, data) => {
            // Alliance total count
            const currentTotal = elementAlliancesTotalCount.html();
            const newTotal = parseInt(currentTotal) + 1;

            elementAlliancesTotalCount.html(newTotal);

            $(row)
                .addClass('aa-intel-alliance-participation-item aa-intel-alliance-id-' + data.id)
                .attr('data-alliance-id', data.id);

            // Highlight
            $(row).on('mouseenter', () => {
                $(row).addClass('dataHighlight');

                corporationTableAddHighlightByAllianceId($(row));
                pilotTableAddHighlightByAllianceId($(row));
            }).on('mouseleave', () => {
                $(row).removeClass('dataHighlight');

                corporationTableRemoveHighlightByAllianceId($(row));
                pilotTableRemoveHighlightByAllianceId($(row));
            });

            // Sticky
            $(row).on('click', () => {
                if ($(row).hasClass('dataHighlightSticky')) {
                    $(row).removeClass('dataHighlightSticky');

                    corporationTableRemoveStickyByAllianceId($(row));
                    pilotTableRemoveStickyByAllianceId($(row));
                } else {
                    $(row).addClass('dataHighlightSticky');

                    corporationTableAddStickyByAllianceId($(row));
                    pilotTableAddStickyByAllianceId($(row));
                }
            }).on('click', '.aa-intel-information-link', (e) => {
                e.stopPropagation();
            });
        }
    });


    /**
     * Datatable Corporations Breakdown
     */
    elementCorporationsTable.DataTable({
        paging: false,
        language: aaIntelToolJsL10n.dataTables.translation,
        lengthChange: false,
        dom:
            '<\'row\'<\'col-sm-12\'f>>' +
            '<\'row\'<\'col-sm-12\'tr>>' +
            '<\'row\'<\'col-sm-12\'i>>',
        ajax: {
            url: aaIntelToolJsOptions.ajax.getCorporationList,
            dataSrc: '',
            cache: true
        },
        columns: [
            {
                data: (data) => {
                    return corporationInfoPanel(data, false);
                }
            },
            {
                data: 'count'
            },
            {
                data: 'ticker'
            }
        ],
        order: [
            [1, 'desc']
        ],
        columnDefs: [
            {
                targets: 1,
                createdCell: (td) => {
                    $(td).addClass('text-right');
                }
            },
            {
                targets: 2,
                visible: false
            }
        ],
        createdRow: (row, data) => {
            // Corporation total count
            const currentTotal = elementCorporationsTotalCount.html();
            const newTotal = parseInt(currentTotal) + 1;

            elementCorporationsTotalCount.html(newTotal);

            $(row)
                .addClass('aa-intel-corporation-participation-item aa-intel-corporation-id-' + data.id)
                .attr('data-corporation-id', data.id)
                .attr('data-alliance-id', data.alliance.id);

            // Highlight
            $(row).on('mouseenter', () => {
                $(row).addClass('dataHighlight');

                allianceTableAddHighlightByAllianceId($(row));
                pilotTableAddHighlightByCorporationId($(row));
            }).on('mouseleave', () => {
                $(row).removeClass('dataHighlight');

                allianceTableRemoveHighlightByAllianceId($(row));
                pilotTableRemoveHighlightByCorporationId($(row));
            });

            // Sticky
            $(row).on('click', () => {
                if ($(row).hasClass('dataHighlightSticky')) {
                    $(row).removeClass('dataHighlightSticky');

                    pilotTableRemoveStickyByCorporationId($(row));

                    if (removeAllianceStickyComplete($(row)) === true) {
                        allianceTableRemoveStickyByAllianceId($(row));
                    }
                } else {
                    $(row).addClass('dataHighlightSticky');

                    allianceTableAddStickyByAllianceId($(row));
                    pilotTableAddStickyByCorporationId($(row));
                }
            }).on('click', '.aa-intel-information-link', (e) => {
                e.stopPropagation();
            });
        }
    });


    /**
     * Datatable Pilots Breakdown
     */
    elementPilotsTable.DataTable({
        paging: false,
        language: aaIntelToolJsL10n.dataTables.translation,
        lengthChange: false,
        dom:
            '<\'row\'<\'col-sm-12\'f>>' +
            '<\'row\'<\'col-sm-12\'tr>>' +
            '<\'row\'<\'col-sm-12\'i>>',
        ajax: {
            url: aaIntelToolJsOptions.ajax.getPilotList,
            dataSrc: '',
            cache: true
        },
        columns: [
            {
                data: (data) => {
                    return pilotInfoPanel(data);
                }
            },
            {
                data: (data) => {
                    return allianceInfoPanel(data.corporation.alliance, true) + data.corporation.alliance.ticker;
                }
            },
            {
                data: (data) => {
                    return corporationInfoPanel(data.corporation, true) + data.corporation.ticker;
                }
            },
            {
                data: 'corporation.alliance.name'
            },
            {
                data: 'corporation.name'
            }
        ],
        order: [
            [0, 'asc']
        ],
        columnDefs: [
            {
                targets: [3, 4],
                visible: false
            }
        ],
        createdRow: (row, data) => {
            // Pilot total count
            const currentTotal = elementPilotsTotalCount.html();
            const newTotal = parseInt(currentTotal) + 1;

            elementPilotsTotalCount.html(newTotal);

            $(row)
                .addClass('aa-intel-corporation-participation-item aa-intel-corporation-id-' + data.id)
                .attr('data-character-id', data.id)
                .attr('data-corporation-id', data.corporation.id)
                .attr('data-alliance-id', data.corporation.alliance.id);

            // Highlight
            $(row).on('mouseenter', () => {
                $(row).addClass('dataHighlight');

                allianceTableAddHighlightByAllianceId($(row));
                corporationTableAddHighlightByCorporationId($(row));
            }).on('mouseleave', () => {
                $(row).removeClass('dataHighlight');

                allianceTableRemoveHighlightByAllianceId($(row));
                corporationTableRemoveHighlightByCorporationId($(row));
            });

            // Sticky
            $(row).on('click', () => {
                if ($(row).hasClass('dataHighlightSticky')) {
                    $(row).removeClass('dataHighlightSticky');

                    if (removeCorporationStickyComplete($(row)) === true) {
                        corporationTableRemoveStickyByCorporationId($(row));
                    }

                    if (removeAllianceStickyComplete($(row)) === true) {
                        allianceTableRemoveStickyByAllianceId($(row));
                    }
                } else {
                    $(row).addClass('dataHighlightSticky');

                    allianceTableAddStickyByAllianceId($(row));
                    corporationTableAddStickyByCorporationId($(row));
                }
            }).on('click', '.aa-intel-information-link', (e) => {
                e.stopPropagation();
            });
        }
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
    const removeCorporationStickyComplete = ((element) => {
        let removeCorporationSticky = true;

        $('table.aa-intel-pilot-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each((i, el) => {
            if ($(el).hasClass('dataHighlightSticky')) {
                removeCorporationSticky = false;
            }
        });

        return removeCorporationSticky;
    });


    /**
     * Determine if we can remove all sticky states for this alliance
     *
     * @param {type} element
     * @returns {Boolean}
     */
    const removeAllianceStickyComplete = ((element) => {
        let removeAllianceSticky = true;

        $('table.aa-intel-pilot-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each((i, el) => {
            if ($(el).hasClass('dataHighlightSticky')) {
                removeAllianceSticky = false;
            }
        });

        return removeAllianceSticky;
    });


    /**
     * Helper function
     *
     * @type {allianceTableAddStickyByAllianceId}
     */
    const allianceTableAddStickyByAllianceId = ((element) => {
        $('table.aa-intel-alliance-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each((i, el) => {
            $(el).addClass('dataHighlightSticky');
        });
    });


    /**
     * Helper function
     *
     * @type {allianceTableAddHighlightByAllianceId}
     */
    const allianceTableAddHighlightByAllianceId = ((element) => {
        $('table.aa-intel-alliance-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each((i, el) => {
            $(el).addClass('dataHighlight');
        });
    });


    /**
     * Helper function
     *
     * @type {allianceTableRemoveStickyByAllianceId}
     */
    const allianceTableRemoveStickyByAllianceId = ((element) => {
        $('table.aa-intel-alliance-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each((i, el) => {
            $(el).removeClass('dataHighlightSticky');
        });
    });


    /**
     * Helper function
     *
     * @type {allianceTableRemoveHighlightByAllianceId}
     */
    const allianceTableRemoveHighlightByAllianceId = ((element) => {
        $('table.aa-intel-alliance-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each((i, el) => {
            $(el).removeClass('dataHighlight');
        });
    });


    /**
     * Helper function
     *
     * @type {corporationTableAddStickyByCorporationId}
     */
    const corporationTableAddStickyByCorporationId = ((element) => {
        $('table.aa-intel-corporation-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each((i, el) => {
            $(el).addClass('dataHighlightSticky');
        });
    });


    /**
     * Helper function
     *
     * @type {corporationTableAddHighlightByCorporationId}
     */
    const corporationTableAddHighlightByCorporationId = ((element) => {
        $('table.aa-intel-corporation-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each((i, el) => {
            $(el).addClass('dataHighlight');
        });
    });


    /**
     * Helper function
     *
     * @type {corporationTableAddStickyByAllianceId}
     */
    const corporationTableAddStickyByAllianceId = ((element) => {
        $('table.aa-intel-corporation-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each((i, el) => {
            $(el).addClass('dataHighlightSticky');
        });
    });


    /**
     * Helper function
     *
     * @type {corporationTableAddHighlightByAllianceId}
     */
    const corporationTableAddHighlightByAllianceId = ((element) => {
        $('table.aa-intel-corporation-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each((i, el) => {
            $(el).addClass('dataHighlight');
        });
    });


    /**
     * Helper function
     *
     * @type {corporationTableRemoveStickyByCorporationId}
     */
    const corporationTableRemoveStickyByCorporationId = ((element) => {
        $('table.aa-intel-corporation-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each((i, el) => {
            $(el).removeClass('dataHighlightSticky');
        });
    });


    /**
     * Helper function
     *
     * @type {corporationTableRemoveHighlightByCorporationId}
     */
    const corporationTableRemoveHighlightByCorporationId = ((element) => {
        $('table.aa-intel-corporation-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each((i, el) => {
            $(el).removeClass('dataHighlight');
        });
    });


    /**
     * Helper function
     *
     * @type {corporationTableRemoveStickyByAllianceId}
     */
    const corporationTableRemoveStickyByAllianceId = ((element) => {
        $('table.aa-intel-corporation-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each((i, el) => {
            $(el).removeClass('dataHighlightSticky');
        });
    });


    /**
     * Helper function
     *
     * @type {corporationTableRemoveHighlightByAllianceId}
     */
    const corporationTableRemoveHighlightByAllianceId = ((element) => {
        $('table.aa-intel-corporation-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each((i, el) => {
            $(el).removeClass('dataHighlight');
        });
    });


    /**
     * Helper function
     *
     * @type {pilotTableAddStickyByCorporationId}
     */
    const pilotTableAddStickyByCorporationId = ((element) => {
        $('table.aa-intel-pilot-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each((i, el) => {
            $(el).addClass('dataHighlightSticky');
        });
    });


    /**
     * Helper function
     *
     * @type {pilotTableAddHighlightByCorporationId}
     */
    const pilotTableAddHighlightByCorporationId = ((element) => {
        $('table.aa-intel-pilot-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each((i, el) => {
            $(el).addClass('dataHighlight');
        });
    });


    /**
     * Helper function
     *
     * @type {pilotTableAddStickyByAllianceId}
     */
    const pilotTableAddStickyByAllianceId = ((element) => {
        $('table.aa-intel-pilot-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each((i, el) => {
            $(el).addClass('dataHighlightSticky');
        });
    });


    /**
     * Helper function
     *
     * @type {pilotTableAddHighlightByAllianceId}
     */
    const pilotTableAddHighlightByAllianceId = ((element) => {
        $('table.aa-intel-pilot-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each((i, el) => {
            $(el).addClass('dataHighlight');
        });
    });


    /**
     * Helper function
     *
     * @type {pilotTableRemoveStickyByCorporationId}
     */
    const pilotTableRemoveStickyByCorporationId = ((element) => {
        $('table.aa-intel-pilot-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each((i, el) => {
            $(el).removeClass('dataHighlightSticky');
        });
    });


    /**
     * Helper function
     *
     * @type {pilotTableRemoveHighlightByCorporationId}
     */
    const pilotTableRemoveHighlightByCorporationId = ((element) => {
        $('table.aa-intel-pilot-participation-list tr[data-corporation-id="' + element.data('corporationId') + '"]').each((i, el) => {
            $(el).removeClass('dataHighlight');
        });
    });


    /**
     * Helper function
     *
     * @type {pilotTableRemoveStickyByAllianceId}
     */
    const pilotTableRemoveStickyByAllianceId = ((element) => {
        $('table.aa-intel-pilot-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each((i, el) => {
            $(el).removeClass('dataHighlightSticky');
        });
    });


    /**
     * Helper function
     *
     * @type {pilotTableRemoveHighlightByAllianceId}
     */
    const pilotTableRemoveHighlightByAllianceId = ((element) => {
        $('table.aa-intel-pilot-participation-list tr[data-alliance-id="' + element.data('allianceId') + '"]').each((i, el) => {
            $(el).removeClass('dataHighlight');
        });
    });
});
