$(function() {
	console.log( "pagination.js ready!!!" );
    if (document.querySelectorAll('[class^=gig_pagination]').length == 0)
    {
        var pageParts = $(".col-md-3");
        // How many parts do we have?
        var numPages = pageParts.length;
        // How many parts do we want per page?
        var perPage = 12;
        pageParts.slice(perPage).hide();
        
        // Apply simplePagination to our placeholder
        $("#page-nav").pagination({
            items: numPages,
            itemsOnPage: perPage,
            cssStyle: "light-theme",
            // We implement the actual pagination
            //   in this next function. It runs on
            //   the event that a user changes page
            onPageClick: function(pageNum) {
                // Which page parts do we show?
                var start = perPage * (pageNum - 1);
                var end = start + perPage;

                // First hide all page parts
                // Then show those just for our page
                pageParts.hide().slice(start, end).show();
            }
        });
    } 
});