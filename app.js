const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("pdf-file");
const summarizeBtn = document.getElementById("summarize-btn");
const progress = document.getElementById("progress");
const result = document.getElementById("result");

let uploadedFile = null;

// Drag & Drop
dropZone.addEventListener("dragover", e => {
    e.preventDefault();
    dropZone.style.opacity = "0.7";
});

dropZone.addEventListener("dragleave", () => {
    dropZone.style.opacity = "1";
});

dropZone.addEventListener("drop", e => {
    e.preventDefault();
    uploadedFile = e.dataTransfer.files[0];
    dropZone.innerHTML = `✅ ${uploadedFile.name}`;
});

// File select
fileInput.addEventListener("change", e => {
    uploadedFile = e.target.files[0];
    dropZone.innerHTML = `✅ ${uploadedFile.name}`;
});

// Summarize
summarizeBtn.addEventListener("click", async () => {
    if (!uploadedFile) {
        alert("Upload a PDF first!");
        return;
    }

    const length = document.getElementById("summary-length").value;
    const formData = new FormData();
    formData.append("file", uploadedFile);
    formData.append("length", length);

    progress.classList.remove("hidden");
    result.classList.add("hidden");

    const response = await fetch("/summarize", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    document.getElementById("title").innerText = data.title;
    document.getElementById("executive-summary").innerText = data.executive_summary;
    document.getElementById("key-points").innerText = data.key_points;
    document.getElementById("important-concepts").innerText = data.important_concepts;
    document.getElementById("final-takeaway").innerText = data.final_takeaway;

    progress.classList.add("hidden");
    result.classList.remove("hidden");
});

// Dark mode
document.getElementById("dark-toggle").onclick = () => {
    document.body.classList.toggle("dark");
};

// Download TXT
document.getElementById("download-txt").onclick = () => {
    const text = document.getElementById("result").innerText;
    const blob = new Blob([text], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "summary.txt";
    link.click();
};
