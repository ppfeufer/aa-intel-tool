-- Deletes all AA Intel Tool tables from the database
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS aa_intel_tool_scandata;
DROP TABLE IF EXISTS aa_intel_tool_scan;
SET FOREIGN_KEY_CHECKS=1;
