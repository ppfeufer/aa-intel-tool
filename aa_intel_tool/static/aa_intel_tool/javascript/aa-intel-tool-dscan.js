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
     * Create the DataTable.
     *
     * @param key
     * @param loadingKey
     * @param tableEl
     * @param url
     * @param containerSelector
     * @param extraSelectors
     * @param rowItemClass
     * @param extraRowClass
     * @param idAttr
     * @param typeIdAttr
     * @param countEl
     * @param massEl
     * @param columns
     * @param tooltipSelector
     * @param highlightType
     * @param highlightOnly
     */
    const createDataTable = ({
        key,
        loadingKey,
        tableEl,
        url,
        containerSelector,
        extraSelectors,
        rowItemClass,
        extraRowClass,
        idAttr,
        typeIdAttr,
        countEl,
        massEl,
        columns,
        tooltipSelector,
        highlightType,
        highlightOnly
    }) => {
        fetchGet({url: url})
            .then((tableData) => {
                if (!tableData) {
                    return;
                }

                // hide loading, show empty or table container
                $(`div.aa-intel-loading-table-info-${loadingKey || key}`).addClass('d-none');

                if (Object.keys(tableData).length === 0) {
                    $(`div.aa-intel-empty-table-info-${loadingKey || key}`).removeClass('d-none');

                    return;
                }

                // unhide main container(s)
                if (containerSelector) {
                    $(containerSelector).removeClass('d-none');
                }

                if (extraSelectors) {
                    extraSelectors.forEach(s => $(s).removeClass('d-none'));
                }

                // initialize DataTable
                const dt = new DataTable(tableEl, { // eslint-disable-line no-unused-vars
                    data: tableData,
                    paging: false,
                    language: settings.language.dataTables,
                    lengthChange: false,
                    dom: settings.dataTables.dom,
                    ordering: settings.dataTables.ordering,
                    columnControl: settings.dataTables.columnControl,
                    columns: columns,
                    order: [[1, 'desc']],
                    columnDefs: columnsDefs,
                    createdRow: (row, data) => {
                        // update counts if provided
                        if (countEl) {
                            const currentTotal = parseInt(countEl.html()) || 0;

                            countEl.html(currentTotal + (data.count || 0));
                        }

                        // update mass if provided
                        if (massEl) {
                            const currentMass = parseInt(massEl.data('mass')) || 0;
                            const newMass = currentMass + (data.mass || 0);

                            massEl.data('mass', newMass);
                            massEl.html(numberFormatter({
                                value: newMass,
                                locales: settings.language.django
                            }));
                        }

                        // row classes and attributes
                        if (rowItemClass) {
                            $(row).addClass(rowItemClass);
                        }

                        if (idAttr) {
                            $(row).attr(idAttr, data.id);
                        }

                        if (typeIdAttr && data.type_id !== undefined) {
                            $(row).attr(typeIdAttr, data.type_id);
                        }

                        if (extraRowClass) {
                            $(row).addClass(extraRowClass);
                        }
                    },
                    initComplete: () => {
                        if (rowItemClass) {
                            const selector = `.${rowItemClass.split(' ').join('.')}`;
                            const el = $(selector);

                            _toggleDscanStickyHighlight({
                                element: el,
                                type: highlightType || 'shipclass',
                                highlightOnly: !!highlightOnly
                            });
                        }

                        if (tooltipSelector) {
                            bootstrapTooltip({selector: tooltipSelector});
                        }
                    }
                });
            })
            .catch((error) => {
                console.error(`Error fetching ${key} data:`, error);
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
