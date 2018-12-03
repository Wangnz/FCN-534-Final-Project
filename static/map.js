function loadMap() {
    let map = new Image();
    map.src = "/static/sdraft3.png";
    map.onload = () => {
      console.log(map.width, map.height);
      start(map);
    };
}

function ImageWrapper(x, y, image, pixelRatio) {
  this.x = x;
  this.y = y;
  this.w = image.width / pixelRatio;
  this.h = image.height / pixelRatio;
  this.image = image;

  this.coffx = 0;
  this.coffy = 0;
}

function start(map) {;
  let cnvs = document.createElement("canvas"),
      ctx = cnvs.getContext("2d"),

      // canvas width & height
      w = window.innerWidth,
      h = window.innerHeight,

      // canvas context translations
      tx = w / 2.0,
      ty = h / 2.0;

  let pr = (() =>{
    var ctx = document.createElement("canvas").getContext("2d"),
        dpr = window.devicePixelRatio || 1,
        bsr = ctx.webkitBackingStorePixelRatio || ctx.mozBackingStorePixelRatio ||
              ctx.msBackingStorePixelRatio || ctx.oBackingStorePixelRatio || ctx.backingStorePixelRatio || 1;
    return dpr / bsr;
  })();

  console.log("pr", pr);
  cnvs.setAttribute("width"  , w * pr);
  cnvs.setAttribute("height" , h * pr);
  cnvs.style.width  = w + "px";
  cnvs.style.height = h + "px";
  
  document.body.appendChild(cnvs);

  ctx.setTransform(pr, 0, 0, pr, 0, 0);
  ctx.translate(tx, ty);

  map = new ImageWrapper(0, 0, map, pr);
  map.x = -map.w / 2;
  map.y = -map.h / 2;
  map.coffx = 237;
  map.coffy = 511;

  let requireUpdate = true,
      data = undefined;

  let point = {
    x: 0,
    y: 0,
  };

  let context = {
    scale : 1.0,
    pixPerMeter: 11.0778,
    offx: 0,
    offy: 0,
    dragStart: {
      x: 0,
      y: 0,
    },
    dragging: false,
  };

  document.body.addEventListener("mousedown", (e) => {
    context.dragStart.x = e.clientX - tx;
    context.dragStart.y = e.clientY - ty;
    context.dragging = true;
  });

  document.body.addEventListener("mousemove", (e) => {
    if(!context.dragging)
      return;

    let x = e.clientX - tx,
        y = e.clientY - ty;

    context.offx += x - context.dragStart.x;
    context.offy += y - context.dragStart.y;

    context.dragStart.x = x;
    context.dragStart.y = y;
    draw();
  });

  document.body.addEventListener("mouseup", (e) => {
    context.dragging = false;
  });

  document.body.addEventListener("mousewheel", (e) => {
    context.scale += e.deltaY / 5000;
    if(context.scale < 0.5)
      context.scale = 0.5;

    if(context.scale > 3.0)
      context.scale = 3.0;

    draw();
  }, { capture: true, passive: true});

  let routerMap = {};
  // for(let i = 0; i < model.routers.length; i++) {
  //   routerMap[model.routers[i].name] = {x: model.routers[i].pos.x, y: model.routers[i].pos.y};
  // }

  console.log("map", routerMap);

  draw();
  update();

  function update() {
    if(requireUpdate)
      sendRequest();

    // draw();
    requestAnimationFrame(update)
  }

  function draw() {
    ctx.fillStyle = "rgba(232, 240, 243)";
    ctx.fillRect(-tx, -ty, w, h);
    ctx.save();

    ctx.drawImage(
      map.image,
      map.x + context.offx,
      map.y + context.offy,
      map.w * context.scale,
      map.h * context.scale,
    );

    if(data){
      let {x, y} = imageRelativePoint(map, data.pos);
      ctx.fillStyle = "rgba(234, 89, 89, 0.6)";
      ctx.strokeStyle = "white";
      ctx.lineWidth = 10;
      ctx.beginPath();
      ctx.arc(x, y, 10 * context.scale, 0, Math.PI * 2, false);
      ctx.stroke()
      ctx.fill()

      drawEstimates(data.estimates);
    }

    ctx.restore()
  }

  function drawEstimates(estimates) {
    for(let i = 0; i < estimates.length; i++) {
      let {x, y} = imageRelativePoint(map, {x:estimates[i][0], y:estimates[i][1]});
      ctx.fillStyle = "green";
      ctx.strokeStyle = "white";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(x, y, 2 * context.scale, 0, Math.PI * 2, false);
      ctx.stroke()
      ctx.fill()
    }
  }

  function imageRelativePoint(map, point) {
    return {
      x: map.x + point.x * context.pixPerMeter * context.scale + map.coffx * context.scale + context.offx,
      y: map.y + point.y * context.pixPerMeter * context.scale + map.coffy * context.scale + context.offy,
    };
  }

  function drawRouters(routers) {
    ctx.strokeStyle = "cyan";
    for(let i = 0; i < routers.length; i++) {
      ctx.beginPath();
      let screenPoint = pointToScreenCoordinates(routers[i].pos);
      ctx.arc(screenPoint.x, screenPoint.y, 10 * context.scale, 0, Math.PI * 2, false);
      ctx.stroke()
    }
  }

  function drawBuilding(building) {
    ctx.strokeStyle = "white"
    ctx.lineWidth = 2;

    let vertices = listToScreenCoordinates(building);
    ctx.moveTo(vertices[0].x, vertices[0].y);
    for(let i = 1; i < vertices.length; i++) {
      ctx.lineTo(vertices[i].x, vertices[i].y)
    }
    ctx.lineTo(vertices[0].x, vertices[0].y);

    ctx.stroke();
  }

  function drawData(data) {
    if(!data)
      return;

    let devicePos = pointToScreenCoordinates(data.pos);

    ctx.fillStyle = "rgba(188, 88, 88, 0.7";
    ctx.strokeStyle = "red";
    ctx.beginPath()
    ctx.arc(devicePos.x, devicePos.y, 5 * context.scale, 0, Math.PI * 2, false);
    ctx.fill();
    ctx.stroke();

    ctx.strokeStyle = "red";
    for(let i = 0; i < data.routers.length; i++){
      let routerPos = pointToScreenCoordinates(routerMap[data.routers[i]]);
      console.log(i, routerPos);

      ctx.beginPath();
      ctx.moveTo(devicePos.x, devicePos.y);
      ctx.lineTo(routerPos.x, routerPos.y);
      ctx.stroke();
    }
  }

  function listToScreenCoordinates(vertices) {
    let result = [];
    for(let i = 0; i < vertices.length; i++) {
      result.push(pointToScreenCoordinates(vertices[i]));
    }

    return result;
  }

  function pointToScreenCoordinates(point) {
    return {
      x: point.x * context.scale * context.pixPerMeter,
      y: point.y * context.scale * context.pixPerMeter,
    };
  }

  function sendRequest() {
    let request = new XMLHttpRequest();
    request.open("GET", "update", true);
    request.onreadystatechange = function() {
      if(request.readyState === 4 && request.status === 200){
        requireUpdate = true;
        data = JSON.parse(request.response)
        console.log("Pos", data);
        draw();
      }
    };

    requireUpdate = false;
    request.send();
  }
}