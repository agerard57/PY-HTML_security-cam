function initial(detect, log, stream, record, jalert){
    document.getElementById("detection").value = detect;
    document.getElementById("loglvl").value = log;
    document.getElementById("streaming").value = stream;
    document.getElementById("recording").value = record;
    document.getElementById("alerting").value = jalert;
    if (stream == "Off"){
        document.getElementById("fluximage").style.display = "none";
        console.log("ca marche")
    }
}
function returnLive(stream){
    if (stream == "On"){
        document.getElementById("fluximage").style.display = "block";
        document.getElementById("fluximage").src = "{{ url_for('video_feed') }}"
        location.reload();
    }
    else{
       alert("Vidéo live désactivée")
    }

}
function fvideo(event){
    const newsrc = event.src.substring(0,event.src.lastIndexOf("."))
    document.getElementById("fluxvideo").style.display = "block";
    document.getElementById("fluximage").style.display = "none";
    document.getElementById("fluxvideo").src = newsrc + ".avi";

}