/* global aaIntelToolJsSettings, addChatscanHighlight, bootstrapTooltip, removeChatscanHighlight, changeChatscanStickyHighlight, fetchAjaxData, pilotInfoPanel, corporationInfoPanel, allianceInfoPanel */

$(() => {
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
     * Datatable Alliances Breakdown
     */
    fetchAjaxData(aaIntelToolJsSettings.url.getAllianceList).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-alliance-participation-list').addClass('d-none');

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-alliance-participation-list').removeClass('d-none');
            } else {
                $('div.table-local-scan-alliances').removeClass('d-none');

                elementAlliancesTable.DataTable({
                    data: tableData,
                    paging: false,
                    language: aaIntelToolJsSettings.language.dataTables,
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
                        const currentTotal = elementAlliancesTotalCount.html();
                        let newTotal;

                        if (data.id !== 1) {
                            newTotal = parseInt(currentTotal) + 1;
                        }

                        elementAlliancesTotalCount.html(newTotal);

                        $(row)
                            .addClass(`aa-intel-alliance-participation-item aa-intel-alliance-id-${data.id}`)
                            .attr('data-alliance-id', data.id);
                    }
                });
            }
        }
    }).then(() => {
        const classTableRow = $('.aa-intel-alliance-participation-item');

        // Highlight
        classTableRow.mouseenter((event) => {
            addChatscanHighlight('alliance', $(event.currentTarget));
        }).mouseleave((event) => {
            removeChatscanHighlight('alliance', $(event.currentTarget));
        });

        // Sticky
        classTableRow.click((event) => {
            if ($(event.target).hasClass('aa-intel-information-link')) {
                event.stopPropagation();
            } else {
                changeChatscanStickyHighlight('alliance', $(event.currentTarget));
            }
        });

        // Initialize Bootstrap tooltips
        bootstrapTooltip('.aa-intel-alliance-participation-list');
    });


    /**
     * Datatable Corporations Breakdown
     */
    fetchAjaxData(aaIntelToolJsSettings.url.getCorporationList).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-corporation-participation-list').addClass('d-none');

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-corporation-participation-list').removeClass('d-none');
            } else {
                $('div.table-local-scan-corporations').removeClass('d-none');

                elementCorporationsTable.DataTable({
                    data: tableData,
                    paging: false,
                    language: aaIntelToolJsSettings.language.dataTables,
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
                        const currentTotal = elementCorporationsTotalCount.html();
                        const newTotal = parseInt(currentTotal) + 1;

                        elementCorporationsTotalCount.html(newTotal);

                        $(row)
                            .addClass(`aa-intel-corporation-participation-item aa-intel-corporation-id-${data.id} aa-intel-alliance-id-${data.alliance.id}`)
                            .attr('data-corporation-id', data.id)
                            .attr('data-alliance-id', data.alliance.id);
                    }
                });
            }
        }
    }).then(() => {
        const classTableRow = $('.aa-intel-corporation-participation-item');

        // Highlight
        classTableRow.mouseenter((event) => {
            addChatscanHighlight('corporation', $(event.currentTarget));
        }).mouseleave((event) => {
            removeChatscanHighlight('corporation', $(event.currentTarget));
        });

        // Sticky
        classTableRow.click((event) => {
            if ($(event.target).hasClass('aa-intel-information-link')) {
                event.stopPropagation();
            } else {
                changeChatscanStickyHighlight('corporation', $(event.currentTarget));
            }
        });

        // Initialize Bootstrap tooltips
        bootstrapTooltip('.aa-intel-corporation-participation-list');
    });


    /**
     * Datatable Pilots Breakdown
     */
    fetchAjaxData(aaIntelToolJsSettings.url.getPilotList).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-pilot-participation-list').addClass('d-none');

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-pilot-participation-list').removeClass('d-none');
            } else {
                $('div.table-local-scan-pilots').removeClass('d-none');

                elementPilotsTable.DataTable({
                    data: tableData,
                    paging: false,
                    language: aaIntelToolJsSettings.language.dataTables,
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
                        const currentTotal = elementPilotsTotalCount.html();
                        const newTotal = parseInt(currentTotal) + 1;

                        elementPilotsTotalCount.html(newTotal);

                        $(row)
                            .addClass(`aa-intel-pilot-participation-item aa-intel-character-id-${data.id} aa-intel-corporation-id-${data.corporation.id} aa-intel-alliance-id-${data.alliance.id}`)
                            .attr('data-character-id', data.id)
                            .attr('data-corporation-id', data.corporation.id)
                            .attr('data-alliance-id', data.alliance.id);
                    }
                });
            }
        }
    }).then(() => {
        const classTableRow = $('.aa-intel-pilot-participation-item');

        // Highlight
        classTableRow.mouseenter((event) => {
            addChatscanHighlight('pilot', $(event.currentTarget));
        }).mouseleave((event) => {
            removeChatscanHighlight('pilot', $(event.currentTarget));
        });

        // Sticky
        classTableRow.click((event) => {
            if ($(event.target).hasClass('aa-intel-information-link')) {
                event.stopPropagation();
            } else {
                changeChatscanStickyHighlight('pilot', $(event.currentTarget));
            }
        });

        // Initialize Bootstrap tooltips
        bootstrapTooltip('.aa-intel-pilot-participation-list');
    });
});
