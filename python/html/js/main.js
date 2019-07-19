 alert(1111)

 $(function(){
 	$.post("/", {"name" : "test", "age" : 100}, function(rsp){
 		console.log(rsp)
 	})
 });