const droparea = document.querySelector('.dropContainer div');

droparea.addEventListener("dragover", (e)=> {
    e.preventDefault();
    droparea.classList.add("hover");
});

droparea.addEventListener("dragleave", ()=> {
    droparea.classList.remove("hover");
});

droparea.addEventListener("drop", (e)=>{
    e.preventDefault();

    const file = e.dataTransfer.files[0];
    const type = file.type;

    return upload(file);
});

const upload = (file) => {
    droparea.innerText = "Added " + file.name;
};