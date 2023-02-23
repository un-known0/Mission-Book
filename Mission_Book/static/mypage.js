const tabList = document.querySelectorAll('.tab_menu .list li');
for (var i = 0; i < tabList.length; i++) {
  tabList[i].querySelector('.btn').addEventListener('click', function (e) {
    e.preventDefault();
    for (var j = 0; j < tabList.length; j++) {
      tabList[j].classList.remove('is_on');
    }

    this.parentNode.classList.add('is_on');
  });
}

// 서브 메뉴 함수
const subtabList = document.querySelectorAll('#complete li');
for (var i = 0; i < subtabList.length; i++) {
  subtabList[i].querySelector('.sub-btn').addEventListener('click', function (ev) {
    ev.preventDefault();
    for (var j = 0; j < subtabList.length; j++) {
      subtabList[j].classList.remove('is_sub');
    }

    this.parentNode.classList.add('is_sub');
  });
}

// 스탯 총 개수 계산
function plus() {
  const cnt1 = Number(document.getElementById("study-complete").innerText);
  const cnt2 = Number(document.getElementById("social-complete").innerText);
  const cnt3 = Number(document.getElementById("exp-complete").innerText);
  const total = document.getElementById("total");
  const result = cnt1 + cnt2 + cnt3;

  console.log(cnt3);
  console.log(result);
  total.innerText = result;
}

//색상 변경 코드
var beforeColor; //이전에 선택된 컬러 저장 할 변수

//HTML 로딩 후, 함수 실행
window.onload = function () {
  init();
}

function init() {
  // 색상 팔레트
  var pallet = [['#D10E0E', '#0E74D1', '#0EBAD1', '#C8D627', '#DA5BC6']];
  var tag = "";

  for (i = 0; i < pallet.length; i++) {
    for (j = 0; j < pallet[i].length; j++) {
      tag += "<div id=" + pallet[i][j] + " class='colorBox' onclick='colorSet(this)'></div>";
    }
  }

  document.getElementById("palletBox").innerHTML = tag;

  //색상 입히기
  var colorBox = document.getElementsByClassName("colorBox");
  for (i = 0; i < colorBox.length; i++) {
    colorBox[i].style.background = colorBox[i].id;
  }
}

// 색상 변경
function colorSet(target) {
  document.querySelector("body").style.color = target.id;

  if (beforeColor != undefined && beforeColor != null) {
    document.getElementById(beforeColor).className = document.getElementById(beforeColor).className.replace(" active", "");
  }

  document.getElementById(target.id).className += " active";
  beforeColor = target.id;
}