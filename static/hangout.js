


function hangoutCancel(btn) {
    var index = btn.nextElementSibling.value;

    $.ajax({
        url:"/hangout/cancel",
        type:"post",
        dataType:"json",
        data:{
            "index": parseInt(index)
    },

        success:function(data) {
            console.log(data);
            console.log(data==true);
            if(data != null) {
                if(data == true) {
                    swal("cancel 완료 ");
                    location.reload(true);
                    //window.location.reload(true);
                }
                else {
                    swal("cancel fail");
                }
            }


        }


    });
}
function hangoutJoin(btn) {
    const CANT_JOIN_NUM = 0;
    const CANT_JOIN_TIME = 1;
    const CAN_JOIN = 2;
    //console.log(this);
     var index = btn.nextElementSibling.value;
     console.log(index);

     $.ajax({
         url:"/hangout/join",
         type:"post",
         dataType:"json",
         data:{
             "index":index
     },

         success:function(data) {
             console.log(data);
             console.log(data==2);
             if(data != null) {
                 if(data == 0) {
                     swal("인원 수 안맞아");
                 }else if(data == 1) {
                     swal("시간 안맞아");
                 }else if(data == 3) {
                     swal("join 횟수 부족 보증금 넣어줘");
                 }else {
                     swal("join 성공");
                     location.reload(true);
                 }
             }


         }


     });
}
function hangoutWrite() {
    swal("구글폼 이용해서 작성하기", {
  buttons: {
    cancel: "되돌아가기",
    catch: {
      text: "구글폼  작성하러가기",
      value: "catch",
    },
  },
})
.then((value) => {
  switch (value) {
    case "catch":
    window.open('https://docs.google.com/forms/d/e/1FAIpQLScxfQc_557L3ogOPAbWEYj336Zp9NWpX8JxNyXb-yiBrEHgqw/viewform');
    window.location.reload();
      break;

  }
});
}

function initList() {
    var tag = document.getElementById("filterVal");
    console.log(tag.value);
    var addListHtml = "";
    $(':focus').blur();

    $.ajax({
        url:"/hangout/filterList",
        type:"post",
        dataType:"json",
        data:{
            "filterVal":tag.value
    },

        success:function(data) {
            //$("#hangoutList").append(data[1].join_url);
            //console.log(data);
            if(data.length==0)
            {
                //document.getElementById('addBtn').remove();
                swal("There is no more page");
            }
            console.log(data);



            for(var i=0;i<data.length;i++) {
                addListHtml+="<form action=\" "+data[i].join_url + "\" method=\"post\">";
                addListHtml+= "<div class=\"job-box d-md-flex align-items-center justify-content-between mb-30\"> ";
                addListHtml+= "<div class=\"job-left my-4 d-md-flex align-items-center flex-wrap\">"
                addListHtml+= "<div class=\"job-content\">";
                addListHtml+= "<h5 class=\"hangout-title text-center text-md-left\">"+data[i].title+"</h5>";
                addListHtml+= "<ul class=\"d-md-flex flex-wrap text-capitalize \">";
                addListHtml+= "<li class=\"mr-md-4 hangout-time\"style=\"width:90%\">";
                addListHtml+= "<i class=\"zmdi zmdi-time mr-2\"></i>" + data[i].meet_time; +"</li>";
                addListHtml+= "<li class=\"mr-md-4\" style=\"width:90%\">";
                addListHtml+= "<i class=\"zmdi zmdi-pin mr-2\" style=\"font-weight:800px;\"></i> <a class=\"hangout-location\" href=\""+ data[i].location_url +"\" >" + data[i].location +"</a></li>";
                if(data[i].openchat != "none") {
                    addListHtml+= "<li class=\"mr-md-4\" style=\"width:90%\"><i class=\"zmdi zmdi-comments mr-2\"></i><a class =\"hangout-openchat\" href=\""+ data[i].openchat + "\">kakao openchat</a></li>";
                }
                addListHtml+= "</ul><div style=\"text-align: center; \">"
                addListHtml+= "<div class=\"cl1\" style=\"display:inline-block; position: relative;margin-right:15px;\"><div style= \"position: absolute; left:35px;  bottom:22px;\"class =\"flag " + data[i].nation_image[0]+ "\"></div>";
                addListHtml+= "<span style=\"position:absolute; left:8px;top:45px; bottom:0; font-size:12px;\">" + data[i].age[0] + " / " + data[i].gender[0] + "</span>";
                addListHtml+= "  <img style=\"height:45px; width:45px; \"class = \"img-holder mb-4 mx-md-0 d-md-none d-lg-flex\" src=\""+ "/static/"+ data[i].profile_image[0]+".png\"></img>";
                addListHtml+= "  </div>";
                addListHtml+= "  <div class=\"cl1\" style=\"display:inline-block; position: relative;margin-right:15px;\">";
                addListHtml+= "    <div style= \"position: absolute; left:35px;  bottom:22px;\"class =\"flag " + data[i].nation_image[1] +"\"></div>";
                addListHtml+= "    <span style=\"position:absolute; left:8px;top:45px; bottom:0; font-size:12px;\">" + data[i].age[1] + " / " + data[i].gender[1] + "</span>";
                addListHtml+= "  <img style=\"height:45px; width:45px; \"class = \"img-holder mb-4 mx-md-0 d-md-none d-lg-flex\" src=\""+ "/static/"+ data[i].profile_image[1]+".png\"></img>";
                addListHtml+= "    </div>";
                addListHtml+= "  <div class=\"cl1\" style=\"display:inline-block; position: relative;margin-right:15px;\">";
                addListHtml+= "    <div style= \"position: absolute; left:35px;  bottom:22px;\"class =\"flag " + data[i].nation_image[2] +"\"></div>";
                addListHtml+= "    <span style=\"position:absolute; left:8px;top:45px; bottom:0; font-size:12px;\">" + data[i].age[2] + " / " + data[i].gender[2] + "</span>";
                addListHtml+= "  <img style=\"height:45px; width:45px; \"class = \"img-holder mb-4 mx-md-0 d-md-none d-lg-flex\" src=\""+ "/static/"+ data[i].profile_image[2]+".png\"></img>";
                addListHtml+= "  </div>";
                addListHtml+= "  <div class=\"cl1\" style=\"display:inline-block; position: relative;margin-right:15px;\">";
                addListHtml+= "    <div style= \"position: absolute; left:35px;  bottom:22px;\"class =\"flag " + data[i].nation_image[3] +"\"></div>";
                addListHtml+= "    <span style=\"position:absolute; left:8px;top:45px; bottom:0; font-size:12px;\">" + data[i].age[3] + " / " + data[i].gender[3] + "</span>";
                addListHtml+= "  <img style=\"height:45px; width:45px; \"class = \"img-holder mb-4 mx-md-0 d-md-none d-lg-flex\" src=\""+ "/static/"+ data[i].profile_image[3]+".png\"></img>";
                addListHtml+= "  </div>";

                addListHtml+= " </div><div class=\"job-right my-4 flex-shrink-0\"><center><input style= \"display:none;\" type=\"text\" name=\"index\" value=\""+ data[i].index +"\">"
                addListHtml+= " <input style=\"background-color:rgba(236,198,53, 0.7);color: rgba(106,57,6);width:52%; padding-left:10px; margin-left:10px;\"type=\"submit\" class=\"btn d-block d-sm-inline-block btn-light\" value = \"" + data[i].join + "\""+ data[i].active +"> "

                addListHtml+= " </center></div> </div></div></div></form>";
            }
            var list = document.getElementById("hangoutList");
            //console.log(addListHtml);
            list.innerHTML=addListHtml;




        }


    });
}

function moreList() {
    var pageNum = $("#hangoutList form").length // 10; // 기본 10  1
    var addListHtml = "";
    $(':focus').blur();

    $.ajax({
        url:"/hangout/moreList",
        type:"post",
        dataType:"json",
        data:{"pageNum":pageNum},

        success:function(data) {
            //console.log(data);
            //console.log(data[0].openchat);
            //$("#hangoutList").append(data[1].join_url);
            //console.log(data);
            //console.log("asd");
            if(data.length==0)
            {
                //document.getElementById('addBtn').remove();
                swal("There is no more page");
            }
            console.log(data);


            for(var i=0;i<data.length;i++) {
                addListHtml+="<form action=\" "+data[i].join_url + "\" method=\"post\">";
                addListHtml+= "<div class=\"job-box d-md-flex align-items-center justify-content-between mb-30\"> ";
                addListHtml+= "<div class=\"job-left my-4 d-md-flex align-items-center flex-wrap\">"
                addListHtml+= "<div class=\"job-content\">";
                addListHtml+= "<h5 class=\"hangout-title text-center text-md-left\">"+data[i].title+"</h5>";
                addListHtml+= "<ul class=\"d-md-flex flex-wrap text-capitalize \">";
                addListHtml+= "<li class=\"mr-md-4 hangout-time\"style=\"width:90%\">";
                addListHtml+= "<i class=\"zmdi zmdi-time mr-2\"></i>" + data[i].meet_time; +"</li>";
                addListHtml+= "<li class=\"mr-md-4\" style=\"width:90%\">";
                addListHtml+= "<i class=\"zmdi zmdi-pin mr-2\" style=\"font-weight:800px;\"></i> <a class=\"hangout-location\" href=\""+ data[i].location_url +"\" >" + data[i].location +"</a></li>";
                if(data[i].openchat != "none") {
                    addListHtml+= "<li class=\"mr-md-4\" style=\"width:90%\"><i class=\"zmdi zmdi-comments mr-2\"></i><a class =\"hangout-openchat\" href=\""+ data[i].openchat + "\">kakao openchat</a></li>";
                }
                addListHtml+= "</ul><div style=\"text-align: center; \">"
                addListHtml+= "<div class=\"cl1\" style=\"display:inline-block; position: relative;margin-right:15px;\"><div style= \"position: absolute; left:35px;  bottom:22px;\"class =\"flag " + data[i].nation_image[0]+ "\"></div>";
                addListHtml+= "<span style=\"position:absolute; left:8px;top:45px; bottom:0; font-size:12px;\">" + data[i].age[0] + " / " + data[i].gender[0] + "</span>";
                addListHtml+= "  <img style=\"height:45px; width:45px; \"class = \"img-holder mb-4 mx-md-0 d-md-none d-lg-flex\" src=\""+ "/static/"+ data[i].profile_image[0]+".png\"></img>";
                addListHtml+= "  </div>";
                addListHtml+= "  <div class=\"cl1\" style=\"display:inline-block; position: relative;margin-right:15px;\">";
                addListHtml+= "    <div style= \"position: absolute; left:35px;  bottom:22px;\"class =\"flag " + data[i].nation_image[1] +"\"></div>";
                addListHtml+= "    <span style=\"position:absolute; left:8px;top:45px; bottom:0; font-size:12px;\">" + data[i].age[1] + " / " + data[i].gender[1] + "</span>";
                addListHtml+= "  <img style=\"height:45px; width:45px; \"class = \"img-holder mb-4 mx-md-0 d-md-none d-lg-flex\" src=\""+ "/static/"+ data[i].profile_image[1]+".png\"></img>";
                addListHtml+= "    </div>";
                addListHtml+= "  <div class=\"cl1\" style=\"display:inline-block; position: relative;margin-right:15px;\">";
                addListHtml+= "    <div style= \"position: absolute; left:35px;  bottom:22px;\"class =\"flag " + data[i].nation_image[2] +"\"></div>";
                addListHtml+= "    <span style=\"position:absolute; left:8px;top:45px; bottom:0; font-size:12px;\">" + data[i].age[2] + " / " + data[i].gender[2] + "</span>";
                addListHtml+= "  <img style=\"height:45px; width:45px; \"class = \"img-holder mb-4 mx-md-0 d-md-none d-lg-flex\" src=\""+ "/static/"+ data[i].profile_image[2]+".png\"></img>";
                addListHtml+= "  </div>";
                addListHtml+= "  <div class=\"cl1\" style=\"display:inline-block; position: relative;margin-right:15px;\">";
                addListHtml+= "    <div style= \"position: absolute; left:35px;  bottom:22px;\"class =\"flag " + data[i].nation_image[3] +"\"></div>";
                addListHtml+= "    <span style=\"position:absolute; left:8px;top:45px; bottom:0; font-size:12px;\">" + data[i].age[3] + " / " + data[i].gender[3] + "</span>";
                addListHtml+= "  <img style=\"height:45px; width:45px; \"class = \"img-holder mb-4 mx-md-0 d-md-none d-lg-flex\" src=\""+ "/static/"+ data[i].profile_image[3]+".png\"></img>";
                addListHtml+= "  </div>";

                addListHtml+= " </div><div class=\"job-right my-4 flex-shrink-0\"><center><input style= \"display:none;\" type=\"text\" name=\"index\" value=\""+ data[i].index +"\">"
                addListHtml+= " <input style=\"background-color:rgba(236,198,53, 0.7);color: rgba(106,57,6);width:52%; padding-left:10px; margin-left:10px;\"type=\"submit\" class=\"btn d-block d-sm-inline-block btn-light\" value = \"" + data[i].join + "\""+ data[i].active +"> "

                addListHtml+= " </center></div> </div></div></div></form>";
            }

            $("#hangoutList").append(addListHtml);




        }


    });
}
