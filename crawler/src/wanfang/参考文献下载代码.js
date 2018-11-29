
function jourDown(id,type,num,isfirst){
	var ll=null;

	if(isfirst==undefined){
		isfirst = null;
	}
	var winRef = window.open("", "_blank","");
	$.ajax({
		type:"post",
		data : {
			"_type":type,
			"id":id,
			"number":1,
			"first":isfirst
		},
		dataType:"json",
		url:"/asynRetrieval/docPaper.do",
		success:function(data){
			data = JSON.parse(data);
			if(num!="1"){
				if(type == "patent"){
					ll="/search/downLoad.do?language=&resourceType="+type+"&source="+data.source_db+"&resourceId="+data.patent_id+"&resourceTitle="+data.title+"";
				}else{
					if((data.first_publish!=null&&data.first_publish=="2"!=undefined)&&(data.first_publish=="2"||data.first_publish=="3")){
						ll="/search/downLoad.do?language="+data.language+"&resourceType="+type+"&source="+data.source_db+"&resourceId="+data.article_id+"&resourceTitle="+data.title+"&first="+data.first_publish;
					}else{
						ll="/search/downLoad.do?language="+data.language+"&resourceType="+type+"&source="+data.source_db+"&resourceId="+data.article_id+"&resourceTitle="+data.title+"";
					}
				}
			}else{
				if((data.first_publish!=null&&data.first_publish=="2"!=undefined)&&(data.first_publish=="2"||data.first_publish=="3")){
					ll="/search/onlineread.do?language="+data.language+"&resourceType="+type+"&source="+data.source_db+"&resourceId="+data.article_id+"&resourceTitle="+data.title+"&first="+data.first_publish;
				}else{
					ll="/search/onlineread.do?language="+data.language+"&resourceType="+type+"&source="+data.source_db+"&resourceId="+data.article_id+"&resourceTitle="+data.title+"";
				}
			}
			  function loc(){
			      winRef.location = ll;//改变页面的 location
			     }
			     setTimeout(loc(),800);//这个等待很重要，如果不等待的话将无法实现
		}
	});
}