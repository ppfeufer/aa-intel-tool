/* global _getAaIntelToolJsSettings, numberFormatter, bootstrapTooltip, fetchGet, shipInfoPanel, _toggleDscanStickyHighlight, DataTable, _removeSearchFromColumnControl */

$(document).ready(() => {
    'use strict';

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

    const columnsDefs = [
        {
            target: 0,
            createdCell: (td) => $(td).addClass('text-ellipsis fix-eve-image-position')
        },
        {
            target: 1,
            width: 35,
            createdCell: (td) => $(td).addClass('text-end'),
            columnControl: _removeSearchFromColumnControl(settings.dataTables.columnControl, 1)
        }
    ];

    /**
     * Create a DataTable for d-scan data.
     *
     * @param {key, loadingKey, tableEl, url, containerSelector, rowItemClass, extraRowClass, idAttr, typeIdAttr, countEl, massEl, columns, tooltipSelector, highlightType, highlightOnly} opts Options for creating the DataTable.
     */
    const createDataTable = (opts) => {
        fetchGet({url: opts.url})
            .then((tableData) => {
                if (!tableData) {
                    return;
                }

                // hide loading, show empty or table container
                $(`div.aa-intel-loading-table-info-${opts.loadingKey || opts.key}`).addClass('d-none');

                if (Object.keys(tableData).length === 0) {
                    $(`div.aa-intel-empty-table-info-${opts.loadingKey || opts.key}`).removeClass('d-none');

                    return;
                }

                // unhide main container(s)
                if (opts.containerSelector) {
                    $(opts.containerSelector).removeClass('d-none');
                }

                if (opts.extraSelectors) {
                    opts.extraSelectors.forEach(s => $(s).removeClass('d-none'));
                }

                // initialize DataTable
                const dt = new DataTable(opts.tableEl, { // eslint-disable-line no-unused-vars
                    data: tableData,
                    paging: false,
                    language: settings.language.dataTables,
                    lengthChange: false,
                    dom: settings.dataTables.dom,
                    ordering: settings.dataTables.ordering,
                    columnControl: settings.dataTables.columnControl,
                    columns: opts.columns,
                    order: [[1, 'desc']],
                    columnDefs: columnsDefs,
                    createdRow: (row, data) => {
                        // update counts if provided
                        if (opts.countEl) {
                            const currentTotal = parseInt(opts.countEl.html()) || 0;

                            opts.countEl.html(currentTotal + (data.count || 0));
                        }

                        // update mass if provided
                        if (opts.massEl) {
                            const currentMass = parseInt(opts.massEl.data('mass')) || 0;
                            const newMass = currentMass + (data.mass || 0);

                            opts.massEl.data('mass', newMass);
                            opts.massEl.html(numberFormatter({
                                value: newMass,
                                locales: settings.language.django
                            }));
                        }

                        // row classes and attributes
                        if (opts.rowItemClass) {
                            $(row).addClass(opts.rowItemClass);
                        }

                        if (opts.idAttr) {
                            $(row).attr(opts.idAttr, data.id);
                        }

                        if (opts.typeIdAttr && data.type_id !== undefined) {
                            $(row).attr(opts.typeIdAttr, data.type_id);
                        }

                        if (opts.extraRowClass) {
                            $(row).addClass(opts.extraRowClass);
                        }
                    },
                    initComplete: () => {
                        if (opts.rowItemClass) {
                            const selector = `.${opts.rowItemClass.split(' ').join('.')}`;
                            const el = $(selector);

                            _toggleDscanStickyHighlight({
                                element: el,
                                type: opts.highlightType || 'shipclass',
                                highlightOnly: !!opts.highlightOnly
                            });
                        }

                        if (opts.tooltipSelector) {
                            bootstrapTooltip({selector: opts.tooltipSelector});
                        }
                    }
                });
            })
            .catch((error) => {
                console.error(`Error fetching ${opts.key} data:`, error);
            });
    };

    // Ship Classes - All
    createDataTable({
        key: 'all',
        loadingKey: 'all',
        tableEl: elements.shipClassesAllTable,
        url: settings.url.getShipClassesAll,
        containerSelector: 'div.table-dscan-ship-classes-all',
        rowItemClass: 'aa-intel-shipclass-all-item',
        extraRowClass: null,
        idAttr: 'data-shipclass-id',
        typeIdAttr: 'data-shiptype-id',
        countEl: elements.dscanCountAll,
        massEl: elements.dscanMassAll,
        columns: [
            {data: (d) => shipInfoPanel(d)},
            {data: 'count'}
        ],
        tooltipSelector: '.aa-intel-dscan-ship-classes-all-list'
    });

    // Ship Classes - On Grid
    createDataTable({
        key: 'ongrid',
        loadingKey: 'ongrid',
        tableEl: elements.shipClassesOngridTable,
        url: settings.url.getShipClassesOngrid,
        containerSelector: 'div.table-dscan-ship-classes-ongrid',
        rowItemClass: 'aa-intel-shipclass-ongrid-item',
        idAttr: 'data-shipclass-id',
        typeIdAttr: 'data-shiptype-id',
        countEl: elements.dscanCountOngrid,
        massEl: elements.dscanMassOnGrid,
        columns: [
            {data: (d) => shipInfoPanel(d)},
            {data: 'count'}
        ],
        tooltipSelector: '.aa-intel-dscan-ship-classes-ongrid-list'
    });

    // Ship Classes - Off Grid
    createDataTable({
        key: 'offgrid',
        loadingKey: 'offgrid',
        tableEl: elements.shipClassesOffgridTable,
        url: settings.url.getShipClassesOffgrid,
        containerSelector: 'div.table-dscan-ship-classes-offgrid',
        rowItemClass: 'aa-intel-shipclass-offgrid-item',
        idAttr: 'data-shipclass-id',
        typeIdAttr: 'data-shiptype-id',
        countEl: elements.dscanCountOffgrid,
        massEl: elements.dscanMassOffGrid,
        columns: [
            {data: (d) => shipInfoPanel(d)},
            {data: 'count'}
        ],
        tooltipSelector: '.aa-intel-dscan-ship-classes-offgrid-list'
    });

    // Ship Types
    createDataTable({
        key: 'ship-types',
        loadingKey: 'ship-types',
        tableEl: elements.shipTypesTable,
        url: settings.url.getShipTypes,
        containerSelector: 'div.table-dscan-ship-types',
        rowItemClass: 'aa-intel-shiptype-item',
        idAttr: 'data-shiptype-id',
        columns: [
            {data: 'name'},
            {data: 'count'}
        ],
        highlightType: 'shiptype'
    });

    // Upwell Structures (on grid)
    createDataTable({
        key: 'upwell-structures',
        loadingKey: 'upwell-structures',
        tableEl: elements.upwellStructuresTable,
        url: settings.url.getStructuresOnGrid,
        containerSelector: 'div#aa-intel-dscan-row-interesting-on-grid',
        extraSelectors: ['div.col-aa-intel-upwell-structures'],
        rowItemClass: 'aa-intel-structuretype-item',
        idAttr: 'data-structuretype-id',
        countEl: elements.dscanCountUpwellStructures,
        columns: [
            {data: (d) => shipInfoPanel(d)},
            {data: 'count'}
        ],
        highlightOnly: true,
        tooltipSelector: '.aa-intel-dscan-upwell-structures-list'
    });

    // Deployables (on grid)
    createDataTable({
        key: 'deployables',
        loadingKey: 'deployables',
        tableEl: elements.deployablesTable,
        url: settings.url.getDeployablesOnGrid,
        containerSelector: 'div#aa-intel-dscan-row-interesting-on-grid',
        extraSelectors: ['div.col-aa-intel-deployables'],
        rowItemClass: 'aa-intel-deployabletype-item',
        idAttr: 'data-deployabletype-id',
        countEl: elements.dscanCountDeployables,
        columns: [
            {data: (d) => shipInfoPanel(d)},
            {data: 'count'}
        ],
        highlightOnly: true,
        tooltipSelector: '.aa-intel-dscan-deployables-list'
    });

    // Starbases (on grid)
    createDataTable({
        key: 'starbases',
        loadingKey: 'starbases',
        tableEl: elements.starbasesTable,
        url: settings.url.getStarbasesOnGrid,
        containerSelector: 'div#aa-intel-dscan-row-interesting-on-grid',
        extraSelectors: ['div.col-aa-intel-starbases'],
        rowItemClass: 'aa-intel-starbasetype-item',
        idAttr: 'data-starbasetype-id',
        countEl: elements.dscanCountStarbases,
        columns: [
            {data: (d) => shipInfoPanel(d)},
            {data: 'count'}
        ],
        highlightOnly: true,
        tooltipSelector: '.aa-intel-dscan-starbases-list'
    });
});
