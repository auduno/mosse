// various utility functions

// requestAnimationFrame shim
(function() {
    var lastTime = 0;
    var vendors = ['ms', 'moz', 'webkit', 'o'];
    for(var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
        window.requestAnimationFrame = window[vendors[x]+'RequestAnimationFrame'];
        window.cancelRequestAnimationFrame = window[vendors[x]+
          'CancelRequestAnimationFrame'];
    }

    if (!window.requestAnimationFrame)
        window.requestAnimationFrame = function(callback, element) {
            var currTime = new Date().getTime();
            var timeToCall = Math.max(0, 16 - (currTime - lastTime));
            var id = window.setTimeout(function() { callback(currTime + timeToCall); }, 
              timeToCall);
            lastTime = currTime + timeToCall;
            return id;
        };

    if (!window.cancelAnimationFrame)
        window.cancelAnimationFrame = function(id) {
            clearTimeout(id);
        };
}());

navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
window.URL = window.URL || window.webkitURL || window.msURL || window.mozURL;

// video support utility functions
			
function supports_video() {
    return !!document.createElement('video').canPlayType;
}

function supports_h264_baseline_video() {
    if (!supports_video()) { return false; }
    var v = document.createElement("video");
    return v.canPlayType('video/mp4; codecs="avc1.42E01E, mp4a.40.2"');
}

function supports_ogg_theora_video() {
    if (!supports_video()) { return false; }
    var v = document.createElement("video");
    return v.canPlayType('video/ogg; codecs="theora, vorbis"');
}

// utility function to get data from canvas at arbitrary rotation

var getData = function(source, leftTop, rightTop, leftBottom, rightBottom, targetWidth, targetHeight) {
    // create new canvas to copy to
    //var sketchCC = document.createElement("canvas");
    var sketch = document.getElementById('target');
    sketch.setAttribute("width", targetWidth);
    sketch.setAttribute("height", targetHeight);
    var sketchCC = sketch.getContext('2d');
    
    // find midpoint
    var translateX = (leftTop[0]+rightTop[0]+leftBottom[0]+rightBottom[0])/4;
    var translateY = (leftTop[1]+rightTop[1]+leftBottom[1]+rightBottom[1])/4;
    
    // rotation
    var A = rightBottom[0]-leftBottom[0];
    var B = rightBottom[1]-leftBottom[1];
    var C = leftBottom[0]-leftTop[0];
    var D = leftBottom[1]-leftTop[1];
    
    if (A > 0 && B > 0) {
        var rotation = Math.atan(B/A);
    } else if (A > 0 && B == 0) {
        var rotation = 0;
    } else if (A > 0 && B < 0) {
        var rotation = Math.atan(B/A);
    } else if (A == 0 && B > 0) {
        var rotation = Math.PI/2;
    } else if (A == 0 && B < 0) {
        var rotation = -Math.PI/2
    } else if (A < 0 && B > 0) {
        var rotation = Math.atan(B/A)+Math.PI;
    } else if (A < 0 && B == 0) {
        var rotation = Math.PI;
    } else if (A < 0 && B < 0) {
        var rotation = Math.atan(B/A)+Math.PI;
    }

    // scaling
    var swidth = sketch.width/Math.sqrt((A*A)+(B*B));
    var sheight = sketch.height/Math.sqrt((C*C)+(D*D));
    
    // do transformations
    sketchCC.save();
    sketchCC.clearRect(0, 0, sketch.width, sketch.height);
    sketchCC.scale(swidth, sheight);
    sketchCC.rotate(-rotation);
    sketchCC.translate(-leftTop[0], -leftTop[1]);
    
    // drawImage
    sketchCC.drawImage(source, 0, 0, source.width, source.height);
    
    sketchCC.restore();
    
    // getImageData from canvas
    var id = sketchCC.getImageData(0, 0, sketch.width, sketch.height);
    return id
}