/* global aaIntelToolJsSettingsDefaults, aaIntelToolJsSettingsOverride, objectDeepMerge */

/* jshint -W097 */
'use strict';

/**
 * Get the settings for aa-intel-tool JavaScript.
 *
 * @private
 */
const _getAaIntelToolJsSettings = () => { // eslint-disable-line no-unused-vars
    if (typeof aaIntelToolJsSettingsDefaults === 'undefined') {
        return null;
    }

    if (typeof aaIntelToolJsSettingsOverride !== 'undefined') {
        return objectDeepMerge(aaIntelToolJsSettingsDefaults, aaIntelToolJsSettingsOverride);
    }

    return aaIntelToolJsSettingsDefaults;
};

const _removeSearchFromColumnControl = (columnControl, index = 1) => { // eslint-disable-line no-unused-vars
    const cc = JSON.parse(JSON.stringify(columnControl));

    if (cc[index]) {
        cc[index].content = [];
    }

    return cc;
};
