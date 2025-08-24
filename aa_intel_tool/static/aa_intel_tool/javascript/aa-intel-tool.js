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
