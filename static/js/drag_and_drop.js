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
        outputZone.querySelector(".output-zone__h3").innerText = "YOUR OUTPUTTED FILE SHOULD BE DOWNLOADING SOON...";
    }
}

function onClick(chosen) {
    //chosen true when encrypt
    //chosen false when decrypt

    //files[0] is how you can access the file.

    if (files[0]) {
        overrideThumbnailOutput(files[0]);

        if (chosen == true) {
            document.querySelector(".submit-form").submit();
            //encryption file and prompt download
        } else if (chosen == false) {
            document.querySelector(".submit-form").submit();
            //decryption file and prompt download
        }
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
