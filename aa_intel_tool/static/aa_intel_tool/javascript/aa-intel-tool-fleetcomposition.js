/* global fetchAjaxData, aaIntelToolJsSettings, bootstrapTooltip, shipInfoPanel, pilotInfoPanel, addFleetcompositionHightlight, removeFleetcompositionHightlight, changeFleetcompositionStickyHighlight */

$(() => {
    'use strict';

    const elementShipClassesTable = $('table.aa-intel-dscan-ship-classes-ship-classes-list');
    const elementShipClassesMass = $('span#aa-intel-dscan-ship-classes-mass');
    const elementShipTypesTable = $('table.aa-intel-dscan-ship-types-list');
    const elementFleetcompositionTable = $('table.aa-intel-fleetcomp-pilot-ships-list');
    const elementPilotsCount = $('span#aa-intel-fleet-participation-count');


    /**
     * Datatable Ship Classes
     */
    fetchAjaxData(aaIntelToolJsSettings.url.getShipClasses).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-ship-classes').addClass('d-none');

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-ship-classes').removeClass('d-none');
            } else {
                $('div.table-dscan-ship-classes-ship-classes').removeClass('d-none');

                elementShipClassesTable.DataTable({
                    data: tableData,
                    paging: false,
                    language: aaIntelToolJsSettings.translation.dataTables,
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
                                $(td).addClass('text-end');
                            }
                        },
                        {
                            targets: 2,
                            visible: false
                        }
                    ],
                    createdRow: (row, data) => {
                        const currentMass = elementShipClassesMass.data('mass') || 0;
                        const newMass = parseInt(currentMass) + data.mass;

                        elementShipClassesMass.data('mass', newMass);
                        elementShipClassesMass.html(
                            new Intl.NumberFormat(
                                aaIntelToolJsSettings.language
                            ).format(newMass)
                        );

                        $(row)
                            .attr('data-shipclass-id', data.id)
                            .attr('data-shiptype-id', data.type_id);

                        // Highlight
                        $(row).mouseenter(() => {
                            addFleetcompositionHightlight('shipclass', $(row));
                        }).mouseleave(() => {
                            removeFleetcompositionHightlight('shipclass', $(row));
                        });

                        // Sticky
                        $(row).click((event) => {
                            const target = $(event.target);

                            if (target.hasClass('aa-intel-information-link')) {
                                event.stopPropagation();
                            } else {
                                changeFleetcompositionStickyHighlight('shipclass', $(row));
                            }
                        });
                    }
                });
            }
        }
    }).then(() => {
        // Initialize Bootstrap tooltips
        bootstrapTooltip('.aa-intel-dscan-ship-classes-ship-classes-list');
    });


    /**
     * Datatable Ship Types
     */
    fetchAjaxData(aaIntelToolJsSettings.url.getShipTypes).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-ship-types').addClass('d-none');

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-ship-types').removeClass('d-none');
            } else {
                $('div.table-dscan-ship-types').removeClass('d-none');

                elementShipTypesTable.DataTable({
                    data: tableData,
                    paging: false,
                    language: aaIntelToolJsSettings.translation.dataTables,
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
                                $(td).addClass('text-end');
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

                        // Sticky
                        $(row).click((event) => {
                            const target = $(event.target);

                            if (target.hasClass('aa-intel-information-link')) {
                                event.stopPropagation();
                            } else {
                                changeFleetcompositionStickyHighlight('shiptype', $(row));
                            }
                        });
                    }
                });
            }
        }
    }).then(() => {
        // Initialize Bootstrap tooltips
        bootstrapTooltip('.aa-intel-dscan-ship-types-list');
    });


    /**
     * Datatable Fleetcomp Details
     */
    fetchAjaxData(aaIntelToolJsSettings.url.getFleetComposition).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-fleetcomp-pilot-ships').addClass('d-none');

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-fleetcomp-pilot-ships').removeClass('d-none');
            } else {
                $('div.table-fleetcomp-pilot-ships').removeClass('d-none');

                elementFleetcompositionTable.DataTable({
                    data: tableData,
                    paging: false,
                    language: aaIntelToolJsSettings.translation.dataTables,
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
                        [0, 'asc']
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

                        // Sticky
                        $(row).click((event) => {
                            const target = $(event.target);

                            if (target.hasClass('aa-intel-information-link')) {
                                event.stopPropagation();
                            } else {
                                changeFleetcompositionStickyHighlight('shiptype', $(row));
                            }
                        });
                    }
                });
            }
        }
    }).then(() => {
        // Initialize Bootstrap tooltips
        bootstrapTooltip('.aa-intel-fleetcomp-pilot-ships-list');
    });
});
