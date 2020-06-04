const canvas = document.querySelector("#canvas");
const submitButton = document.querySelector("#submit");
const ctx = canvas.getContext("2d");
axios.defaults.baseURL = "http://localhost:5000";
canvas.height = 280;
canvas.width = 280;
ctx.strokeStyle = "white";
ctx.lineWidth = 15;
let drawing = false;

function dataURLtoFile(dataurl, filename) {
  var arr = dataurl.split(","),
    mime = arr[0].match(/:(.*?);/)[1],
    bstr = atob(arr[1]),
    n = bstr.length,
    u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  return new File([u8arr], filename, { type: mime });
}

const getPostion = (e) => {
  let rect = canvas.getBoundingClientRect();
  let posX = e.clientX - rect.left;
  let posY = e.clientY - rect.top;
  return [posX, posY];
};

const handleMouseDown = (e) => {
  [clientX, clientY] = getPostion(e);
  drawing = true;
  ctx.beginPath();
  ctx.moveTo(clientX, clientY);
};

const handleMouseMove = (e) => {
  if (drawing) {
    [clientX, clientY] = getPostion(e);
    ctx.lineTo(clientX, clientY);
    ctx.stroke();
  }
};

const handleMouseUp = (e) => {
  [clientX, clientY] = getPostion(e);
  drawing = false;
};

const handleClick = (e) => {
  ctx.beginPath();
  ctx.moveTo(e.clientX, e.clientY);
};

const handleSubmit = (event) => {
  event.preventDefault();
  const url = "/predict";
  newObject = { file: canvas.toDataURL("image/jpeg") };
  let file = dataURLtoFile(newObject.file, "temp.jpg");
  var bodyFormData = new FormData();
  bodyFormData.append("file", file);
  axios({
    method: "post",
    url: url,
    data: bodyFormData,
    headers: { "Content-Type": "multipart/form-data" },
  })
    .then((res) => {
      console.log(res);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    })
    .catch((err) => console.log(err));
};

canvas.addEventListener("mousedown", handleMouseDown);
canvas.addEventListener("mousemove", handleMouseMove);
canvas.addEventListener("mouseup", handleMouseUp);
