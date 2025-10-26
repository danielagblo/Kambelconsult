// Auto-fill icon class based on selected platform and show platform logo preview
(function($) {
    'use strict';
    
    // Icon classes for each platform
    const ICON_CLASSES = {
        'facebook': 'fab fa-facebook',
        'twitter': 'fab fa-twitter',
        'linkedin': 'fab fa-linkedin',
        'instagram': 'fab fa-instagram',
        'youtube': 'fab fa-youtube',
        'tiktok': 'fab fa-tiktok',
    };
    
    function updateIconClass() {
        const platformField = $('#id_platform');
        const iconClassField = $('#id_icon_class');
        const iconClassRow = iconClassField.closest('.form-row, .field-icon_class');
        
        if (platformField.length && iconClassField.length) {
            const selectedPlatform = platformField.val();
            
            if (selectedPlatform && ICON_CLASSES[selectedPlatform]) {
                // Auto-fill icon class
                iconClassField.val(ICON_CLASSES[selectedPlatform]);
                
                // Hide the icon_class field and show platform logo preview instead
                if (iconClassRow.length) {
                    iconClassRow.hide();
                    
                    // Remove existing preview if any
                    iconClassRow.siblings('.platform-logo-preview').remove();
                    
                    // Create and show platform logo preview
                    const previewHtml = `
                        <div class="form-row platform-logo-preview" style="margin-bottom: 15px;">
                            <div>
                                <label>Platform Logo:</label>
                                <div style="margin-top: 10px;">
                                    <i class="${ICON_CLASSES[selectedPlatform]} fa-3x" style="color: #2563eb;"></i>
                                    <span style="margin-left: 10px; font-weight: 600; text-transform: capitalize;">${selectedPlatform}</span>
                                </div>
                                <p class="help" style="margin-top: 10px; color: #666;">The logo is automatically set based on your platform selection.</p>
                            </div>
                        </div>
                    `;
                    iconClassRow.after(previewHtml);
                }
            } else {
                // Show icon_class field if no platform selected
                if (iconClassRow.length) {
                    iconClassRow.show();
                    iconClassRow.siblings('.platform-logo-preview').remove();
                }
            }
        }
    }
    
    // Run on page load
    $(document).ready(function() {
        updateIconClass();
        
        // Update when platform changes
        $('#id_platform').on('change', function() {
            updateIconClass();
        });
    });
})(django.jQuery);
