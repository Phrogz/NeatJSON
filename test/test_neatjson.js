var neatJSON = require('../javascript/neatjson.js').neatJSON;
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
		if (!success){
			console.log(mesg+")");
			console.log('EXPECTED');
			console.log(test.json);
			console.log('ACTUAL');
			console.log(json,"\n");
		}
	});
});
