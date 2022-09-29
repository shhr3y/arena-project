
var client = new io('192.168.0.103:9876', { 
   transports : ['websocket'] });
   var counter = 0
   client.on("connect", () => {
  counter += 1
  console.log('connected', counter, client.id);
});

client.on('render', function (data) {
  let landmarks = data['data']
  console.log(landmarks)
  updateLandmarks(landmarks)
});

function updateLandmarks(landmarks) {
  // if (landmarks) {
      grid.updateLandmarks(landmarks, mpPose.POSE_CONNECTIONS);
    // } else {
    //   grid.updateLandmarks([]);
    // }
}

const landmarkContainer = document.body.getElementsByClassName('landmark-grid-container')[0];
const grid = new LandmarkGrid(landmarkContainer, {
  connectionColor: 0xCCCCCC,
  definedColors:
      [{name: 'LEFT', value: 0xffa500}, {name: 'RIGHT', value: 0x00ffff}],
  range: 2,
  fitToGrid: true,
  labelSuffix: 'm',
  landmarkSize: 2,
  numCellsPerAxis: 4,
  showHidden: false,
  centered: true,
});


