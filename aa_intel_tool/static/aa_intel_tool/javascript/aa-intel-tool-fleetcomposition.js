/* global fetchGet, _getAaIntelToolJsSettings, _numberFormatter, bootstrapTooltip, shipInfoPanel, pilotInfoPanel, _toggleFleetcompStickyHighlight */

$(() => {
    'use strict';

    /* Variables and helpers
    --------------------------------------------------------------------------------- */
    const settings = _getAaIntelToolJsSettings();
    const elements = {
        shipClassesTable: $('table.aa-intel-dscan-ship-classes-ship-classes-list'),
        shipClassesMass: $('span#aa-intel-dscan-ship-classes-mass'),
        shipTypesTable: $('table.aa-intel-dscan-ship-types-list'),
        fleetcompositionTable: $('table.aa-intel-fleetcomp-pilot-ships-list'),
        pilotsCount: $('span#aa-intel-fleet-participation-count')
    };

    /* DataTables
    --------------------------------------------------------------------------------- */
    /**
     * Datatable Ship Classes
     */
    fetchGet({url: settings.url.getShipClasses})
        .then((tableData) => {
            if (tableData) {
                $('div.aa-intel-loading-table-info-ship-classes').addClass('d-none');

                if (Object.keys(tableData).length === 0) {
                    $('div.aa-intel-empty-table-info-ship-classes').removeClass('d-none');
                } else {
                    $('div.table-dscan-ship-classes-ship-classes').removeClass('d-none');

                    elements.shipClassesTable.DataTable({
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
                            const currentMass = elements.shipClassesMass.data('mass') || 0;
                            const newMass = parseInt(currentMass) + data.mass;

                            elements.shipClassesMass.data('mass', newMass);
                            elements.shipClassesMass.html(_numberFormatter(newMass));

                            $(row)
                                .addClass(`aa-intel-shipclass-item aa-intel-shipclass-id-${data.id} aa-intel-shiptype-id-${data.type_id}`)
                                .attr('data-shipclass-id', data.id)
                                .attr('data-shiptype-id', data.type_id);
                        },
                        initComplete: () => {
                            const classTableRow = $('.aa-intel-shipclass-item');

                            _toggleFleetcompStickyHighlight({
                                element: classTableRow,
                                type: 'shipclass'
                            });

                            // Initialize Bootstrap tooltips
                            bootstrapTooltip({selector: '.aa-intel-dscan-ship-classes-ship-classes-list'});
                        }
                    });
                }
            }
        })
        .catch((error) => {
            console.error('Error fetching ship classes data:', error);
        });

    /**
     * Datatable Ship Types
     */
    fetchGet({url: settings.url.getShipTypes})
        .then((tableData) => {
            if (tableData) {
                $('div.aa-intel-loading-table-info-ship-types').addClass('d-none');

                if (Object.keys(tableData).length === 0) {
                    $('div.aa-intel-empty-table-info-ship-types').removeClass('d-none');
                } else {
                    $('div.table-dscan-ship-types').removeClass('d-none');

                    elements.shipTypesTable.DataTable({
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
                            }
                        ],
                        createdRow: (row, data) => {
                            $(row)
                                .addClass(`aa-intel-shiptype-item aa-intel-shiptype-id-${data.id}`)
                                .attr('data-shiptype-id', data.id);
                        },
                        initComplete: () => {
                            const classTableRow = $('.aa-intel-shiptype-item');

                            _toggleFleetcompStickyHighlight({
                                element: classTableRow,
                                type: 'shiptype'
                            });

                            // Initialize Bootstrap tooltips
                            bootstrapTooltip({selector: '.aa-intel-dscan-ship-types-list'});
                        }
                    });
                }
            }
        })
        .catch((error) => {
            console.error('Error fetching ship types data:', error);
        });

    /**
     * Datatable Fleetcomp Details
     */
    fetchGet({url: settings.url.getFleetComposition})
        .then((tableData) => {
            if (tableData) {
                $('div.aa-intel-loading-table-info-fleetcomp-pilot-ships').addClass('d-none');

                if (Object.keys(tableData).length === 0) {
                    $('div.aa-intel-empty-table-info-fleetcomp-pilot-ships').removeClass('d-none');
                } else {
                    $('div.table-fleetcomp-pilot-ships').removeClass('d-none');

                    elements.fleetcompositionTable.DataTable({
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
                            const currentTotal = elements.pilotsCount.html();
                            const newTotal = parseInt(currentTotal) + 1;

                            elements.pilotsCount.html(newTotal);

                            $(row)
                                .addClass(`aa-intel-pilotship-item aa-intel-shipclass-id-${data.ship_id} aa-intel-shiptype-id-${data.ship_type_id}`)
                                .attr('data-shipclass-id', data.ship_id)
                                .attr('data-shiptype-id', data.ship_type_id);
                        },
                        initComplete: () => {
                            const classTableRow = $('.aa-intel-pilotship-item');

                            _toggleFleetcompStickyHighlight({
                                element: classTableRow,
                                type: 'shiptype'
                            });

                            // Initialize Bootstrap tooltips
                            bootstrapTooltip({selector: '.aa-intel-fleetcomp-pilot-ships-list'});
                        }
                    });
                }
            }
        })
        .catch((error) => {
            console.error('Error fetching fleet composition data:', error);
        });
});
