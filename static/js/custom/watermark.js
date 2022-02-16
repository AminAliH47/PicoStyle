/**
 *Picture path to canvas
 *@ param {image URL} URL
 */
async function imgToCanvas(url) {
  //Create img element
  const img = document.createElement("img");
  img.src = url;
  img.setAttribute ("crossorigin", "anonymous"); // prevent failed to execute 'todataurl' on 'htmlcanvas element' caused by cross domain: tainted canvas may not be exported
  await new Promise((resolve) => (img.onload = resolve));
  //Create the canvas DOM element and set its width and height to be the same as the picture
  const canvas = document.createElement("canvas");
  canvas.width = img.width;
  canvas.height = img.height;
  //The coordinates (0,0) indicate that the drawing starts from here and is equivalent to an offset.
  canvas.getContext("2d").drawImage(img, 0, 0);
  return canvas;
}

/**
 *Add watermark to canvas
 *@ param {canvas object} canvas
 *@ param {watermark text} text
 */
function addWatermark(canvas, text) {
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = "red";
  ctx.textBaseline = "middle";
  ctx.fillText(text, 20, 20);
  return canvas;
}

/**
 *Convert canvas to img
 *@ param {canvas object} canvas
 */
function convasToImg(canvas) {
  //Create a new image object, which can be understood as dom
  var image = new Image();
  // canvas.toDataURL  It returns a string of Base64 encoded URLs
  //Specified format png
  image.src = canvas.toDataURL("image/png");
  return image;
}

//Running examples
async function run() {
  const imgUrl =
    "https://imgs.developpaper.com/imgs/test.jpg";
  //1. Convert the image path to canvas
  const tempCanvas = await imgToCanvas(imgUrl);
  //2. Add watermark to canvas
  const canvas = addWatermark(tempCanvas, "zpfei.ink");
  //3. Convert canvas to img
  const img = convasToImg(canvas);
  //View effects
  document.body.appendChild(img);
}