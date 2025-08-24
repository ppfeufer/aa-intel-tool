/* global _getAaIntelToolJsSettings, _numberFormatter, bootstrapTooltip, fetchGet, shipInfoPanel, _toggleDscanStickyHighlight */

$(document).ready(() => {
    'use strict';

    /* Variables and helpers
    --------------------------------------------------------------------------------- */
    const settings = _getAaIntelToolJsSettings();
    const elements = {
        shipClassesAllTable: $('table.aa-intel-dscan-ship-classes-all-list'),
        dscanCountAll: $('span#aa-intel-dscan-all-count'),
        dscanMassAll: $('span#aa-intel-dscan-all-mass'),
        shipClassesOngridTable: $('table.aa-intel-dscan-ship-classes-ongrid-list'),
        dscanCountOngrid: $('span#aa-intel-dscan-ongrid-count'),
        dscanMassOnGrid: $('span#aa-intel-dscan-ongrid-mass'),
        shipClassesOffgridTable: $('table.aa-intel-dscan-ship-classes-offgrid-list'),
        dscanCountOffgrid: $('span#aa-intel-dscan-offgrid-count'),
        dscanMassOffGrid: $('span#aa-intel-dscan-offgrid-mass'),
        shipTypesTable: $('table.aa-intel-dscan-ship-types-list'),
        upwellStructuresTable: $('table.aa-intel-dscan-upwell-structures-list'),
        dscanCountUpwellStructures: $('span#aa-intel-dscan-upwell-structures-count'),
        deployablesTable: $('table.aa-intel-dscan-deployables-list'),
        dscanCountDeployables: $('span#aa-intel-dscan-deployables-count'),
        starbasesTable: $('table.aa-intel-dscan-starbases-list'),
        dscanCountStarbases: $('span#aa-intel-dscan-starbases-count')
    };

    /* DataTables
    --------------------------------------------------------------------------------- */
    /**
     * Datatable D-Scan All
     */
    fetchGet({url: settings.url.getShipClassesAll})
        .then((tableData) => {
            if (tableData) {
                $('div.aa-intel-loading-table-info-all').addClass('d-none');

                if (Object.keys(tableData).length === 0) {
                    $('div.aa-intel-empty-table-info-all').removeClass('d-none');
                } else {
                    $('div.table-dscan-ship-classes-all').removeClass('d-none');

                    elements.shipClassesAllTable.DataTable({
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
                            // D-Scan total count
                            const currentTotal = elements.dscanCountAll.html();
                            const newTotal = parseInt(currentTotal) + data.count;

                            elements.dscanCountAll.html(newTotal);

                            const currentMass = elements.dscanMassAll.data('mass') || 0;
                            const newMass = parseInt(currentMass) + data.mass;

                            elements.dscanMassAll.data('mass', newMass);
                            elements.dscanMassAll.html(_numberFormatter(newMass));

                            $(row)
                                .addClass(`aa-intel-shipclass-all-item aa-intel-shipclass-id-${data.id} aa-intel-shiptype-id-${data.type_id}`)
                                .attr('data-shipclass-id', data.id)
                                .attr('data-shiptype-id', data.type_id);
                        },
                        initComplete: () => {
                            const classTableRow = $('.aa-intel-shipclass-all-item');

                            _toggleDscanStickyHighlight({
                                element: classTableRow,
                                type: 'shipclass'
                            });

                            // Initialize Bootstrap tooltips
                            bootstrapTooltip({selector: '.aa-intel-dscan-ship-classes-all-list'});
                        }
                    });
                }
            }
        })
        .catch((error) => {
            console.error('Error fetching all ship classes data:', error);
        });

    /**
     * Datatable D-Scan On Grid
     */
    fetchGet({url: settings.url.getShipClassesOngrid})
        .then((tableData) => {
            if (tableData) {
                $('div.aa-intel-loading-table-info-ongrid').addClass('d-none');

                if (Object.keys(tableData).length === 0) {
                    $('div.aa-intel-empty-table-info-ongrid').removeClass('d-none');
                } else {
                    $('div.table-dscan-ship-classes-ongrid').removeClass('d-none');

                    elements.shipClassesOngridTable.DataTable({
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
                            // D-Scan total count
                            const currentTotal = elements.dscanCountOngrid.html();
                            const newTotal = parseInt(currentTotal) + data.count;

                            elements.dscanCountOngrid.html(newTotal);

                            const currentMass = elements.dscanMassOnGrid.data('mass') || 0;
                            const newMass = parseInt(currentMass) + data.mass;

                            elements.dscanMassOnGrid.data('mass', newMass);
                            elements.dscanMassOnGrid.html(_numberFormatter(newMass));

                            $(row)
                                .addClass(`aa-intel-shipclass-ongrid-item aa-intel-shipclass-id-${data.id} aa-intel-shiptype-id-${data.type_id}`)
                                .attr('data-shipclass-id', data.id)
                                .attr('data-shiptype-id', data.type_id);
                        },
                        initComplete: () => {
                            const classTableRow = $('.aa-intel-shipclass-ongrid-item');

                            _toggleDscanStickyHighlight({
                                element: classTableRow,
                                type: 'shipclass'
                            });

                            // Initialize Bootstrap tooltips
                            bootstrapTooltip({selector: '.aa-intel-dscan-ship-classes-ongrid-list'});
                        }
                    });
                }
            }
        })
        .catch((error) => {
            console.error('Error fetching ongrid ship classes data:', error);
        });

    /**
     * Datatable D-Scan Off Grid
     */
    fetchGet({url: settings.url.getShipClassesOffgrid})
        .then((tableData) => {
            if (tableData) {
                $('div.aa-intel-loading-table-info-offgrid').addClass('d-none');

                if (Object.keys(tableData).length === 0) {
                    $('div.aa-intel-empty-table-info-offgrid').removeClass('d-none');
                } else {
                    $('div.table-dscan-ship-classes-offgrid').removeClass('d-none');

                    elements.shipClassesOffgridTable.DataTable({
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
                            // D-Scan total count
                            const currentTotal = elements.dscanCountOffgrid.html();
                            const newTotal = parseInt(currentTotal) + data.count;

                            elements.dscanCountOffgrid.html(newTotal);

                            const currentMass = elements.dscanMassOffGrid.data('mass') || 0;
                            const newMass = parseInt(currentMass) + data.mass;

                            elements.dscanMassOffGrid.data('mass', newMass);
                            elements.dscanMassOffGrid.html(_numberFormatter(newMass));

                            $(row)
                                .addClass(`aa-intel-shipclass-offgrid-item aa-intel-shipclass-id-${data.id} aa-intel-shiptype-id-${data.type_id}`)
                                .attr('data-shipclass-id', data.id)
                                .attr('data-shiptype-id', data.type_id);
                        },
                        initComplete: () => {
                            const classTableRow = $('.aa-intel-shipclass-offgrid-item');

                            _toggleDscanStickyHighlight({
                                element: classTableRow,
                                type: 'shipclass'
                            });

                            // Initialize Bootstrap tooltips
                            bootstrapTooltip({selector: '.aa-intel-dscan-ship-classes-offgrid-list'});
                        }
                    });
                }
            }
        })
        .catch((error) => {
            console.error('Error fetching offgrid ship classes data:', error);
        });

    /**
     * Datatable D-Scan Ship Types
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

                            _toggleDscanStickyHighlight({
                                element: classTableRow,
                                type: 'shiptype'
                            });
                        }
                    });
                }
            }
        })
        .catch((error) => {
            console.error('Error fetching ship types data:', error);
        });

    /**
     * Datatable D-Scan Upwell Structures on Grid
     */
    fetchGet({url: settings.url.getStructuresOnGrid})
        .then((tableData) => {
            if (tableData) {
                $('div.aa-intel-loading-table-info-upwell-structures').addClass('d-none');

                if (Object.keys(tableData).length === 0) {
                    $('div.aa-intel-empty-table-info-upwell-structures').removeClass('d-none');
                } else {
                    $('div#aa-intel-dscan-row-interesting-on-grid').removeClass('d-none');
                    $('div.col-aa-intel-upwell-structures').removeClass('d-none');

                    elements.upwellStructuresTable.DataTable({
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
                            // Upwell Structures total count
                            const currentTotal = elements.dscanCountUpwellStructures.html();
                            const newTotal = parseInt(currentTotal) + data.count;

                            elements.dscanCountUpwellStructures.html(newTotal);

                            $(row)
                                .addClass(`aa-intel-structuretype-item aa-intel-structuretype-id-${data.id}`)
                                .attr('data-structuretype-id', data.id);
                        },
                        initComplete: () => {
                            const classTableRow = $('.aa-intel-structuretype-item');

                            _toggleDscanStickyHighlight({
                                element: classTableRow,
                                highlightOnly: true
                            });

                            // Initialize Bootstrap tooltips
                            bootstrapTooltip({selector: '.aa-intel-dscan-upwell-structures-list'});
                        }
                    });
                }
            }
        })
        .catch((error) => {
            console.error('Error fetching upwell structures data:', error);
        });

    /**
     * Datatable D-Scan Deployables on Grid
     */
    fetchGet({url: settings.url.getDeployablesOnGrid})
        .then((tableData) => {
            if (tableData) {
                $('div.aa-intel-loading-table-info-deployables').addClass('d-none');

                if (Object.keys(tableData).length === 0) {
                    $('div.aa-intel-empty-table-info-deployables').removeClass('d-none');
                } else {
                    $('div#aa-intel-dscan-row-interesting-on-grid').removeClass('d-none');
                    $('div.col-aa-intel-deployables').removeClass('d-none');

                    elements.deployablesTable.DataTable({
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
                            // Upwell Structures total count
                            const currentTotal = elements.dscanCountDeployables.html();
                            const newTotal = parseInt(currentTotal) + data.count;

                            elements.dscanCountDeployables.html(newTotal);

                            $(row)
                                .addClass(`aa-intel-deployabletype-item aa-intel-deployabletype-id-${data.id}`)
                                .attr('data-deployabletype-id', data.id);
                        },
                        initComplete: () => {
                            const classTableRow = $('.aa-intel-deployabletype-item');

                            _toggleDscanStickyHighlight({
                                element: classTableRow,
                                highlightOnly: true
                            });

                            // Initialize Bootstrap tooltips
                            bootstrapTooltip({selector: '.aa-intel-dscan-deployables-list'});
                        }
                    });
                }
            }
        })
        .catch((error) => {
            console.error('Error fetching deployables data:', error);
        });

    /**
     * Datatable D-Scan POS/POS Modules on Grid
     */
    fetchGet({url: settings.url.getStarbasesOnGrid})
        .then((tableData) => {
            if (tableData) {
                $('div.aa-intel-loading-table-info-starbases').addClass('d-none');

                if (Object.keys(tableData).length === 0) {
                    $('div.aa-intel-empty-table-info-starbases').removeClass('d-none');
                } else {
                    $('div#aa-intel-dscan-row-interesting-on-grid').removeClass('d-none');
                    $('div.col-aa-intel-starbases').removeClass('d-none');

                    elements.starbasesTable.DataTable({
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
                            // Upwell Structures total count
                            const currentTotal = elements.dscanCountStarbases.html();
                            const newTotal = parseInt(currentTotal) + data.count;

                            elements.dscanCountStarbases.html(newTotal);

                            $(row)
                                .addClass(`aa-intel-starbasetype-item aa-intel-starbasetype-id-${data.id}`)
                                .attr('data-starbasetype-id', data.id);
                        },
                        initComplete: () => {
                            const classTableRow = $('.aa-intel-starbasetype-item');

                            _toggleDscanStickyHighlight({
                                element: classTableRow,
                                highlightOnly: true
                            });

                            // Initialize Bootstrap tooltips
                            bootstrapTooltip({selector: '.aa-intel-dscan-starbases-list'});
                        }
                    });
                }
            }
        })
        .catch((error) => {
            console.error('Error fetching starbases data:', error);
        });
});
