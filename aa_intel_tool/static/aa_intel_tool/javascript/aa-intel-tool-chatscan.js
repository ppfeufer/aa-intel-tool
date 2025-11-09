/* global _getAaIntelToolJsSettings, _toggleChatscanStickyHighlight, bootstrapTooltip, fetchGet, pilotInfoPanel, corporationInfoPanel, allianceInfoPanel, _removeSearchFromColumnControl, DataTable */

$(document).ready(() => {
    'use strict';

    const settings = _getAaIntelToolJsSettings();
    const elements = {
        pilotsTable: $('table.aa-intel-pilot-participation-list'),
        corporationsTable: $('table.aa-intel-corporation-participation-list'),
        alliancesTable: $('table.aa-intel-alliance-participation-list'),
        pilotsTotalCount: $('span#aa-intel-pilots-count'),
        corporationsTotalCount: $('span#aa-intel-corporations-count'),
        alliancesTotalCount: $('span#aa-intel-alliances-count')
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
     * Create the DataTable.
     *
     * @param table
     * @param url
     * @param loadingClass
     * @param emptyClass
     * @param containerClass
     * @param columns
     * @param rowClass
     * @param totalCountElement
     * @param rowAttributes
     * @param highlightType
     * @param tooltipSelector
     * @param columnDefs
     * @param order
     */
    const createDataTable = ({
        table,
        url,
        loadingClass,
        emptyClass,
        containerClass,
        columns,
        rowClass,
        totalCountElement,
        rowAttributes,
        highlightType,
        tooltipSelector,
        columnDefs,
        order
    }) => {
        fetchGet({url})
            .then((tableData) => {
                $(`div.${loadingClass}`).addClass('d-none');

                if (!tableData || Object.keys(tableData).length === 0) {
                    $(`div.${emptyClass}`).removeClass('d-none');

                    return;
                }

                $(`div.${containerClass}`).removeClass('d-none');

                const dt = new DataTable(table, { // eslint-disable-line no-unused-vars
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
                    createdRow: (row, data) => {
                        if (totalCountElement) {
                            const currentTotal = parseInt(totalCountElement.html()) || 0;

                            totalCountElement.html(currentTotal + 1);
                        }

                        $(row).addClass(rowClass);

                        if (rowAttributes) {
                            Object.entries(rowAttributes(data)).forEach(([key, value]) => {
                                $(row).attr(key, value);
                            });
                        }
                    },
                    initComplete: () => {
                        _toggleChatscanStickyHighlight({
                            element: $(`.${rowClass}`),
                            type: highlightType
                        });

                        if (tooltipSelector) {
                            bootstrapTooltip({selector: tooltipSelector});
                        }
                    }
                });
            })
            .catch((error) => console.error(`Error fetching data for ${rowClass}:`, error));
    };

    // Create the alliances DataTable.
    createDataTable({
        table: elements.alliancesTable,
        url: settings.url.getAllianceList,
        loadingClass: 'aa-intel-loading-table-info-alliance-participation-list',
        emptyClass: 'aa-intel-empty-table-info-alliance-participation-list',
        containerClass: 'table-local-scan-alliances',
        columns: [
            {data: (data) => `${allianceInfoPanel(data)}<span class="d-none">${(data.ticker || '')}</span>`},
            {data: 'count'}
        ],
        rowClass: 'aa-intel-alliance-participation-item',
        totalCountElement: elements.alliancesTotalCount,
        rowAttributes: (data) => ({'data-alliance-id': data.id}),
        highlightType: 'alliance',
        tooltipSelector: '.aa-intel-alliance-participation-list'
    });

    // Create the corporations DataTable.
    createDataTable({
        table: elements.corporationsTable,
        url: settings.url.getCorporationList,
        loadingClass: 'aa-intel-loading-table-info-corporation-participation-list',
        emptyClass: 'aa-intel-empty-table-info-corporation-participation-list',
        containerClass: 'table-local-scan-corporations',
        columns: [
            {data: (data) => `${corporationInfoPanel(data)}<span class="d-none">${(data.ticker || '')}, ${(data.alliance && data.alliance.name) || ''}, ${(data.alliance && data.alliance.ticker) || ''}</span>`},
            {data: 'count'}
        ],
        rowClass: 'aa-intel-corporation-participation-item',
        totalCountElement: elements.corporationsTotalCount,
        rowAttributes: (data) => ({
            'data-corporation-id': data.id,
            'data-alliance-id': (data.alliance && data.alliance.id) || ''
        }),
        highlightType: 'corporation',
        tooltipSelector: '.aa-intel-corporation-participation-list'
    });

    // Create the pilots DataTable.
    createDataTable({
        table: elements.pilotsTable,
        url: settings.url.getPilotList,
        loadingClass: 'aa-intel-loading-table-info-pilot-participation-list',
        emptyClass: 'aa-intel-empty-table-info-pilot-participation-list',
        containerClass: 'table-local-scan-pilots',
        columns: [
            {data: (data) => pilotInfoPanel(data)},
            {data: (data) => `${allianceInfoPanel((data.alliance || {}), true)}${((data.alliance && data.alliance.ticker) || '')}<span class="d-none">${((data.alliance && data.alliance.name) || '')}</span>`},
            {data: (data) => `${corporationInfoPanel((data.corporation || {}), true)}${((data.corporation && data.corporation.ticker) || '')}<span class="d-none">${((data.corporation && data.corporation.name) || '')}</span>`}
        ],
        // custom order
        order: [
            [0, 'asc']
        ],
        // custom columnDefs
        columnDefs: [
            {
                target: 0,
                createdCell: (td) => $(td).addClass('text-ellipsis fix-eve-image-position')
            },
            {
                target: 1,
                width: 35,
                createdCell: (td) => $(td).addClass('text-end')
            },
            {
                target: 2,
                width: 35,
                createdCell: (td) => $(td).addClass('text-end')
            }
        ],
        rowClass: 'aa-intel-pilot-participation-item',
        totalCountElement: elements.pilotsTotalCount,
        rowAttributes: (data) => ({
            'data-character-id': data.id,
            'data-corporation-id': (data.corporation && data.corporation.id) || '',
            'data-alliance-id': (data.alliance && data.alliance.id) || ''
        }),
        highlightType: 'pilot',
        tooltipSelector: '.aa-intel-pilot-participation-list'
    });
});
