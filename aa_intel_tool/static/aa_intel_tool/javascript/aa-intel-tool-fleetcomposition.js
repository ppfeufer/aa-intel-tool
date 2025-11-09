/* global fetchGet, _getAaIntelToolJsSettings, numberFormatter, bootstrapTooltip, shipInfoPanel, pilotInfoPanel, _toggleFleetcompStickyHighlight, _removeSearchFromColumnControl */

$(document).ready(() => {
    'use strict';

    const settings = _getAaIntelToolJsSettings();
    const elements = {
        shipClassesTable: $('table.aa-intel-dscan-ship-classes-ship-classes-list'),
        shipClassesMass: $('span#aa-intel-dscan-ship-classes-mass'),
        shipTypesTable: $('table.aa-intel-dscan-ship-types-list'),
        fleetcompositionTable: $('table.aa-intel-fleetcomp-pilot-ships-list'),
        pilotsCount: $('span#aa-intel-fleet-participation-count')
    };
    const defaultOrder = [[1, 'desc']];
    const defaultColumnDefs = [
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
     * Create a data table.
     *
     * @param {jQuery | HTMLElement} tableElement The table element.
     * @param {string} url The URL to fetch data from.
     * @param {string} loadingClass The class of the loading div.
     * @param {string} emptyClass The class of the empty div.
     * @param containerClass
     * @param {Array} order The order for the data table.
     * @param {Array} columns The columns for the data table.
     * @param {Array} columnDefs The column definitions for the data table.
     * @param {CallableFunction} createdRowCallback The created row callback.
     * @param {CallableFunction} initCompleteCallback The init complete callback.
     */
    const createDataTable = ({
        tableElement,
        url,
        loadingClass,
        emptyClass,
        containerClass,
        order,
        columns,
        columnDefs,
        createdRowCallback,
        initCompleteCallback
    }) => {
        fetchGet({url})
            .then((tableData) => {
                $(`div.${loadingClass}`).addClass('d-none');

                if (!tableData || Object.keys(tableData).length === 0) {
                    $(`div.${emptyClass}`).removeClass('d-none');

                    return;
                }

                $(`div.${containerClass}`).removeClass('d-none');

                tableElement.DataTable({
                    data: tableData,
                    paging: false,
                    language: settings.language.dataTables,
                    lengthChange: false,
                    dom: settings.dataTables.dom,
                    ordering: settings.dataTables.ordering,
                    columnControl: settings.dataTables.columnControl,
                    columns: columns,
                    order: order || defaultOrder,
                    columnDefs: columnDefs || defaultColumnDefs,
                    createdRow: createdRowCallback,
                    initComplete: initCompleteCallback
                });
            })
            .catch((error) => console.error(`Error fetching data for ${containerClass}:`, error));
    };

    createDataTable({
        tableElement: elements.shipClassesTable,
        url: settings.url.getShipClasses,
        loadingClass: 'aa-intel-loading-table-info-ship-classes',
        emptyClass: 'aa-intel-empty-table-info-ship-classes',
        containerClass: 'table-dscan-ship-classes-ship-classes',
        columns: [
            {data: (data) => `${shipInfoPanel(data)}<span class="d-none">${data.type_name}</span>`},
            {data: 'count'}
        ],
        createdRowCallback: (row, data) => {
            const currentMass = elements.shipClassesMass.data('mass') || 0;
            const newMass = parseInt(currentMass) + data.mass;

            elements.shipClassesMass.data('mass', newMass);
            elements.shipClassesMass.html(numberFormatter({
                value: newMass,
                locales: settings.language.django
            }));

            $(row)
                .addClass(`aa-intel-shipclass-item aa-intel-shipclass-id-${data.id} aa-intel-shiptype-id-${data.type_id}`)
                .attr('data-shipclass-id', data.id)
                .attr('data-shiptype-id', data.type_id);
        },
        initCompleteCallback: () => {
            _toggleFleetcompStickyHighlight({
                element: $('.aa-intel-shipclass-item'),
                type: 'shipclass'
            });
            bootstrapTooltip({selector: '.aa-intel-dscan-ship-classes-ship-classes-list'});
        }
    });

    createDataTable({
        tableElement: elements.shipTypesTable,
        url: settings.url.getShipTypes,
        loadingClass: 'aa-intel-loading-table-info-ship-types',
        emptyClass: 'aa-intel-empty-table-info-ship-types',
        containerClass: 'table-dscan-ship-types',
        columns: [
            {data: 'name'},
            {data: 'count'}
        ],
        createdRowCallback: (row, data) => {
            $(row)
                .addClass(`aa-intel-shiptype-item aa-intel-shiptype-id-${data.id}`)
                .attr('data-shiptype-id', data.id);
        },
        initCompleteCallback: () => {
            _toggleFleetcompStickyHighlight({
                element: $('.aa-intel-shiptype-item'),
                type: 'shiptype'
            });
            bootstrapTooltip({selector: '.aa-intel-dscan-ship-types-list'});
        }
    });

    createDataTable({
        tableElement: elements.fleetcompositionTable,
        url: settings.url.getFleetComposition,
        loadingClass: 'aa-intel-loading-table-info-fleetcomp-pilot-ships',
        emptyClass: 'aa-intel-empty-table-info-fleetcomp-pilot-ships',
        containerClass: 'table-fleetcomp-pilot-ships',
        columns: [
            {data: (data) => pilotInfoPanel(data)},
            {data: 'ship'},
            {data: 'solarsystem'}
        ],
        order: [
            [0, 'asc']
        ],
        columnDefs: [
            {target: 0, createdCell: (td) => $(td).addClass('fix-eve-image-position')}
        ],
        createdRowCallback: (row, data) => {
            const currentTotal = elements.pilotsCount.html();
            const newTotal = parseInt(currentTotal) + 1;

            elements.pilotsCount.html(newTotal);

            $(row)
                .addClass(`aa-intel-pilotship-item aa-intel-shipclass-id-${data.ship_id} aa-intel-shiptype-id-${data.ship_type_id}`)
                .attr('data-shipclass-id', data.ship_id)
                .attr('data-shiptype-id', data.ship_type_id);
        },
        initCompleteCallback: () => {
            _toggleFleetcompStickyHighlight({
                element: $('.aa-intel-pilotship-item'),
                type: 'shiptype'
            });
            bootstrapTooltip({selector: '.aa-intel-fleetcomp-pilot-ships-list'});
        }
    });
});
