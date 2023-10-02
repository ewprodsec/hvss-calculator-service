document.addEventListener('DOMContentLoaded', () => {
    // Access version variables from version.js
    document.getElementById('mlModelBuildDate').textContent = ml_models_build_date;
    document.getElementById('mlModelBuildID').textContent = ml_models_build_id;
});
