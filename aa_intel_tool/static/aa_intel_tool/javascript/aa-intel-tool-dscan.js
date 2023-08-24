/* global aaIntelToolJsL10n, aaIntelToolJsOptions, addHightlight, removeHightlight, changeStickyHighlight */

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

    /**
     * Corporation info element in datatable
     *
     * @param shipData
     * @returns {string}
     */
    const ShipInfoPanel = (shipData) => {
        let html_logo = '' +
            '<span class="aa-intel-ship-image-wrapper">\n' +
            '    <img ' +
            '        class="eve-image" ' +
            '        data-eveid="' + shipData['id'] + '" ' +
            '        src="' + shipData['image'] + '" ' +
            '        alt="' + shipData['name'] + '" ' +
            '        title="' + shipData['name'] + '" ' +
            '        width="32" ' +
            '        height="32">\n' +
            '</span>';

        let html_info = '' +
            '<span class="aa-intel-ship-information-wrapper">\n' +
            '    <span class="aa-intel-ship-name-wrapper">\n' +
            '        ' + shipData['name'] + '\n' +
            '    </span>\n' +
            '</span>\n';

        return html_logo + html_info;
    };

    /**
     * Datatable D-Scan All
     */
    fetch(aaIntelToolJsOptions.ajax.getShipClassesAll)
        .then(response => {
            if (response.ok) {
                return Promise.resolve(response);
            } else {
                return Promise.reject(new Error('Failed to load'));
            }
        })
        .then(response => response.json())
        .then(tableData => {
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
                                return ShipInfoPanel(data);
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
                        const newTotal = parseInt(currentTotal) + data['count'];

                        elementDscanCountAll.html(newTotal);

                        $(row)
                            .attr('data-shipclass-id', data['id'])
                            .attr('data-shiptype-id', data['type_id']);

                        // Highlight
                        $(row).mouseenter(() => {
                            addHightlight('shipclass', $(row));
                        }).mouseleave(() => {
                            removeHightlight('shipclass', $(row));
                        });

                        // Sticky
                        $(row).click(() => {
                            changeStickyHighlight('shipclass', $(row));
                        }).click('.aa-intel-information-link', (e) => {
                            e.stopPropagation();
                        });
                    }
                });
            }
        })
        .catch(function (error) {
            console.log(`Error: ${error.message}`);
        });


    /**
     * Datatable D-Scan On Grid
     */
    fetch(aaIntelToolJsOptions.ajax.getShipClassesOngrid)
        .then(response => {
            if (response.ok) {
                return Promise.resolve(response);
            } else {
                return Promise.reject(new Error('Failed to load'));
            }
        })
        .then(response => response.json())
        .then(tableData => {
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
                                return ShipInfoPanel(data);
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
                        const newTotal = parseInt(currentTotal) + data['count'];

                        elementDscanCountOngrid.html(newTotal);

                        $(row)
                            .attr('data-shipclass-id', data['id'])
                            .attr('data-shiptype-id', data['type_id']);

                        // Highlight
                        $(row).mouseenter(() => {
                            addHightlight('shipclass', $(row));
                        }).mouseleave(() => {
                            removeHightlight('shipclass', $(row));
                        });

                        // Sticky
                        $(row).click(() => {
                            changeStickyHighlight('shipclass', $(row));
                        }).click('.aa-intel-information-link', (e) => {
                            e.stopPropagation();
                        });
                    }
                });
            }
        })
        .catch(function (error) {
            console.log(`Error: ${error.message}`);
        });


    /**
     * Datatable D-Scan Off Grid
     */
    fetch(aaIntelToolJsOptions.ajax.getShipClassesOffgrid)
        .then(response => {
            if (response.ok) {
                return Promise.resolve(response);
            } else {
                return Promise.reject(new Error('Failed to load'));
            }
        })
        .then(response => response.json())
        .then(tableData => {
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
                                return ShipInfoPanel(data);
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
                        const newTotal = parseInt(currentTotal) + data['count'];

                        elementDscanCountOffgrid.html(newTotal);

                        $(row)
                            .attr('data-shipclass-id', data['id'])
                            .attr('data-shiptype-id', data['type_id']);

                        // Highlight
                        $(row).mouseenter(() => {
                            addHightlight('shipclass', $(row));
                        }).mouseleave(() => {
                            removeHightlight('shipclass', $(row));
                        });

                        // Sticky
                        $(row).click(() => {
                            changeStickyHighlight('shipclass', $(row));
                        }).click('.aa-intel-information-link', (e) => {
                            e.stopPropagation();
                        });
                    }
                });
            }
        })
        .catch(function (error) {
            console.log(`Error: ${error.message}`);
        });


    /**
     * Datatable D-Scan Ship Types
     */
    fetch(aaIntelToolJsOptions.ajax.getShipTypes)
        .then(response => {
            if (response.ok) {
                return Promise.resolve(response);
            } else {
                return Promise.reject(new Error('Failed to load'));
            }
        })
        .then(response => response.json())
        .then(tableData => {
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
                        $(row).attr('data-shiptype-id', data['id']);

                        // Highlight
                        $(row).mouseenter(() => {
                            addHightlight('shiptype', $(row));
                        }).mouseleave(() => {
                            removeHightlight('shiptype', $(row));
                        });

                        // Sticky
                        $(row).click(() => {
                            changeStickyHighlight('shiptype', $(row));
                        }).click('.aa-intel-information-link', (e) => {
                            e.stopPropagation();
                        });
                    }
                });
            }
        })
        .catch(function (error) {
            console.log(`Error: ${error.message}`);
        });


    /**
     * Datatable D-Scan Upwell Structures on Grid
     */
    fetch(aaIntelToolJsOptions.ajax.getStructuresOnGrid)
        .then(response => {
            if (response.ok) {
                return Promise.resolve(response);
            } else {
                return Promise.reject(new Error('Failed to load'));
            }
        })
        .then(response => response.json())
        .then(tableData => {
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
                                return ShipInfoPanel(data);
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
                        const newTotal = parseInt(currentTotal) + data['count'];

                        elementDscanCountUpwellStructures.html(newTotal);

                        $(row).attr('data-shiptype-id', data['id']);

                        // Highlight
                        $(row).mouseenter(() => {
                            $(row).addClass('aa-intel-highlight');
                        }).mouseleave(() => {
                            $(row).removeClass('aa-intel-highlight');
                        });
                    }
                });
            }
        })
        .catch(function (error) {
            console.log(`Error: ${error.message}`);
        });
});
