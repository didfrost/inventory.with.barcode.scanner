$(document).ready(function(){
	$("#addNewItem").click(function(){
		$.ajax(
		{
			url: '/addNewItem',
			contentType: "application/json",
			data: JSON.stringify(
				{'sk': $("#sk").attr("value"),
				'idDep': $("#idDep").attr("value"),
				 'itemName':$("#itemName").val()
				}
			),
			type: 'POST',
			success: function(response) {
				$("#info").text("Товар успішно внесний в базу даних. Продовжуйте сканування");
				console.log(response);
			},
			error: function(error) {
				$("#info").text("Не вдалось записати товар в базу даних");
				console.log(error);
			}
		});
	});
});