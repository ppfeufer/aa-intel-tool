/* global aaIntelToolJsSettingsDefaults, aaIntelToolJsSettingsOverride, objectDeepMerge */

/* jshint -W097 */
'use strict';

// Build the settings object
let aaIntelToolJsSettings = typeof aaIntelToolJsSettingsDefaults !== 'undefined' ? aaIntelToolJsSettingsDefaults : null;

if (aaIntelToolJsSettings && typeof aaIntelToolJsSettingsOverride !== 'undefined') {
    aaIntelToolJsSettings = objectDeepMerge(
        aaIntelToolJsSettings,
        aaIntelToolJsSettingsOverride
    );
}
