var neatJSON = require('../javascript/neatjson.js').neatJSON;
var startTime = new Date;
var count=0, pass=0;
require('./tests.js').tests.forEach(function(valTest){
	var value = valTest.value;
	valTest.tests.forEach(function(test){
		var mesg = "neatJSON("+JSON.stringify(value);
		if (test.opts){
			var opts = {};
			for (var k in test.opts) opts[k] = test.opts[k];
			var json = neatJSON(value,opts);
			mesg += ","+JSON.stringify(test.opts);
		}else{
			var json = neatJSON(value);
		}
		var success = (test.json.constructor==RegExp) ? test.json.test(json) : json==test.json;
		if (success) pass+=1;
		else{
			console.log(mesg+")");
			console.log('EXPECTED');
			console.log(test.json);
			console.log('ACTUAL');
			console.log(json,"\n");
		}
		count+=1;
	});
});
var elapsed = (new Date)-startTime;
console.log(pass+"/"+count+" test"+(count==1 ? '' : 's')+" passed in "+elapsed.toFixed(2)+"ms ("+(count/elapsed*1000).toFixed(0)+" tests per second)");

