"""
Asset bundles to use with django-assets
"""
try:
    from django_assets import Bundle, register
except ImportError:
    DJANGO_ASSETS_INSTALLED = False
else:
    DJANGO_ASSETS_INSTALLED = True

    AVALAIBLE_BUNDLES = {
        'sveedocuments_css': Bundle(
            "css/sveedocuments_app.css",
            filters='yui_css',
            output='css/sveedocuments_app.min.css'
        ),
        'sveedocuments_js': Bundle(
            "js/jquery/jquery.slugify.js",
            "js/jquery/moment.js",
            "js/jquery/pikaday.js",
            "js/jquery/tree.jquery.js",
            "js/sveedocuments_plugins.js",
            filters='yui_js',
            output='js/sveedocuments.min.js'
        ),
    }

    ENABLED_BUNDLES = (
        'sveedocuments_css',
        'sveedocuments_js',
    )

    for item in ENABLED_BUNDLES:
        register(item, AVALAIBLE_BUNDLES[item])
