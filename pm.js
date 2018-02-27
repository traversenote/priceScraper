var priceFile = 'prices.json?'+ new Date().getTime();
var pricesFiltered = [];
String.prototype.stripSlashes = function(){
    return this.replace(/\\(.)/mg, "$1");
}
function setIgnore(id){
	action = 1;
	if ($(document).data('viewName') == 'ignored'){
		action = 0;
	};
		$('.loading').html('Working');
		$('.loading').addClass('show');
    $.post("writeIgnore.php?cache", { id: id, action: action}, function(data, status){
	    $('.loading').html('&nbsp;');
		$('.loading').removeClass('show');
/*		if(status != 'success'){*/
			//console.log(" javascript: "+data+" ");
/*		};*/
		showPage($(document).data('viewName'), $(document).data('sortCol'), 1);
	    
	    });
}
function sortByKey(array, key, direction) {

	if(direction == 1){
		d = 1;
	}else{
		d = -1;
	}
		/* Sort Decending */
	    return array.sort(
	    	function(a, b) {
	    		if (key == 'ourPrice'){
			    	var x = a.ourPrice;
				    var y = b.ourPrice;
				}
				else if(key == 'theirPrice'){
					var x = a.theirPrice;
				    var y = b.theirPrice;
				}
				else if(key == 'product'){
					var x = a.product;
				    var y = b.product;
				}
		        if(x>y){
		        	return -1 * d;
		        }
		        else if(x<y){
		        	return 1 * d;
		        }
		        else{
		        	return 0 * d;
		        }
		});
};	
function buildList(record){
	
	current = {"product" : record.product, 
	"theirPrice" : parseInt(record.theirPrice), 
	"ourPrice" : parseInt(record.ourPrice), 
	"ignoreStatus" : record.ignoreStatus, 
	"productID" : record.productID, 
	"link" : record.link,
	"dateScraped" : record.dateScraped };
	if(typeof record.dateIgnored != 'undefined'){
			current.dateIgnored = record.dateIgnored;
		}
	pricesFiltered.push(current);
	return pricesFiltered;
}
function printPrices(target, col, direction){
	
	$.getJSON(priceFile, function(json){
		pricesFiltered = [];
		switch(target){
			case 'decrease':
				for(i = 0; i < json.length; i++){
					if (parseInt(json[i].theirPrice) < parseInt(json[i].ourPrice) && json[i].ignoreStatus != 1){
						buildList(json[i]);
					}					
				}
				break;
			case 'increase':
				for(i = 0; i < json.length; i++){
					if (parseInt(json[i].theirPrice) > parseInt(json[i].ourPrice) && json[i].ignoreStatus != 1){
							buildList(json[i]);
					}
				}
				break;
			case 'ignored':
				for(i = 0; i < json.length; i++){
					if (json[i].ignoreStatus == 1){
							buildList(json[i]);
					}
				}
				break;
			default:
				console.log("Something is wrong, I wasn't given a condition for display");
				break;
		};
		pricesFiltered = sortByKey(pricesFiltered, col, direction);
		$('#tableContent').html("");
		if($(document).data('viewName') == 'ignored'){
			buttonText = 'Unignore';
		}else{
			buttonText = 'Ignore';
		}
		for(i = 0; i < pricesFiltered.length; i++){
			$('#tableContent').append(
				"<div class='row prodRows'><div class='col-md-1'><input class='btn' type='button' value='"+buttonText+"' onclick='setIgnore("+pricesFiltered[i].productID+")'></div>"+
				"<a href='"+pricesFiltered[i].link+"' target='_blank'>\n"+
				"<div class='col-md-5 prodName'>"+pricesFiltered[i].product.stripSlashes()+"<br>Date Scraped: "+pricesFiltered[i].dateScraped+"</div>\n"+
				"<div class='col-md-3' id='fd"+pricesFiltered[i].productID+"'></div>"+
				"<div class='col-md-1 theirPrice'>$"+pricesFiltered[i].theirPrice+"</div>\n"+
				"<div class='col-md-1 ourPrice'>$"+pricesFiltered[i].ourPrice+"</div>\n"+
				"</a><br>\n</div></a>");
			
			if(typeof pricesFiltered[i].dateIgnored != 'undefined' && pricesFiltered[i].ignoreStatus == 1){
				filtercell = '#fd'+pricesFiltered[i].productID;
				$(filtercell).html("Date Ignored: "+pricesFiltered[i].dateIgnored);
			};
		};
	});
}
function showPage(page, col, reverse){
	if(reverse != 1){
		if($(document).data('sortOrder') == 1){
			$(document).data('sortOrder', 0);
		}else{
			$(document).data('sortOrder', 1);
		};
	};
	$(document).data('viewName', page);
	direction = $(document).data('sortOrder');
	$(document).data('sortCol', col);
	$('#nameBox').html('Product Name');	
	$('#priceBox2').html('Our Price');
	switch(page){
		case 'pricesUp':
			$('#tableTitle').html('');
			$('#priceBox1').html('Next Best Price');
			$('#linkUp').addClass('active');
			$('#linkDown').removeClass('active');
			$('#linkIgnored').removeClass('active');
			$(document).data('viewName', 'pricesUp');
			printPrices('increase', col, direction);
			break;
		case 'pricesDn':
			$('#tableTitle').html('');
			$('#priceBox1').html('Best Price');
			$('#linkUp').removeClass('active');
			$('#linkDown').addClass('active');
			$('#linkIgnored').removeClass('active');
			$(document).data('viewName', 'pricesDn');
			printPrices('decrease', col, direction);
			break;
		case 'ignored':
			$('#tableTitle').html('');
			$('#priceBox1').html('Best Price');
			$('#linkUp').removeClass('active');
			$('#linkDown').removeClass('active');
			$('#linkIgnored').addClass('active');
			$(document).data('viewName', 'ignored');
			$(document).data('sortCol', '');
			printPrices('ignored', col, direction);
			break;
	};
};
$(document).ready(function(){
	showPage('pricesDn');
});