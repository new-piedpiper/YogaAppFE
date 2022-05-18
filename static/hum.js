var video=document.querySelector('#videoEl');
let canvas = document.querySelector("#canvasElement");
let ctx= canvas.getContext('2d')
function accam(){
navigator.mediaDevices.getUserMedia({video: true}).then(function (stream){
        video.srcObject=stream;
        localMediaStream=stream;
        video.play();
        setInterval(
            function(){
                sendSnapshot();
            },50
        );
    }).catch(function(err){
        console.log(err.name+':'+err.message);
    });
}

function Vidstop(e) {
    var stream = video.srcObject;
    var tracks = stream.getTracks();  
    for (var i = 0; i < tracks.length; i++) {
        var track = tracks[i];
        track.stop();
    } 
    video.srcObject = null;
}

function sendSnapshot() {
    if (!localMediaStream) {
      return;
    }

    ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);

    let dataURL = canvas.toDataURL('image/jpeg');
    ws.emit('input image', dataURL);

    ws.emit('output image')

    var img = new Image();
    ws.on('out-image-event',function(data){


    img.src = dataURL//data.image_data
    photo.setAttribute('src', data.image_data);

    });


  }


var ws=io();

ws.on('connect',function(){
        alert("Connected to server");
    });
    
ws.on('connect_error',function(){
        alert("Could not connect to server");
    });