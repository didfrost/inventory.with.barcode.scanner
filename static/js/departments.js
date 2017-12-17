$(document).ready(function(){
	$(".departmentRow").click(function(){
		var valDep = $(this).attr("value");
		var answer = confirm("Ви справді хочете взяти відділ "+$(this).text());
		if (answer) {
			$.ajax({
				url: '/changeDep',
				contentType: "application/json",
				data: JSON.stringify(
				{'newDepId': valDep}),
				type: 'POST',
				success: function(response) {
					$('.departmentRow').each(function(i, obj) {
						var k = $(".depId"+i).attr('value');
						if (valDep == k){
							$(".depId"+i).css("background-color","red")
						}else{
							$(".depId"+i).css("background-color","lightcyan")
						}
					});					
					console.log(response);
				},
				error: function(error) {
					console.log(error);
				}
			});
		}
	});
}); 