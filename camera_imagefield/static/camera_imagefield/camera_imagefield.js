document.addEventListener("DOMContentLoaded", function() {
    function setupField(field) {
        var img = null;

        function startCapture(ev) {
            var video = document.createElement("video");
            video.autoplay = true;
            field.appendChild(video);
            var constraints = {

                video: { width: 1280, height: 720 }
            };

            function handleSuccess(stream) {
                function close() {
                    field.removeChild(video);
                    field.removeChild(cancelButton);
                    field.removeChild(captureButton);
                    field.removeChild(captureDelayButton);
                    var tracks = stream.getTracks();
                    for (var i = 0; i < tracks.length; i++) tracks[i].stop();
                    stream = null;

                }

                video.src = window.URL.createObjectURL(stream);

                var cancelButton = document.createElement("i");
                cancelButton.classList.add("fa");
                cancelButton.classList.add("fa-times");
                cancelButton.classList.add("cancel-capture");
                cancelButton.setAttribute("role", "button");
                cancelButton.title = "Cancel";
                field.appendChild(cancelButton);

                var captureButton = document.createElement("i");
                captureButton.classList.add("fa");
                captureButton.classList.add("fa-camera");
                captureButton.classList.add("do-capture");
                captureButton.setAttribute("role", "button");
                captureButton.title = "Take photo";
                field.appendChild(captureButton);

                var captureDelayButton = document.createElement("i");
                captureDelayButton.classList.add("fa");
                captureDelayButton.classList.add("fa-history");
                captureDelayButton.classList.add("do-capture-delay");
                captureDelayButton.setAttribute("role", "button");
                captureDelayButton.title = "Take photo after 3 second delay";
                field.appendChild(captureDelayButton);



                cancelButton.addEventListener("click", function() {
                    close();
                });

                captureButton.addEventListener("click", function() {
                    var width = video.videoWidth, height = video.videoHeight;
                    if (img == null) {
                        img = document.createElement("img");
                        img.setAttribute("class", "captured-image");
                        field.appendChild(img);
                    }
                    var canvas = document.createElement("canvas");
                    canvas.setAttribute("width", width);
                    canvas.setAttribute("height", height);
                    canvas.style.display = "none";
                    field.appendChild(canvas);

                    var context = canvas.getContext('2d');
                    context.drawImage(video, 0, 0, width, height);
                    dataInput.value = img.src = canvas.toDataURL("image/png");
                    console.log(dataInput.value.length);
                    close();
                })
            }

            function handleError(error) {
                field.removeChild(video);
                console.log("denied");
            }

            navigator.mediaDevices.getUserMedia(constraints).
            then(handleSuccess).catch(handleError);
            ev.preventDefault();
        }

        field.addEventListener("drop", function(ev) {
            ev.preventDefault();
            console.log("dropped", arguments);
        });
        field.querySelector("input").style.display = "none";

        var dataInput = document.createElement("input");
        dataInput.type = "hidden";
        dataInput.name = field.getAttribute("data-name") + '_data';
        field.appendChild(dataInput);

        var buttonsDiv = document.createElement("div");
        buttonsDiv.classList.add('buttons');

        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            var cameraButton = document.createElement("button");
            var cameraButtonI = document.createElement("i");
            cameraButtonI.textContent = " ";
            cameraButtonI.setAttribute("class", "fa fa-fw fa-camera");
            cameraButton.appendChild(cameraButtonI);
            buttonsDiv.appendChild(cameraButton);

            cameraButton.addEventListener("click", startCapture);
        }

        var uploadButton = document.createElement("button");
        var uploadButtonI = document.createElement("i");
        uploadButtonI.textContent = " ";
        uploadButtonI.classList.add("fa");
        uploadButtonI.classList.add("fa-fw");
        uploadButtonI.classList.add("fa-upload");
        uploadButton.appendChild(uploadButtonI);
        buttonsDiv.appendChild(uploadButton);
        uploadButton.addEventListener("click", function(ev) { field.querySelector("input").click(ev); ev.preventDefault(); });

        field.appendChild(buttonsDiv);
    }

    var fields = document.getElementsByClassName("camera-imagefield");
    for (var i = 0; i < fields.length; i++) {
        setupField(fields.item(i));
    }
});