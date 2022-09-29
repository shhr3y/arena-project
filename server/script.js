const mpPose = window;
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

var client = new io('192.168.0.103:9876', { 
   transports : ['websocket'] });

client.on("connect", () => {
  console.log('Connection Established to Socket!', client.id);
});

client.on('render', function (data) {
  let landmarks = data['data']
  
  if (landmarks) {
    grid.updateLandmarks(landmarks, mpPose.POSE_CONNECTIONS, [
      { list: Object.values(mpPose.POSE_LANDMARKS_LEFT), color: 'LEFT' },
      { list: Object.values(mpPose.POSE_LANDMARKS_RIGHT), color: 'RIGHT' },
    ]);
  } else {
    grid.updateLandmarks([]);
  }
});

