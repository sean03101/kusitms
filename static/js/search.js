
(function ($) {


function search(target){ 
var word = target.value; 
var encodeWord = encodeURI(word); 
console.log(word); 
console.log(encodeWord); 



//start Ajax 
$.ajax({ type : 'GET', dataType : 'json', 
	url : "http://www.career.go.kr/cnet/openapi/getOpenApi?" 
	+"apiKey=본인의appKey(회원가입 후 승인받아야함)" 
	+"&svcType=api&svcCode=SCHOOL&contentType=json&gubun=elem_list" 
	+"&searchSchulNm="+word, 
	error : function(err) { 
		console.log("실행중 오류가 발생하였습니다."); }, 
	success : function(data) { 
		console.log("data확인 : "+data); 
		console.log("결과 갯수 : "+data.dataSearch.content.length); 
		console.log("첫번째 결과 : "+data.dataSearch.content[0]); 
		$("#schoolList").empty(); 
		var checkWord = $("#word").val(); //검색어 입력값 
		console.log(data.dataSearch.content.length); 
		if(checkWord.length > 0 && data.dataSearch.content.length > 0){ 
			for (i = 0; i < data.dataSearch.content.length; i++) { 
				$("#schoolList") 
				.append( 
				"<li class='schoolList' value='" 
				+ data.dataSearch.content[i].schoolName 
				+ "' data-input='" 
				+ data.dataSearch.content[i].schoolName 
				+ ">" 
				+ "<a href='javascript:void(0);'>" 
				+ data.dataSearch.content[i].schoolName 
				+ "</a>" 
				+ "</li>"); 
				} 
		} 
	} 
	});//end Ajax 
	}







})(jQuery);