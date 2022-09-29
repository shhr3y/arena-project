var express = require('express');
var bodyParser = require('body-parser');

var app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

app.post("/landmarks", (req, res) => {
    // Return json response
	res.json({ received: true });

    // Retrieve array form post body
	var list = req.body;
	console.log(list)
    if (list) {
        grid.updateLandmarks(list, mpPose.POSE_CONNECTIONS);
      } else {
        grid.updateLandmarks([]);
      }

	
});

// Server listening to PORT 3000
app.listen(3000);
