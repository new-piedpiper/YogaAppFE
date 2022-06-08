var video=document.querySelector('#videoEl');
let canvas = document.querySelector("#canvasElement");
let ctx= canvas.getContext('2d')
Ps=document.getElementById('Pose')
Cr=document.getElementById('Correction')
var ws;

function accam(){
navigator.mediaDevices.getUserMedia({video: true}).then(function (stream){
        video.srcObject=stream;
        localMediaStream=stream;
        video.play();
        setInterval(
            function(){
                sendSnapshot();
            },5000
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
    console.log(video.videoHeight,video.videoWidth);
    ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);

    let dataURL = canvas.toDataURL('image/jpeg');
    ws.emit('input image', dataURL);
  }

ws=io();

ws.on('connect',function(){
        alert("Connected to server");
    });
    
ws.on('connect_error',function(){
        alert("Could not connect to server");
    });

ws.on('Answer_Response',(Pose)=>{
        Ps.innerText=Pose.Pose
        console.log(Pose.Pose)
        });