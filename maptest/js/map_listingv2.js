var mapObject;
var currentLocation;
var Location1;
var Location2;
var Location3;
var Location4;
var Location5;


function initMap() {

    currentLocation = { lat: 32.027227, lng: 118.794644 };
	
	Location1={lat: 32.027081718573854, lng: 118.79521999339607}; 
	Location2={lat: 32.02774395091252, lng: 118.79523536699658}; 
	Location3={lat: 32.02664641893529, lng: 118.79171149414205}; 
	Location4={lat: 32.040613954051466, lng: 118.75147800730005};
	Location5={lat: 32.04903823294875, lng: 118.8039743524893}; 


    var mapOptions = {
        zoom: 14,
        center: currentLocation,
        mapTypeId: google.maps.MapTypeId.ROADMAP,

        mapTypeControl: true,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
            position: google.maps.ControlPosition.LEFT_BOTTOM
        },
        panControl: false,
        panControlOptions: {
            position: google.maps.ControlPosition.TOP_RIGHT
        },
        zoomControl: true,
        zoomControlOptions: {
            style: google.maps.ZoomControlStyle.LARGE,
            position: google.maps.ControlPosition.RIGHT_BOTTOM
        },
        scrollwheel: true,
        scaleControl: true,
        scaleControlOptions: {
            position: google.maps.ControlPosition.LEFT_CENTER
        },
        streetViewControl: true,
        streetViewControlOptions: {
            position: google.maps.ControlPosition.RIGHT_BOTTOM
        },
        styles: [
                 {
                     "featureType": "landscape",
                     "stylers": [
                                 {
                                     "hue": "#FFBB00"
                                 },
                                 {
                                     "saturation": 43.400000000000006
                                 },
                                 {
                                     "lightness": 37.599999999999994
                                 },
                                 {
                                     "gamma": 1
                                 }
                     ]
                 },
                 {
                     "featureType": "road.highway",
                     "stylers": [
                                 {
                                     "hue": "#FFC200"
                                 },
                                 {
                                     "saturation": -61.8
                                 },
                                 {
                                     "lightness": 45.599999999999994
                                 },
                                 {
                                     "gamma": 1
                                 }
                     ]
                 },
                 {
                     "featureType": "road.arterial",
                     "stylers": [
                                 {
                                     "hue": "#FF0300"
                                 },
                                 {
                                     "saturation": -100
                                 },
                                 {
                                     "lightness": 51.19999999999999
                                 },
                                 {
                                     "gamma": 1
                                 }
                     ]
                 },
                 {
                     "featureType": "road.local",
                     "stylers": [
                                 {
                                     "hue": "#FF0300"
                                 },
                                 {
                                     "saturation": -100
                                 },
                                 {
                                     "lightness": 52
                                 },
                                 {
                                     "gamma": 1
                                 }
                     ]
                 },
                 {
                     "featureType": "water",
                     "stylers": [
                                 {
                                     "hue": "#0078FF"
                                 },
                                 {
                                     "saturation": -13.200000000000003
                                 },
                                 {
                                     "lightness": 2.4000000000000057
                                 },
                                 {
                                     "gamma": 1
                                 }
                     ]
                 },
                 {
                     "featureType": "poi",
                     "stylers": [
                                 {
                                     "hue": "#00FF6A"
                                 },
                                 {
                                     "saturation": -1.0989010989011234
                                 },
                                 {
                                     "lightness": 11.200000000000017
                                 },
                                 {
                                     "gamma": 1
                                 }
                     ]
                 }
        ]
    };

    //initiate the google map
    mapObject = new google.maps.Map(document.getElementById('map_listing'), mapOptions);
	var currentIcon = {
        url: "img/hotel.png",
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(50, 50)
    };
    //add user marker
    var currentMarker = new google.maps.Marker({ position: currentLocation, map: mapObject, icon: currentIcon });
    //add bounce animation
    currentMarker.addListener('mouseover', function () {
        if (currentMarker.getAnimation() == null) {
            currentMarker.setAnimation(google.maps.Animation.BOUNCE);
        }
    });
    currentMarker.addListener('mouseout', function () {
        if (currentMarker.getAnimation() !== null) {
            currentMarker.setAnimation(null);
        }
    });
	var Icon1 = {
        url: "img/location.png",
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(30, 40)
    };
    //add user marker
    var Marker1 = new google.maps.Marker({ position: Location1, map: mapObject, icon: Icon1 });
    //add bounce animation
    Marker1.addListener('mouseover', function () {
        if (Marker1.getAnimation() == null) {
            Marker1.setAnimation(google.maps.Animation.BOUNCE);
        }
    });
    Marker1.addListener('mouseout', function () {
        if (Marker1.getAnimation() !== null) {
            Marker1.setAnimation(null);
        }
    });
	
	var Icon2 = {
        url: "img/location.png",
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(30, 40)
    };
    //add user marker
    var Marker2 = new google.maps.Marker({ position: Location2, map: mapObject, icon: Icon2 });
    //add bounce animation
    Marker2.addListener('mouseover', function () {
        if (Marker2.getAnimation() == null) {
            Marker2.setAnimation(google.maps.Animation.BOUNCE);
        }
    });
    Marker2.addListener('mouseout', function () {
        if (Marker2.getAnimation() !== null) {
            Marker2.setAnimation(null);
        }
    });
	
	var Icon3 = {
        url: "img/location.png",
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(30, 40)
    };
	//add user marker
    var Marker3 = new google.maps.Marker({ position: Location3, map: mapObject, icon: Icon3 });
    //add bounce animation
    Marker3.addListener('mouseover', function () {
        if (Marker3.getAnimation() == null) {
            Marker3.setAnimation(google.maps.Animation.BOUNCE);
        }
    });
    Marker3.addListener('mouseout', function () {
        if (Marker3.getAnimation() !== null) {
            Marker3.setAnimation(null);
        }
    });
	
	var Icon4 = {
        url: "img/location.png",
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(30, 40)
    };
	//add user marker
    var Marker4 = new google.maps.Marker({ position: Location4, map: mapObject, icon: Icon4 });
    //add bounce animation
    Marker4.addListener('mouseover', function () {
        if (Marker4.getAnimation() == null) {
            Marker4.setAnimation(google.maps.Animation.BOUNCE);
        }
    });
    Marker4.addListener('mouseout', function () {
        if (Marker4.getAnimation() !== null) {
            Marker4.setAnimation(null);
        }
    });
	
	var Icon5 = {
        url: "img/location.png",
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(30, 40)
    };
	//add user marker
    var Marker5 = new google.maps.Marker({ position: Location5, map: mapObject, icon: Icon5 });
    //add bounce animation
    Marker5.addListener('mouseover', function () {
        if (Marker5.getAnimation() == null) {
            Marker5.setAnimation(google.maps.Animation.BOUNCE);
        }
    });
    Marker5.addListener('mouseout', function () {
        if (Marker5.getAnimation() !== null) {
            Marker5.setAnimation(null);
        }
    });
	
	var directionsService = new google.maps.DirectionsService();

	var renderOptions = { draggable: true };
	var directionDisplay = new google.maps.DirectionsRenderer(renderOptions);

	//set the directions display service to the map
	directionDisplay.setMap(mapObject);
	//set the directions display panel
	//panel is usually just and empty div.  
	//This is where the turn by turn directions appear.

//build the waypoints
//free api allows a max of 9 total stops including the start and end address
//premier allows a total of 25 stops. 
	var items = [Location1, Location2, Location3, Location4, Location5];
	var waypoints = [];
	for (var i = 0; i < items.length; i++) {
		var address = items[i];
		if (address !== "") {
			waypoints.push({
				location: address,
            stopover: true
        });
		}
	}
	//set the starting address and destination address
	var originAddress = currentLocation;
	var destinationAddress = currentLocation;

	//build directions request
	var request = {
            origin: originAddress,
            destination: destinationAddress,
            waypoints: waypoints, //an array of waypoints
            optimizeWaypoints: false, //set to true if you want google to determine the shortest route or false to use the order specified.
            travelMode: 'DRIVING'
        };

	//get the route from the directions service
	directionsService.route(request, function (response, status) {
    if (status == google.maps.DirectionsStatus.OK) {
        directionDisplay.setDirections(response);
    }
    else {
        //handle error
    }
	});
}