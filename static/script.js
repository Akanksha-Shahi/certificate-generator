let templateImg = null;
let fontFace = null;

const canvas = document.getElementById("certificateCanvas");
const ctx = canvas.getContext("2d");

document.getElementById("templateUpload").addEventListener("change", (e) => {
  const file = e.target.files[0];
  const reader = new FileReader();
  reader.onload = (event) => {
    templateImg = new Image();
    templateImg.onload = () => {
      canvas.width = templateImg.width;
      canvas.height = templateImg.height;
      drawCertificate();
    };
    templateImg.src = event.target.result;
  };
  reader.readAsDataURL(file);
});

document.getElementById("fontUpload").addEventListener("change", (e) => {
  const file = e.target.files[0];
  const reader = new FileReader();
  reader.onload = (event) => {
    fontFace = new FontFace("Allura", event.target.result);
    fontFace.load().then((loaded) => {
      document.fonts.add(loaded);
      drawCertificate();
    });
  };
  reader.readAsArrayBuffer(file);
});

document.getElementById("nameInput").addEventListener("input", drawCertificate);

function drawCertificate() {
  if (!templateImg) return;

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(templateImg, 0, 0);

  const name = document.getElementById("nameInput").value;
  if (name && fontFace) {
    ctx.font = "100px Allura";
    ctx.fillStyle = "black";
    ctx.textAlign = "center";
    ctx.fillText(name, canvas.width / 2, 620); // vertical Y fixed at 620
  }
}

document.getElementById("downloadBtn").addEventListener("click", () => {
  const link = document.createElement("a");
  link.download = "certificate.png";
  link.href = canvas.toDataURL("image/png");
  link.click();
});
