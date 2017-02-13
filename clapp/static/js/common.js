
$( document ).ready(function() {
    var size = document.querySelectorAll('[class^=green]').length;
    for ( var i = 1; i <= size; i++ ){
    	var counter = i;
    	var price_id = "price-"+counter.toString();
        var title_id = "title-"+counter.toString();
        var module = document.getElementById(title_id);
        $clamp(module, {clamp: 1});
    	var price = document.getElementById(price_id).innerHTML;
        if (price[1] == '-' || price[1] == 0)
        {
            document.getElementById(price_id).innerHTML = "FREE~!!!"
            document.getElementById(price_id).style.color = "green";
        }
        else
        {
            var number = price.replace( /^\D+/g, '');
            if (number < 20) {
                document.getElementById(price_id).style.color = "red";
            }            
        }
    	  	
	}
});