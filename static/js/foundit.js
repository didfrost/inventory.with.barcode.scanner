function scanTable() {
	var totalSum = 0;
	var totalItem = 0;
	var result = [];
	
	$('div.chosensku').each(function(i,el) {
		totalItem++;
		totalSum += parseFloat($(el).attr('qty'));
	});
	
	result.push(totalSum);
	result.push(totalItem);
	
	$("#total").hide();
	
	if (totalItem >= 2){
		$("#total").show();
		$("#totalNumbers").text(" ...  "+totalItem.toString()+"/"+totalSum.toString());
	}else{
		$("#total").hide();
	}
    return result; 
}

$(document).ready(function(){
	scanTable();
				
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

	// Вибираємо рядок, перемальовуємо шапку
	// Choose the row, repaint all above
	$(document.body).on('click','.divTableCell',function(){	
		if ($(this).hasClass('divChoosable')) {
			var thisClass = $(this).parent("div");
			var idRow = thisClass.attr('idRow');
			var qty = thisClass.attr('qty');
			var sk = thisClass.attr('sk');
			var name = thisClass.attr('itemName');
			var kod1c = thisClass.attr('kod1c');
			document.getElementById("nameGoods").setAttribute("value",name);
			$('#nameGoodsText').text(name);
			
			document.getElementById("idKod").setAttribute("value",kod1c);
			$('#idKodText').text(kod1c);
			
			document.getElementById("idSk").setAttribute("value",sk);
			$('#idSkText').text(sk);
			
			document.getElementById("idRow").setAttribute("value",idRow);
			$('#idRowText').text(idRow);
			
			$('#qtyText').text(qty);
			
			var page =  $(document.getElementById('justappened'));
			console.log(page);
			page.removeClass("chosensku");
			
			if (thisClass.hasClass("chosensku") == false) {  
				// take class chosensku from everybody
				$('.divTableRow').each(function(i,el) {
					$(el).removeClass("chosensku");
				});
				// assign class chosensku for sk = current sk
				$('div[sk="'+sk+'"]').each(function(i,el) {
					$(el).addClass("chosensku");
				});
			}
			
			$('html,body').scrollTop(0);
			$('#change').prop("disabled", false); // Element(s) are now enabled.
			$('#add').prop("disabled", true); // Element(s) are now enabled.
			scanTable();
		}
	});
	$(".buttonCalc").click(function(){
		var touched = $(this).attr('value');
		
		if ($(this).attr('value') == ",") {
			if ($('#inputQty').val() == "") {
				var touched = "0.";
			} else if ($('#inputQty').val().includes(".")) {
				var touched = "";
			} else {
				var touched = ".";
			}
		}else if ($(this).attr('value') == "0") {
			if ($('#inputQty').val() == "") {
				var touched = "0.";
			}	
		}
		if ($(this).attr('value').includes("c")) {
			$('#inputQty').val('');
			$('#qtyText').text('');
		}else{
			var inputQtyNew = $("#inputQty").val() + touched;
			$('#inputQty').val(inputQtyNew);
			$('#qtyText').text(inputQtyNew);
		}	
	});
	$("#change").click(function(){
		var idKod = $("#idKod").attr("value");
		var idRow = $("#idRow").attr("value");
		var qty = $("#inputQty").val();
		if (qty == ''){
			var answer = confirm("Ввести нульові дані по даному елементу?")
			if (!answer) {
				return;
			}
		}else{
			var answer = confirm("Змінити дані по цьому елементу?")
			if (!answer) {
				return;
			}
		}	
		if (document.getElementById("idKod"+idRow) == null) {
			alert("Не зайдено товар із кодом рядка "+idRow)
			stop();
		}else{
			$("#qty"+idRow).text(qty);
		}

		$('#inputQty').val('');
		scanTable();
		
		$.ajax(
		{
			url: '/changeSku',
			contentType: "application/json",
			data: JSON.stringify(
				{'kod1c':$("#idKod").attr("value"),
				 'qty': qty, 
				 'sk': $("#idSk").attr("value"),
				 'idRow': idRow
				}
			),
			type: 'POST',
			success: function(response) {
				console.log(response);
			},
			error: function(error) {
				console.log(error);
			}
		});
	});
	$("#add").click(function(){
		var idKod = $("#idKod").attr("value");
		var curDep = $("#curDep").attr("value");;
		var qty = $("#inputQty").val();
		if (qty == ''){
			alert("Ви збираєтесь внести нульові дані по поточному елементу");
			return;
		}	
		var sk = $("#idSk").attr("value");
		var name = $("#nameGoods").attr("value");
		var d = new Date()
		var timeCreate = d.getHours()+":"+d.getMinutes().toString()+":"+d.getSeconds().toString();

		$('#inputQty').val('');
		$.ajax(
		{
			url: '/addSku',
			contentType: "application/json",
			data: JSON.stringify(
				{'kod1c':$("#idKod").attr("value"),
						'qty': qty, 
						'sk': $("#idSk").attr("value")
				}
			),
			type: 'POST',
			success: function(response) {
				idRow = response;

				$('#billtable').prepend('<div id = "justappened" class="divTableRow chosensku" \
				idRow="'+idRow+'" kod1C="'+idKod+'" sk="'+sk+'" itemName="'+name+'" qty = "'+qty+'">\
				<div class="divTableCell">'+0+'</div>\
				<div id="idKod'+idRow+'" class="divTableCell">'+idKod+'</div>\
				<div class="divTableCell">'+sk+'</div>\
				<div class="divTableCell divChoosable">'+name+'</div>\
				<div id="qty'+idRow+'" class="divTableCell divChoosable">'+qty+'</div>\
				<div class="divTableCell">'+timeCreate+'</div>\
				<div class="divTableCell">'+curDep+'</div>\
				<div class="divTableCell">'+idRow+'</div>\
				</div>');

				$('#idRowText').text(idRow);
				document.getElementById("idRow").setAttribute("value",idRow);
				console.log(response);
			},
			error: function(error) {
				console.log(error);
			}
		});
		$('#change').prop("disabled", false); // Element(s) are now enabled.
		$('#add').prop("disabled", true); // Element(s) are now enabled.
		scanTable();
	});
	$("#upload").click(function(){
		$.ajax(
		{
			url: '/upload',
			contentType: "application/json",
			data: JSON.stringify(
				{'idDep':$("#curDep").attr("value")
				}
			),
			type: 'POST',
			success: function(response) {
				$("#myflash").text("Вивантаження пройшло вдало");
				alert(respose);
				console.log(response);
			},
			error: function(error) {
				$("#myflash").text("Якісь проблеми під час вивантаження");
				alert(error);
				console.log(error);
			}
		});
	});

	$("#btnskmanuallysearch").click(function(){
		window.location = "/foundit?sku="+$("#sk_manually").val();
	});
});
