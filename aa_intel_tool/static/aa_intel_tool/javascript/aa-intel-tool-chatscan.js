/* global aaIntelToolJsOptions, aaIntelToolJsL10n, addHightlight, removeHightlight, changeStickyHighlight, fetchAjaxData */

jQuery(document).ready(($) => {
    'use strict';

    /* Elements
    --------------------------------------------------------------------------------- */
    const elementPilotsTable = $('table.aa-intel-pilot-participation-list');
    const elementCorporationsTable = $('table.aa-intel-corporation-participation-list');
    const elementAlliancesTable = $('table.aa-intel-alliance-participation-list');

    const elementPilotsTotalCount = $('span#aa-intel-pilots-count');
    const elementCorporationsTotalCount = $('span#aa-intel-corporations-count');
    const elementAlliancesTotalCount = $('span#aa-intel-alliances-count');


    /**
     * Pilot info element in datatable
     *
     * @param pilotData
     * @returns {string}
     */
    const pilotInfoPanel = (pilotData) => {
        let html_logo = '' +
            '<span class="aa-intel-pilot-avatar-wrapper">\n' +
            '    <img ' +
            '        class="eve-image" ' +
            '        data-eveid="' + pilotData['id'] + '" ' +
            '        src="' + pilotData['portrait'] + '" ' +
            '        alt="' + pilotData['name'] + '" ' +
            '        title="' + pilotData['name'] + '" ' +
            '        width="32" ' +
            '        height="32">\n' +
            '</span>';

        let html_info = '' +
            '<span class="aa-intel-pilot-information-wrapper">\n' +
            '    <span class="aa-intel-pilot-name-wrapper">\n' +
            '        ' + pilotData['name'] + '\n' +
            '    </span>\n';

        html_info += '' +
            '    <span class="aa-intel-pilot-links-wrapper">\n' +
            '        <small>\n' +
            '            <a ' +
            '                class="aa-intel-information-link" ' +
            '                href="' + pilotData['evewho'] + '" ' +
            '                target="_blank" ' +
            '                rel="noopener noreferer"' +
            '            >' +
            '               evewho <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
            '            </a> |\n' +

            '            <a ' +
            '                class="aa-intel-information-link" ' +
            '                href="' + pilotData['zkillboard'] + '" ' +
            '                target="_blank" rel="noopener noreferer"' +
            '            >' +
            '                zkillboard <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
            '            </a>\n' +
            '        </small>\n' +
            '    </span>\n';

        return html_logo + html_info;
    };


    /**
     * Corporation info element in datatable
     *
     * @param corporationData
     * @param logoOnly {boolean} Returns only the corporation logo
     * @returns {string}
     */
    const corporationInfoPanel = (corporationData, logoOnly = false) => {
        let html_logo = '' +
            '<span class="aa-intel-corporation-logo-wrapper">\n' +
            '    <img ' +
            '        class="eve-image" ' +
            '        data-eveid="' + corporationData['id'] + '" ' +
            '        src="' + corporationData['logo'] + '" ' +
            '        alt="' + corporationData['name'] + '" ' +
            '        title="' + corporationData['name'] + '" ' +
            '        width="32" ' +
            '        height="32">\n' +
            '</span>';

        let html_info = '' +
            '<span class="aa-intel-corporation-information-wrapper">\n' +
            '    <span class="aa-intel-corporation-name-wrapper">\n' +
            '        ' + corporationData['name'] + '\n' +
            '    </span>\n';

        html_info += '' +
            '    <span class="aa-intel-corporation-links-wrapper">\n' +
            '        <small>\n';

        if ((1000000 <= corporationData['id']) && corporationData['id'] <= 2000000) {
            html_info += '' +
                '            (' + aaIntelToolJsL10n.scanData.npcCorp + ')';
        } else {
            html_info += '' +
                '            <a ' +
                '                class="aa-intel-information-link" ' +
                '                href="' + corporationData['dotlan'] + '" ' +
                '                target="_blank" ' +
                '                rel="noopener noreferer"' +
                '            >' +
                '               dotlan <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
                '            </a> |\n' +

                '            <a ' +
                '                class="aa-intel-information-link" ' +
                '                href="' + corporationData['zkillboard'] + '" ' +
                '                target="_blank" rel="noopener noreferer"' +
                '            >' +
                '                zkillboard <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
                '            </a>\n' +
                '        </small>\n' +
                '    </span>\n';
        }

        html_info += '' +
            '</span>';

        if (logoOnly) {
            return html_logo;
        }

        return html_logo + html_info;
    };


    /**
     * Alliance info element in datatable
     *
     * @param allianceData
     * @param logoOnly {boolean} Returns only the alliance logo
     * @returns {string}
     */
    const allianceInfoPanel = (allianceData, logoOnly = false) => {
        if (allianceData['name'] === '') {
            allianceData['name'] = aaIntelToolJsL10n.scanData.empty;
        }

        let html_logo = '' +
            '<span class="aa-intel-alliance-logo-wrapper alliance-id-' + allianceData['id'] + '">\n' +
            '    <img ' +
            '        class="eve-image" ' +
            '        data-eveid="' + allianceData['id'] + '" ' +
            '        src="' + allianceData['logo'] + '" ' +
            '        alt="' + allianceData['name'] + '" ' +
            '        title="' + allianceData['name'] + '" ' +
            '        width="32" ' +
            '        height="32">\n' +
            '</span>';

        let html_info = '' +
            '<span class="aa-intel-alliance-information-wrapper">\n' +
            '    <span class="aa-intel-alliance-name-wrapper">\n' +
            '        ' + allianceData['name'] + '\n' +
            '    </span>\n';

        if (allianceData['id'] > 1) {
            html_info += '' +
                '    <span class="aa-intel-alliance-links-wrapper">\n' +
                '        <small>\n' +
                '            <a ' +
                '                class="aa-intel-information-link" ' +
                '                href="' + allianceData['dotlan'] + '" ' +
                '                target="_blank" ' +
                '                rel="noopener noreferer"' +
                '            >' +
                '               dotlan <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
                '            </a> |\n' +

                '            <a ' +
                '                class="aa-intel-information-link" ' +
                '                href="' + allianceData['zkillboard'] + '" ' +
                '                target="_blank" rel="noopener noreferer"' +
                '            >' +
                '                zkillboard <i class="fas fa-external-link-alt" aria-hidden="true"></i>' +
                '            </a>\n' +
                '        </small>\n' +
                '    </span>\n';
        }

        html_info += '' +
            '</span>';

        if (logoOnly) {
            if (allianceData.id === 1) {
                return '';
            }

            return html_logo;
        }

        return html_logo + html_info;
    };


    /**
     * Datatable Alliances Breakdown
     */
    fetchAjaxData(aaIntelToolJsOptions.ajax.getAllianceList).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-alliance-participation-list').hide();

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-alliance-participation-list').show();
            } else {
                $('div.table-local-scan-alliances').show();

                elementAlliancesTable.DataTable({
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
                                return allianceInfoPanel(data);
                            }
                        },
                        {
                            data: 'count'
                        },
                        {
                            data: 'ticker'
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
                                $(td).addClass('text-right');
                            }
                        },
                        {
                            targets: 2,
                            visible: false
                        }
                    ],
                    createdRow: (row, data) => {
                        // Alliance total count
                        const currentTotal = elementAlliancesTotalCount.html();
                        let newTotal;

                        if (data['id'] !== 1) {
                            newTotal = parseInt(currentTotal) + 1;
                        }

                        elementAlliancesTotalCount.html(newTotal);

                        $(row)
                            .addClass(`aa-intel-alliance-participation-item aa-intel-alliance-id-${data['id']}`)
                            .attr('data-alliance-id', data['id']);

                        // Highlight
                        $(row).mouseenter(() => {
                            addHightlight('alliance', $(row));
                        }).mouseleave(() => {
                            removeHightlight('alliance', $(row));
                        });

                        // Sticky
                        $(row).click(() => {
                            changeStickyHighlight('alliance', $(row));
                        }).click('.aa-intel-information-link', (e) => {
                            e.stopPropagation();
                        });
                    }
                })
            }
        }
    });


    /**
     * Datatable Corporations Breakdown
     */
    fetchAjaxData(aaIntelToolJsOptions.ajax.getCorporationList).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-corporation-participation-list').hide();

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-corporation-participation-list').show();
            } else {
                $('div.table-local-scan-corporations').show();

                elementCorporationsTable.DataTable({
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
                                return corporationInfoPanel(data);
                            }
                        },
                        {
                            data: 'count'
                        },
                        {
                            data: 'ticker'
                        },
                        {
                            data: 'alliance.name'
                        },
                        {
                            data: 'alliance.ticker'
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
                                $(td).addClass('text-right');
                            }
                        },
                        {
                            targets: [2, 3, 4],
                            visible: false
                        }
                    ],
                    createdRow: (row, data) => {
                        // Corporation total count
                        const currentTotal = elementCorporationsTotalCount.html();
                        const newTotal = parseInt(currentTotal) + 1;

                        elementCorporationsTotalCount.html(newTotal);

                        $(row)
                            .addClass(`aa-intel-corporation-participation-item aa-intel-corporation-id-${data['id']}`)
                            .attr('data-corporation-id', data['id'])
                            .attr('data-alliance-id', data['alliance']['id']);

                        // Highlight
                        $(row).mouseenter(() => {
                            addHightlight('corporation', $(row));
                        }).mouseleave(() => {
                            removeHightlight('corporation', $(row));
                        });

                        // Sticky
                        $(row).click(() => {
                            changeStickyHighlight('corporation', $(row));
                        }).click('.aa-intel-information-link', (e) => {
                            e.stopPropagation();
                        });
                    }
                })
            }
        }
    });


    /**
     * Datatable Pilots Breakdown
     */
    fetchAjaxData(aaIntelToolJsOptions.ajax.getPilotList).then(tableData => {
        if (tableData) {
            $('div.aa-intel-loading-table-info-pilot-participation-list').hide();

            if (Object.keys(tableData).length === 0) {
                $('div.aa-intel-empty-table-info-pilot-participation-list').show();
            } else {
                $('div.table-local-scan-pilots').show();

                elementPilotsTable.DataTable({
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
                                return pilotInfoPanel(data);
                            }
                        },
                        {
                            data: (data) => {
                                return allianceInfoPanel(data['alliance'], true) + data['alliance']['ticker'];
                            }
                        },
                        {
                            data: (data) => {
                                return corporationInfoPanel(data['corporation'], true) + data['corporation']['ticker'];
                            }
                        },
                        {
                            data: 'alliance.name'
                        },
                        {
                            data: 'corporation.name'
                        }
                    ],
                    order: [
                        [0, 'asc']
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
                            width: 125
                        },
                        {
                            targets: 2,
                            width: 125
                        },
                        {
                            targets: [3, 4],
                            visible: false
                        }
                    ],
                    createdRow: (row, data) => {
                        // Pilot total count
                        const currentTotal = elementPilotsTotalCount.html();
                        const newTotal = parseInt(currentTotal) + 1;

                        elementPilotsTotalCount.html(newTotal);

                        $(row)
                            .addClass(`aa-intel-corporation-participation-item aa-intel-corporation-id-${data['id']}`)
                            .attr('data-character-id', data['id'])
                            .attr('data-corporation-id', data['corporation']['id'])
                            .attr('data-alliance-id', data['alliance']['id']);

                        // Highlight
                        $(row).mouseenter(() => {
                            addHightlight('pilot', $(row));
                        }).mouseleave(() => {
                            removeHightlight('pilot', $(row));
                        });

                        // Sticky
                        $(row).click(() => {
                            changeStickyHighlight('pilot', $(row));
                        }).click('.aa-intel-information-link', (e) => {
                            e.stopPropagation();
                        });
                    }
                })
            }
        }
    });
});
