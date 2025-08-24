/* global _getAaIntelToolJsSettings, _toggleChatscanStickyHighlight, bootstrapTooltip, fetchGet, pilotInfoPanel, corporationInfoPanel, allianceInfoPanel */

$(document).ready(() => {
    'use strict';

    /* Variables and helpers
    --------------------------------------------------------------------------------- */
    const settings = _getAaIntelToolJsSettings();
    const elements = {
        // Tables
        pilotsTable: $('table.aa-intel-pilot-participation-list'),
        corporationsTable: $('table.aa-intel-corporation-participation-list'),
        alliancesTable: $('table.aa-intel-alliance-participation-list'),

        // Totals counters
        pilotsTotalCount: $('span#aa-intel-pilots-count'),
        corporationsTotalCount: $('span#aa-intel-corporations-count'),
        alliancesTotalCount: $('span#aa-intel-alliances-count')
    };

    /* DataTables
    --------------------------------------------------------------------------------- */
    /**
     * Datatable Alliances Breakdown
     */
    fetchGet({url: settings.url.getAllianceList})
        .then((tableData) => {
            if (tableData) {
                $('div.aa-intel-loading-table-info-alliance-participation-list').addClass('d-none');

                if (Object.keys(tableData).length === 0) {
                    $('div.aa-intel-empty-table-info-alliance-participation-list').removeClass('d-none');
                } else {
                    $('div.table-local-scan-alliances').removeClass('d-none');

                    elements.alliancesTable.DataTable({
                        data: tableData,
                        paging: false,
                        language: settings.language.dataTables,
                        lengthChange: false,
                        dom:
                            '<\'row\'<\'col-sm-12\'f>>' +
                            '<\'row\'<\'col-sm-12\'tr>>' +
                            '<\'row\'<\'col-sm-12\'i>>',
                        columns: [
                            {
                                data: (data) => {
                                    return allianceInfoPanel(data);
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
                                targets: 0,
                                createdCell: (td) => {
                                    $(td).addClass('text-ellipsis fix-eve-image-position');
                                }
                            },
                            {
                                targets: 1,
                                width: 35,
                                createdCell: (td) => {
                                    $(td).addClass('text-end');
                                }
                            },
                            {
                                targets: 2,
                                visible: false
                            }
                        ],
                        createdRow: (row, data) => {
                            // Alliance total count
                            const currentTotal = elements.alliancesTotalCount.html();
                            let newTotal;

                            if (data.id !== 1) {
                                newTotal = parseInt(currentTotal) + 1;
                            }

                            elements.alliancesTotalCount.html(newTotal);

                            $(row)
                                .addClass(`aa-intel-alliance-participation-item aa-intel-alliance-id-${data.id}`)
                                .attr('data-alliance-id', data.id);
                        },
                        initComplete: () => {
                            const classTableRow = $('.aa-intel-alliance-participation-item');

                            _toggleChatscanStickyHighlight({
                                element: classTableRow,
                                type: 'alliance'
                            });

                            // Initialize Bootstrap tooltips
                            bootstrapTooltip({selector: '.aa-intel-alliance-participation-list'});
                        }
                    });
                }
            }
        })
        .catch((error) => {
            console.error('Error fetching alliance list data:', error);
        });

    /**
     * Datatable Corporations Breakdown
     */
    fetchGet({url: settings.url.getCorporationList})
        .then((tableData) => {
            if (tableData) {
                $('div.aa-intel-loading-table-info-corporation-participation-list').addClass('d-none');

                if (Object.keys(tableData).length === 0) {
                    $('div.aa-intel-empty-table-info-corporation-participation-list').removeClass('d-none');
                } else {
                    $('div.table-local-scan-corporations').removeClass('d-none');

                    elements.corporationsTable.DataTable({
                        data: tableData,
                        paging: false,
                        language: settings.language.dataTables,
                        lengthChange: false,
                        dom:
                            '<\'row\'<\'col-sm-12\'f>>' +
                            '<\'row\'<\'col-sm-12\'tr>>' +
                            '<\'row\'<\'col-sm-12\'i>>',
                        columns: [
                            {
                                data: (data) => {
                                    return corporationInfoPanel(data);
                                }
                            },
                            {
                                data: 'count'
                            },
                            {
                                data: 'ticker'
                            },
                            {
                                data: 'alliance.name'
                            },
                            {
                                data: 'alliance.ticker'
                            }
                        ],
                        order: [
                            [1, 'desc']
                        ],
                        columnDefs: [
                            {
                                targets: 0,
                                createdCell: (td) => {
                                    $(td).addClass('text-ellipsis fix-eve-image-position');
                                }
                            },
                            {
                                targets: 1,
                                width: 35,
                                createdCell: (td) => {
                                    $(td).addClass('text-end');
                                }
                            },
                            {
                                targets: [2, 3, 4],
                                visible: false
                            }
                        ],
                        createdRow: (row, data) => {
                            // Corporation total count
                            const currentTotal = elements.corporationsTotalCount.html();
                            const newTotal = parseInt(currentTotal) + 1;

                            elements.corporationsTotalCount.html(newTotal);

                            $(row)
                                .addClass(`aa-intel-corporation-participation-item aa-intel-corporation-id-${data.id} aa-intel-alliance-id-${data.alliance.id}`)
                                .attr('data-corporation-id', data.id)
                                .attr('data-alliance-id', data.alliance.id);
                        },
                        initComplete: () => {
                            const classTableRow = $('.aa-intel-corporation-participation-item');

                            _toggleChatscanStickyHighlight({
                                element: classTableRow,
                                type: 'corporation'
                            });

                            // Initialize Bootstrap tooltips
                            bootstrapTooltip({selector: '.aa-intel-corporation-participation-list'});
                        }
                    });
                }
            }
        })
        .catch((error) => {
            console.error('Error fetching corporation list data:', error);
        });

    /**
     * Datatable Pilots Breakdown
     */
    fetchGet({url: settings.url.getPilotList})
        .then((tableData) => {
            if (tableData) {
                $('div.aa-intel-loading-table-info-pilot-participation-list').addClass('d-none');

                if (Object.keys(tableData).length === 0) {
                    $('div.aa-intel-empty-table-info-pilot-participation-list').removeClass('d-none');
                } else {
                    $('div.table-local-scan-pilots').removeClass('d-none');

                    elements.pilotsTable.DataTable({
                        data: tableData,
                        paging: false,
                        language: settings.language.dataTables,
                        lengthChange: false,
                        dom:
                            '<\'row\'<\'col-sm-12\'f>>' +
                            '<\'row\'<\'col-sm-12\'tr>>' +
                            '<\'row\'<\'col-sm-12\'i>>',
                        columns: [
                            {
                                data: (data) => {
                                    return pilotInfoPanel(data);
                                }
                            },
                            {
                                data: (data) => {
                                    return allianceInfoPanel(data.alliance, true) + data.alliance.ticker;
                                }
                            },
                            {
                                data: (data) => {
                                    return corporationInfoPanel(data.corporation, true) + data.corporation.ticker;
                                }
                            },
                            {
                                data: 'alliance.name'
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
                                targets: 0,
                                createdCell: (td) => {
                                    $(td).addClass('text-ellipsis fix-eve-image-position');
                                }
                            },
                            {
                                targets: 1,
                                width: 125
                            },
                            {
                                targets: 2,
                                width: 125
                            },
                            {
                                targets: [3, 4],
                                visible: false
                            }
                        ],
                        createdRow: (row, data) => {
                            // Pilot total count
                            const currentTotal = elements.pilotsTotalCount.html();
                            const newTotal = parseInt(currentTotal) + 1;

                            elements.pilotsTotalCount.html(newTotal);

                            $(row)
                                .addClass(`aa-intel-pilot-participation-item aa-intel-character-id-${data.id} aa-intel-corporation-id-${data.corporation.id} aa-intel-alliance-id-${data.alliance.id}`)
                                .attr('data-character-id', data.id)
                                .attr('data-corporation-id', data.corporation.id)
                                .attr('data-alliance-id', data.alliance.id);
                        },
                        initComplete: () => {
                            const classTableRow = $('.aa-intel-pilot-participation-item');

                            _toggleChatscanStickyHighlight({
                                element: classTableRow,
                                type: 'pilot'
                            });

                            // Initialize Bootstrap tooltips
                            bootstrapTooltip({selector: '.aa-intel-pilot-participation-list'});
                        }
                    });
                }
            }
        })
        .catch((error) => {
            console.error('Error fetching pilot list data:', error);
        });
});
