from django_assets import Bundle, register

AVALAIBLE_BUNDLES = {
    'sveedocuments_frontend_css': Bundle(
        "css/sveedocuments/frontend.css",
        filters='yui_css',
        output='css/sveedocuments/frontend.min.css'
    ),
    'sveedocuments_board_css': Bundle(
        "css/sveedocuments/board.css",
        filters='yui_css',
        output='css/sveedocuments/board.min.css'
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
