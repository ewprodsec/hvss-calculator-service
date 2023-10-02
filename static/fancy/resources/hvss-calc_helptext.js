// src="https://www.first.org/_/cvsscalc31_helptext.js"
// var CVSS31_Help = {};
var HVSS10_Help = {};

// This object is used as an associative array mapping the names of elements on the web page to help text that is
// added as title text. Browsers will display the text when the element is hovered over with the cursor.
HVSS10_Help.helpText_en = {

    // Extended Attack Complexity (XAC)
    // --------------------------------
    // Negligible (N)
    "EAC_N_Label": "Unplanned change of state on the product can be achieved through application interface (example: ability to permanently silence alarms)",
    // Low (L)
    "EAC_L_Label": "Unplanned change of state on the product can be achieved without a need to install own code(example: XSS attack or escaping application constraints and altering data through OS or changing OS configuration or caring out attack on unprotected data-in-transit)",
    // Medium (M)
    "EAC_M_Label": "Unplanned change of state on the product can be achieved through installing malicious code and subsequently altering data in persistent storage. (example: malicious updates, DLL injections, manual installations of the scripts, etc. or through altering data-in-transit on protected channel)",
    // High (H)
    "EAC_H_Label": "Unplanned change of state on the product can be achieved through installing malicious code and subsequently altering data in memory (example: same as in 3), but data-at-rest is protected and attacker can't get circumvent this protection, while data-in-use is available)",
    // Critical (C)
    "EAC_C_Label": "Unplanned change of state on the product can be achieved through breaking physical encasement open and installing malicious code through directly plugging into ports on the board (example: reflashing chip through JTAG connection)",
    // Extreme (E)
    "EAC_E_Label": "Unplanned change of state on the product can be achieved by introducing extraordinary efforts only (example: stealing code signing key from HSM of one of the major PKI providers)",

    // Impact Type: Patient Safety (EXT:XPS)
    // --------------------------------
    // Neglible (N)
    "XPS_N_Label": "No illness or injury to patient or user. Inconvenience to use. Labeling issues not impacting expiration date, product size. No effect on product performance, but product may be exchanged prior to use (e.g., cosmetic issues).",
    // Limited (L)
    "XPS_L_Label": "May cause transient, self-limiting illness or injury to patient or user (e.g., delay in procedure, removal and re-insertion of device, fever, bruise/hematoma or other condition typically not requiring medical intervention).",
    // Moderate (MD)
    "XPS_MD_Label": "May cause recoverable injury to patient or user (e.g., unintended treatment, percutaneous cut-down for device removal, condition requiring percutaneous or pharmaceutical intervention).",
    // Major (MJ)
    "XPS_MJ_Label": "May cause permanent or significant disability or severe illness in a patient or user that requires treatment but is not likely to result in death (e.g., myocardial infarction, stroke, peripheral vascular rupture, surgical intervention required).",
    // Critical (C)
    "XPS_C_Label": "Potential for death, failure of the device or procedure likely to lead to patient or user death. (e.g., perforation of aorta/cardiac chamber, endocarditis)."

}

// Merge HVSS v1.0 help text with CVSS v3.1 help text
Object.assign(HVSS10_Help.helpText_en, CVSS31_Help.helpText_en);
const helpText = JSON.stringify(HVSS10_Help.helpText_en, null, '\t');
// console.log(`---> DEBUG: HVSS v1.0 help text: ${helpText}`);
