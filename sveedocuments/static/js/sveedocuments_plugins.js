(function( $ ) {

// Get all nodes ids
function get_all_node_ids(node, finded_ids){
    var ids = (finded_ids) ? finded_ids : [];
    for (var i=0; i < node.children.length; i++) {
        var child = node.children[i];
        ids.push(child.id);
        // Recursive finding
        ids = get_all_node_ids(child, ids);
    }
    return ids;
};

// Get all folder nodes ids
function get_all_folder_ids(node, finded_ids){
    var ids = (finded_ids) ? finded_ids : [];
    for (var i=0; i < node.children.length; i++) {
        var child = node.children[i];
        if(child.children.length>0){
            ids.push(child.id);
            // Recursive finding
            ids = get_all_folder_ids(child, ids);
        }
    }
    return ids;
};

/*
 * Display page tree with jqtree
 */
$.fn.jqtree_documents_index = function(options) {
    return this.each(function() {
        
        var settings = $.extend({
                'state_cookie_name': 'sveedocuments_tree_all',
                'icon_closed': '<i class="icon-folder-o"></i>',
                'icon_opened': '<i class="icon-folder-open-o"></i>',
                'link_add_child_title': 'New child page',
                'link_delete_title': 'Delete',
                'json_tree_data': [],
                'admin_mode': false
            }, options),
            $sitemap_tree = $(this).tree({
                data: settings.json_tree_data, // The JSON tree datas
                useContextMenu: false, // Dont intercept right click
                saveState: settings.state_cookie_name, // Save tree opening state in a cookie
                selectable: false, // Disable selection that is not usefull
                
                closedIcon: $(settings.icon_closed),
                openedIcon: $(settings.icon_opened),
                // Post item creation event
                onCreateLi: function(node, $li) {
                    // Append a link to view the page because the label from jqTree capture link click
                    var item, item_classes;
                    if(settings.admin_mode){
                        item_classes = (node.visible) ? '' : ' secondary';
                        item = '<a href="'+ node.edit_url +'" class="view button'+ item_classes +' split" data-node-id="'+ node.id +'">'+ node.name +' <span data-dropdown="drop-'+ node.id +'"></span></a>'+
                            '<ul id="drop-'+ node.id +'" class="f-dropdown" data-dropdown-content>'+
                            '<li><a href="'+ node.add_child_url +'">'+ settings.link_add_child_title +'</a></li>'+
                            '<li><a href="'+ node.delete_url +'">'+ settings.link_delete_title +'</a></li>'+
                            '</ul>';
                    } else {
                        item = '<a href="'+ node.view_url +'" class="view" data-node-id="'+ node.id +'">'+ node.name +'</a>';
                    }
                    $li.find('.jqtree-element').append(item);
                }
            });
        //$(document).foundation();
        $(document).foundation('dropdown', 'reflow');
        // Handle "open all" link to open all folder nodes
        $('.button-group .tree-open-link').click(function() {
            $.each(get_all_folder_ids($sitemap_tree.tree('getTree')), function( index, value ) {
                $sitemap_tree.tree('openNode', $sitemap_tree.tree('getNodeById', value, false));
            });
            return false;
        });
        // Handle "close all" link to close all folder nodes
        $('.button-group .tree-close-link').click(function() {
            $.each(get_all_folder_ids($sitemap_tree.tree('getTree')), function( index, value ) {
                $sitemap_tree.tree('closeNode', $sitemap_tree.tree('getNodeById', value, false));
            });
            return false;
        });
        
        
    });
};

}( jQuery ));