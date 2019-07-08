var mapObject;
var currentLocation;
var Location1;
var Location2;
var Location3;
var Location4;
var Location5;


function initMap() {
	mapObject = new BMap.Map("map_listing");
    mapObject.centerAndZoom(new BMap.Point(118.794644,32.027227), 10);
    mapObject.enableScrollWheelZoom();
}
function mapRoute(longitudea,latitudea,longitudeb,latitudeb){
	var pointa=new BMap.Point(longitudea,latitudea);
	var pointb=new BMap.Point(longitudeb,latitudeb);
	var transit = new BMap.TransitRoute(mapObject, { 
    renderOptions: { 
        map: mapObject, 
        autoViewport: true
        
    },
    // 配置跨城公交的换成策略为优先出发早
    intercityPolicy: BMAP_INTERCITY_POLICY_EARLY_START,
    // 配置跨城公交的交通方式策略为飞机优先
    transitTypePolicy: BMAP_TRANSIT_TYPE_POLICY_AIRPLANE
	});
	transit.search(pointa,pointb);
	
}
function map(day,city,title,time,longitude,latitude){
	initMap();
	var pointc=new BMap.Point(longitude[0],latitude[0]);
	mapObject.panTo(pointc);
	mapObject.setZoom(13);
	var marker=[];
	var point=[];
	var lab=[];
	
	for(a=0;a<title.length;a++){
		point[a]=new BMap.Point(longitude[a],latitude[a]);
		
		marker[a]=new BMap.Marker(point[a]);
		mapObject.addOverlay(marker[a]);
		lab[a] = new BMap.Label(a+1,{position:point[a]});        //创建3个label
        mapObject.addOverlay(lab[a]);
	}
	var listdiv=document.getElementById("listdiv");
	var html="";
	longitude[title.length]=longitude[0];
	latitude[title.length]=latitude[0];
	listdiv.innerHTML="";
	for(m=0;m<title.length;m++){
		html+="<li><a href='javascript:void(0)' onclick='mapinfo("+longitude[m]+","+latitude[m]+")'><strong>"+(m+1)+"</strong>"+title[m]+"   推荐游玩时长: "+time[m]+"h</a></li><li><a href='javascript:void(0)' onclick='mapRoute("+longitude[m]+","+latitude[m]+","+longitude[m+1]+","+latitude[m+1]+")'><strong>Bus</strong></a></li>";
	}
	html+="<li><a href='javascript:void(0)' onclick='mapinfo("+longitude[0]+","+latitude[0]+")'><strong>"+(title.length+1)+"</strong>"+title[0]+"</a></li>";
	
	listdiv.innerHTML="<div id='d1' class='list_home'><div class='list_title'><h3>"+day+"</h3><br>"+city+"<br></div><ul>"+html+"</ul></div>";
	
}
function mapinfo(x,y){
	var pointc=new BMap.Point(x,y);
	mapObject.panTo(pointc);
	mapObject.setZoom(15);
	
}
