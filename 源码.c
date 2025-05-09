var currentVid = ""; //当前id
var umark = ""; //验证码唯一标识
var retry = 0; //重试次数
var callback = ""; //回调地址
var server = ""; //游戏服地址
var token = "";
var clickEnable = true; //是否可点击
var userAgent = ""; //判断是否是webview
var vtype = 0; //是什么类型的验证码
var isrobot = 0; //是否是机器人验证
var textClickNumber = 3; //文字点选可点击次数
var currentClickNumber = 1; //当前点击次数
var textClickArr = []; //文字点选的点数组
var slideClickAble = false; //是否在点击状态下
var slideOutAble = false; //是否可触发移出事件
var slideUpAble = false; //是否可触发抬起事件
var slideDownAble = true; //滑块是否可点击拖动
var refreshAble = true; //刷新按钮是否可用
var isrobotAble = true; //检测机器人按钮是否可用
var imageClickAble = true; //图片验证码点击是否可用
var textClickAble = true; //文字点选点击是否可用
var puzzleClickAble = true; //图片拼图点击是否可用
var currentPuzzle = 0; //当前点选的拼图图片
var currentPuzzleDomIndex = 0; //当前点选的拼图图片所在的元素的下标
var puzzleMoveAble = false; //拼图图片是否可拖动
var puzzleUpAble = false; //拼图抬起事件是否可触发
var puzzleEnd = 0; //图片拼图落下点
var puzzleEndDomIndex = 0; //图片拼图落下点所在的元素的下标
var imgArr = [];
var translate = {};
var lang = "";
var successText = "";
var failText = "";
var puzzleDomCount = 8; //拼图dom的数量
var puzzleZoomType = 2; //1拼图大小不变，大图根据拼图数量变化；2大图大小不变，拼图根据拼图数量变化
var projectCode = "";
var timer = null;
var countdown = 60;

var imgContentWidth;

// just debugger
var dev_test = false;

String.prototype.padStart = String.prototype.padStart
  ? String.prototype.padStart
  : function (targetLength, padString) {
    targetLength = Math.floor(targetLength) || 0;
    if (targetLength < this.length) return String(this);

    padString = padString ? String(padString) : " ";

    var pad = "";
    var len = targetLength - this.length;
    var i = 0;
    while (pad.length < len) {
      if (!padString[i]) {
        i = 0;
      }
      pad += padString[i];
      i++;
    }

    return pad + String(this).slice(0);
  };

if (typeof String.prototype.endsWith !== "function") {
  String.prototype.endsWith = function (suffix) {
    return this.indexOf(suffix, this.length - suffix.length) !== -1;
  };
}

// ios拖动整个页面问题
(function () {
  $(window).bind("touchmove", function (e) {
    e.preventDefault && e.preventDefault();
  });
  $(document).bind("touchmove", function (e) {
    e.preventDefault && e.preventDefault();
  });
})();

function resize() {
  imgContentWidth = $("#img-content").width();
}
window.addEventListener("resize", function () {
  resize();
});

resize();

function initPuzzlePosi() { }

function getUrlParam(name) {
  if (window.location.search) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = window.location.search.substr(1).match(reg); //匹配目标参数
    if (r != null) return unescape(r[2]);
    return null; //返回参数值
  }
}
function transformRobot() {
  if (isrobotAble) {
    if (isrobot) {
      isrobot = 0;
    } else {
      isrobot = 1;
    }
  } else {
    return;
  }
}
var getImage = function (server, token) {
  userAgent = navigator.userAgent;
  $.ajax({
    url: server + "verification_code",
    headers: {
      Authorization: token,
    },
    data: { vtype: vtype, lang: lang, umark: umark },
    type: "get",
    beforeSend: function (XMLHttpRequest) {
      $("#loading").show(); // 数据加载成功之前，显示loading...
      $("#img-content").hide();
    },
    success: function (data) {
      $("#confirm-fail").hide();
      $("#loading").hide();
      $("#img-content").show();
      $("#confirm-info").show();
      $("#confirm-info").text(JSON.parse(data).data.question);
      currentVid = JSON.parse(data).data.vid;
      translate = JSON.parse(data).data.extra;
      successText = JSON.parse(data).data.localization.success;
      failText = JSON.parse(data).data.localization.fail;
      $("#confirm-result-success").html(successText);
      $("#confirm-result-fail").html(failText);
      if (JSON.parse(data).data.vtype === 1) {
        vtype = 1;
        $("#image").attr(
          "src",
          "data:image/png;base64," + JSON.parse(data).data.verification_code
        );
        $("#slide-image-bg").hide();
        $("#slide-image-slider").hide();
        $("#text-click-image").hide();
      } else if (JSON.parse(data).data.vtype === 2) {
        vtype = 2;
        $("#slide-image-slider").css("left", 0);
        $("#slide-image-slider").css("top", 0);
        $("#slide-image-bg").attr(
          "src",
          "data:image/png;base64," + JSON.parse(data).data.background
        );
        $("#slide-image-slider").attr(
          "src",
          "data:image/png;base64," + JSON.parse(data).data.slider
        );
        $("#image").hide();
        $("#text-click-image").hide();
        // $('#isrobot-info').show();
      } else if (JSON.parse(data).data.vtype === 3) {
        vtype = 3;
        $("#text-click-image").attr(
          "src",
          "data:image/png;base64," + JSON.parse(data).data.verification_code
        );
        $("#slide-image-bg").hide();
        $("#slide-image-slider").hide();
        $("#image").hide();
        currentClickNumber = 1;
        if (JSON.parse(data).data.hasOwnProperty("click_word")) {
          textClickNumber = JSON.parse(data).data.click_word;
        } else {
          textClickNumber = 3;
        }
      } else if (JSON.parse(data).data.vtype === 4) {
        vtype = 4;
        $("#text-click-image").hide();
        $("#slide-image-bg").hide();
        $("#slide-image-slider").hide();
        $("#image").hide();
        $("#puzzle-container").show();
        imgArr = JSON.parse(data).data.backgrounds;
        // imgArr.length = 6;

        var widthPrecent = (2 / imgArr.length) * 100;

        $("#puzzle-container-hide").css("width", widthPrecent + "%");

        var puzzleContainer = $("#puzzle-container");
        switch (+puzzleZoomType) {
          case 1:
            var containerWidth = (imgArr.length / puzzleDomCount) * 100;
            puzzleContainer.css("width", containerWidth + "%");
            puzzleContainer.css("margin-left", 50 - containerWidth / 2 + "%");
            break;
          case 2:
            puzzleContainer.css("width", "100%");
            puzzleContainer.css("margin-left", "0%");
            break;
        }

        // $("#puzzle-container").attr("puzzle-count", imgArr.length);

        for (var i = 0; i < puzzleDomCount; i++) {
          // $('.cover').eq(i).hover && $('.cover').eq(i).hover(
          //     function () {
          //       if (!puzzleMoveAble) {
          //         $('.cover').eq(i).css('background', 'rgb(255,255,255,0.8)');
          //       }
          //     },
          //     function () {
          //       if (!puzzleMoveAble) {
          //         $('.cover').eq(i).css('background', 'transparent');
          //       }
          //     },
          //   );
          $(".cover").eq(i).css("background", "transparent");

          var domObj = $(".puzzle-single-container").eq(i);

          var offset =
            i * 2 < imgArr.length ? 0 : imgArr.length / 2 - puzzleDomCount / 2;
          if (offset && (i % (puzzleDomCount / 2)) + 1 > imgArr.length / 2) {
            domObj.hide();
            continue;
          }

          domObj.show();
          domObj.css("width", widthPrecent + "%");
          domObj.css("left", widthPrecent * (i % 4) + "%");
          $(".puzzle-image")
            .eq(i)
            .attr(
              "src",
              "data:image/png;base64," +
              JSON.parse(data).data.backgrounds[i + offset]
            );
        }
      }
    },
  });
};

function customization() {
  // 显示倒计时区域
  $("#all-chance").text(retry);
  $("#done-chance").text(retry);
  // size show
  window.addEventListener("resize", function (e) {
    var _target = e.target;
    $("#size-container").text(_target.innerWidth + "*" + _target.innerHeight);
  });
  $("#size-container").text($("html").width() + "*" + $("html").height());
  $("#size-container").on("click", function () {
    $("#size-container").text($("html").width() + "*" + $("html").height());
  });
  // 开始倒计时
  doCountdown({
    count: countdown,
    container: ".countdown-time",
    finished: function () {
      // 倒计时结束回调,走验证失败逻辑
      switch (vtype) {
        case 1:
          clickEnable = false;
          refreshAble = false;
          break;
        case 2:
          clickEnable = false;
          slideClickAble = false;
          refreshAble = false;
          slideDownAble = false;
          // 倒计时结束
          sliderConfirm([], 0, 0, true);
          break;
        case 3:
          clickEnable = false;
          refreshAble = false;
          textClickAble = false;
          // 倒计时结束
          textClickTimeOutFetch();
          break;
        case 4:
          refreshAble = false;
          puzzleClickAble = false;
          puzzleMoveAble = false;
          puzzleUpAble = false;
          break;
      }
      $("#confirm-info").hide();
      $("#confirm-fail").show();
      window.$Interface.close();
    },
  });
}
// 倒计数，传一个秒数
function doCountdown(params) {
  var count = params.count;

  $(params.container).text(transSecondToTimeStr(count));
  timer = setInterval(function () {
    if (timer && count <= 0) {
      clearInterval(timer);
      params.finished();
    } else {
      count -= 1;
      $(params.container).text(transSecondToTimeStr(count));
    }
  }, 1000);
}

function transSecondToTimeStr(second) {
  var hh = Math.floor(second / (60 * 60));
  var mm = Math.floor((second - hh * 3600) / 60);
  var ss = second - hh * 3600 - mm * 60;
  return [hh, mm, ss]
    .map(function (v) {
      return String(v).padStart(2, "0");
    })
    .join(":");
}

// $(document).on('click', '#isrobot-info', transformRobot);

var getBackground = function (server, token) {
  $.ajax({
    url: server + "background",
    headers: {
      Authorization: token,
    },
    type: "get",
    success: function (data) {
      var backgroundUrl = "";
      var bottomFrameUrl = "";
      try {
        backgroundUrl = JSON.parse(data).data.background;
      } catch (error) { }

      if (!window.fullScreen) {
        if (backgroundUrl) {
          $("#body").css("background-image", "url(" + backgroundUrl + ")");
        } else {
          $("#body").css(
            "background-image",
            "url('./static/images/pic_bg.png')"
          );
        }
      }
    },
  });
};

$(function () {
  dev_test = getUrlParam("dev");
  projectCode = getUrlParam("project");
  scene = getUrlParam("scene");
  umark = getUrlParam("umark");
  retry = Number(getUrlParam("retry"));
  callback = getUrlParam("callback");
  server = getUrlParam("server");
  server = server.endsWith("/") ? server : server + "/";
  // server = "/api/auth/";
  token = getUrlParam("token");
  vtype = getUrlParam("vtype") || 0;
  lang = getUrlParam("lang");
  countdown = Math.abs(parseInt(getUrlParam("countdown"))) || 60;
  // 最多24h
  countdown = countdown > 86400 ? 86400 : countdown;
  getBackground(server, token);
  getImage(server, token);
  if (projectCode === "g18") {
    if (scene === "default") {
      customization();
    }
  }
});

function refreshClick(e) {
  if (refreshAble) {
    if (vtype === 3) {
      textClickArr = [];
      // textClickNumber = 3;
      $("#text-click-icon-one").hide();
      $("#text-click-icon-two").hide();
      $("#text-click-icon-three").hide();
    }
    getImage(server, token);
  } else {
    return;
  }
}

$(document).on("click", "#refresh-btn", refreshClick);

function hideRefreshBtnAfterRetry() {
  if (retry == 0) {
    $("#refresh-btn").hide();
  }
}

function imageClick(e) {
  if (imageClickAble) {
    if (vtype === 1) {
      if (clickEnable) {
        var y = e.offsetY;
        var x = e.offsetX;
        var width = $("#image").width();
        var height = $("#image").height();
        $.ajax({
          url: server + "check_verification_code",
          headers: {
            Authorization: token,
          },
          contentType: "application/json",
          type: "post",
          data: JSON.stringify({
            umark: umark,
            vid: currentVid,
            px: x / width,
            py: y / height,
            final: retry === 1 ? true : false,
            callback: callback,
            vtype: vtype,
            extra: translate,
          }),
          dataType: "json",
          beforeSend: function (XMLHttpRequest) {
            imageClickAble = false;
          },
          success: function (data) {
            if (data.data.status === 5000) {
              timer && clearInterval(timer);
              if (userAgent.indexOf("Unisdk") === -1) {
                alert("连接超时");
                refreshAble = false;
                imageClickAble = false;
                isrobotAble = false;
              } else {
                window.$Interface.close();
              }
            } else {
              if (data.data.res) {
                timer && clearInterval(timer);
                $("#confirm-result").show();
                $("#confirm-info").hide();
                clickEnable = false;
                refreshAble = false;
                setTimeout(function () {
                  if (data.data.forward) {
                    window.location.replace(data.data.forward);
                  } else {
                    window.$Interface.close();
                  }
                }, 500);
              } else {
                retry > 0 && retry--;
                $("#done-chance").text(retry);
                hideRefreshBtnAfterRetry();
                if (retry === 0) {
                  timer && clearInterval(timer);
                  clickEnable = false;
                  refreshAble = false;
                  $("#confirm-info").hide();
                  $("#confirm-fail").show();
                  if (data.data.forward) {
                    window.location.replace(data.data.forward);
                  } else {
                    // window.$Interface.close();
                  }
                } else {
                  $("#confirm-info").hide();
                  $("#confirm-fail").show();
                  clickEnable = false;
                  refreshAble = false;
                  isrobotAble = false;
                  setTimeout(function () {
                    clickEnable = true;
                    refreshAble = true;
                    imageClickAble = true;
                    // $(document).on('click', '#isrobot-info', transformRobot);
                    getImage(server, token);
                  }, 500);
                }
              }
            }
          },
        });
      }
    }
  }
}

$(document).on("click", "#image", imageClick);

function textClickTimeOutFetch() {
  $.ajax({
    url: server + "check_verification_code",
    headers: {
      Authorization: token,
    },
    contentType: "application/json",
    type: "post",
    data: JSON.stringify({
      umark: umark,
      vid: currentVid,
      positions: textClickArr,
      final: retry === 1 ? true : false,
      callback: callback,
      vtype: vtype,
      extra: translate,
      countdown_end: true, // 倒计时参数，只有为true表示倒计时结束，验证失败

    }),
    dataType: "json",
    beforeSend: function (XMLHttpRequest) {
      textClickAble = false;
    },
    success: function (data) {
      if (data.data.status === 5000) {
        timer && clearInterval(timer);
        if (userAgent.indexOf("Unisdk") === -1) {
          alert("连接超时");
          refreshAble = false;
          imageClickAble = false;
        } else {
          window.$Interface.close();
        }
      } else {
        if (data.data.res) {
          timer && clearInterval(timer);
          $("#confirm-result").show();
          $("#confirm-info").hide();
          clickEnable = false;
          refreshAble = false;
          setTimeout(function () {
            if (data.data.forward) {
              window.location.replace(data.data.forward);
            } else {
              window.$Interface.close();
            }
          }, 500);
        } else {
          // retry > 0 && retry--;
          // $("#done-chance").text(retry);
          hideRefreshBtnAfterRetry();
          textClickArr = [];
          // textClickNumber = 3;
          $("#text-click-icon-one").hide();
          $("#text-click-icon-two").hide();
          $("#text-click-icon-three").hide();
          $("#text-click-icon-four").hide();
          $("#text-click-icon-five").hide();
          $("#text-click-icon-six").hide();
          $("#text-click-icon-seven").hide();
          $("#text-click-icon-eight").hide();
          $("#text-click-icon-nine").hide();
          $("#text-click-icon-ten").hide();
          timer && clearInterval(timer);

          clickEnable = false;
          refreshAble = false;
          textClickAble = false;
          $("#confirm-info").hide();
          $("#confirm-fail").show();
          if (data.data.forward) {
            window.location.replace(data.data.forward);
          } else {
            // window.$Interface.close();
          }
          // if (retry === 0) {
          //   timer && clearInterval(timer);
          //   clickEnable = false;
          //   refreshAble = false;
          //   textClickAble = false;
          //   $("#confirm-info").hide();
          //   $("#confirm-fail").show();
          //   if (data.data.forward) {
          //     window.location.replace(data.data.forward);
          //   } else {
          //     // window.$Interface.close();
          //   }
          // } else {
          //   $("#confirm-info").hide();
          //   $("#confirm-fail").show();
          //   clickEnable = false;
          //   refreshAble = false;
          //   setTimeout(function () {
          //     clickEnable = true;
          //     textClickAble = true;
          //     refreshAble = true;
          //     getImage(server, token);
          //   }, 500);
          // }
        }
      }
    },
  });
}

function textClick(e, countdown_end) {
  if (textClickAble) {
    var width = $("#text-click-image").width();
    var height = $("#text-click-image").height();
    if (currentClickNumber < textClickNumber) {
      if (currentClickNumber === 1) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-one").show();
        $("#text-click-icon-one").css("left", x - 13);
        $("#text-click-icon-one").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      } else if (currentClickNumber === 2) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-two").show();
        $("#text-click-icon-two").css("left", x - 13);
        $("#text-click-icon-two").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      } else if (currentClickNumber === 3) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-three").show();
        $("#text-click-icon-three").css("left", x - 13);
        $("#text-click-icon-three").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      } else if (currentClickNumber === 4) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-four").show();
        $("#text-click-icon-four").css("left", x - 13);
        $("#text-click-icon-four").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      } else if (currentClickNumber === 5) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-five").show();
        $("#text-click-icon-five").css("left", x - 13);
        $("#text-click-icon-five").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      } else if (currentClickNumber === 6) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-six").show();
        $("#text-click-icon-six").css("left", x - 13);
        $("#text-click-icon-six").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      } else if (currentClickNumber === 7) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-seven").show();
        $("#text-click-icon-seven").css("left", x - 13);
        $("#text-click-icon-seven").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      } else if (currentClickNumber === 8) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-eight").show();
        $("#text-click-icon-eight").css("left", x - 13);
        $("#text-click-icon-eight").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      } else if (currentClickNumber === 9) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-nine").show();
        $("#text-click-icon-nine").css("left", x - 13);
        $("#text-click-icon-nine").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      }
    } else if (currentClickNumber === textClickNumber) {
      var y = e.offsetY;
      var x = e.offsetX;
      if (currentClickNumber === 1) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-one").show();
        $("#text-click-icon-one").css("left", x - 13);
        $("#text-click-icon-one").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      } else if (currentClickNumber === 2) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-two").show();
        $("#text-click-icon-two").css("left", x - 13);
        $("#text-click-icon-two").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      } else if (currentClickNumber === 3) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-three").show();
        $("#text-click-icon-three").css("left", x - 13);
        $("#text-click-icon-three").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      } else if (currentClickNumber === 4) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-four").show();
        $("#text-click-icon-four").css("left", x - 13);
        $("#text-click-icon-four").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      } else if (currentClickNumber === 5) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-five").show();
        $("#text-click-icon-five").css("left", x - 13);
        $("#text-click-icon-five").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      } else if (currentClickNumber === 6) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-six").show();
        $("#text-click-icon-six").css("left", x - 13);
        $("#text-click-icon-six").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      } else if (currentClickNumber === 7) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-seven").show();
        $("#text-click-icon-seven").css("left", x - 13);
        $("#text-click-icon-seven").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      } else if (currentClickNumber === 8) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-eight").show();
        $("#text-click-icon-eight").css("left", x - 13);
        $("#text-click-icon-eight").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      } else if (currentClickNumber === 9) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-nine").show();
        $("#text-click-icon-nine").css("left", x - 13);
        $("#text-click-icon-nine").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      } else if (currentClickNumber === 9) {
        var y = e.offsetY;
        var x = e.offsetX;
        $("#text-click-icon-ten").show();
        $("#text-click-icon-ten").css("left", x - 13);
        $("#text-click-icon-ten").css("top", y - 32);
        currentClickNumber++;
        textClickArr.push([x / width, y / height]);
      }
      $.ajax({
        url: server + "check_verification_code",
        headers: {
          Authorization: token,
        },
        contentType: "application/json",
        type: "post",
        data: JSON.stringify({
          umark: umark,
          vid: currentVid,
          positions: textClickArr,
          final: retry === 1 ? true : false,
          callback: callback,
          vtype: vtype,
          extra: translate,
        }),
        dataType: "json",
        beforeSend: function (XMLHttpRequest) {
          textClickAble = false;
        },
        success: function (data) {
          if (data.data.status === 5000) {
            timer && clearInterval(timer);
            if (userAgent.indexOf("Unisdk") === -1) {
              alert("连接超时");
              refreshAble = false;
              imageClickAble = false;
            } else {
              window.$Interface.close();
            }
          } else {
            if (data.data.res) {
              timer && clearInterval(timer);
              $("#confirm-result").show();
              $("#confirm-info").hide();
              clickEnable = false;
              refreshAble = false;
              setTimeout(function () {
                if (data.data.forward) {
                  window.location.replace(data.data.forward);
                } else {
                  window.$Interface.close();
                }
              }, 500);
            } else {
              retry > 0 && retry--;
              $("#done-chance").text(retry);
              hideRefreshBtnAfterRetry();
              textClickArr = [];
              // textClickNumber = 3;
              $("#text-click-icon-one").hide();
              $("#text-click-icon-two").hide();
              $("#text-click-icon-three").hide();
              $("#text-click-icon-four").hide();
              $("#text-click-icon-five").hide();
              $("#text-click-icon-six").hide();
              $("#text-click-icon-seven").hide();
              $("#text-click-icon-eight").hide();
              $("#text-click-icon-nine").hide();
              $("#text-click-icon-ten").hide();
              if (retry === 0) {
                timer && clearInterval(timer);
                clickEnable = false;
                refreshAble = false;
                textClickAble = false;
                $("#confirm-info").hide();
                $("#confirm-fail").show();
                if (data.data.forward) {
                  window.location.replace(data.data.forward);
                } else {
                  // window.$Interface.close();
                }
              } else {
                $("#confirm-info").hide();
                $("#confirm-fail").show();
                clickEnable = false;
                refreshAble = false;
                setTimeout(function () {
                  clickEnable = true;
                  textClickAble = true;
                  refreshAble = true;
                  getImage(server, token);
                }, 500);
              }
            }
          }
        },
      });
    }
  } else {
    return;
  }
}

$(document).on("click", "#text-click-image", textClick);

function sliderConfirm(trace, resultX, resultY, countdown_end) {
  // slideClickAble = false;
  slideOutAble = false;
  slideUpAble = false;
  hasMoved = false;
  $.ajax({
    url: server + "check_verification_code",
    headers: {
      Authorization: token,
    },
    contentType: "application/json",
    type: "post",
    data: JSON.stringify({
      umark: umark,
      vid: currentVid,
      px: resultX,
      py: resultY,
      trace: trace,
      final: retry === 1 ? true : false,
      callback: callback,
      vtype: vtype,
      isrobot: isrobot,
      extra: translate,
      countdown_end: countdown_end, // 倒计时参数，只有为true表示倒计时结束，验证失败
    }),
    dataType: "json",
    beforeSend: function (XMLHttpRequest) { },
    success: function (data) {
      if (data.data.status === 5000) {
        timer && clearInterval(timer);
        if (userAgent.indexOf("Unisdk") === -1) {
          alert("连接超时");
          refreshAble = false;
          imageClickAble = false;
          slideClickAble = false;
          slideDownAble = false;
        } else {
          // window.location.replace('unisdk-jsbridge://msg/close');
          window.$Interface.close();
        }
      } else {
        if (data.data.res) {
          timer && clearInterval(timer);
          $("#confirm-result").show();
          $("#confirm-info").hide();
          clickEnable = false;
          refreshAble = false;
          slideClickAble = false;
          slideDownAble = false;
          setTimeout(function () {
            if (data.data.forward) {
              window.location.replace(data.data.forward);
            } else {
              window.$Interface.close();
            }
          }, 500);
        } else {
          if (!countdown_end && retry > 0) {
            retry--;
          }
          $("#done-chance").text(retry);
          hideRefreshBtnAfterRetry();
          if (retry === 0 || countdown_end) {
            timer && clearInterval(timer);
            clickEnable = false;
            slideClickAble = false;
            refreshAble = false;
            slideDownAble = false;
            $("#confirm-info").hide();
            $("#confirm-fail").show();
            if (data.data.forward) {
              window.location.replace(data.data.forward);
            } else {
              // window.$Interface.close();
            }
          } else {
            $("#confirm-info").hide();
            $("#confirm-fail").show();
            clickEnable = false;
            slideClickAble = false;
            refreshAble = true;
            setTimeout(function () {
              clickEnable = true;
              isrobot = 0;
              getImage(server, token);
            }, 500);
          }
        }
      }
    },
  });
}

function puzzleConfirm(e1, e2) {
  puzzleMoveAble = false;
  puzzleUpAble = false;
  if (e1 != e2) {
    $(".puzzle-image")
      .eq(e1)
      .attr("src", "data:image/png;base64," + imgArr[e2]);
    $(".puzzle-image")
      .eq(e2)
      .attr("src", "data:image/png;base64," + imgArr[e1]);
  }

  $("#puzzle-container-hide").hide();
  $.ajax({
    url: server + "check_verification_code",
    headers: {
      Authorization: token,
    },
    contentType: "application/json",
    type: "post",
    data: JSON.stringify({
      umark: umark,
      vid: currentVid,
      final: retry === 1 ? true : false,
      callback: callback,
      vtype: vtype,
      e1: e1,
      e2: e2,
      extra: translate,
    }),
    dataType: "json",
    beforeSend: function (XMLHttpRequest) { },
    success: function (data) {
      if (data.data.status === 5000) {
        timer && clearInterval(timer);
        if (userAgent.indexOf("Unisdk") === -1) {
          alert("连接超时");
          refreshAble = false;
          imageClickAble = false;
        } else {
          // window.location.replace('unisdk-jsbridge://msg/close');
          window.$Interface.close();
        }
      } else {
        if (data.data.res) {
          timer && clearInterval(timer);
          $("#confirm-result").show();
          $("#confirm-info").hide();
          refreshAble = false;
          puzzleClickAble = false;
          puzzleMoveAble = false;
          puzzleUpAble = false;
          setTimeout(function () {
            if (data.data.forward) {
              window.location.replace(data.data.forward);
            } else {
              window.$Interface.close();
            }
          }, 500);
        } else {
          retry > 0 && retry--;
          $("#done-chance").text(retry);
          hideRefreshBtnAfterRetry();
          if (retry === 0) {
            timer && clearInterval(timer);
            refreshAble = false;
            puzzleClickAble = false;
            puzzleMoveAble = false;
            puzzleUpAble = false;
            $("#confirm-info").hide();
            $("#confirm-fail").show();
            if (data.data.forward) {
              window.location.replace(data.data.forward);
            } else {
              // window.$Interface.close();
            }
          } else {
            $("#confirm-info").hide();
            $("#confirm-fail").show();
            refreshAble = false;
            puzzleClickAble = false;
            puzzleMoveAble = false;
            puzzleUpAble = false;
            setTimeout(function () {
              puzzleClickAble = true;
              refreshAble = true;
              getImage(server, token);
            }, 500);
          }
        }
      }
    },
  });
}

var init_left = 0;
var init_top = 0;
var track = [];
var x = 0;
var y = 0;
var mouseX = 0;
var mouseY = 0;
var bg_origin_width = $("#img-content").width();
var bg_origin_height = $("#img-content").height();
// 是否按下，未松开
var keyDown = false;
// 按下鼠标，是否有移动过。默认没有。
var hasMoved = false;

function sliderDown(e) {
  keyDown = true;
  if (slideDownAble) {
    slideClickAble = true;
    slideOutAble = true;
    slideUpAble = true;
    init_left = parseInt($("#slide-image-slider").css("left"));
    init_top = parseInt($("#slide-image-slider").css("top"));
    track = [];
    x = e.clientX;
    y = e.clientY;
    mouseX = e.offsetX;
    mouseY = e.offsetY;
    bg_origin_width = $("#slide-image-bg").width();
    bg_origin_height = $("#slide-image-bg").height();
    e.preventDefault();
  } else {
    return;
  }
}

function sliderTouchDown(e) {
  keyDown = true;
  if (slideDownAble) {
    slideClickAble = true;
    slideOutAble = true;
    slideUpAble = true;
    init_left = parseInt($("#slide-image-slider").css("left"));
    init_top = parseInt($("#slide-image-slider").css("top"));
    track = [];
    x = e.originalEvent.changedTouches[0].clientX;
    y = e.originalEvent.changedTouches[0].clientY;
    mouseX = e.originalEvent.changedTouches[0].pageX;
    mouseY = e.originalEvent.changedTouches[0].pageY;
    console.log(init_top, mouseX);
    bg_origin_width = $("#slide-image-bg").width();
    bg_origin_height = $("#slide-image-bg").height();
    // e.preventDefault();
  } else {
    return;
  }
}
$(document).on("mousedown", "#slide-image-slider", sliderDown);
$(document).on("touchstart", "#slide-image-slider", sliderTouchDown);

function sliderPuzzleMove(e, type) {
  var eventObj = type == "click" ? e : e.originalEvent.changedTouches[0];
  if (vtype === 2) {
    if (keyDown) {
      hasMoved = true;
    }
    if (slideClickAble) {
      var mx1 = eventObj.clientX - x;
      var my1 = eventObj.clientY - y;
      x = eventObj.clientX;
      y = eventObj.clientY;
      init_left += mx1;
      // init_top += my1;
      mouseX += mx1;
      mouseY += my1;
      // e.preventDefault();
      track.push([
        mouseX / bg_origin_width,
        mouseY / bg_origin_height,
        e.timeStamp,
      ]);
      $("#slide-image-slider").css("left", Math.max(init_left, 0));
      if (init_left < 0) {
        init_left = 0;
        // 允许贴着最左边，如果不允许，就用下面这些代码
        // if (slideOutAble) {
        //   sliderConfirm(
        //     track,
        //     init_left / bg_origin_width,
        //     init_top / bg_origin_height
        //   );
        // }
      }
      $("#slide-image-slider").css(
        "left",
        Math.min(bg_origin_width - $("#slide-image-slider").width(), init_left)
      );
      if (init_left > bg_origin_width - $("#slide-image-slider").width()) {
        init_left = bg_origin_width - $("#slide-image-slider").width();
        // 允许贴着最右边，如果不允许，就用下面这些代码
        // if (slideOutAble) {
        //   sliderConfirm(
        //     track,
        //     init_left / bg_origin_width,
        //     init_top / bg_origin_height
        //   );
        // }
      }
      /* if (mouseY > bg_origin_height || mouseY < 0) {
        console.log(mouseY, bg_origin_height);
        if (slideOutAble) {
          sliderConfirm(
            track,
            init_left / bg_origin_width,
            init_top / bg_origin_height
          );
        }
      } */
      /* if (mouseY > bg_origin_width || mouseY < 0) {
        if (slideOutAble) {
          sliderConfirm(
            track,
            init_left / bg_origin_width,
            init_top / bg_origin_height
          );
        }
      } */
    }
  } else if (vtype === 4) {
    if (puzzleMoveAble) {
      var mx1 = eventObj.clientX - x;
      var my1 = eventObj.clientY - y;
      x = eventObj.clientX;
      y = eventObj.clientY;
      init_left += mx1;
      init_top += my1;
      mouseX += mx1;
      mouseY += my1;
      e.preventDefault();
      getCurrentPuzzle(
        mouseX - $("#img-content").offset().left,
        mouseY - $("#img-content").offset().top
      );
      $(".puzzle-image")
        .eq(currentPuzzleDomIndex)
        .attr("src", "data:image/png;base64," + imgArr[puzzleEnd]);
      if (currentPuzzle === puzzleEnd) {
        for (var i = 0; i < puzzleDomCount; i++) {
          $(".cover").eq(i).css("background", "transparent");
        }
        $(".cover")
          .eq(currentPuzzleDomIndex)
          .css("background", "rgb(255,255,255,0.8)");
      } else {
        $(".cover").eq(currentPuzzleDomIndex).css("background", "transparent");
        for (var i = 0; i < puzzleDomCount; i++) {
          $(".cover").eq(i).css("background", "transparent");
        }
        $(".cover").eq(puzzleEndDomIndex).css("background", "rgb(0,0,0,0.4)");
      }

      var puzzleContainerObj = $("#puzzle-container");
      var maxLeft =
        puzzleContainerObj.width() - $("#puzzle-container-hide").width();
      if (init_left < 0) {
        init_left = 0;
      } else if (init_left > maxLeft) {
        init_left = maxLeft;
      }
      $("#puzzle-container-hide").css("left", init_left);

      var maxTop =
        puzzleContainerObj.height() - $("#puzzle-container-hide").height();
      if (init_top < 0) {
        init_top = 0;
      } else if (init_top > maxTop) {
        init_top = maxTop;
      }
      $("#puzzle-container-hide").css("top", init_top);

      // $("#puzzle-container-hide").css("left", Math.max(init_left, 0));
      // $("#puzzle-container-hide").css("top", Math.max(init_top, 0));
      // 因为拼图相对于父元素偏移了，所以计算拼图的位置时需要偏移回来
      if (
        mouseY < puzzleContainerObj.offset().top ||
        mouseY > puzzleContainerObj.offset().top + puzzleContainerObj.height()
      ) {
        if (puzzleUpAble) {
          getCurrentPuzzle(
            mouseX - puzzleContainerObj.offset().left,
            mouseY - puzzleContainerObj.offset().top
          );
          puzzleConfirm(currentPuzzle, puzzleEnd);
        }
      }
    }
  } else {
    return;
  }
}

/* function sliderMove(e) {
  if (vtype === 2) {
    if (slideClickAble) {
      var mx1 = e.clientX - x;
      var my1 = e.clientY - y;
      x = e.clientX;
      y = e.clientY;
      init_left += mx1;
      // init_top += my1;
      mouseX += mx1;
      mouseY += my1;
      e.preventDefault();
      track.push([
        mouseX / bg_origin_width,
        mouseY / bg_origin_height,
        e.timeStamp,
      ]);
      $("#slide-image-slider").css("left", Math.max(init_left, 0));
      if (init_left < 0) {
        init_left = 0;
        if (slideOutAble) {
          sliderConfirm(
            track,
            init_left / bg_origin_width,
            init_top / bg_origin_height
          );
        }
      }
      $("#slide-image-slider").css(
        "left",
        Math.min(bg_origin_width - $("#slide-image-slider").width(), init_left)
      );
      if (init_left > bg_origin_width - $("#slide-image-slider").width()) {
        init_left = bg_origin_width - $("#slide-image-slider").width();
        if (slideOutAble) {
          sliderConfirm(
            track,
            init_left / bg_origin_width,
            init_top / bg_origin_height
          );
        }
      }
      if (mouseY > bg_origin_height || mouseY < 0) {
        if (slideOutAble) {
          sliderConfirm(
            track,
            init_left / bg_origin_width,
            init_top / bg_origin_height
          );
        }
      }
    }
  } else if (vtype === 4) {
    if (puzzleMoveAble) {
      var mx1 = e.clientX - x;
      var my1 = e.clientY - y;
      x = e.clientX;
      y = e.clientY;
      init_left += mx1;
      init_top += my1;
      mouseX += mx1;
      mouseY += my1;
      e.preventDefault();
      getCurrentPuzzle(
        mouseX - $("#img-content").offset().left,
        mouseY - $("#img-content").offset().top
      );
      $(".puzzle-image")
        .eq(currentPuzzleDomIndex)
        .attr("src", "data:image/png;base64," + imgArr[puzzleEnd]);
      if (currentPuzzle === puzzleEnd) {
        for (var i = 0; i < puzzleDomCount; i++) {
          $(".cover").eq(i).css("background", "transparent");
        }
        $(".cover")
          .eq(currentPuzzleDomIndex)
          .css("background", "rgb(255,255,255,0.8)");
      } else {
        $(".cover").eq(currentPuzzleDomIndex).css("background", "transparent");
        for (var i = 0; i < puzzleDomCount; i++) {
          $(".cover").eq(i).css("background", "transparent");
        }
        $(".cover").eq(puzzleEndDomIndex).css("background", "rgb(0,0,0,0.4)");
      }
      if (init_left < 0) {
        init_left = 0;
        $("#puzzle-container-hide").css("left", 0);
      } else if (
        init_left >
        $("#img-content").width() - $("#puzzle-container-hide").width()
      ) {
        init_left =
          $("#img-content").width() - $("#puzzle-container-hide").width();
        $("#puzzle-container-hide").css(
          "left",
          $("#img-content").width() - $("#puzzle-container-hide").width()
        );
      } else {
        $("#puzzle-container-hide").css("left", init_left);
      }
      if (init_top < 0) {
        init_top = 0;
        $("#puzzle-container-hide").css("top", 0);
      } else if (
        init_top >
        $("#img-content").height() - $("#puzzle-container-hide").height()
      ) {
        init_top =
          $("#img-content").height() - $("#puzzle-container-hide").height();
        $("#puzzle-container-hide").css(
          "top",
          $("#img-content").height() - $("#puzzle-container-hide").height()
        );
      } else {
        $("#puzzle-container-hide").css("top", init_top);
      }
      $("#puzzle-container-hide").css("left", Math.max(init_left, 0));
      $("#puzzle-container-hide").css("top", Math.max(init_top, 0));
      if (
        mouseX < $("#img-content").offset().left ||
        mouseX > $("#img-content").offset().left + $("#img-content").width() ||
        mouseY < $("#img-content").offset().top ||
        mouseY > $("#img-content").offset().top + $("#img-content").height()
      ) {
        if (puzzleUpAble) {
          getCurrentPuzzle(
            mouseX - $("#img-content").offset().left,
            mouseY - $("#img-content").offset().top
          );
          puzzleConfirm(currentPuzzle, puzzleEnd);
        }
      }
    }
  } else {
    return;
  }
}

function sliderTouchMove(e) {
  if (vtype === 2) {
    if (slideClickAble) {
      var mx1 = e.originalEvent.changedTouches[0].clientX - x;
      var my1 = e.originalEvent.changedTouches[0].clientY - y;
      x = e.originalEvent.changedTouches[0].clientX;
      y = e.originalEvent.changedTouches[0].clientY;
      init_left += mx1;
      // init_top += my1;
      mouseX += mx1;
      mouseY += my1;
      e.preventDefault();
      track.push([
        mouseX / bg_origin_width,
        mouseY / bg_origin_height,
        e.timeStamp,
      ]);
      if (init_left < 0) {
        $("#slide-image-slider").css("left", 0);
      } else if (
        init_left >
        bg_origin_width - $("#slide-image-slider").width()
      ) {
        init_left = bg_origin_width - $("#slide-image-slider").width();
        $("#slide-image-slider").css(
          "left",
          bg_origin_width - $("#slide-image-slider").width()
        );
      } else {
        $("#slide-image-slider").css("left", init_left);
      }
      $("#slide-image-slider").css("left", Math.max(init_left, 0));
      if (
        mouseX <
        $("#img-content")[0].offsetLeft + $(".container")[0].offsetLeft
      ) {
        init_left = 0;
        if (slideOutAble) {
          sliderConfirm(
            track,
            init_left / bg_origin_width,
            init_top / bg_origin_height
          );
        }
      }
      if (
        mouseX >
        $("#img-content")[0].offsetLeft +
          $(".container")[0].offsetLeft +
          $("#img-content")[0].offsetWidth
      ) {
        init_left = bg_origin_width - $("#slide-image-slider").width();
        if (slideOutAble) {
          sliderConfirm(
            track,
            init_left / bg_origin_width,
            init_top / bg_origin_height
          );
        }
      }
      if (
        mouseY >
          $("#img-content")[0].offsetTop +
            $(".container")[0].offsetTop +
            $("#img-content")[0].offsetHeight ||
        mouseY < $("#img-content")[0].offsetTop + $(".container")[0].offsetTop
      ) {
        if (slideOutAble) {
          sliderConfirm(
            track,
            init_left / bg_origin_width,
            init_top / bg_origin_height
          );
        }
      }
    }
  } else if (vtype === 4) {
    if (puzzleMoveAble) {
      var mx1 = e.originalEvent.changedTouches[0].clientX - x;
      var my1 = e.originalEvent.changedTouches[0].clientY - y;
      x = e.originalEvent.changedTouches[0].clientX;
      y = e.originalEvent.changedTouches[0].clientY;
      init_left += mx1;
      init_top += my1;
      mouseX += mx1;
      mouseY += my1;
      e.preventDefault();
      getCurrentPuzzle(
        mouseX - $("#img-content").offset().left,
        mouseY - $("#img-content").offset().top
      );
      $(".puzzle-image")
        .eq(currentPuzzleDomIndex)
        .attr("src", "data:image/png;base64," + imgArr[puzzleEnd]);
      if (currentPuzzle === puzzleEnd) {
        for (var i = 0; i < puzzleDomCount; i++) {
          $(".cover").eq(i).css("background", "transparent");
        }
        $(".cover")
          .eq(currentPuzzleDomIndex)
          .css("background", "rgb(255,255,255,0.8)");
      } else {
        $(".cover").eq(currentPuzzleDomIndex).css("background", "transparent");
        for (var i = 0; i < puzzleDomCount; i++) {
          $(".cover").eq(i).css("background", "transparent");
        }
        $(".cover").eq(puzzleEndDomIndex).css("background", "rgb(0,0,0,0.4)");
      }
      if (init_left < 0) {
        init_left = 0;
        $("#puzzle-container-hide").css("left", 0);
      } else if (
        init_left >
        $("#img-content").width() - $("#puzzle-container-hide").width()
      ) {
        init_left =
          $("#img-content").width() - $("#puzzle-container-hide").width();
        $("#puzzle-container-hide").css(
          "left",
          $("#img-content").width() - $("#puzzle-container-hide").width()
        );
      } else {
        $("#puzzle-container-hide").css("left", init_left);
      }
      if (init_top < 0) {
        init_top = 0;
        $("#puzzle-container-hide").css("top", 0);
      } else if (
        init_top >
        $("#img-content").height() - $("#puzzle-container-hide").height()
      ) {
        init_top =
          $("#img-content").height() - $("#puzzle-container-hide").height();
        $("#puzzle-container-hide").css(
          "top",
          $("#img-content").height() - $("#puzzle-container-hide").height()
        );
      } else {
        $("#puzzle-container-hide").css("top", init_top);
      }
      if (
        mouseX < $("#img-content").offset().left ||
        mouseX > $("#img-content").offset().left + $("#img-content").width() ||
        mouseY < $("#img-content").offset().top ||
        mouseY > $("#img-content").offset().top + $("#img-content").height()
      ) {
        if (puzzleUpAble) {
          getCurrentPuzzle(
            mouseX - $("#img-content").offset().left,
            mouseY - $("#img-content").offset().top
          );
          puzzleConfirm(currentPuzzle, puzzleEnd);
        }
      }
    }
  } else {
    return;
  }
} */

/* $(document).on("mousemove", "body", sliderMove);
$(document).on("touchmove", "body", sliderTouchMove); */
$(document).on("mousemove", "body", function (e) {
  sliderPuzzleMove(e, "click");
});
$(document).on("touchmove", "body", function (e) {
  sliderPuzzleMove(e, "touch");
});

function slideUp(e) {
  keyDown = false;
  if (hasMoved) {
    if (slideUpAble) {
      sliderConfirm(
        track,
        init_left / bg_origin_width,
        init_top / bg_origin_height
      );
    } else {
      return;
    }
  } else {
    slideClickAble = false;
    hasMoved = false;
  }
}

/* 点击起始拼图 i: 0-7 */
function touchDownPuzzle(i) {
  currentPuzzleDomIndex = i;
  var value = i;
  if (i >= puzzleDomCount / 2) {
    value = i - (puzzleDomCount / 2 - imgArr.length / 2);
  }
  currentPuzzle = value;
  // console.log(i);
  $("#puzzle-hide-image").attr("src", "data:image/png;base64," + imgArr[value]);
}

function getCurrentPuzzle(x, y) {
  /* if (x / bg_origin_width < 0.25 && y / bg_origin_height < 0.5) {
    puzzleEnd = 0;
  } else if (x / bg_origin_width < 0.5 && y / bg_origin_height < 0.5) {
    puzzleEnd = 1;
  } else if (x / bg_origin_width < 0.75 && y / bg_origin_height < 0.5) {
    puzzleEnd = 2;
  } else if (x / bg_origin_width > 0.75 && y / bg_origin_height < 0.5) {
    puzzleEnd = 3;
  }
  if (x / bg_origin_width < 0.25 && y / bg_origin_height > 0.5) {
    puzzleEnd = 4;
  } else if (x / bg_origin_width < 0.5 && y / bg_origin_height > 0.5) {
    puzzleEnd = 5;
  } else if (x / bg_origin_width < 0.75 && y / bg_origin_height > 0.5) {
    puzzleEnd = 6;
  } else if (x / bg_origin_width > 0.75 && y / bg_origin_height > 0.5) {
    puzzleEnd = 7;
  } */
  x -= (imgContentWidth - bg_origin_width) / 2;

  var xOffset = Math.min(
    imgArr.length / 2 - 1,
    Math.max(0, Math.floor((x / bg_origin_width) * (imgArr.length / 2)))
  );
  if (xOffset < imgArr.length / 2) {
    if (y / bg_origin_height < 0.5) {
      puzzleEndDomIndex = xOffset;
      puzzleEnd = xOffset;
    } else {
      puzzleEndDomIndex = xOffset + puzzleDomCount / 2;
      puzzleEnd = xOffset + imgArr.length / 2;
    }
  }
  // console.log(puzzleEnd, puzzleEndDomIndex);
}

function puzzleTouch(e, type) {
  init_left = parseInt(
    $(".puzzle-single-container").eq(currentPuzzleDomIndex).css("left")
  );
  init_top = parseInt(
    $(".puzzle-single-container").eq(currentPuzzleDomIndex).css("top")
  );
  $("#puzzle-container-hide").css("left", init_left);
  $("#puzzle-container-hide").css("top", init_top);
  $("#puzzle-container-hide").show();
  bg_origin_width = $("#puzzle-container").width();
  bg_origin_height = $("#puzzle-container").height();
  e.preventDefault();
  if (type == "click") {
    x = e.clientX;
    y = e.clientY;
    mouseX = e.pageX;
    mouseY = e.pageY;
  } else {
    x = e.originalEvent.changedTouches[0].clientX;
    y = e.originalEvent.changedTouches[0].clientY;
    mouseX = e.originalEvent.changedTouches[0].pageX;
    mouseY = e.originalEvent.changedTouches[0].pageY;
  }
}
/* function puzzleDown(e) {
  init_left = parseInt(
    $(".puzzle-single-container").eq(currentPuzzle).css("left")
  );
  init_top = parseInt(
    $(".puzzle-single-container").eq(currentPuzzle).css("top")
  );
  $("#puzzle-container-hide").css("left", init_left);
  $("#puzzle-container-hide").css("top", init_top);
  $("#puzzle-container-hide").show();
  x = e.clientX;
  y = e.clientY;
  mouseX = e.pageX;
  mouseY = e.pageY;
  bg_origin_width = $("#puzzle-container").width();
  bg_origin_height = $("#puzzle-container").height();
  e.preventDefault();
}

function puzzleTouchDown(e) {
  init_left = parseInt(
    $(".puzzle-single-container").eq(currentPuzzle).css("left")
  );
  init_top = parseInt(
    $(".puzzle-single-container").eq(currentPuzzle).css("top")
  );
  $("#puzzle-container-hide").css("left", init_left);
  $("#puzzle-container-hide").css("top", init_top);
  $("#puzzle-container-hide").show();
  x = e.originalEvent.changedTouches[0].clientX;
  y = e.originalEvent.changedTouches[0].clientY;
  mouseX = e.originalEvent.changedTouches[0].pageX;
  mouseY = e.originalEvent.changedTouches[0].pageY;
  bg_origin_width = $("#puzzle-container").width();
  bg_origin_height = $("#puzzle-container").height();
  e.preventDefault();
} */

for (var i = 0; i < puzzleDomCount; i++) {
  (function (index) {
    $(".puzzle-single-container")
      .eq(index)
      .on("mousedown", function (e) {
        if (puzzleClickAble) {
          puzzleClickAble = false;
          puzzleMoveAble = true;
          puzzleUpAble = true;
          /* currentPuzzle = i;
          $("#puzzle-hide-image").attr(
            "src",
            "data:image/png;base64," + imgArr[i]
          ); */
          touchDownPuzzle(index);
          // puzzleDown(e);
          puzzleTouch(e, "click");
        } else {
          return;
        }
      });
  })(i);

}

for (var i = 0; i < puzzleDomCount; i++) {
  (function (index) {
    $(".puzzle-single-container")
      .eq(index)
      .on("touchstart", function (e) {
        if (puzzleClickAble) {
          puzzleClickAble = false;
          puzzleMoveAble = true;
          puzzleUpAble = true;
          /* currentPuzzle = i;
          $("#puzzle-hide-image").attr(
            "src",
            "data:image/png;base64," + imgArr[i]
          ); */
          touchDownPuzzle(index);
          // puzzleTouchDown(e);
          puzzleTouch(e, "touch");
        } else {
          return;
        }
      });
  })(i);

}

$(document).on("mouseup", function (e) {
  if (vtype === 4) {
    if (puzzleUpAble) {
      getCurrentPuzzle(
        mouseX - $("#img-content").offset().left,
        mouseY - $("#img-content").offset().top
      );
      if (currentPuzzle === puzzleEnd) {
        puzzleMoveAble = false;
        puzzleUpAble = false;
        puzzleClickAble = true;
        refreshAble = true;
        $("#puzzle-container-hide").hide();
        $(".cover").eq(currentPuzzleDomIndex).css("background", "transparent");
      } else {
        puzzleConfirm(currentPuzzle, puzzleEnd);
      }
    }
  } else {
    slideUp(e);
  }
});

$(document).on("touchend", function (e) {
  if (vtype === 4) {
    if (puzzleUpAble) {
      getCurrentPuzzle(
        mouseX - $("#img-content").offset().left,
        mouseY - $("#img-content").offset().top
      );
      if (currentPuzzle === puzzleEnd) {
        puzzleMoveAble = false;
        puzzleUpAble = false;
        puzzleClickAble = true;
        refreshAble = true;
        $("#puzzle-container-hide").hide();
        $(".cover").eq(currentPuzzleDomIndex).css("background", "transparent");
      } else {
        puzzleConfirm(currentPuzzle, puzzleEnd);
      }
    }
  } else {
    slideUp(e);
  }
});
