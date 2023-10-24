/* global fetchAjaxData, aaIntelToolJsOptions, aaIntelToolJsL10n, shipInfoPanel, pilotInfoPanel, addFleetcompositionHightlight, removeFleetcompositionHightlight */

jQuery(document).ready(($) => {
    'use strict';

    const elementShipClassesTable = $('table.aa-intel-dscan-ship-classes-ship-classes-list');
    const elementShipTypesTable = $('table.aa-intel-dscan-ship-types-list');
    const elementFleetcompositionTable = $('table.aa-intel-fleetcomp-pilot-ships-list');
    const elementPilotsCount = $('span#aa-intel-fleet-participation-count');


    /**
     * Datatable Ship Classes
     */
    fetchAjaxData(aaIntelToolJsOptions.ajax.getShipClasses).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-ship-classes').hide();

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-ship-classes').show();
            } else {
                $('div.table-dscan-ship-classes-ship-classes').show();

                elementShipClassesTable.DataTable({
                    data: tableData,
                    paging: false,
                    language: aaIntelToolJsL10n.dataTables.translation,
                    lengthChange: false,
                    dom:
                        '<\'row\'<\'col-sm-12\'f>>' +
                        '<\'row\'<\'col-sm-12\'tr>>' +
                        '<\'row\'<\'col-sm-12\'i>>',
                    columns: [
                        {
                            data: (data) => {
                                return shipInfoPanel(data);
                            }
                        },
                        {
                            data: 'count'
                        },
                        {
                            data: 'type_name'
                        }
                    ],
                    order: [
                        [1, 'desc']
                    ],
                    columnDefs: [
                        {
                            targets: 0,
                            createdCell: (td) => {
                                $(td).addClass('text-ellipsis');
                            }
                        },
                        {
                            targets: 1,
                            width: 45,
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
                        $(row)
                            .attr('data-shipclass-id', data.id)
                            .attr('data-shiptype-id', data.type_id);

                        // Highlight
                        $(row).mouseenter(() => {
                            addFleetcompositionHightlight('shipclass', $(row));
                        }).mouseleave(() => {
                            removeFleetcompositionHightlight('shipclass', $(row));
                        });
                    }
                });
            }
        }
    });


    /**
     * Datatable Ship Types
     */
    fetchAjaxData(aaIntelToolJsOptions.ajax.getShipTypes).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-ship-types').hide();

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-ship-types').show();
            } else {
                $('div.table-dscan-ship-types').show();

                elementShipTypesTable.DataTable({
                    data: tableData,
                    paging: false,
                    language: aaIntelToolJsL10n.dataTables.translation,
                    lengthChange: false,
                    dom:
                        '<\'row\'<\'col-sm-12\'f>>' +
                        '<\'row\'<\'col-sm-12\'tr>>' +
                        '<\'row\'<\'col-sm-12\'i>>',
                    columns: [
                        {
                            data: 'name'
                        },
                        {
                            data: 'count'
                        }
                    ],
                    order: [
                        [1, 'desc']
                    ],
                    columnDefs: [
                        {
                            targets: 1,
                            width: 45,
                            createdCell: (td) => {
                                $(td).addClass('text-right');
                            }
                        }
                    ],
                    createdRow: (row, data) => {
                        $(row).attr('data-shiptype-id', data.id);

                        // Highlight
                        $(row).mouseenter(() => {
                            addFleetcompositionHightlight('shiptype', $(row));
                        }).mouseleave(() => {
                            removeFleetcompositionHightlight('shiptype', $(row));
                        });
                    }
                });
            }
        }
    });


    /**
     * Datatable Fleetcomp Details
     */
    fetchAjaxData(aaIntelToolJsOptions.ajax.getFleetComposition).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-fleetcomp-pilot-ships').hide();

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-fleetcomp-pilot-ships').show();
            } else {
                $('div.table-fleetcomp-pilot-ships').show();

                elementFleetcompositionTable.DataTable({
                    data: tableData,
                    paging: false,
                    language: aaIntelToolJsL10n.dataTables.translation,
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
                            data: 'ship'
                        },
                        {
                            data: 'solarsystem'
                        }
                    ],
                    order: [
                        [1, 'desc']
                    ],
                    columnDefs: [
                        {
                            targets: 0,
                            createdCell: (td) => {
                                $(td).addClass('fix-eve-image-position');
                            }
                        }
                    ],
                    createdRow: (row, data) => {
                        // Pilots total count
                        const currentTotal = elementPilotsCount.html();
                        const newTotal = parseInt(currentTotal) + 1;

                        elementPilotsCount.html(newTotal);

                        $(row)
                            .attr('data-shipclass-id', data.ship_id)
                            .attr('data-shiptype-id', data.ship_type_id);

                        // Highlight
                        $(row).mouseenter(() => {
                            addFleetcompositionHightlight('shiptype', $(row));
                        }).mouseleave(() => {
                            removeFleetcompositionHightlight('shiptype', $(row));
                        });
                    }
                });
            }
        }
    });
});