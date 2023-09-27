/* global aaIntelToolJsL10n, aaIntelToolJsOptions, addDscanHightlight, removeDscanHightlight, changeDscanStickyHighlight, fetchAjaxData, shipInfoPanel */

jQuery(document).ready(($) => {
    'use strict';

    const elementShipClassesAllTable = $('table.aa-intel-dscan-ship-classes-all-list');
    const elementDscanCountAll = $('span#aa-intel-dscan-all-count');
    const elementShipClassesOngridTable = $('table.aa-intel-dscan-ship-classes-ongrid-list');
    const elementDscanCountOngrid = $('span#aa-intel-dscan-ongrid-count');
    const elementShipClassesOffgridTable = $('table.aa-intel-dscan-ship-classes-offgrid-list');
    const elementDscanCountOffgrid = $('span#aa-intel-dscan-offgrid-count');
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
    fetchAjaxData(aaIntelToolJsOptions.ajax.getShipClassesAll).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-all').hide();

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-all').show();
            } else {
                $('div.table-dscan-ship-classes-all').show();

                elementShipClassesAllTable.DataTable({
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
                        // D-Scan total count
                        const currentTotal = elementDscanCountAll.html();
                        const newTotal = parseInt(currentTotal) + data.count;

                        elementDscanCountAll.html(newTotal);

                        $(row)
                            .attr('data-shipclass-id', data.id)
                            .attr('data-shiptype-id', data.type_id);

                        // Highlight
                        $(row).mouseenter(() => {
                            addDscanHightlight('shipclass', $(row));
                        }).mouseleave(() => {
                            removeDscanHightlight('shipclass', $(row));
                        });

                        // Sticky
                        $(row).click((event) => {
                            const target = $(event.target);

                            if (target.hasClass('aa-intel-information-link')) {
                                event.stopPropagation();
                            } else {
                                changeDscanStickyHighlight('shipclass', $(row));
                            }
                        });
                    }
                });
            }
        }
    });


    /**
     * Datatable D-Scan On Grid
     */
    fetchAjaxData(aaIntelToolJsOptions.ajax.getShipClassesOngrid).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-ongrid').hide();

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-ongrid').show();
            } else {
                $('div.table-dscan-ship-classes-ongrid').show();

                elementShipClassesOngridTable.DataTable({
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
                        // D-Scan total count
                        const currentTotal = elementDscanCountOngrid.html();
                        const newTotal = parseInt(currentTotal) + data.count;

                        elementDscanCountOngrid.html(newTotal);

                        $(row)
                            .attr('data-shipclass-id', data.id)
                            .attr('data-shiptype-id', data.type_id);

                        // Highlight
                        $(row).mouseenter(() => {
                            addDscanHightlight('shipclass', $(row));
                        }).mouseleave(() => {
                            removeDscanHightlight('shipclass', $(row));
                        });

                        // Sticky
                        $(row).click((event) => {
                            const target = $(event.target);

                            if (target.hasClass('aa-intel-information-link')) {
                                event.stopPropagation();
                            } else {
                                changeDscanStickyHighlight('shipclass', $(row));
                            }
                        });
                    }
                });
            }
        }
    });


    /**
     * Datatable D-Scan Off Grid
     */
    fetchAjaxData(aaIntelToolJsOptions.ajax.getShipClassesOffgrid).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-offgrid').hide();

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-offgrid').show();
            } else {
                $('div.table-dscan-ship-classes-offgrid').show();

                elementShipClassesOffgridTable.DataTable({
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
                        // D-Scan total count
                        const currentTotal = elementDscanCountOffgrid.html();
                        const newTotal = parseInt(currentTotal) + data.count;

                        elementDscanCountOffgrid.html(newTotal);

                        $(row)
                            .attr('data-shipclass-id', data.id)
                            .attr('data-shiptype-id', data.type_id);

                        // Highlight
                        $(row).mouseenter(() => {
                            addDscanHightlight('shipclass', $(row));
                        }).mouseleave(() => {
                            removeDscanHightlight('shipclass', $(row));
                        });

                        // Sticky
                        $(row).click((event) => {
                            const target = $(event.target);

                            if (target.hasClass('aa-intel-information-link')) {
                                event.stopPropagation();
                            } else {
                                changeDscanStickyHighlight('shipclass', $(row));
                            }
                        });
                    }
                });
            }
        }
    });


    /**
     * Datatable D-Scan Ship Types
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
                            addDscanHightlight('shiptype', $(row));
                        }).mouseleave(() => {
                            removeDscanHightlight('shiptype', $(row));
                        });

                        // Sticky
                        $(row).click((event) => {
                            const target = $(event.target);

                            if (target.hasClass('aa-intel-information-link')) {
                                event.stopPropagation();
                            } else {
                                changeDscanStickyHighlight('shiptype', $(row));
                            }
                        });
                    }
                });
            }
        }
    });


    /**
     * Datatable D-Scan Upwell Structures on Grid
     */
    fetchAjaxData(aaIntelToolJsOptions.ajax.getStructuresOnGrid).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-upwell-structures').hide();
            $('div#aa-intel-dscan-row-interesting-on-grid').show();

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-upwell-structures').show();
            } else {
                $('div.col-aa-intel-upwell-structures').show();

                elementUpwellStructuresTable.DataTable({
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
                        // Upwell Structures total count
                        const currentTotal = elementDscanCountUpwellStructures.html();
                        const newTotal = parseInt(currentTotal) + data.count;

                        elementDscanCountUpwellStructures.html(newTotal);

                        $(row).attr('data-shiptype-id', data.id);

                        // Highlight
                        $(row).mouseenter(() => {
                            $(row).addClass('aa-intel-highlight');
                        }).mouseleave(() => {
                            $(row).removeClass('aa-intel-highlight');
                        });
                    }
                });
            }
        }
    });


    /**
     * Datatable D-Scan Deployables on Grid
     */
    fetchAjaxData(aaIntelToolJsOptions.ajax.getDeployablesOnGrid).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-deployables').hide();
            $('div#aa-intel-dscan-row-interesting-on-grid').show();

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-deployables').show();
            } else {
                $('div.col-aa-intel-deployables').show();

                elementDeployablesTable.DataTable({
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
                        // Upwell Structures total count
                        const currentTotal = elementDscanCountDeployables.html();
                        const newTotal = parseInt(currentTotal) + data.count;

                        elementDscanCountDeployables.html(newTotal);

                        $(row).attr('data-shiptype-id', data.id);

                        // Highlight
                        $(row).mouseenter(() => {
                            $(row).addClass('aa-intel-highlight');
                        }).mouseleave(() => {
                            $(row).removeClass('aa-intel-highlight');
                        });
                    }
                });
            }
        }
    });


    /**
     * Datatable D-Scan Deployables on Grid
     */
    fetchAjaxData(aaIntelToolJsOptions.ajax.getStarbasesOnGrid).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-starbases').hide();
            $('div#aa-intel-dscan-row-interesting-on-grid').show();

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-starbases').show();
            } else {
                $('div.col-aa-intel-starbases').show();

                elementStarbasesTable.DataTable({
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
                        // Upwell Structures total count
                        const currentTotal = elementDscanCountStarbases.html();
                        const newTotal = parseInt(currentTotal) + data.count;

                        elementDscanCountStarbases.html(newTotal);

                        $(row).attr('data-shiptype-id', data.id);

                        // Highlight
                        $(row).mouseenter(() => {
                            $(row).addClass('aa-intel-highlight');
                        }).mouseleave(() => {
                            $(row).removeClass('aa-intel-highlight');
                        });
                    }
                });
            }
        }
    });
});
