/* global aaIntelToolJsSettings, addDscanHighlight, bootstrapTooltip, removeDscanHighlight, changeDscanStickyHighlight, fetchAjaxData, shipInfoPanel */

$(() => {
    'use strict';

    const elementShipClassesAllTable = $('table.aa-intel-dscan-ship-classes-all-list');
    const elementDscanCountAll = $('span#aa-intel-dscan-all-count');
    const elementDscanMassAll = $('span#aa-intel-dscan-all-mass');
    const elementShipClassesOngridTable = $('table.aa-intel-dscan-ship-classes-ongrid-list');
    const elementDscanCountOngrid = $('span#aa-intel-dscan-ongrid-count');
    const elementDscanMassOnGrid = $('span#aa-intel-dscan-ongrid-mass');
    const elementShipClassesOffgridTable = $('table.aa-intel-dscan-ship-classes-offgrid-list');
    const elementDscanCountOffgrid = $('span#aa-intel-dscan-offgrid-count');
    const elementDscanMassOffGrid = $('span#aa-intel-dscan-offgrid-mass');
    const elementShipTypesTable = $('table.aa-intel-dscan-ship-types-list');
    const elementUpwellStructuresTable = $('table.aa-intel-dscan-upwell-structures-list');
    const elementDscanCountUpwellStructures = $('span#aa-intel-dscan-upwell-structures-count');
    const elementDeployablesTable = $('table.aa-intel-dscan-deployables-list');
    const elementDscanCountDeployables = $('span#aa-intel-dscan-deployables-count');
    const elementStarbasesTable = $('table.aa-intel-dscan-starbases-list');
    const elementDscanCountStarbases = $('span#aa-intel-dscan-starbases-count');


    /**
     * Datatable D-Scan All
     */
    fetchAjaxData(aaIntelToolJsSettings.url.getShipClassesAll).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-all').addClass('d-none');

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-all').removeClass('d-none');
            } else {
                $('div.table-dscan-ship-classes-all').removeClass('d-none');

                elementShipClassesAllTable.DataTable({
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
                        const currentTotal = elementDscanCountAll.html();
                        const newTotal = parseInt(currentTotal) + data.count;

                        elementDscanCountAll.html(newTotal);

                        const currentMass = elementDscanMassAll.data('mass') || 0;
                        const newMass = parseInt(currentMass) + data.mass;

                        elementDscanMassAll.data('mass', newMass);
                        elementDscanMassAll.html(
                            new Intl.NumberFormat(
                                aaIntelToolJsSettings.language.django
                            ).format(newMass)
                        );

                        $(row)
                            .addClass(`aa-intel-shipclass-all-item aa-intel-shipclass-id-${data.id} aa-intel-shiptype-id-${data.type_id}`)
                            .attr('data-shipclass-id', data.id)
                            .attr('data-shiptype-id', data.type_id);
                    }
                });
            }
        }
    }).then(() => {
        const classTableRow = $('.aa-intel-shipclass-all-item');

        // Highlight
        classTableRow.mouseenter((event) => {
            addDscanHighlight('shipclass', $(event.currentTarget));
        }).mouseleave((event) => {
            removeDscanHighlight('shipclass', $(event.currentTarget));
        });

        // Sticky
        classTableRow.click((event) => {
            if ($(event.target).hasClass('aa-intel-information-link')) {
                event.stopPropagation();
            } else {
                changeDscanStickyHighlight('shipclass', $(event.currentTarget));
            }
        });

        // Initialize Bootstrap tooltips
        bootstrapTooltip('.aa-intel-dscan-ship-classes-all-list');
    });


    /**
     * Datatable D-Scan On Grid
     */
    fetchAjaxData(aaIntelToolJsSettings.url.getShipClassesOngrid).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-ongrid').addClass('d-none');

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-ongrid').removeClass('d-none');
            } else {
                $('div.table-dscan-ship-classes-ongrid').removeClass('d-none');

                elementShipClassesOngridTable.DataTable({
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
                        const currentTotal = elementDscanCountOngrid.html();
                        const newTotal = parseInt(currentTotal) + data.count;

                        elementDscanCountOngrid.html(newTotal);

                        const currentMass = elementDscanMassOnGrid.data('mass') || 0;
                        const newMass = parseInt(currentMass) + data.mass;

                        elementDscanMassOnGrid.data('mass', newMass);
                        elementDscanMassOnGrid.html(
                            new Intl.NumberFormat(
                                aaIntelToolJsSettings.language.django
                            ).format(newMass)
                        );

                        $(row)
                            .addClass(`aa-intel-shipclass-ongrid-item aa-intel-shipclass-id-${data.id} aa-intel-shiptype-id-${data.type_id}`)
                            .attr('data-shipclass-id', data.id)
                            .attr('data-shiptype-id', data.type_id);
                    }
                });
            }
        }
    }).then(() => {
        const classTableRow = $('.aa-intel-shipclass-ongrid-item');

        // Highlight
        classTableRow.mouseenter((event) => {
            addDscanHighlight('shipclass', $(event.currentTarget));
        }).mouseleave((event) => {
            removeDscanHighlight('shipclass', $(event.currentTarget));
        });

        // Sticky
        classTableRow.click((event) => {
            if ($(event.target).hasClass('aa-intel-information-link')) {
                event.stopPropagation();
            } else {
                changeDscanStickyHighlight('shipclass', $(event.currentTarget));
            }
        });

        // Initialize Bootstrap tooltips
        bootstrapTooltip('.aa-intel-dscan-ship-classes-ongrid-list');
    });


    /**
     * Datatable D-Scan Off Grid
     */
    fetchAjaxData(aaIntelToolJsSettings.url.getShipClassesOffgrid).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-offgrid').addClass('d-none');

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-offgrid').removeClass('d-none');
            } else {
                $('div.table-dscan-ship-classes-offgrid').removeClass('d-none');

                elementShipClassesOffgridTable.DataTable({
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
                        const currentTotal = elementDscanCountOffgrid.html();
                        const newTotal = parseInt(currentTotal) + data.count;

                        elementDscanCountOffgrid.html(newTotal);

                        const currentMass = elementDscanMassOffGrid.data('mass') || 0;
                        const newMass = parseInt(currentMass) + data.mass;

                        elementDscanMassOffGrid.data('mass', newMass);
                        elementDscanMassOffGrid.html(
                            new Intl.NumberFormat(
                                aaIntelToolJsSettings.language.django
                            ).format(newMass)
                        );

                        $(row)
                            .addClass(`aa-intel-shipclass-offgrid-item aa-intel-shipclass-id-${data.id} aa-intel-shiptype-id-${data.type_id}`)
                            .attr('data-shipclass-id', data.id)
                            .attr('data-shiptype-id', data.type_id);
                    }
                });
            }
        }
    }).then(() => {
        const classTableRow = $('.aa-intel-shipclass-offgrid-item');

        // Highlight
        classTableRow.mouseenter((event) => {
            addDscanHighlight('shipclass', $(event.currentTarget));
        }).mouseleave((event) => {
            removeDscanHighlight('shipclass', $(event.currentTarget));
        });

        // Sticky
        classTableRow.click((event) => {
            if ($(event.target).hasClass('aa-intel-information-link')) {
                event.stopPropagation();
            } else {
                changeDscanStickyHighlight('shipclass', $(event.currentTarget));
            }
        });

        // Initialize Bootstrap tooltips
        bootstrapTooltip('.aa-intel-dscan-ship-classes-offgrid-list');
    });


    /**
     * Datatable D-Scan Ship Types
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
                    language: aaIntelToolJsSettings.language.dataTables,
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
                    }
                });
            }
        }
    }).then(() => {
        const classTableRow = $('.aa-intel-shiptype-item');

        // Highlight
        classTableRow.mouseenter((event) => {
            addDscanHighlight('shiptype', $(event.currentTarget));
        }).mouseleave((event) => {
            removeDscanHighlight('shiptype', $(event.currentTarget));
        });

        // Sticky
        classTableRow.click((event) => {
            if ($(event.target).hasClass('aa-intel-information-link')) {
                event.stopPropagation();
            } else {
                changeDscanStickyHighlight('shiptype', $(event.currentTarget));
            }
        });
    });


    /**
     * Datatable D-Scan Upwell Structures on Grid
     */
    fetchAjaxData(aaIntelToolJsSettings.url.getStructuresOnGrid).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-upwell-structures').addClass('d-none');

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-upwell-structures').removeClass('d-none');
            } else {
                $('div#aa-intel-dscan-row-interesting-on-grid').removeClass('d-none');
                $('div.col-aa-intel-upwell-structures').removeClass('d-none');

                elementUpwellStructuresTable.DataTable({
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
                        const currentTotal = elementDscanCountUpwellStructures.html();
                        const newTotal = parseInt(currentTotal) + data.count;

                        elementDscanCountUpwellStructures.html(newTotal);

                        $(row)
                            .addClass(`aa-intel-structuretype-item aa-intel-structuretype-id-${data.id}`)
                            .attr('data-structuretype-id', data.id);
                    }
                });
            }
        }
    }).then(() => {
        const classTableRow = $('.aa-intel-structuretype-item');

        // Highlight
        classTableRow.mouseenter((event) => {
            $(event.currentTarget).addClass('aa-intel-highlight');
        }).mouseleave((event) => {
            $(event.currentTarget).removeClass('aa-intel-highlight');
        });

        // Initialize Bootstrap tooltips
        bootstrapTooltip('.aa-intel-dscan-upwell-structures-list');
    });


    /**
     * Datatable D-Scan Deployables on Grid
     */
    fetchAjaxData(aaIntelToolJsSettings.url.getDeployablesOnGrid).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-deployables').addClass('d-none');

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-deployables').removeClass('d-none');
            } else {
                $('div#aa-intel-dscan-row-interesting-on-grid').removeClass('d-none');
                $('div.col-aa-intel-deployables').removeClass('d-none');

                elementDeployablesTable.DataTable({
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
                        const currentTotal = elementDscanCountDeployables.html();
                        const newTotal = parseInt(currentTotal) + data.count;

                        elementDscanCountDeployables.html(newTotal);

                        $(row)
                            .addClass(`aa-intel-deployabletype-item aa-intel-deployabletype-id-${data.id}`)
                            .attr('data-deployabletype-id', data.id);
                    }
                });
            }
        }
    }).then(() => {
        const classTableRow = $('.aa-intel-deployabletype-item');

        // Highlight
        classTableRow.mouseenter((event) => {
            $(event.currentTarget).addClass('aa-intel-highlight');
        }).mouseleave((event) => {
            $(event.currentTarget).removeClass('aa-intel-highlight');
        });

        // Initialize Bootstrap tooltips
        bootstrapTooltip('.aa-intel-dscan-deployables-list');
    });


    /**
     * Datatable D-Scan POS/POS Modules on Grid
     */
    fetchAjaxData(aaIntelToolJsSettings.url.getStarbasesOnGrid).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-starbases').addClass('d-none');

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-starbases').removeClass('d-none');
            } else {
                $('div#aa-intel-dscan-row-interesting-on-grid').removeClass('d-none');
                $('div.col-aa-intel-starbases').removeClass('d-none');

                elementStarbasesTable.DataTable({
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
                        const currentTotal = elementDscanCountStarbases.html();
                        const newTotal = parseInt(currentTotal) + data.count;

                        elementDscanCountStarbases.html(newTotal);

                        $(row)
                            .addClass(`aa-intel-starbasetype-item aa-intel-starbasetype-id-${data.id}`)
                            .attr('data-starbasetype-id', data.id);
                    }
                });
            }
        }
    }).then(() => {
        const classTableRow = $('.aa-intel-starbasetype-item');

        // Highlight
        classTableRow.mouseenter((event) => {
            $(event.currentTarget).addClass('aa-intel-highlight');
        }).mouseleave((event) => {
            $(event.currentTarget).removeClass('aa-intel-highlight');
        });

        // Initialize Bootstrap tooltips
        bootstrapTooltip('.aa-intel-dscan-starbases-list');
    });
});
