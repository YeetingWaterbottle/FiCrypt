//DRAG AND DROP
var files = [];
var outputZone = null;

document.querySelectorAll(".output-zone__h3").forEach((inputElement) => {
    outputZone = inputElement.closest(".output_zone");
});

document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");

    dropZoneElement.addEventListener("click", (e) => {
        inputElement.click();
    });

    inputElement.addEventListener("change", (e) => {
        if (inputElement.files.length) {
            updateThumbnail(dropZoneElement, inputElement.files[0]);
        }
    });

    dropZoneElement.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZoneElement.classList.add("drop-zone--over");
    });

    ["dragleave", "dragend"].forEach((type) => {
        dropZoneElement.addEventListener(type, (e) => {
            dropZoneElement.classList.remove("drop-zone--over");
        });
    });

    dropZoneElement.addEventListener("drop", (e) => {
        e.preventDefault();

        if (e.dataTransfer.files.length) {
            inputElement.files = e.dataTransfer.files;
            updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
        }

        dropZoneElement.classList.remove("drop-zone--over");
    });
});

/**
 * Updates the thumbnail on a drop zone element.
 *
 * @param {HTMLElement} dropZoneElement
 * @param {File} file
 */
function updateThumbnail(dropZoneElement, file) {
    files = [];
    files.push(file);

    let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

    // First time - remove the prompt
    if (dropZoneElement.querySelector(".drop-zone__prompt")) {
        dropZoneElement.querySelector(".drop-zone__prompt").remove();
    }

    // First time - there is no thumbnail element, so lets create it
    if (!thumbnailElement) {
        thumbnailElement = document.createElement("div");
        thumbnailElement.classList.add("drop-zone__thumb");
        dropZoneElement.appendChild(thumbnailElement);
    }

    thumbnailElement.dataset.label = file.name;

    // Show thumbnail for image files
    if (file.type.startsWith("image/")) {
        const reader = new FileReader();

        reader.readAsDataURL(file);
        reader.onload = () => {
            thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
        };
    } else {
        thumbnailElement.style.backgroundImage = null;
    }
}

// function downloadFile(file) {
//     // Create a link and set the URL using `createObjectURL`
//     const link = document.createElement("a");
//     link.style.display = "none";
//     link.href = URL.createObjectURL(file);
//     link.download = file.name;

//     // It needs to be added to the DOM so it can be clicked
//     document.body.appendChild(link);
//     link.click();

//     // To make this work on Firefox we need to wait
//     // a little while before removing it.
//     setTimeout(() => {
//         URL.revokeObjectURL(link.href);
//         link.parentNode.removeChild(link);
//     }, 0);
// }

//POPUP DARK BACKGROUND

function overrideThumbnailOutput(file) {
    let thumbnailElement = outputZone.querySelector(".output-zone__thumb");

    if (outputZone.querySelector(".output-zone__prompt")) {
        outputZone.querySelector(".output-zone__prompt").remove();
        outputZone.querySelector(".output-zone__h3").innerText = "THE FILE IS BEING ENCRYPTED, THIS MIGHT TAKE A FEW SECONDS. FILE SIZE WILL AFFECT THE TIME REQUIRED FOR THIS PROCESS...";
        // outputZone.querySelector(".output-zone__h3").innerText = "THE ENCRYPTED FILE SHOULD BE PROMPTED FOR DOWNLOAD SOON...";
    }
}

function update_progress() {
    fetch("/progress")
        .then((response) => response.json())
        .then((progress) => {
            document.querySelector(".meter-1").style.strokeDashoffset = 240 - progress[0] * 2.4; // 240 will make the progress circle empty, as the value decreases, the circle gets filled little by little.
            outputZone.querySelector(".output-zone__h3").innerText = progress[1];
            
            if (progress[0] == 100) {
                return "finished";
            }
            setTimeout(update_progress, 1000);
        });
    // .catch((error) => console.log(error));
}

function onClick(chosen) {
    //chosen true when encrypt
    //chosen false when decrypt

    //files[0] is how you can access the file.

    if (files[0]) {
        overrideThumbnailOutput(files[0]);
        let submit_form = document.querySelector(".submit-form");
        let password = prompt("Enter The File Password: ");

        while (password.length <= 0) {
            password = prompt("Enter The File Password: ");
        }

        // hash the password with sha256
        password = CryptoJS.SHA256(password).toString();

        if (chosen == true) {
            submit_form.children["file_password"].value = password;
            submit_form.children["file_action"].value = "en";
            submit_form.submit();
            //encryption file and prompt download
        } else if (chosen == false) {
            submit_form.children["file_password"].value = password;
            submit_form.children["file_action"].value = "de";
            submit_form.submit();
            //decryption file and prompt download
        }

        document.querySelector(".meter-1").style.strokeDashoffset = 240;
        document.querySelector(".bg").style.display = "block";

        update_progress();
    } else {
        alert("Please upload a file first!");
    }
}

const button1 = document.getElementsByClassName("EncryptB")[0];
const button2 = document.getElementsByClassName("DecryptB")[0];

if (button1) {
    button1.addEventListener("click", () => {
        onClick(true);
    });
}

if (button2) {
    button2.addEventListener("click", () => {
        onClick(false);
    });
}
