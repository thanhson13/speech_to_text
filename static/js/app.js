$(function() {
    let shouldStop = false;
    let stopped = false;
    const startButton = document.getElementById('start');
    const stopButton = document.getElementById('stop');

    startButton.addEventListener('click', function() {
        console.log('start');
        shouldStop = false;
        stopped = false;
        navigator.mediaDevices.getUserMedia({ audio: true, video: false })
            .then(handleSuccess);
    });

    stopButton.addEventListener('click', function() {
        console.log('stop');
        shouldStop = true;
    });

    const handleSuccess = function(stream) {
        const options = {mimeType: 'audio/webm'};
        const recordedChunks = [];
        const mediaRecorder = new MediaRecorder(stream, options);

        mediaRecorder.ondataavailable = function(e) {
            if (e.data.size > 0) {
                console.log('recording');
                recordedChunks.push(e.data);
            }

            if(shouldStop === true && stopped === false) {
                console.log('stop recording');
                mediaRecorder.stop();
                stopped = true;
            }
        };
        mediaRecorder.onstart = function() {
            console.log("start recording");
        };
        mediaRecorder.onstop = function() {
            console.log("stop recording");
            let blob = new Blob(recordedChunks);
            $.ajax({
                type: 'POST',
                url: '/upload',
                data: blob,
                processData: false,
                contentType: false
            }).done(function(data) {
                console.log(data);
            });
        };
        mediaRecorder.start(500);
    };

});