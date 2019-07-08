var mapObject;
var currentLocation;
var portLocation_HK;
var portLocation_China;
var directionsDisplay_OutHK = [];
var directionsDisplay_InHK = [];
var lorryMarker_OutHK = [];
var lorryMarker_InHK = [];

function initMap() {

    currentLocation = { lat: 32.078559, lng: 118.782615 };
    portLocation_HK = { lat: 22.512915, lng: 114.071813 };
    portLocation_China = { lat: 22.516761, lng: 114.068069 };

    var mapOptions = {
        zoom: 10,
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
    //initiate all the routeDisplays and icons
    var lorryIcon = {
        url: "img/map_icons/lorry.png",
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(50, 50)
    };
    //establish xmlhttprequest to the server and request supplier data
    var urlSupplier = "php/mysql_db_supplier.php";
    var urlControlPoint = "php/mysql_db_controlpoint.php";

    //show project and suppliers as marks on the map
    var urlProject = "php/mysql_db.php";
    downloadUrl(urlSupplier, addSupplierMarkers);
    downloadUrl(urlProject, addProjectMarkers);
    downloadUrl(urlSupplier, addCurrentMarker);
	downloadUrl(urlControlPoint,addControlPointMarkers);

    //alert("item.location_latitude");
    /*for(var node in markersData_supplier){
     var nodeLatLng={lat: node.location_latitude,lng: node.location_longitude};
     var marker_node = new google.maps.Marker({
     position: nodeLatLng,
     map: mapObject
     //icon: 'img/pins/' + key + '.png',
     })
     }*/

    /*if ('undefined' === typeof markers[key])
     markers[key] = [];
     markers[key].push(marker);
     google.maps.event.addListener(marker, 'click', (function () {
     closeInfoBox();
     getInfoBox(item).open(mapObject, this);
     mapObject.setCenter(new google.maps.LatLng(item.location_latitude, item.location_longitude));
     }));
     );
     //}
     
     // Try HTML5 geolocation.
     /*var infoWindow = new google.maps.InfoWindow;
     if (navigator.geolocation) {
     navigator.geolocation.getCurrentPosition(function(position) {
     var pos = {
     lat: position.coords.latitude,
     lng: position.coords.longitude
     };
     
     infoWindow.setPosition(pos);
     infoWindow.setContent('Location found.');
     infoWindow.open(mapObject);
     mapObject.setCenter(pos);
     }, function() {
     handleLocationError(true, infoWindow, mapObject.getCenter());
     });
     } else {
     // Browser doesn't support Geolocation
     handleLocationError(false, infoWindow, mapObject.getCenter());
     }
     
     function handleLocationError(browserHasGeolocation, infoWindow, pos) {
     infoWindow.setPosition(pos);
     infoWindow.setContent(browserHasGeolocation ?
     'Error: The Geolocation service failed.' :
     'Error: Your browser doesn\'t support geolocation.');
     infoWindow.open(mapObject);
     }*/

    /*function hideAllMarkers () {
     for (var key in markers)
     markers[key].forEach(function (marker) {
     marker.setMap(null);
     });
     };
     
     function toggleMarkers (category) {
     hideAllMarkers();
     closeInfoBox();
     
     if ('undefined' === typeof markers[category])
     return false;
     markers[category].forEach(function (marker) {
     marker.setMap(mapObject);
     marker.setAnimation(google.maps.Animation.DROP);
     
     });
     };
     
     function closeInfoBox() {
     $('div.infoBox').remove();
     };
     
     function getInfoBox(item) {
     return new InfoBox({
     content:
     '<div class="marker_info">' +
     '<figure><a href='+ item.url_detail +'><img src="' + item.map_image_url + '" alt="Image"></a></figure>' +
     '<small>'+ item.type +'</small>' +
     '<h3><a href='+ item.url_detail +'>'+ item.name_point +'</a></h3>' +
     '<span>'+ item.description_point +'</span>' +
     '<div class="marker_tools">' +
     '<form action="http://maps.google.com/maps" method="get" target="_blank" style="display:inline-block""><input name="saddr" value="'+ item.get_directions_start_address +'" type="hidden"><input type="hidden" name="daddr" value="'+ item.location_latitude +',' +item.location_longitude +'"><button type="submit" value="Get directions" class="btn_infobox_get_directions">Directions</button></form>' +
     '<a href="tel://'+ item.phone +'" class="btn_infobox_phone">'+ item.phone +'</a>' +
     '</div>' +
     '</div>',
     disableAutoPan: false,
     maxWidth: 0,
     pixelOffset: new google.maps.Size(10, 105),
     closeBoxMargin: '',
     closeBoxURL: "img/close_infobox.png",
     isHidden: false,
     alignBottom: true,
     pane: 'floatPane',
     enableEventPropagation: true
     });
     };
     
     function onHtmlClick(location_type, key){
     google.maps.event.trigger(markers[location_type][key], "click");
     }*/
}

function downloadUrl(url, addMarkers) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            addMarkers(this);
        }
    };
    request.open("GET", url, true);
    request.send();
}

function addProjectMarkers(request) {
    //establish xmlhttprequest to the server
    var xmlDoc = request.responseXML;
    var rootNode = xmlDoc.documentElement;
    var projectMarkers = rootNode.childNodes;
    var projectIcon = {
        url: "img/map_icons/project.png",
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(50, 50)
    };
    Array.prototype.forEach.call(projectMarkers, function (markerElem) {
        var projectLocation = { lat: parseFloat(markerElem.getAttribute('Lat')), lng: parseFloat(markerElem.getAttribute('Lng')) };
		var projectimg = markerElem.getAttribute('img');
        var projectName = markerElem.getAttribute('Name');
		var projectAddress= markerElem.getAttribute('address');
		var projectDate= markerElem.getAttribute('date');
		var projectStorey= markerElem.getAttribute('storey');
		var projectArea= markerElem.getAttribute('area');
		var projectSType= markerElem.getAttribute('stype');
        var projectMarker = new google.maps.Marker({ position: projectLocation, map: mapObject, icon: projectIcon });
        projectMarker.addListener('mouseover', function () {
            if (projectMarker.getAnimation() == null) {
                projectMarker.setAnimation(google.maps.Animation.BOUNCE);
            }
        });
        projectMarker.addListener('mouseout', function () {
            if (projectMarker.getAnimation() !== null) {
                projectMarker.setAnimation(null);
            }
        });
        /*var infowincontent = document.createElement('div');
       var strong = document.createElement('strong');
       strong.textContent = name
       infowincontent.appendChild(strong);
       infowincontent.appendChild(document.createElement('br'));
       
       var text = document.createElement('text');
       text.textContent = address
       infowincontent.appendChild(text);
       var icon = customLabel[type] || {};*/
	   var projectString="<img src='"+projectimg+"' alt='' width='100' height='100'><br><ul><li>Name: "+projectName+"</li><li>Address: "+projectAddress+"</li><li>Starting Date: "+projectDate+"</li><li>Storey: "+projectStorey+"</li><li>Ground Area: "+projectArea+"</li><li>Structure Type: "+projectSType+"</li></ul>";
       var infoWindow = new google.maps.InfoWindow({
        content: projectString//revise here to info box
       });
       projectMarker.addListener('click', function () {
        infoWindow.open(mapObject, projectMarker);
       });
    });
}

function addControlPointMarkers(request) {
    //establish xmlhttprequest to the server
    var xmlDoc = request.responseXML;
    var rootNode = xmlDoc.documentElement;
    var controlPointMarkers = rootNode.childNodes;
    var controlPointIcon = {
        url: "img/map_icons/lorry.png",
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(50, 50)
    };
    Array.prototype.forEach.call(controlPointMarkers, function (markerElem) {
        var controlLocation = { lat: parseFloat(markerElem.getAttribute('Lat')), lng: parseFloat(markerElem.getAttribute('Lng')) };
        var controlName = markerElem.getAttribute('Name');
        var controlMarker = new google.maps.Marker({ position: controlLocation, map: mapObject, icon: controlPointIcon });
        controlMarker.addListener('mouseover', function () {
            if (controlMarker.getAnimation() == null) {
                controlMarker.setAnimation(google.maps.Animation.BOUNCE);
            }
        });
        controlMarker.addListener('mouseout', function () {
            if (controlMarker.getAnimation() !== null) {
                controlMarker.setAnimation(null);
            }
        });
       var infoWindow = new google.maps.InfoWindow({
        content: controlName//revise here to info box
       });
       controlMarker.addListener('click', function () {
        infoWindow.open(mapObject, controlMarker);
       });
    });
}

function addSupplierMarkers(request) {
    //establish xmlhttprequest to the server
    var xmlDoc = request.responseXML;
    var rootNode = xmlDoc.documentElement;
    var suppliers = rootNode.childNodes;
    var supplierIcon = {
        url: "img/map_icons/factory.png",
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(50, 50)
    };
    Array.prototype.forEach.call(suppliers, function (markerElem) {
        var supplierID = parseInt(markerElem.getAttribute('SupplierID'))-1;
        var supplierName = markerElem.getAttribute('Name');
		var supplieAddress = markerElem.getAttribute('address');
		var supplieimg = markerElem.getAttribute('img');
		var supplieConcrete = markerElem.getAttribute('concrete');
		var supplieSteel = markerElem.getAttribute('steel');
		var supplieComposite = markerElem.getAttribute('composite');
        var supplierLocation = new google.maps.LatLng(parseFloat(markerElem.getAttribute('Lat')), parseFloat(markerElem.getAttribute('Lng')));
        var supplierMarker = new google.maps.Marker({ position: supplierLocation, map: mapObject, icon: supplierIcon });
        supplierMarker.addListener('mouseover', function () {
            if (supplierMarker.getAnimation() == null) {
                supplierMarker.setAnimation(google.maps.Animation.BOUNCE);
            }
        });
        supplierMarker.addListener('mouseout', function () {
            if (supplierMarker.getAnimation() !== null) {
                supplierMarker.setAnimation(null);
            }
        });
        /*var infowincontent = document.createElement('div');
       var strong = document.createElement('strong');
       strong.textContent = name
       infowincontent.appendChild(strong);
       infowincontent.appendChild(document.createElement('br'));
       
       var text = document.createElement('text');
       text.textContent = address
       infowincontent.appendChild(text);
       var icon = customLabel[type] || {};*/
	   var supplierString="<img src='"+supplieimg+"' alt='' width='100' height='100'><br><ul><li>Name: "+supplierName+"</li><li>Address: "+supplieAddress+"</li><li>Structure Type:<br>"+supplieConcrete+"<br>"+supplieSteel+"<br>"+supplieComposite+"</li></ul>";
       var infoWindow = new google.maps.InfoWindow({
        content: supplierString
		//supplierID+
       });
       supplierMarker.addListener('click', function () {
        infoWindow.open(mapObject, supplierMarker);
       });
        //identify the key points on the route
        var start = supplierLocation;
        var end = currentLocation;
        //right click the icon to show the route
        var onOff = true;
        supplierMarker.addListener('rightclick', function () {
            var directionsService = new google.maps.DirectionsService();
            if (onOff) {
                for(var j=0;j<suppliers.length;j++){
                    if(j!==supplierID){
                      directionsDisplay_OutHK[j].setMap(null);
                      directionsDisplay_InHK[j].setMap(null);
                      lorryMarker_OutHK[j].setMap(null);
                      lorryMarker_InHK[j].setMap(null);
                    }
                }
                directionsDisplay_OutHK[supplierID].setMap(mapObject);
                directionsDisplay_InHK[supplierID].setMap(mapObject);
                //route outside HK
                directionsService.route({
                    origin: start,
                    destination: portLocation_China,
                    optimizeWaypoints: true,
                    travelMode: 'DRIVING',
                }, function (response, status) {
                    if (status == 'OK') {
                        directionsDisplay_OutHK[supplierID].setDirections(response);
                        var route = response.routes[0];
                        lorryMarker_OutHK[supplierID].setMap(mapObject);
                        /*lorryMarker_OutHK[supplierID].addListener('mouseover', function () {

                        });
                        lorryMarker_OutHK[supplierID].addListener('mouseout', function () {

                        });*/
                        var routeLength = 0;
                        for(var k=0; k<route.legs.length; k++){
                          routeLength += route.legs[k].distance.value/1000;
                        }
                        var infoWindow_lorry_OutHK = new google.maps.InfoWindow({
                            content: routeLength.toString() + ' km'
                        });
                        var i = 1;                      
                        var timer = setInterval(function () { lorryMarker_OutHK[supplierID].setPosition(route.overview_path[i]); i = i + 1; if (i == route.overview_path.length - 1) i = 1; }, 50);
                        lorryMarker_OutHK[supplierID].addListener('mouseover', function () {
                            clearInterval(timer);
                            infoWindow_lorry_OutHK.open(mapObject, lorryMarker_OutHK[supplierID]);
                        });
                        lorryMarker_OutHK[supplierID].addListener('mouseout', function () {
                            infoWindow_lorry_OutHK.close();
                            timer = setInterval(function () { lorryMarker_OutHK[supplierID].setPosition(route.overview_path[i]); i = i + 1; if (i == route.overview_path.length - 1) i = 1; }, 50);
                        });
                    } else {
                        window.alert('Directions request failed due to ' + status);
                    }
                });
                //route inside HK
                directionsService.route({
                    origin: portLocation_HK,
                    destination: end,
                    optimizeWaypoints: true,
                    travelMode: 'DRIVING',
                }, function (response, status) {
                    if (status == 'OK') {
                        directionsDisplay_InHK[supplierID].setDirections(response);
                        var route = response.routes[0];
                        lorryMarker_InHK[supplierID].setMap(mapObject);
                        var routeLength = 0;
                        for(var k=0; k<route.legs.length; k++){
                          routeLength += route.legs[k].distance.value/1000;
                        }
                        var infoWindow_lorry_InHK = new google.maps.InfoWindow({
                            content: routeLength.toString() + ' km'
                        });
                        var i = 1;
                        var timer = setInterval(function () { lorryMarker_InHK[supplierID].setPosition(route.overview_path[i]); i = i + 1; if (i == route.overview_path.length - 1) i = 1; }, 50);
                        lorryMarker_InHK[supplierID].addListener('mouseover', function () {
                            clearInterval(timer);
                            infoWindow_lorry_InHK.open(mapObject, lorryMarker_InHK[supplierID]);
                        });
                        lorryMarker_InHK[supplierID].addListener('mouseout', function () {
                            infoWindow_lorry_InHK.close();
                            timer = setInterval(function () { lorryMarker_InHK[supplierID].setPosition(route.overview_path[i]); i = i + 1; if (i == route.overview_path.length - 1) i = 1; }, 50);
                        });
                    } else {
                        window.alert('Directions request failed due to ' + status);
                    }
                });
            } else {
                directionsDisplay_OutHK[supplierID].setMap(null);
                directionsDisplay_InHK[supplierID].setMap(null);
                lorryMarker_OutHK[supplierID].setMap(null);
                lorryMarker_InHK[supplierID].setMap(null);
            }
            if (onOff) { onOff = false; } else { onOff = true; }
        });
    });
}

//add marker to current location
function addCurrentMarker(request){
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
    //add right-click event listener to show all routes to current project
    //establish xmlhttprequest to the server
    var xmlDoc = request.responseXML;
    var rootNode = xmlDoc.documentElement;
    var suppliers = rootNode.childNodes;
    var onOff = true;
    currentMarker.addListener('rightclick', function () {
        //visualize route and marker on the map
        var directionsService = new google.maps.DirectionsService();
        if(onOff){
            //visualize comparison div block to compare different schemes
            var routeCompareBlock = document.getElementsByClassName("margin_60_35");
            routeCompareBlock[0].style.display = "inline";
            //clear existing routes and markers
            for(var j=0;j<suppliers.length;j++){
                directionsDisplay_OutHK[j].setMap(null);
                lorryMarker_OutHK[j].setMap(null);
                directionsDisplay_InHK[j].setMap(null);
                lorryMarker_InHK[j].setMap(null);
            }
            Array.prototype.forEach.call(suppliers, function (markerElem) {
                var supplierID = parseInt(markerElem.getAttribute('SupplierID'))-1;
                var supplierLocation = new google.maps.LatLng(parseFloat(markerElem.getAttribute('Lat')), parseFloat(markerElem.getAttribute('Lng')));
                //route outside HK      
                directionsDisplay_OutHK[supplierID].setMap(mapObject);
                directionsService.route({
                    origin: supplierLocation,
                    destination: portLocation_China,
                    optimizeWaypoints: true,
                    travelMode: 'DRIVING',
                }, function (response, status) {
                    if (status == 'OK') {
                        directionsDisplay_OutHK[supplierID].setDirections(response);
                        var route = response.routes[0];
                        lorryMarker_OutHK[supplierID].setMap(mapObject);
                        var routeLength = 0;
                        for(var k=0; k<route.legs.length; k++){
                          routeLength += route.legs[k].distance.value/1000;
                        }
                        var infoWindow_lorry_OutHK = new google.maps.InfoWindow({
                            content: routeLength.toString() + ' km'
                        });
                        var i = 1;
                        var timer = setInterval(function () { lorryMarker_OutHK[supplierID].setPosition(route.overview_path[i]); i = i + 1; if (i == route.overview_path.length - 1) i = 1; }, 50);
                        lorryMarker_OutHK[supplierID].addListener('mouseover', function () {
                            clearInterval(timer);
                            infoWindow_lorry_OutHK.open(mapObject, lorryMarker_OutHK[supplierID]);
                        });
                        lorryMarker_OutHK[supplierID].addListener('mouseout', function () {
                            infoWindow_lorry_OutHK.close();
                            timer = setInterval(function () { lorryMarker_OutHK[supplierID].setPosition(route.overview_path[i]); i = i + 1; if (i == route.overview_path.length - 1) i = 1; }, 50);
                        });
                    } else {
                        window.alert('Directions request failed due to ' + status);
                    }
                });
                //route inside HK
                directionsDisplay_InHK[supplierID].setMap(mapObject);
                directionsService.route({
                    origin: portLocation_HK,
                    destination: currentLocation,
                    optimizeWaypoints: true,
                    travelMode: 'DRIVING',
                }, function (response, status) {
                    if (status == 'OK') {
                        directionsDisplay_InHK[supplierID].setDirections(response);
                        var route = response.routes[0];
                        lorryMarker_InHK[supplierID].setMap(mapObject);
                        var routeLength = 0;
                        for(var k=0; k<route.legs.length; k++){
                            routeLength += route.legs[k].distance.value/1000;
                        }
                        var infoWindow_lorry_InHK = new google.maps.InfoWindow({
                            content: routeLength.toString() + ' km'
                        });
                        var i = 1;
                        var timer = setInterval(function () { lorryMarker_InHK[supplierID].setPosition(route.overview_path[i]); i = i + 1; if (i == route.overview_path.length - 1) i = 1; }, 50);
                        lorryMarker_InHK[supplierID].addListener('mouseover', function () {
                            clearInterval(timer);
                            infoWindow_lorry_InHK.open(mapObject, lorryMarker_InHK[supplierID]);
                        });
                        lorryMarker_InHK[supplierID].addListener('mouseout', function () {
                            infoWindow_lorry_InHK.close();
                            timer = setInterval(function () { lorryMarker_InHK[supplierID].setPosition(route.overview_path[i]); i = i + 1; if (i == route.overview_path.length - 1) i = 1; }, 50);
                        });
                    } else {
                        window.alert('Directions request failed due to ' + status);
                    }
                });
            });  
        }else{
            //hide comparison div block to compare different schemes
            var routeCompareBlock = document.getElementsByClassName("margin_60_35");
            routeCompareBlock[0].style.display = "none";
            for(var j=0;j<suppliers.length;j++){
                directionsDisplay_OutHK[j].setMap(null);
                lorryMarker_OutHK[j].setMap(null);
                directionsDisplay_InHK[j].setMap(null);
                lorryMarker_InHK[j].setMap(null);
            }
            
        }

        if (onOff) { onOff = false; } else { onOff = true; }

    });
}
function panTo(x, y) {
					var centertest = new google.maps.LatLng(x, y);
					mapObject.setZoom(10);
					mapObject.setCenter(centertest);
					var supplierIcon = {
						url: "img/map_icons/factory.png",
						size: new google.maps.Size(71, 71),
						origin: new google.maps.Point(0, 0),
						anchor: new google.maps.Point(17, 34),
						scaledSize: new google.maps.Size(50, 50)
					};
					var supplierMarkertest = new google.maps.Marker({ position: centertest, map: mapObject, icon: supplierIcon });
					if (supplierMarkertest.getAnimation() == null) {
						supplierMarkertest.setAnimation(google.maps.Animation.BOUNCE);
					}
					window.setTimeout(function(){
						supplierMarkertest.setMap(null);
					},3000);
					//long start = System.currentTimeMillis();
					//if(System.currentTimeMillis()-start>=5000){
						//supplierMarkertest.setMap(null);
					//}
        }
function panToP(x, y) {
					var centertest = new google.maps.LatLng(x, y);
					mapObject.setZoom(10);
					mapObject.setCenter(centertest);
					var projectIcon = {
						url: "img/map_icons/project.png",
						size: new google.maps.Size(71, 71),
						origin: new google.maps.Point(0, 0),
						anchor: new google.maps.Point(17, 34),
						scaledSize: new google.maps.Size(50, 50)
					};
					var projectMarkertest = new google.maps.Marker({ position: centertest, map: mapObject, icon: projectIcon });
					if (projectMarkertest.getAnimation() == null) {
						projectMarkertest.setAnimation(google.maps.Animation.BOUNCE);
					}
					window.setTimeout(function(){
						projectMarkertest.setMap(null);
					},3000);
					//long start = System.currentTimeMillis();
					
        }