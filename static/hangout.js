/*
(로그인 한 경우) 첫 조인 때 팝업 > For your next hangout join, you need to pay 5,000 won deposit. 다음번 행아웃 참여를 위해서는 5,000원의 보증금이 필요합니다.
(로그인 x) 첫 조인 때 팝업 > Please sign in with your Kakao account to join. 행아웃 참여를 위해 카카오 로그인을 진행해주세요.
두번째 조인 누를 때 팝업 > You need to pay 5,000 won deposit to join to prevent last minute cancellations or not showing up. Please write your name on the form and send money to our business account. You can cancel at any time, if it is more than an hour before the hangout. 노쇼 방지를 위해 5,000원 보증금을 내고 행아웃을 참여하실 수 있습니다. 아래 확인 버튼을 누르셔서 구글폼에 이름을 작성하시고, 비즈니스계좌로 송금해주세요. 1시간 전에는 언제든 취소하실 수 있습니다.
세번째, 네번째 이상 조인 누를 때 팝업  (보증금 넣은 유저의 경우 ) > 팝업 없음
세번째, 네번째 이상 조인 누를 때 팝업  (보증금 뺀 유저의 경우 ) > 두번째와 동일 - You need to pay 5,000 won deposit to join to prevent last minute cancellations or not showing up. Please fill out the form and send money to our business account. You can cancel at any time, if it is more than an hour before the hangout. 노쇼 방지를 위해 5,000원 보증금을 내고 행아웃을 참여하실 수 있습니다. 아래 확인 버튼을 누르셔서 구글폼에 이름을 작성하시고, 비즈니스계좌로 송금해주세요. 1시간 전에는 언제든 취소하실 수 있습니다.
첫 조인인데 캔슬 누를 때 팝업 > If you cancel now or do not show up for the meet-up, you can join other hangouts with 5,000 won deposit. 지금 취소하시거나 행아웃에 불참하시면, 다음 행아웃부터 5,000원 보증금을 내고 참여하실 수 있습니다.
그냥 캔슬 누를 때 팝업 > 없음
캔슬 1시간 이내일 때 눌렀을 때 팝업 > If you cancel now, you cannot get the refund as it is last minute. If you don’t show up, neither can you get the refund nor can you join other hangouts for the next 4 hours. 지금 취소하시면, 보증금 환불이 불가합니다. 행아웃에 불참하셔도, 환불이 불가하며, 4시간동안 다른 행아웃 참여가 불가합니다.



*/

/*
    0 - 인원수 딸려서
    1 - 4시간 이내 행아웃
    2 - 생애 첫 조인
    3 - 조인불가 보증금 넣어주세요
    4 - 조인 성공 // 이미 여러번 조인 해본 person
*/

var pig = document.createElement("span");
pig.innerHTML = "<center><img style =\"width:125px; height:100px; \"src=\"/static/pig.jpeg\"/></center><p><br><br>Put 5,000won deposit to prevent last minute cancellations. Cancel at any time, if it is more than an hour before the hangout. Let us know if you already paid the deposit. <br> 노쇼 방지를 위해 5,000원 보증금을 내고 행아웃을 참여하실 수 있습니다. 1시간 전에는 언제든 취소하실 수 있습니다. 이미 납부하셨다면 저희에게 연락주세요.</p>";

var kakao = document.createElement("span");
kakao.innerHTML = "<center><img style =\"width:150px; margin-top:40px; height:150px; \"src=\"/static/kakao_icon.png\"/></center><p><br><br>Wait! Click OK and join the chat room! 잠시만요! OK를 눌러서 오픈채팅방에 입장해주세요 :)</p>";

function getUserInfo(user_id) {
    if(user_id != "none") {
        window.location.href = '/sign/userInfo/'+user_id;
    }

}

function checkCancelTime(btn) {
    var index = btn.nextElementSibling.value;
    var res;
    $.ajax({
        url:"/hangout/checkCancelTime",
        type:"GET",
        dataType:"json",
        async:false,
        data :{
            "index": parseInt(index)
        },
        success:function(data) {
            res = data;
        }
    });
    return res;
}
function doCancel(btn){
    var index = btn.nextElementSibling.value;
    $.ajax({
        url:"/hangout/cancel",
        type:"post",
        dataType:"json",
        async:false,
        data:{
            "index": parseInt(index)
    },
        success:function(data) {
            if(data != null) {
                if(data == true) {
                    //swal("cancel 완료 ");
                    window.location.reload(true);
                }
                else {
                    swal("cancel fail");
                }
            }


        }


    });
}
function hangoutCancel(btn) {
    var index = btn.nextElementSibling.value;
    if(checkCancelTime(btn) == false) {
        swal({
            text:"If you cancel now, you cannot get the refund as it is last minute. If you don’t show up, neither can you get the refund nor can you join other hangouts for the next 4 hours. 지금 취소하시면, 보증금 환불이 불가합니다. 행아웃에 불참하셔도, 환불이 불가하며, 4시간동안 다른 행아웃 참여가 불가합니다.",
            icon:'error',
            buttons :{
                cancel: "back",
                confirm : {
                    text:'OK',
                    value:true
                },
            },
        }).then((result) => {
            if(result) {
                btn.setAttribute("disabled","disabled");
                doCancel(btn);
            }
        });
    } else {
        btn.setAttribute("disabled","disabled");
        doCancel(btn);
    }


}

/*
    0 - 인원수 딸려서
    1 - 4시간 이내 행아웃
    2 - 생애 첫 조인
    3 - 조인불가 보증금 넣어주세요
    4 - 조인 성공 // 이미 여러번 조인 해본 person
*/

function getUserCancel() {
    var result;
    $.ajax({
        url:"/sign/getUserCancel",
        type:"GET",
        async: false,
        dataType:"json",
        data:{

    },

        success:function(data) {
            result = data;
        }

    });
    return result;

}
var clock = document.createElement("span");
clock.innerHTML = "<center><img style =\"width:100px; height:100px; \"src=\"/static/clock.jpeg\"/></center><p><br><br>You cannot join another hangout within 4 hours before or after your previous one.<br> 기존 행아웃의 4시간 전후로는 행아웃을 새로 신청하실 수 없습니다.</p>";
function join(btn) {
    var index = btn.nextElementSibling.value;
    $.ajax({
        url:"/hangout/join",
        type:"post",
        async: false,
        dataType:"json",
        data:{
            "index":index
    },
        success:function(data) {
            console.log(data);
            if(data == 0) // 인원수 충족 못해서 참가 못함
            {
                swal({
                    text:"배피 행아웃은 같은 국적 3명 이상 참가 불가합니다.\n Bappy Hangout cannot be played by more than 3 people of the same nationality.",
                    icon:'error',
                    buttons :{
                        confirm : {
                            text:'OK'
                        }
                    }
                })
            } else if(data == 1) {// 4시간 이내
                swal({
                    content: (clock),
                    buttons : {
                        confirm :{
                            text:'OK'
                            }
                        }
                })
            } else if(data == 2) { // join success
                //swal("join success");
                btn.setAttribute("disabled","disabled");
                swal({
                    content:(kakao),
                    buttons : {
                        cancel:"Back",
                        confirm: {
                            text: 'OK',
                            value : true,
                        },

                    },
                }).then((result) => {
                    if(result) {
                        location.href = btn.parentNode.parentNode.parentNode.getElementsByClassName("hangout-openchat")[0].getAttribute('href');
                    } else {
                        window.location.reload(true);

                    }
                });
            } else { // join 수
                console.log("join 수 부족");
            }


        }


    });

}
function hangoutJoin(btn) {
    var userCancel = getUserCancel();
    console.log(userCancel);
    if(userCancel == 0) { // 참가불가
        swal({
            content:(pig),
            buttons : {
                cancel:"Back",
                confirm: {
                    text: 'Deposit',
                    value : true,
                },

            },
        }).then((result) => {
            if(result) {
                location.href = 'https://docs.google.com/forms/d/e/1FAIpQLSd-Xl3mV9KT32Ee4O9Aqz1mr91_ZKION1670zzNsYyJXBwUoQ/viewform';
            }
        });
    } else if(userCancel == 1) { // 생애 첫 조인
        swal({
            text:"For your next hangout join, you need to pay 5,000 won deposit.\n 다음번 행아웃 참여를 위해서는 5,000원의 보증금이 필요합니다.",
            icon:'warning',
            buttons : {
                cancel:"Back",
                confirm : {
                    text:'Join',
                    value:true,
                },
            },
        }).then((result)=> {
            if(result) {
                // join
                join(btn);
            }
        });
    } else { // 조인 여러번
        join(btn);
    }
}
/*
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
             //console.log(data);
             //console.log(data==2);
             if(data != null) {
                 if(data == 0) { // 0 -> no seat
                     swal("If you cancel now, you cannot get the refund as it is last minute. If you don’t show up, neither can you get the refund nor can you join other hangouts for the next 4 hours. 지금 취소하시면, 보증금 환불이 불가합니다. 행아웃에 불참하셔도, 환불이 불가하며, 4시간동안 다른 행아웃 참여가 불가합니다.", {
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
               });                 }else if(data == 1) { // 1-> cause time
                     swal("Put 5,000won deposit to prevent last minute cancellations. Cancel at any time, if it is more than an hour before the hangout. Fill out the form below.\n 노쇼 방지를 위해 5,000원 보증금을 내고 행아웃을 참여하실 수 있습니다. 1시간 전에는 언제든 취소하실 수 있습니다. 아래 구글폼을 참고해주세요.", {
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
               });                 }else if(data == 2) { // 2-> first join in life
                     swal("For your next hangout join, you need to pay 5,000 won deposit. 다음번 행아웃 참여를 위해서는 5,000원의 보증금이 필요합니다.", {
                   buttons: {
                     cancel: "Back",
                     catch: {
                       text: "Join",
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
               });                 }else if(data == 3){ // 3 -> cant join
                     swal("Put 5,000won deposit to prevent last minute cancellations. Cancel at any time, if it is more than an hour before the hangout. Fill out the form below.\n노쇼 방지를 위해 5,000원 보증금을 내고 행아웃을 참여하실 수 있습니다. 1시간 전에는 언제든 취소하실 수 있습니다. 아래 구글폼을 참고해주세요.", {
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
                     location.reload(true);
                 } else { // data == 4 join success
                     swal("Put 5,000won deposit to prevent last minute cancellations. Cancel at any time, if it is more than an hour before the hangout. Fill out the form below.\n노쇼 방지를 위해 5,000원 보증금을 내고 행아웃을 참여하실 수 있습니다. 1시간 전에는 언제든 취소하실 수 있습니다. 아래 구글폼을 참고해주세요.", {
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
                     location.reload(true);
                 }
             }


         }


     });
}
*/
function hangoutWrite() {
    swal( {
        text:"Make a hangout yourself by filling out the form!\n 구글폼에 원하는 행아웃을 직접 신청해보아요!",
        buttons: {
          cancel: "Back",
          catch: {
            text: "Go",
            value: "catch",
          },
        },
    }).then((value) => {
  switch (value) {
    case "catch":
    window.open('https://forms.gle/x5obVm1soKZT5Yv9A');
    window.location.reload();
      break;

  }
});
}

function initList() {
    var tag = document.getElementById("filterVal");
    //console.log(tag.value);
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
            //console.log(data);



            for(var i=0;i<data.length;i++) {
                addListHtml+="<form action=\" "+data[i].join_url + "\" method=\"post\">";
                addListHtml+= "<div class=\"job-box d-md-flex align-items-center justify-content-between mb-30\"> ";
                addListHtml+= "<div class=\"job-left my-4 d-md-flex align-items-center flex-wrap\">"
                addListHtml+= "<div class=\"job-content\">";
                addListHtml+= "<h6 class=\"hangout-title text-center text-md-left\">"+data[i].title+"</h6>";
                addListHtml+= "<center><img src=\"../static/hangout/"+data[i].image + ".jpg\" style=\"height:130px; object-fit: cover;width:80%;border-radius: 10%; margin-top:10px; \"></center>";
                addListHtml+= "<ul class=\"d-md-flex flex-wrap text-capitalize \">";
                addListHtml+= "<li class=\"mr-md-4 hangout-time\"style=\"width:90%\">";
                addListHtml+= "<img src=\"../static/widget/calender.png\" style=\"width:16.29px; height:16.85px;\">" + data[i].meet_time; +"</li>";
                addListHtml+= "<li class=\"mr-md-4\" style=\"width:90%\">";
                addListHtml+= "<img src=\"../static/widget/location.png\" style=\"width:15px; height:19.65px;\"> <a class=\"hangout-location\" href=\""+ data[i].location_url +"\" >" + data[i].location +"</a></li>";
                if(data[i].join == "cancel") {
                    addListHtml+= "<li class=\"mr-md-4\" style=\"width:90%\"><img src=\"../static/widget/openchat.png\" style=\"width:18px; height:18.62px;\"><a class =\"hangout-openchat\" href=\""+ data[i].openchat + "\">kakao openchat</a></li>";
                }
                else {
                    addListHtml+= "<li class=\"mr-md-4\" style=\"width:90%; display:none;\"><i class=\"zmdi zmdi-comments mr-2\"></i><a class =\"hangout-openchat\" href=\""+ data[i].openchat + "\">kakao openchat</a></li>";
                }
                addListHtml+= "</ul>";
                if(data[i].join != "cancel") {
                    addListHtml+="<center style=\"height:0px;\"><div style=\"z-index:1;top:10px;position:relative; color: rgba(106,57,6); font-size:20px;font-weight:600;\">Join to see who's here!</div></center>";
                }
                if(data[i].join == "cancel") {
                    addListHtml+="<div style=\"text-align: center; z-index:-1;\">";
                }else {
                    addListHtml+="<div style=\"text-align: center; filter: blur(3px);z-index:-1;\">";
                }
                addListHtml+= "<div class=\"cl1\" style=\"display:inline-block; position: relative;margin-right:15px;\"><div style= \"position: absolute; left:35px;  bottom:22px;\"class =\"flag " + data[i].nation_image[0]+ "\"></div>";
                addListHtml+= "<span style=\"position:absolute; left:8px;top:45px; bottom:0; font-size:12px;\">" + data[i].age[0] + " / " + data[i].gender[0] + "</span>";
                addListHtml+= "  <img style=\"height:45px; width:45px; \"class = \"img-holder mb-4 mx-md-0 d-md-none d-lg-flex\" onclick=\"getUserInfo(" +  data[i].participants_id[0] +")\" src=\""+ "/static/profileImage/"+ data[i].profile_image[0]+".png\"></img>";
                addListHtml+= "  </div>";
                addListHtml+= "  <div class=\"cl1\" style=\"display:inline-block; position: relative;margin-right:15px;\">";
                addListHtml+= "    <div style= \"position: absolute; left:35px;  bottom:22px;\"class =\"flag " + data[i].nation_image[1] +"\"></div>";
                addListHtml+= "    <span style=\"position:absolute; left:8px;top:45px; bottom:0; font-size:12px;\">" + data[i].age[1] + " / " + data[i].gender[1] + "</span>";
                addListHtml+= "  <img style=\"height:45px; width:45px; \"class = \"img-holder mb-4 mx-md-0 d-md-none d-lg-flex\" onclick=\"getUserInfo(" +  data[i].participants_id[1] +")\" src=\""+ "/static/profileImage/"+ data[i].profile_image[1]+".png\"></img>";
                addListHtml+= "    </div>";
                addListHtml+= "  <div class=\"cl1\" style=\"display:inline-block; position: relative;margin-right:15px;\">";
                addListHtml+= "    <div style= \"position: absolute; left:35px;  bottom:22px;\"class =\"flag " + data[i].nation_image[2] +"\"></div>";
                addListHtml+= "    <span style=\"position:absolute; left:8px;top:45px; bottom:0; font-size:12px;\">" + data[i].age[2] + " / " + data[i].gender[2] + "</span>";
                addListHtml+= "  <img style=\"height:45px; width:45px; \"class = \"img-holder mb-4 mx-md-0 d-md-none d-lg-flex\" onclick=\"getUserInfo(" +  data[i].participants_id[2] +")\" src=\""+ "/static/profileImage/"+ data[i].profile_image[2]+".png\"></img>";
                addListHtml+= "  </div>";
                addListHtml+= "  <div class=\"cl1\" style=\"display:inline-block; position: relative;margin-right:15px;\">";
                addListHtml+= "    <div style= \"position: absolute; left:35px;  bottom:22px;\"class =\"flag " + data[i].nation_image[3] +"\"></div>";
                addListHtml+= "    <span style=\"position:absolute; left:8px;top:45px; bottom:0; font-size:12px;\">" + data[i].age[3] + " / " + data[i].gender[3] + "</span>";
                addListHtml+= "  <img style=\"height:45px; width:45px; \"class = \"img-holder mb-4 mx-md-0 d-md-none d-lg-flex\" onclick=\"getUserInfo(" +  data[i].participants_id[3] +")\" src=\""+ "/static/profileImage/"+ data[i].profile_image[3]+".png\"></img>";
                addListHtml+= "  </div>";
                addListHtml+= " </div><div class=\"job-right my-4 flex-shrink-0\"><center>"

                if(data[i].join == "join") {
                    addListHtml+= "<input style=\"background-color:rgba(236,198,53, 0.7);color: rgba(106,57,6);width:52%; padding-left:10px;margin-left:10px;\" " +data[i].active+" type=\"button\"onclick=\"hangoutJoin(this);\" class=\"btn d-block d-sm-inline-block btn-light\" value = "+data[i].join+"  >";
                } else {
                    addListHtml+= "<input style=\"background-color:rgba(236,198,53, 0.7);color: rgba(106,57,6);width:52%; padding-left:10px;margin-left:10px;\" " +data[i].active+" type=\"button\"onclick=\"hangoutCancel(this);\" class=\"btn d-block d-sm-inline-block btn-light\" value = "+data[i].join+"  >";
                }


                addListHtml+= "<input style= \"display:none;\" type=\"text\" name=\"index\" value=\""+ data[i].index +"\"></center>";

                addListHtml+= " </div></div></div></div></form>";
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
                addListHtml+= "<h6 class=\"hangout-title text-center text-md-left\">"+data[i].title+"</h6>";
                addListHtml+= "<center><img src=\"../static/hangout/"+data[i].image + ".jpg\" style=\"height:130px;object-fit: cover; width:80%;border-radius: 10%; margin-top:10px; \"></center>";
                addListHtml+= "<ul class=\"d-md-flex flex-wrap text-capitalize \">";
                addListHtml+= "<li class=\"mr-md-4 hangout-time\"style=\"width:90%\">";
                addListHtml+= "<img src=\"../static/widget/calender.png\" style=\"width:16.29px; height:16.85px;\">" + data[i].meet_time; +"</li>";
                addListHtml+= "<li class=\"mr-md-4\" style=\"width:90%\">";
                addListHtml+= "<img src=\"../static/widget/location.png\" style=\"width:15px; height:19.65px;\"> <a class=\"hangout-location\" href=\""+ data[i].location_url +"\" >" + data[i].location +"</a></li>";
                if(data[i].join == "cancel") {
                    addListHtml+= "<li class=\"mr-md-4\" style=\"width:90%\"><img src=\"../static/widget/openchat.png\" style=\"width:18px; height:18.62px;\"><a class =\"hangout-openchat\" href=\""+ data[i].openchat + "\">kakao openchat</a></li>";
                }
                else {
                    addListHtml+= "<li class=\"mr-md-4\" style=\"width:90%; display:none;\"><i class=\"zmdi zmdi-comments mr-2\"></i><a class =\"hangout-openchat\" href=\""+ data[i].openchat + "\">kakao openchat</a></li>";
                }
                addListHtml+= "</ul><div style=\"text-align: center; \">"
                addListHtml+= "<div class=\"cl1\" style=\"display:inline-block; position: relative;margin-right:15px;\"><div style= \"position: absolute; left:35px;  bottom:22px;\"class =\"flag " + data[i].nation_image[0]+ "\"></div>";
                addListHtml+= "<span style=\"position:absolute; left:8px;top:45px; bottom:0; font-size:12px;\">" + data[i].age[0] + " / " + data[i].gender[0] + "</span>";
                addListHtml+= "  <img style=\"height:45px; width:45px; \"class = \"img-holder mb-4 mx-md-0 d-md-none d-lg-flex\" onclick=\"getUserInfo(" +  data[i].participants_id[0] +")\" src=\""+ "/static/profileImage/"+ data[i].profile_image[0]+".png\"></img>";
                addListHtml+= "  </div>";
                addListHtml+= "  <div class=\"cl1\" style=\"display:inline-block; position: relative;margin-right:15px;\">";
                addListHtml+= "    <div style= \"position: absolute; left:35px;  bottom:22px;\"class =\"flag " + data[i].nation_image[1] +"\"></div>";
                addListHtml+= "    <span style=\"position:absolute; left:8px;top:45px; bottom:0; font-size:12px;\">" + data[i].age[1] + " / " + data[i].gender[1] + "</span>";
                addListHtml+= "  <img style=\"height:45px; width:45px; \"class = \"img-holder mb-4 mx-md-0 d-md-none d-lg-flex\" onclick=\"getUserInfo(" +  data[i].participants_id[1] +")\"src=\""+ "/static/profileImage/"+ data[i].profile_image[1]+".png\"></img>";
                addListHtml+= "    </div>";
                addListHtml+= "  <div class=\"cl1\" style=\"display:inline-block; position: relative;margin-right:15px;\">";
                addListHtml+= "    <div style= \"position: absolute; left:35px;  bottom:22px;\"class =\"flag " + data[i].nation_image[2] +"\"></div>";
                addListHtml+= "    <span style=\"position:absolute; left:8px;top:45px; bottom:0; font-size:12px;\">" + data[i].age[2] + " / " + data[i].gender[2] + "</span>";
                addListHtml+= "  <img style=\"height:45px; width:45px; \"class = \"img-holder mb-4 mx-md-0 d-md-none d-lg-flex\" onclick=\"getUserInfo(" +  data[i].participants_id[2] +")\" src=\""+ "/static/profileImage/"+ data[i].profile_image[2]+".png\"></img>";
                addListHtml+= "  </div>";
                addListHtml+= "  <div class=\"cl1\" style=\"display:inline-block; position: relative;margin-right:15px;\">";
                addListHtml+= "    <div style= \"position: absolute; left:35px;  bottom:22px;\"class =\"flag " + data[i].nation_image[3] +"\"></div>";
                addListHtml+= "    <span style=\"position:absolute; left:8px;top:45px; bottom:0; font-size:12px;\">" + data[i].age[3] + " / " + data[i].gender[3] + "</span>";
                addListHtml+= "  <img style=\"height:45px; width:45px; \"class = \"img-holder mb-4 mx-md-0 d-md-none d-lg-flex\" onclick=\"getUserInfo(" +  data[i].participants_id[3] +")\" src=\""+ "/static/profileImage/"+ data[i].profile_image[3]+".png\"></img>";
                addListHtml+= "  </div>";
                addListHtml+= " </div><div class=\"job-right my-4 flex-shrink-0\"><center>"

                if(data[i].join == "join") {
                    addListHtml+= "<input style=\"background-color:rgba(236,198,53, 0.7);color: rgba(106,57,6);width:52%; padding-left:10px;margin-left:10px;\" " +data[i].active+" type=\"button\"onclick=\"hangoutJoin(this);\" class=\"btn d-block d-sm-inline-block btn-light\" value = "+data[i].join+"  >";
                } else {
                    addListHtml+= "<input style=\"background-color:rgba(236,198,53, 0.7);color: rgba(106,57,6);width:52%; padding-left:10px;margin-left:10px;\" " +data[i].active+" type=\"button\"onclick=\"hangoutCancel(this);\" class=\"btn d-block d-sm-inline-block btn-light\" value = "+data[i].join+"  >";
                }


                addListHtml+= "<input style= \"display:none;\" type=\"text\" name=\"index\" value=\""+ data[i].index +"\"></center>";

                addListHtml+= " </div></div></div></div></form>";
            }

            $("#hangoutList").append(addListHtml);




        }


    });
}
