$(document).ready(function(){
	$(document.body).on('click','.divTableCellpm',function(){
		var btn = $(this).text();
		var id_qty = 0;
		if (btn == '+'){
			id_qty = $(this).attr('id').replace('bpid','bqid');
		}else{
			id_qty = $(this).attr('id').replace('bmid','bqid');
		}
		var qty = $('#'+id_qty).text();
		if (btn == '+'){
			var newqty = Number(qty) + 1;
		}else{
			var newqty = Number(qty) - 1;
		}
		$('#'+id_qty).html(newqty);
	});
	$(".menudishes").click(function(){
		var dish = $(this).text();
		var id_dish = $(this).attr('id').replace('menu','bgid');
		var id_plus = $(this).attr('id').replace('menu','bpid');
		var id_minus = $(this).attr('id').replace('menu','bmid');
		var id_qty = $(this).attr('id').replace('menu','bqid');
		if (document.getElementById(id_dish)) {
			var qty = $('#'+id_qty).text();
			var newqty = Number(qty) + 1;
			$('#'+id_qty).html(newqty);
		} else {
			var qty = 1;
			$('#billtable').prepend('<div class="divTableRow"><div id = "'+id_dish+'" class="divTableCell">'+dish+'</div>\
			<div id = "'+id_plus+'" class="divTableCellpm">+</div>\
			<div id = "'+id_minus+'" class="divTableCellpm">-</div>\
			<div id = "'+id_qty+'" class="divTableCell">'+qty+'</div><div class="divTableCell">&nbsp;</div><div class="divTableCell">&nbsp;</div></div>');
		}	
	});
});
