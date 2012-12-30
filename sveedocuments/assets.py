from django_assets import Bundle, register

AVALAIBLE_BUNDLES = {
    'sveedocuments_frontend_css': Bundle(
        "sveedocuments/css/frontend.css",
        filters='yui_css',
        output='css/sveedocuments_frontend.min.css'
    ),
    'sveedocuments_board_css': Bundle(
        "sveedocuments/css/board.css",
        filters='yui_css',
        output='css/sveedocuments_board.min.css'
    ),
    'sveedocuments_board_js': Bundle(
        "js/jquery/jquery.slugify.js",
        "js/jquery/moment.js",
        "js/jquery/pikaday.js",
        filters='yui_js',
        output='js/sveedocuments_board.min.js'
    ),
}

ENABLED_BUNDLES = (
    'sveedocuments_frontend_css',
    'sveedocuments_board_css',
    'sveedocuments_board_js',
)

for item in ENABLED_BUNDLES:
    register(item, AVALAIBLE_BUNDLES[item])
