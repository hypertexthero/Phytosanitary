// Global JavaScripts for IPPC.int
// Last update: Wednesday, 10 November 2010 at 13:09:17


/*
=======================================================================
Title: JQuery Cookie plugin
Use: General jQuery plugin to set cookies to remember page settings
Documentation URL: http://plugins.jquery.com/project/cookie
Uncompressed Script URL: http://hypertexthero.com/ippc/js/uncompressed/jquery.cookie.js
Version: 1.0
=======================================================================
*/
jQuery.cookie=function(name,value,options){if(typeof value!='undefined'){options=options||{};if(value===null){value='';options.expires=-1;}
var expires='';if(options.expires&&(typeof options.expires=='number'||options.expires.toUTCString)){var date;if(typeof options.expires=='number'){date=new Date();date.setTime(date.getTime()+(options.expires*24*60*60*1000));}else{date=options.expires;}
expires='; expires='+date.toUTCString();}
var path=options.path?'; path='+(options.path):'';var domain=options.domain?'; domain='+(options.domain):'';var secure=options.secure?'; secure':'';document.cookie=[name,'=',encodeURIComponent(value),expires,path,domain,secure].join('');}else{var cookieValue=null;if(document.cookie&&document.cookie!=''){var cookies=document.cookie.split(';');for(var i=0;i<cookies.length;i++){var cookie=jQuery.trim(cookies[i]);if(cookie.substring(0,name.length+1)==(name+'=')){cookieValue=decodeURIComponent(cookie.substring(name.length+1));break;}}}
return cookieValue;}};


/*
=======================================================================
Title: JQuery Tablesorter (compressed)
Use: Sort existing HTML table data by clicking on headers without reloading page 
Documentation URL: http://tablesorter.com/docs/
Uncompressed Script URL: http://hypertexthero.com/ippc/js/uncompressed/jquery.tablesorter.js
Version: 2.0.3
=======================================================================
*/
(function($){$.extend({tablesorter:new function(){var parsers=[],widgets=[];this.defaults={cssHeader:"header",cssAsc:"headerSortUp",cssDesc:"headerSortDown",sortInitialOrder:"asc",sortMultiSortKey:"shiftKey",sortForce:null,sortAppend:null,textExtraction:"simple",parsers:{},widgets:[],widgetZebra:{css:["even","odd"]},headers:{},widthFixed:false,cancelSelection:true,sortList:[],headerList:[],dateFormat:"uk",decimal:'.',debug:false};function benchmark(s,d){log(s+","+(new Date().getTime()-d.getTime())+"ms");}this.benchmark=benchmark;function log(s){if(typeof console!="undefined"&&typeof console.debug!="undefined"){console.log(s);}else{alert(s);}}function buildParserCache(table,$headers){if(table.config.debug){var parsersDebug="";}var rows=table.tBodies[0].rows;if(table.tBodies[0].rows[0]){var list=[],cells=rows[0].cells,l=cells.length;for(var i=0;i<l;i++){var p=false;if($.metadata&&($($headers[i]).metadata()&&$($headers[i]).metadata().sorter)){p=getParserById($($headers[i]).metadata().sorter);}else if((table.config.headers[i]&&table.config.headers[i].sorter)){p=getParserById(table.config.headers[i].sorter);}if(!p){p=detectParserForColumn(table,cells[i]);}if(table.config.debug){parsersDebug+="column:"+i+" parser:"+p.id+"\n";}list.push(p);}}if(table.config.debug){log(parsersDebug);}return list;};function detectParserForColumn(table,node){var l=parsers.length;for(var i=1;i<l;i++){if(parsers[i].is($.trim(getElementText(table.config,node)),table,node)){return parsers[i];}}return parsers[0];}function getParserById(name){var l=parsers.length;for(var i=0;i<l;i++){if(parsers[i].id.toLowerCase()==name.toLowerCase()){return parsers[i];}}return false;}function buildCache(table){if(table.config.debug){var cacheTime=new Date();}var totalRows=(table.tBodies[0]&&table.tBodies[0].rows.length)||0,totalCells=(table.tBodies[0].rows[0]&&table.tBodies[0].rows[0].cells.length)||0,parsers=table.config.parsers,cache={row:[],normalized:[]};for(var i=0;i<totalRows;++i){var c=table.tBodies[0].rows[i],cols=[];cache.row.push($(c));for(var j=0;j<totalCells;++j){cols.push(parsers[j].format(getElementText(table.config,c.cells[j]),table,c.cells[j]));}cols.push(i);cache.normalized.push(cols);cols=null;};if(table.config.debug){benchmark("Building cache for "+totalRows+" rows:",cacheTime);}return cache;};function getElementText(config,node){if(!node)return"";var t="";if(config.textExtraction=="simple"){if(node.childNodes[0]&&node.childNodes[0].hasChildNodes()){t=node.childNodes[0].innerHTML;}else{t=node.innerHTML;}}else{if(typeof(config.textExtraction)=="function"){t=config.textExtraction(node);}else{t=$(node).text();}}return t;}function appendToTable(table,cache){if(table.config.debug){var appendTime=new Date()}var c=cache,r=c.row,n=c.normalized,totalRows=n.length,checkCell=(n[0].length-1),tableBody=$(table.tBodies[0]),rows=[];for(var i=0;i<totalRows;i++){rows.push(r[n[i][checkCell]]);if(!table.config.appender){var o=r[n[i][checkCell]];var l=o.length;for(var j=0;j<l;j++){tableBody[0].appendChild(o[j]);}}}if(table.config.appender){table.config.appender(table,rows);}rows=null;if(table.config.debug){benchmark("Rebuilt table:",appendTime);}applyWidget(table);setTimeout(function(){$(table).trigger("sortEnd");},0);};function buildHeaders(table){if(table.config.debug){var time=new Date();}var meta=($.metadata)?true:false,tableHeadersRows=[];for(var i=0;i<table.tHead.rows.length;i++){tableHeadersRows[i]=0;};$tableHeaders=$("thead th",table);$tableHeaders.each(function(index){this.count=0;this.column=index;this.order=formatSortingOrder(table.config.sortInitialOrder);if(checkHeaderMetadata(this)||checkHeaderOptions(table,index))this.sortDisabled=true;if(!this.sortDisabled){$(this).addClass(table.config.cssHeader);}table.config.headerList[index]=this;});if(table.config.debug){benchmark("Built headers:",time);log($tableHeaders);}return $tableHeaders;};function checkCellColSpan(table,rows,row){var arr=[],r=table.tHead.rows,c=r[row].cells;for(var i=0;i<c.length;i++){var cell=c[i];if(cell.colSpan>1){arr=arr.concat(checkCellColSpan(table,headerArr,row++));}else{if(table.tHead.length==1||(cell.rowSpan>1||!r[row+1])){arr.push(cell);}}}return arr;};function checkHeaderMetadata(cell){if(($.metadata)&&($(cell).metadata().sorter===false)){return true;};return false;}function checkHeaderOptions(table,i){if((table.config.headers[i])&&(table.config.headers[i].sorter===false)){return true;};return false;}function applyWidget(table){var c=table.config.widgets;var l=c.length;for(var i=0;i<l;i++){getWidgetById(c[i]).format(table);}}function getWidgetById(name){var l=widgets.length;for(var i=0;i<l;i++){if(widgets[i].id.toLowerCase()==name.toLowerCase()){return widgets[i];}}};function formatSortingOrder(v){if(typeof(v)!="Number"){i=(v.toLowerCase()=="desc")?1:0;}else{i=(v==(0||1))?v:0;}return i;}function isValueInArray(v,a){var l=a.length;for(var i=0;i<l;i++){if(a[i][0]==v){return true;}}return false;}function setHeadersCss(table,$headers,list,css){$headers.removeClass(css[0]).removeClass(css[1]);var h=[];$headers.each(function(offset){if(!this.sortDisabled){h[this.column]=$(this);}});var l=list.length;for(var i=0;i<l;i++){h[list[i][0]].addClass(css[list[i][1]]);}}function fixColumnWidth(table,$headers){var c=table.config;if(c.widthFixed){var colgroup=$('<colgroup>');$("tr:first td",table.tBodies[0]).each(function(){colgroup.append($('<col>').css('width',$(this).width()));});$(table).prepend(colgroup);};}function updateHeaderSortCount(table,sortList){var c=table.config,l=sortList.length;for(var i=0;i<l;i++){var s=sortList[i],o=c.headerList[s[0]];o.count=s[1];o.count++;}}function multisort(table,sortList,cache){if(table.config.debug){var sortTime=new Date();}var dynamicExp="var sortWrapper = function(a,b) {",l=sortList.length;for(var i=0;i<l;i++){var c=sortList[i][0];var order=sortList[i][1];var s=(getCachedSortType(table.config.parsers,c)=="text")?((order==0)?"sortText":"sortTextDesc"):((order==0)?"sortNumeric":"sortNumericDesc");var e="e"+i;dynamicExp+="var "+e+" = "+s+"(a["+c+"],b["+c+"]); ";dynamicExp+="if("+e+") { return "+e+"; } ";dynamicExp+="else { ";}var orgOrderCol=cache.normalized[0].length-1;dynamicExp+="return a["+orgOrderCol+"]-b["+orgOrderCol+"];";for(var i=0;i<l;i++){dynamicExp+="}; ";}dynamicExp+="return 0; ";dynamicExp+="}; ";eval(dynamicExp);cache.normalized.sort(sortWrapper);if(table.config.debug){benchmark("Sorting on "+sortList.toString()+" and dir "+order+" time:",sortTime);}return cache;};function sortText(a,b){return((a<b)?-1:((a>b)?1:0));};function sortTextDesc(a,b){return((b<a)?-1:((b>a)?1:0));};function sortNumeric(a,b){return a-b;};function sortNumericDesc(a,b){return b-a;};function getCachedSortType(parsers,i){return parsers[i].type;};this.construct=function(settings){return this.each(function(){if(!this.tHead||!this.tBodies)return;var $this,$document,$headers,cache,config,shiftDown=0,sortOrder;this.config={};config=$.extend(this.config,$.tablesorter.defaults,settings);$this=$(this);$headers=buildHeaders(this);this.config.parsers=buildParserCache(this,$headers);cache=buildCache(this);var sortCSS=[config.cssDesc,config.cssAsc];fixColumnWidth(this);$headers.click(function(e){$this.trigger("sortStart");var totalRows=($this[0].tBodies[0]&&$this[0].tBodies[0].rows.length)||0;if(!this.sortDisabled&&totalRows>0){var $cell=$(this);var i=this.column;this.order=this.count++%2;if(!e[config.sortMultiSortKey]){config.sortList=[];if(config.sortForce!=null){var a=config.sortForce;for(var j=0;j<a.length;j++){if(a[j][0]!=i){config.sortList.push(a[j]);}}}config.sortList.push([i,this.order]);}else{if(isValueInArray(i,config.sortList)){for(var j=0;j<config.sortList.length;j++){var s=config.sortList[j],o=config.headerList[s[0]];if(s[0]==i){o.count=s[1];o.count++;s[1]=o.count%2;}}}else{config.sortList.push([i,this.order]);}};setTimeout(function(){setHeadersCss($this[0],$headers,config.sortList,sortCSS);appendToTable($this[0],multisort($this[0],config.sortList,cache));},1);return false;}}).mousedown(function(){if(config.cancelSelection){this.onselectstart=function(){return false};return false;}});$this.bind("update",function(){this.config.parsers=buildParserCache(this,$headers);cache=buildCache(this);}).bind("sorton",function(e,list){$(this).trigger("sortStart");config.sortList=list;var sortList=config.sortList;updateHeaderSortCount(this,sortList);setHeadersCss(this,$headers,sortList,sortCSS);appendToTable(this,multisort(this,sortList,cache));}).bind("appendCache",function(){appendToTable(this,cache);}).bind("applyWidgetId",function(e,id){getWidgetById(id).format(this);}).bind("applyWidgets",function(){applyWidget(this);});if($.metadata&&($(this).metadata()&&$(this).metadata().sortlist)){config.sortList=$(this).metadata().sortlist;}if(config.sortList.length>0){$this.trigger("sorton",[config.sortList]);}applyWidget(this);});};this.addParser=function(parser){var l=parsers.length,a=true;for(var i=0;i<l;i++){if(parsers[i].id.toLowerCase()==parser.id.toLowerCase()){a=false;}}if(a){parsers.push(parser);};};this.addWidget=function(widget){widgets.push(widget);};this.formatFloat=function(s){var i=parseFloat(s);return(isNaN(i))?0:i;};this.formatInt=function(s){var i=parseInt(s);return(isNaN(i))?0:i;};this.isDigit=function(s,config){var DECIMAL='\\'+config.decimal;var exp='/(^[+]?0('+DECIMAL+'0+)?$)|(^([-+]?[1-9][0-9]*)$)|(^([-+]?((0?|[1-9][0-9]*)'+DECIMAL+'(0*[1-9][0-9]*)))$)|(^[-+]?[1-9]+[0-9]*'+DECIMAL+'0+$)/';return RegExp(exp).test($.trim(s));};this.clearTableBody=function(table){if($.browser.msie){function empty(){while(this.firstChild)this.removeChild(this.firstChild);}empty.apply(table.tBodies[0]);}else{table.tBodies[0].innerHTML="";}};}});$.fn.extend({tablesorter:$.tablesorter.construct});var ts=$.tablesorter;ts.addParser({id:"text",is:function(s){return true;},format:function(s){return $.trim(s.toLowerCase());},type:"text"});ts.addParser({id:"digit",is:function(s,table){var c=table.config;return $.tablesorter.isDigit(s,c);},format:function(s){return $.tablesorter.formatFloat(s);},type:"numeric"});ts.addParser({id:"currency",is:function(s){return/^[£$€?.]/.test(s);},format:function(s){return $.tablesorter.formatFloat(s.replace(new RegExp(/[^0-9.]/g),""));},type:"numeric"});ts.addParser({id:"ipAddress",is:function(s){return/^\d{2,3}[\.]\d{2,3}[\.]\d{2,3}[\.]\d{2,3}$/.test(s);},format:function(s){var a=s.split("."),r="",l=a.length;for(var i=0;i<l;i++){var item=a[i];if(item.length==2){r+="0"+item;}else{r+=item;}}return $.tablesorter.formatFloat(r);},type:"numeric"});ts.addParser({id:"url",is:function(s){return/^(https?|ftp|file):\/\/$/.test(s);},format:function(s){return jQuery.trim(s.replace(new RegExp(/(https?|ftp|file):\/\//),''));},type:"text"});ts.addParser({id:"isoDate",is:function(s){return/^\d{4}[\/-]\d{1,2}[\/-]\d{1,2}$/.test(s);},format:function(s){return $.tablesorter.formatFloat((s!="")?new Date(s.replace(new RegExp(/-/g),"/")).getTime():"0");},type:"numeric"});ts.addParser({id:"percent",is:function(s){return/\%$/.test($.trim(s));},format:function(s){return $.tablesorter.formatFloat(s.replace(new RegExp(/%/g),""));},type:"numeric"});ts.addParser({id:"usLongDate",is:function(s){return s.match(new RegExp(/^[A-Za-z]{3,10}\.? [0-9]{1,2}, ([0-9]{4}|'?[0-9]{2}) (([0-2]?[0-9]:[0-5][0-9])|([0-1]?[0-9]:[0-5][0-9]\s(AM|PM)))$/));},format:function(s){return $.tablesorter.formatFloat(new Date(s).getTime());},type:"numeric"});ts.addParser({id:"shortDate",is:function(s){return/\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}/.test(s);},format:function(s,table){var c=table.config;s=s.replace(/\-/g,"/");if(c.dateFormat=="us"){s=s.replace(/(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})/,"$3/$1/$2");}else if(c.dateFormat=="uk"){s=s.replace(/(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})/,"$3/$2/$1");}else if(c.dateFormat=="dd/mm/yy"||c.dateFormat=="dd-mm-yy"){s=s.replace(/(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2})/,"$1/$2/$3");}return $.tablesorter.formatFloat(new Date(s).getTime());},type:"numeric"});ts.addParser({id:"time",is:function(s){return/^(([0-2]?[0-9]:[0-5][0-9])|([0-1]?[0-9]:[0-5][0-9]\s(am|pm)))$/.test(s);},format:function(s){return $.tablesorter.formatFloat(new Date("2000/01/01 "+s).getTime());},type:"numeric"});ts.addParser({id:"metadata",is:function(s){return false;},format:function(s,table,cell){var c=table.config,p=(!c.parserMetadataName)?'sortValue':c.parserMetadataName;return $(cell).metadata()[p];},type:"numeric"});ts.addWidget({id:"zebra",format:function(table){if(table.config.debug){var time=new Date();}$("tr:visible",table.tBodies[0]).filter(':even').removeClass(table.config.widgetZebra.css[1]).addClass(table.config.widgetZebra.css[0]).end().filter(':odd').removeClass(table.config.widgetZebra.css[0]).addClass(table.config.widgetZebra.css[1]);if(table.config.debug){$.tablesorter.benchmark("Applying Zebra widget",time);}}});})(jQuery);

// Initialize Tablesorter
$(document).ready(
  function()
  { 
    // Tablesorter initialization with 'Zebra' default widget - http://tablesorter.com/docs/
    $("table").tablesorter( {widgets: ['zebra']} ); 
  }
);


/*
=======================================================================
Title: Metadata - jQuery plugin for parsing metadata from elements
Use: Required for setting inline options such as class="{sorter: false}" to disable table sorting for particular headers
Documentation URL: http://plugins.jquery.com/project/metadata
Uncompressed Script URL: http://hypertexthero.com/ippc/js/uncompressed/jquery.metadata.js
Version: Revision: $Id: jquery.metadata.js 3640 2007-10-11 18:34:38Z pmclanahan $
=======================================================================
*/
(function($){$.extend({metadata:{defaults:{type:'class',name:'metadata',cre:/({.*})/,single:'metadata'},setType:function(type,name){this.defaults.type=type;this.defaults.name=name;},get:function(elem,opts){var settings=$.extend({},this.defaults,opts);if(!settings.single.length)settings.single='metadata';var data=$.data(elem,settings.single);if(data)return data;data="{}";var getData=function(data){if(typeof data!="string")return data;if(data.indexOf('{')<0){data=eval("("+data+")");}}
var getObject=function(data){if(typeof data!="string")return data;data=eval("("+data+")");return data;}
if(settings.type=="html5"){var object={};$(elem.attributes).each(function(){var name=this.nodeName;if(name.match(/^data-/))name=name.replace(/^data-/,'');else return true;object[name]=getObject(this.nodeValue);});}else{if(settings.type=="class"){var m=settings.cre.exec(elem.className);if(m)
data=m[1];}else if(settings.type=="elem"){if(!elem.getElementsByTagName)return;var e=elem.getElementsByTagName(settings.name);if(e.length)
data=$.trim(e[0].innerHTML);}else if(elem.getAttribute!=undefined){var attr=elem.getAttribute(settings.name);if(attr)
data=attr;}
object=getObject(data.indexOf("{")<0?"{"+data+"}":data);}
$.data(elem,settings.single,object);return object;}}});$.fn.metadata=function(opts){return $.metadata.get(this[0],opts);};})(jQuery);


 /*
 =======================================================================
 Title: Treeview 1.4 - jQuery plugin to hide and show branches of a tree
 Use: Section navigation menu in sidebar
 Documentation URL: http://bassistance.de/jquery-plugins/jquery-plugin-treeview/ and http://docs.jquery.com/Plugins/Treeview
 Uncompressed Script URL: http://hypertexthero.com/ippc/js/uncompressed/jquery.treeview.js
 Version: $Id: jquery.treeview.js 4684 2008-02-07 19:08:06Z joern.zaefferer, Copyright (c) 2007 Jörn Zaefferer
 =======================================================================
 */
eval(function(p,a,c,k,e,r){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)r[e(c)]=k[c]||e(c);k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}(';(4($){$.1l($.F,{E:4(b,c){l a=3.n(\'.\'+b);3.n(\'.\'+c).o(c).m(b);a.o(b).m(c);8 3},s:4(a,b){8 3.n(\'.\'+a).o(a).m(b).P()},1n:4(a){a=a||"1j";8 3.1j(4(){$(3).m(a)},4(){$(3).o(a)})},1h:4(b,a){b?3.1g({1e:"p"},b,a):3.x(4(){T(3)[T(3).1a(":U")?"H":"D"]();7(a)a.A(3,O)})},12:4(b,a){7(b){3.1g({1e:"D"},b,a)}1L{3.D();7(a)3.x(a)}},11:4(a){7(!a.1k){3.n(":r-1H:G(9)").m(k.r);3.n((a.1F?"":"."+k.X)+":G(."+k.W+")").6(">9").D()}8 3.n(":y(>9)")},S:4(b,c){3.n(":y(>9):G(:y(>a))").6(">1z").C(4(a){c.A($(3).19())}).w($("a",3)).1n();7(!b.1k){3.n(":y(>9:U)").m(k.q).s(k.r,k.t);3.G(":y(>9:U)").m(k.u).s(k.r,k.v);3.1r("<J 14=\\""+k.5+"\\"/>").6("J."+k.5).x(4(){l a="";$.x($(3).B().1o("14").13(" "),4(){a+=3+"-5 "});$(3).m(a)})}3.6("J."+k.5).C(c)},z:4(g){g=$.1l({N:"z"},g);7(g.w){8 3.1K("w",[g.w])}7(g.p){l d=g.p;g.p=4(){8 d.A($(3).B()[0],O)}}4 1m(b,c){4 L(a){8 4(){K.A($("J."+k.5,b).n(4(){8 a?$(3).B("."+a).1i:1I}));8 1G}}$("a:10(0)",c).C(L(k.u));$("a:10(1)",c).C(L(k.q));$("a:10(2)",c).C(L())}4 K(){$(3).B().6(">.5").E(k.Z,k.Y).E(k.I,k.M).P().E(k.u,k.q).E(k.v,k.t).6(">9").1h(g.1f,g.p);7(g.1E){$(3).B().1D().6(">.5").s(k.Z,k.Y).s(k.I,k.M).P().s(k.u,k.q).s(k.v,k.t).6(">9").12(g.1f,g.p)}}4 1d(){4 1C(a){8 a?1:0}l b=[];j.x(4(i,e){b[i]=$(e).1a(":y(>9:1B)")?1:0});$.V(g.N,b.1A(""))}4 1c(){l b=$.V(g.N);7(b){l a=b.13("");j.x(4(i,e){$(e).6(">9")[1y(a[i])?"H":"D"]()})}}3.m("z");l j=3.6("Q").11(g);1x(g.1w){18"V":l h=g.p;g.p=4(){1d();7(h){h.A(3,O)}};1c();17;18"1b":l f=3.6("a").n(4(){8 3.16.15()==1b.16.15()});7(f.1i){f.m("1v").1u("9, Q").w(f.19()).H()}17}j.S(g,K);7(g.R){1m(3,g.R);$(g.R).H()}8 3.1t("w",4(a,b){$(b).1s().o(k.r).o(k.v).o(k.t).6(">.5").o(k.I).o(k.M);$(b).6("Q").1q().11(g).S(g,K)})}});l k=$.F.z.1J={W:"W",X:"X",q:"q",Y:"q-5",M:"t-5",u:"u",Z:"u-5",I:"v-5",v:"v",t:"t",r:"r",5:"5"};$.F.1p=$.F.z})(T);',62,110,'|||this|function|hitarea|find|if|return|ul||||||||||||var|addClass|filter|removeClass|toggle|expandable|last|replaceClass|lastExpandable|collapsable|lastCollapsable|add|each|has|treeview|apply|parent|click|hide|swapClass|fn|not|show|lastCollapsableHitarea|div|toggler|handler|lastExpandableHitarea|cookieId|arguments|end|li|control|applyClasses|jQuery|hidden|cookie|open|closed|expandableHitarea|collapsableHitarea|eq|prepareBranches|heightHide|split|class|toLowerCase|href|break|case|next|is|location|deserialize|serialize|height|animated|animate|heightToggle|length|hover|prerendered|extend|treeController|hoverClass|attr|Treeview|andSelf|prepend|prev|bind|parents|selected|persist|switch|parseInt|span|join|visible|binary|siblings|unique|collapsed|false|child|true|classes|trigger|else'.split('|'),0,{}))

// initialize treeview #menu

// Option 1: (cookie-based persitence)
// $(document).ready(function(){
//  $("#menu").treeview({
//      animated: "fast",
//      collapsed: true,
//      unique: true,
//      persist: "cookie",
//      toggle: function() {
//          window.console && console.log("%o was toggled", this);
//      }
//  });
// });

// Option 2: (location-based persitence)
$(document).ready(function(){
    $("#menu").treeview({
        control: "#treecontrol",
        animated:"fast",
        persist: "location",
        collapsed: true,
        unique: false
    });
});


/*
=======================================================================
Title: Show/hide banners
Use: Show/hide ippc.int section banners, uses jQuery cookie plugin above to remember setting
Documentation URL: http://andylangton.co.uk/articles/javascript/jquery-accessible-show-hide/
Uncompressed Script URL: http://hypertexthero.com/ippc/js/uncompressed/jquery.sectionbannertoggle.js
Version: 17.05.2008
======================================================================= */
$(document).ready(function(){var showText="[ = ]";var hideText="[ - ]";$("#sectionbanner").before("<p class='toggle'><a href='#' id='toggle_link'>"+hideText+"</a></p>");$('#sectionbanner').show();$('a#toggle_link').click(function(){if($('a#toggle_link').text()==hideText){$('a#toggle_link').text(showText);$.cookie('bannercookie','collapsed',{expires:120});}
else{$('a#toggle_link').text(hideText);$.cookie('bannercookie','expanded',{expires:120});}
$('#sectionbanner').toggle('fast');return false;});var bannercookie=$.cookie('bannercookie');if(bannercookie=='collapsed'){$("#sectionbanner").hide();$("#toggle_link").text(showText);};});


/*
=======================================================================
Title: Show/hide homepage stage
Use: Show/hide ippc.int work area sidebar, uses jQuery cookie plugin above to remember setting
Documentation URL: http://andylangton.co.uk/articles/javascript/jquery-accessible-show-hide/
Uncompressed Script URL: http://hypertexthero.com/ippc/js/uncompressed/jquery.showhidestage.js
Version: 17.05.2008
======================================================================= */
// $(document).ready(function(){var showText="[ = ]";var hideText="[ - ]";$("#slogan").prepend("<p class='hometoggle'><a href='#' id='toggle_link_homestage'>"+hideText+"</a></p>");$('#stage').show();$('a#toggle_link_homestage').click(function(){if($('a#toggle_link_homestage').text()==hideText){$('a#toggle_link_homestage').text(showText);$.cookie('bannercookie','collapsed',{expires:120});}
// else{$('a#toggle_link_homestage').text(hideText);$.cookie('bannercookie','expanded',{expires:120});}
// $('#stage').toggle('fast');return false;});var bannercookie=$.cookie('bannercookie');if(bannercookie=='collapsed'){$("#stage").hide();$("#toggle_link_homestage").text(showText);};});


/*
=======================================================================
Title: jQuery Text resize + Cookie recall
Use: Font resizing usability links
Documentation URL: http://www.shopdev.co.uk/blog/text-resizing-with-jquery/ and http://hypertexthero.com/ippc/work/textresize.html
Uncompressed Script URL: http://hypertexthero.com/ippc/js/uncompressed/jquery.textresize.js
Version: Wednesday, 4 November 2009, based on work by Faisal, Homar and Jonny Kamaly
======================================================================= */
var sitefunctions={textresize:function(){$(".FontSize").show();var $cookie_name="ippc-FontSize";var originalFontSize=$("html").css("font-size");if($.cookie($cookie_name)){var $getSize=$.cookie($cookie_name);$("html").css({fontSize:$getSize+($getSize.indexOf("px")!=-1?"":"px")});}else{$.cookie($cookie_name,originalFontSize);}
$(".FontSizeReset").bind("click",function(){$("html").css("font-size",originalFontSize);$.cookie($cookie_name,originalFontSize);return false});$(".FontSizeInc").bind("click",function(){var currentFontSize=$("html").css("font-size");var currentFontSizeNum=parseFloat(currentFontSize,10);var newFontSize=currentFontSizeNum*1.2;if(newFontSize,11){$("html").css("font-size",newFontSize);$.cookie($cookie_name,newFontSize);}
return false;});$(".FontSizeDec").bind("click",function(){var currentFontSize=$("html").css("font-size");var currentFontSizeNum=parseFloat(currentFontSize,10);var newFontSize=currentFontSizeNum*0.8;if(newFontSize,11){$("html").css("font-size",newFontSize);$.cookie($cookie_name,newFontSize);}
return false;});}}
$(document).ready(function(){sitefunctions.textresize();})


/*
=======================================================================
Title: Country Selector (do not confuse with jQuery Autosuggest Country Selector!)
Use: Select jump menu to go to a Country information page
Documentation URL: http://hypertexthero.com/ippc/work/countryselector.html
Uncompressed Script URL: http://hypertexthero.com/ippc/js/uncompressed/countryselector.js
Version: Thursday, 22 October 2009
======================================================================= */
function menu_goto( menuform )
{
    // Make sure var baseurl points to the production server for production
//    var baseurl = "http://193.43.36.147/ippctypo3_test/index.php?id=nppo" ;
	    var baseurl = "https://www.ippc.int/index.php?id=nppo" ;
    selecteditem = menuform.countryurl.selectedIndex ;
    countryurl = menuform.countryurl.options[ selecteditem ].value ;
    if (countryurl.length != 0) {
      location.href = baseurl + countryurl ;
    }
}
function menu_goto_adp( menuform )
{
    // Make sure var baseurl points to the production server for production
//    var baseurl = "http://193.43.36.147/ippctypo3_test/index.php?id=nppo" ;
	    var baseurl = "https://www.ippc.int/" ;
    selecteditem = menuform.countryurl.selectedIndex ;
    countryurl = menuform.countryurl.options[ selecteditem ].value ;
    if (countryurl.length != 0) {
      location.href = baseurl + countryurl ;
    }
}


/*
=======================================================================
Title: Styleswitch
Use: Switch stylesheets for different look and accessibility. Remember setting with cookie. Built on jQuery.
Documentation URL: http://www.kelvinluck.com/
Uncompressed Script URL: http://hypertexthero.com/ippc/js/uncompressed/jquery.styleswitch.js
Version: Thursday, 22 October 2009 - By Kelvin Luck - Under an Attribution, Share Alike License
======================================================================= */
(function($)
{var availableStylesheets=[];var activeStylesheetIndex=0;$.stylesheetToggle=function()
{activeStylesheetIndex++;activeStylesheetIndex%=availableStylesheets.length;$.stylesheetSwitch(availableStylesheets[activeStylesheetIndex]);};$.stylesheetSwitch=function(styleName)
{$('link[rel*=style][title]').each(function(i)
{this.disabled=true;if(this.getAttribute('title')==styleName){this.disabled=false;activeStylesheetIndex=i;}});createCookie('ippcstyle',styleName,365);};$.stylesheetInit=function()
{$('link[rel*=style][title]').each(function(i)
{availableStylesheets.push(this.getAttribute('title'));});var c=readCookie('ippcstyle');if(c){$.stylesheetSwitch(c);}};})(jQuery);function createCookie(name,value,days)
{if(days)
{var date=new Date();date.setTime(date.getTime()+(days*24*60*60*1000));var expires="; expires="+date.toGMTString();}
else var expires="";document.cookie=name+"="+value+expires+"; path=/";}
function readCookie(name)
{var nameEQ=name+"=";var ca=document.cookie.split(';');for(var i=0;i<ca.length;i++)
{var c=ca[i];while(c.charAt(0)==' ')c=c.substring(1,c.length);if(c.indexOf(nameEQ)==0)return c.substring(nameEQ.length,c.length);}
return null;}
function eraseCookie(name)
{createCookie(name,"",-1);}
$(function()
{$.stylesheetInit();$('#toggler').bind('click',function(e)
{$.stylesheetToggle();return false;});$('.styleswitch').bind('click',function(e)
{$.stylesheetSwitch(this.getAttribute('rel'));return false;});});


/*
=======================================================================
Title: ColorBox - full-featured, light-weight, customizable lightbox based on jQuery 1.3
Use: Inline help after click on link assigned class="help", eg: <a class="help" href="/ippc/help/help-item.html">?</a>
Documentation URL: http://colorpowered.com/colorbox/
Uncompressed Script URL: http://hypertexthero.com/ippc/js/uncompressed/jquery.colorbox.js
Version: v1.3.3
======================================================================= */
(function(c){var s="colorbox",B="hover",o=true,g=false,e,E=!c.support.opacity,N=E&&!window.XMLHttpRequest,O="click.colorbox",fa="cbox_open",J="cbox_load",P="cbox_complete",Q="cbox_cleanup",aa="cbox_closed",R="resize.cbox_resize",u,j,x,p,S,T,U,V,h,r,n,K,L,ba,W,y,F,G,M,C,D,z,A,m,k,a,H,I,X,Y={transition:"elastic",speed:350,width:g,height:g,innerWidth:g,innerHeight:g,initialWidth:"400",initialHeight:"400",maxWidth:g,maxHeight:g,scalePhotos:o,scrolling:o,inline:g,html:g,iframe:g,photo:g,href:g,title:g, rel:g,opacity:0.9,preloading:o,current:"image {current} of {total}",previous:"previous",next:"next",close:"close",open:g,overlayClose:o,slideshow:g,slideshowAuto:o,slideshowSpeed:2500,slideshowStart:"start slideshow",slideshowStop:"stop slideshow",preloadIMG:o};function v(b,d){d=d==="x"?document.documentElement.clientWidth:document.documentElement.clientHeight;return typeof b==="string"?Math.round(b.match(/%/)?d/100*parseInt(b,10):parseInt(b,10)):b}function Z(b){return a.photo||b.match(/\.(gif|png|jpg|jpeg|bmp)(?:\?([^#]*))?(?:#(\.*))?$/i)} function ca(){for(var b in a)if(typeof a[b]==="function")a[b]=a[b].call(m)}e=c.fn.colorbox=function(b,d){this.length?this.each(function(){var i=c(this).data(s)?c.extend({},c(this).data(s),b):c.extend({},Y,b);c(this).data(s,i).addClass("cboxelement")}):c(this).data(s,c.extend({},Y,b));c(this).unbind(O).bind(O,function(i){m=this;a=c(m).data(s);ca();X=d||g;var l=a.rel||m.rel;if(l&&l!=="nofollow"){h=c(".cboxelement").filter(function(){var f=c(this).data(s).rel||this.rel;return f===l});k=h.index(m);if(k< 0){h=h.add(m);k=h.length-1}}else{h=c(m);k=0}if(!H){I=H=o;c().bind("keydown.cbox_close",function(f){if(f.keyCode===27){f.preventDefault();e.close()}}).bind("keydown.cbox_arrows",function(f){if(f.keyCode===37){f.preventDefault();G.click()}else if(f.keyCode===39){f.preventDefault();F.click()}});a.overlayClose&&u.css({cursor:"pointer"}).one("click",e.close);m.blur();c.event.trigger(fa);M.html(a.close);u.css({opacity:a.opacity}).show();a.w=v(a.initialWidth,"x");a.h=v(a.initialHeight,"y");e.position(0); N&&r.bind("resize.cboxie6 scroll.cboxie6",function(){u.css({width:r.width(),height:r.height(),top:r.scrollTop(),left:r.scrollLeft()})}).trigger("scroll.cboxie6")}e.slideshow();e.load();i.preventDefault()});b&&b.open&&c(this).triggerHandler(O);return this};e.init=function(){function b(d){return c('<div id="cbox'+d+'"/>')}r=c(window);j=c('<div id="colorbox"/>');u=b("Overlay").hide();x=b("Wrapper");p=b("Content").append(n=b("LoadedContent").css({width:0,height:0}),K=b("LoadingOverlay"),L=b("LoadingGraphic"), ba=b("Title"),W=b("Current"),y=b("Slideshow"),F=b("Next"),G=b("Previous"),M=b("Close"));x.append(c("<div/>").append(b("TopLeft"),S=b("TopCenter"),b("TopRight")),c("<div/>").append(T=b("MiddleLeft"),p,U=b("MiddleRight")),c("<div/>").append(b("BottomLeft"),V=b("BottomCenter"),b("BottomRight"))).children().children().css({"float":"left"});c("body").prepend(u,j.append(x));if(E){j.addClass("cboxIE");N&&u.css("position","absolute")}p.children().addClass(B).mouseover(function(){c(this).addClass(B)}).mouseout(function(){c(this).removeClass(B)}).hide(); C=S.height()+V.height()+p.outerHeight(o)-p.height();D=T.width()+U.width()+p.outerWidth(o)-p.width();z=n.outerHeight(o);A=n.outerWidth(o);j.css({"padding-bottom":C,"padding-right":D}).hide();F.click(e.next);G.click(e.prev);M.click(e.close);p.children().removeClass(B)};e.position=function(b,d){var i=document.documentElement.clientHeight;i=Math.max(i-a.h-z-C,0)/2+r.scrollTop();var l=Math.max(document.documentElement.clientWidth-a.w-A-D,0)/2+r.scrollLeft();b=j.width()===a.w+A&&j.height()===a.h+z?0:b; x[0].style.width=x[0].style.height="9999px";function f(q){S[0].style.width=V[0].style.width=p[0].style.width=q.style.width;L[0].style.height=K[0].style.height=p[0].style.height=T[0].style.height=U[0].style.height=q.style.height}j.dequeue().animate({width:a.w+A,height:a.h+z,top:i,left:l},{duration:b,complete:function(){f(this);I=g;x[0].style.width=a.w+A+D+"px";x[0].style.height=a.h+z+C+"px";d&&d()},step:function(){f(this)}})};e.resize=function(b){if(H){function d(w){e.position(w,function(){if(H){if(E){q&& n.fadeIn(100);j[0].style.removeAttribute("filter")}p.children().show();if(a.iframe)n.append("<iframe id='cboxIframe'"+(a.scrolling?" ":"scrolling='no'")+" name='iframe_"+(new Date).getTime()+"' frameborder=0 src='"+(a.href||m.href)+"' />");K.hide();L.hide();y.hide();if(h.length>1){W.html(a.current.replace(/\{current\}/,k+1).replace(/\{total\}/,h.length));F.html(a.next);G.html(a.previous);a.slideshow&&y.show()}else{W.hide();F.hide();G.hide()}ba.html(a.title||m.title);c.event.trigger(P);X&&X.call(m); a.transition==="fade"&&j.fadeTo(t,1,function(){E&&j[0].style.removeAttribute("filter")});r.bind(R,function(){e.position(0)})}})}function i(){a.h=a.h||n.height();return a.h}function l(){a.w=a.w||n.width();return a.w}var f,q,t=a.transition==="none"?0:a.speed;r.unbind(R);if(b){n.remove();n=c('<div id="cboxLoadedContent"/>').html(b);n.hide().appendTo(u).css({width:l(),overflow:a.scrolling?"auto":"hidden"}).css({height:i()}).prependTo(p);c("#cboxPhoto").css({cssFloat:"none"});N&&c("select:not(#colorbox select)").filter(function(){return this.style.visibility!== "hidden"}).css({visibility:"hidden"}).one(Q,function(){this.style.visibility="inherit"});a.transition==="fade"&&j.fadeTo(t,0,function(){d(0)})||d(t);if(a.preloading&&h.length>1){b=k>0?h[k-1]:h[h.length-1];f=k<h.length-1?h[k+1]:h[0];f=c(f).data(s).href||f.href;b=c(b).data(s).href||b.href;Z(f)&&c("<img />").attr("src",f);Z(b)&&c("<img />").attr("src",b)}}else b=setTimeout(function(){var w=n.wrapInner("<div style='overflow:auto'></div>").children();a.h=w.height();n.css({height:a.h});w.replaceWith(w.children()); e.position(t)},1)}};e.load=function(){var b,d,i,l=e.resize;I=o;function f(q){var t=c(q),w=t.find("img"),$=w.length;function da(){var ea=new Image;$-=1;if($>=0&&a.preloadIMG){ea.onload=da;ea.src=w[$].src}else l(t)}da()}m=h[k];a=c(m).data(s);ca();c.event.trigger(J);a.h=a.height?v(a.height,"y")-z-C:a.innerHeight?v(a.innerHeight,"y"):g;a.w=a.width?v(a.width,"x")-A-D:a.innerWidth?v(a.innerWidth,"x"):g;a.mw=a.w;a.mh=a.h;if(a.maxWidth){a.mw=v(a.maxWidth,"x")-A-D;a.mw=a.w&&a.w<a.mw?a.w:a.mw}if(a.maxHeight){a.mh= v(a.maxHeight,"y")-z-C;a.mh=a.h&&a.h<a.mh?a.h:a.mh}b=a.href||c(m).attr("href");K.show();L.show();M.show();if(a.inline){c('<div id="cboxInlineTemp" />').hide().insertBefore(c(b)[0]).bind(J+" "+Q,function(){c(this).replaceWith(n.children())});l(c(b))}else if(a.iframe)l(" ");else if(a.html)f(a.html);else if(Z(b)){d=new Image;d.onload=function(){var q;d.onload=null;d.id="cboxPhoto";c(d).css({margin:"auto",border:"none",display:"block",cssFloat:"left"});if(a.scalePhotos){i=function(){d.height-=d.height* q;d.width-=d.width*q};if(a.mw&&d.width>a.mw){q=(d.width-a.mw)/d.width;i()}if(a.mh&&d.height>a.mh){q=(d.height-a.mh)/d.height;i()}}if(a.h)d.style.marginTop=Math.max(a.h-d.height,0)/2+"px";l(d);h.length>1&&c(d).css({cursor:"pointer"}).click(e.next);if(E)d.style.msInterpolationMode="bicubic"};d.src=b}else c("<div />").load(b,function(q,t){t==="success"?f(this):l(c("<p>Request unsuccessful.</p>"))})};e.next=function(){if(!I){k=k<h.length-1?k+1:0;e.load()}};e.prev=function(){if(!I){k=k>0?k-1:h.length- 1;e.load()}};e.slideshow=function(){var b,d,i="cboxSlideshow_";y.bind(aa,function(){y.unbind();clearTimeout(d);j.removeClass(i+"off "+i+"on")});function l(){y.text(a.slideshowStop).bind(P,function(){d=setTimeout(e.next,a.slideshowSpeed)}).bind(J,function(){clearTimeout(d)}).one("click",function(){b();c(this).removeClass(B)});j.removeClass(i+"off").addClass(i+"on")}b=function(){clearTimeout(d);y.text(a.slideshowStart).unbind(P+" "+J).one("click",function(){l();d=setTimeout(e.next,a.slideshowSpeed); c(this).removeClass(B)});j.removeClass(i+"on").addClass(i+"off")};if(a.slideshow&&h.length>1)a.slideshowAuto?l():b()};e.close=function(){c.event.trigger(Q);H=g;c().unbind("keydown.cbox_close keydown.cbox_arrows");r.unbind(R+" resize.cboxie6 scroll.cboxie6");u.css({cursor:"auto"}).fadeOut("fast");j.stop(o,g).fadeOut("fast",function(){n.remove();j.css({opacity:1});p.children().hide();c.event.trigger(aa)})};e.element=function(){return c(m)};e.settings=Y;c(e.init)})(jQuery);

// Initialization of help & popup image
$(document).ready(function(){
  $(".help").colorbox({opacity:0.35});
  $(".popupimg").colorbox({opacity:0.78});
  // $(".iframe").colorbox({width:"80%", height:"80%", opacity:0.35, iframe:true});
});


/*
=======================================================================
Title: jQuery script to use form labels as text field values
Use: Put 'Type country name' label inside country input on homepage (and possibly Countries section)
Documentation URL: http://cssglobe.com/post/2494/using-form-labels-as-text-field-values
Uncompressed Script URL: http://hypertexthero.com/ippc/js/uncompressed/jquery.labelininput.js
Version: v1 by Alen Grakalic
======================================================================= */
this.label2value = function(){  

    var inactive = "inactive";
    var active = "active";
    var focused = "focused";

    $("label.labelininput").each(function(){    
        obj = document.getElementById($(this).attr("for"));
        if(($(obj).attr("type") == "text") || (obj.tagName.toLowerCase() == "textarea")){
            $(obj).addClass(inactive);      
            var text = $(this).text();
            $(this).css("display","none");      
            $(obj).val(text);
            $(obj).focus(function(){  
                $(this).addClass(focused);
                $(this).removeClass(inactive);
                $(this).removeClass(active);                  
                if($(this).val() == text) $(this).val("");
            });  
            $(obj).blur(function(){  
                $(this).removeClass(focused);                           
                if($(this).val() == "") {
                    $(this).val(text);
                    $(this).addClass(inactive);
                } else {
                    $(this).addClass(active);    
                };        
            });        
        };  
    });    
};
$(document).ready(function(){  
    label2value();  
});


// 'Latest' tabs for docnav go here…removed for now for debugging. Targetting tabs in homepage only for now. Remove div#latestbox to target all tabs across site. UNUSED? REMOVE EVENTUALLY? 
$(function () {
var tabContainers = $('div#latestbox div.docs > div');
tabContainers.hide().filter(':first').show();

$('div#latestbox div.docs ul.docnav a').click(function () {
  tabContainers.hide();
  tabContainers.filter(this.hash).show();
  $('div#latestbox div.docs ul.docnav a').removeClass('docnavselected');
  $(this).addClass('docnavselected');
  return false;
  }).filter(':first').click();
});

// Hack to increase the size of the Assign Group Select input in Edit Contact
$(document).ready(function(){
    $('#body_admin select[name="usergroup[]"][size="4"]').attr("size",40);
});

// Andy Langton's show/hide/mini-accordion - updated 23/11/2009
// Latest version @ http://andylangton.co.uk/jquery-show-hide
// this tells jquery to run the function below once the DOM is ready
$(document).ready(function() {
// choose text for the show/hide link - can contain HTML (e.g. an image)
var showText='Show';
var hideText='Hide';
// initialise the visibility check
var is_visible = false;
// append show/hide links to the element directly preceding the element with a class of "toggle"
$('.toggleanything').prev().append(' (<a href="#" class="toggleLink">'+showText+'</a>)');
// hide all of the elements with a class of 'toggle'
$('.toggleanything').hide();
// capture clicks on the toggle links
$('a.toggleLink').click(function() {
// switch visibility
is_visible = !is_visible;
// change the link depending on whether the element is shown or hidden
$(this).html( (!is_visible) ? showText : hideText);
// toggle the display - uncomment the next line for a basic "accordion" style
//$('.toggle').hide();$('a.toggleLink').html(showText);
$(this).parent().next('.toggleanything').toggle('slow');
// return false so any link destination is not followed
return false;
});
});