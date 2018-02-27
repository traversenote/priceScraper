<!-- Version 1 -->

<!DOCTYPE html>
 <html lang='en'>
<head>
<meta http-equiv='content-type' content='text/html; charset=utf-8'>
 <!-- Latest compiled and minified CSS -->
 <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
 <!-- Optional theme -->
 <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
 <script
			  src="https://code.jquery.com/jquery-3.2.1.js"
			  integrity="sha256-DZAnKJ/6XZ9si04Hgrsxu/8s717jcIzLy3oi35EouyE="
			  crossorigin="anonymous"></script>
<script language="javascript" src="pm.js"></script>
 <link rel='stylesheet' href='scraper.css' />

 <title>Price Comparator</title>
 </head>

<body>
<div class='container'>
<div class='panel panel-default'>
	<nav class="navbar navbar-default">
		<div class="container-fluid">
			<div class="navbar-header">
	      		<a class="navbar-brand" href="#">Price Spy Scraper</a>
	    	</div>
	    		<ul class="nav navbar-nav">
	      		<li class='navLink' id='linkDown'><a onclick="showPage('pricesDn')" href="javascript:void(0);">Prices to Match</a></li>
	      		<li class='navLink' id='linkUp'><a onclick="showPage('pricesUp')" href="javascript:void(0);">Prices to Increase</a></li>
	      		<li class='navLink' id='linkIgnored'><a onclick="showPage('ignored')" href="javascript:void(0);">Ignored Products</a></li>
	    	</ul>
	  	</div>
	</nav>
	<div class='container-fluid loading'>&nbsp;</div>
	<div id='mainContent'>

		<div class='row' id='titleRow'>
			<div class='col-md-12' id='tableTitle'></div>
		</div>
		<div class='row' id='headerRow'>
		<div class='col-md-2' id='markBox'></div>
		<a class='viewLink' onclick="showPage($(document).data('viewName'), 'product')" href="javascript:void(0);"><div class='col-md-4' id='nameBox'></div></a>
		<div class='col-md-3' id='dateBox'></div>
		<a class='viewLink' onclick="showPage($(document).data('viewName'), 'theirPrice')" href="javascript:void(0);"><div class='col-md-1' id='priceBox1'></div></a>
		<a class='viewLink' onclick="showPage($(document).data('viewName'), 'ourPrice')" href="javascript:void(0);"><div class='col-md-1' id='priceBox2'></div></a>
		</div>
		<div id='tableContent'>
			
		</div>
	</div>
</div>
</div>
</body>
</html>