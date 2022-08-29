(function(exports){
exports.neatJSON = neatJSON;

function neatJSON(value,opts){
	opts = opts || {}
	if (!('wrap'          in opts)) opts.wrap = 80;
	if (opts.wrap==true) opts.wrap = -1;
	if (!('indent'        in opts)) opts.indent = '  ';
	if (!('arrayPadding'  in opts)) opts.arrayPadding  = ('padding' in opts) ? opts.padding : 0;
	if (!('objectPadding' in opts)) opts.objectPadding = ('padding' in opts) ? opts.padding : 0;
	if (!('beforeComma'   in opts)) opts.beforeComma   = ('aroundComma' in opts) ? opts.aroundComma : 0;
	if (!('afterComma'    in opts)) opts.afterComma    = ('aroundComma' in opts) ? opts.aroundComma : 0;
	if (!('beforeColon'   in opts)) opts.beforeColon   = ('aroundColon' in opts) ? opts.aroundColon : 0;
	if (!('afterColon'    in opts)) opts.afterColon    = ('aroundColon' in opts) ? opts.aroundColon : 0;
	if (!('beforeColon1'  in opts)) opts.beforeColon1  = ('aroundColon1' in opts) ? opts.aroundColon1 : ('beforeColon' in opts) ? opts.beforeColon : 0;
	if (!('afterColon1'   in opts)) opts.afterColon1   = ('aroundColon1' in opts) ? opts.aroundColon1 : ('afterColon'  in opts) ? opts.afterColon  : 0;
	if (!('beforeColonN'  in opts)) opts.beforeColonN  = ('aroundColonN' in opts) ? opts.aroundColonN : ('beforeColon' in opts) ? opts.beforeColon : 0;
	if (!('afterColonN'   in opts)) opts.afterColonN   = ('aroundColonN' in opts) ? opts.aroundColonN : ('afterColon'  in opts) ? opts.afterColon  : 0;
	if (!('forceFloatsIn' in opts)) opts.forceFloatsIn = [];

	const apad   = repeat(' ',opts.arrayPadding),
	      opad   = repeat(' ',opts.objectPadding),
	      comma  = repeat(' ',opts.beforeComma)+','+repeat(' ',opts.afterComma),
	      colon1 = repeat(' ',opts.beforeColon1)+':'+repeat(' ',opts.afterColon1),
	      colonN = repeat(' ',opts.beforeColonN)+':'+repeat(' ',opts.afterColonN);

	const build = memoize();
	return build(value,'',opts.forceFloats);

	function memoize(){
		const memo = new Map;
		return function(o,indent,floatsForced){
			const byFloats = floatsForced ? {o,floatsForced} : o;
			let byIndent=memo.get(byFloats);
			if (!byIndent) memo.set(byFloats,byIndent={});
			if (!byIndent[indent]) byIndent[indent] = rawBuild(o,indent,floatsForced);
			return byIndent[indent];
		}
	}

	function rawBuild(o,indent,floatsForced){
		if (o===null || o===undefined) return indent+'null';
		else{
			if (typeof o==='number'){
				if (o===Infinity) {
					return indent+'9e9999';
				}else if (o===-Infinity){
					return indent+'-9e9999';
				}else if (Number.isNaN(o)){
					return indent+'"NaN"';
				}else{
					const treatAsFloat = floatsForced || (o === +o && o !== (o|0));
					let result = indent + ((treatAsFloat && ('decimals' in opts)) ? o.toFixed(opts.decimals) : (o+''));
					if (opts.trimTrailingZeros) result = (+result)+'';
					if (floatsForced && result.indexOf('.')==-1) result += '.0';
					return result;
				}
			}else if (o instanceof Array){
				if (!o.length) return indent+"[]";
				let pieces = o.map(function(v){ return build(v,'',floatsForced) });
				const oneLine = indent+'['+apad+pieces.join(comma)+apad+']';
				if (opts.wrap===false || oneLine.length<=opts.wrap) return oneLine;
				if (opts.short){
					const indent2 = indent+' '+apad;
					pieces = o.map(function(v){ return build(v,indent2,floatsForced) });
					pieces[0] = pieces[0].replace(indent2,indent+'['+apad);
					pieces[pieces.length-1] = pieces[pieces.length-1]+apad+']';
					return pieces.join(',\n');
				}else{
					const indent2 = indent+opts.indent;
					return indent+'[\n'+o.map(function(v){ return build(v,indent2,floatsForced) }).join(',\n')+'\n'+(opts.indentLast?indent2:indent)+']';
				}
			}else if (o instanceof Object){
				let sortedKV=[], i=0;
				const sort = opts.sort || opts.sorted;
				for (let k in o){
					const kv = sortedKV[i++] = [k,o[k]];
					if (sort===true) kv[2] = k;
					else if (typeof sort==='function') kv[2]=sort(k,o[k],o);
				}
				if (!sortedKV.length) return indent+'{}';
				if (sort) sortedKV = sortedKV.sort(function(a,b){ a=a[2]; b=b[2]; return a<b?-1:a>b?1:0 });
				let keyvals=sortedKV.map(([k,v]) => [JSON.stringify(k), build(v,'',(opts.forceFloats || opts.forceFloatsIn.includes(k)))].join(colon1) ).join(comma);
				const oneLine = indent+"{"+opad+keyvals+opad+"}";
				if (opts.wrap===false || oneLine.length<opts.wrap) return oneLine;
				if (opts.short){
					keyvals = sortedKV.map(function(kv){ return [indent+' '+opad+JSON.stringify(kv[0]), kv[1]] });
					keyvals[0][0] = keyvals[0][0].replace(indent+' ',indent+'{');
					if (opts.aligned){
						let longest = 0;
						for (let i=keyvals.length;i--;) if (keyvals[i][0].length>longest) longest = keyvals[i][0].length;
						const padding = repeat(' ',longest);
						for (let i=keyvals.length;i--;) keyvals[i][0] = padRight(padding,keyvals[i][0]);
					}
					for (let i=keyvals.length;i--;){
						let k=keyvals[i][0], v=keyvals[i][1];
						const indent2 = repeat(' ',(k+colonN).length);
						floatsForced = (opts.forceFloats || opts.forceFloatsIn.includes(k));
						const oneLine = k+colonN+build(v,'',floatsForced);
						keyvals[i] = (opts.wrap===false || oneLine.length<=opts.wrap || !v || typeof v!="object") ? oneLine : (k+colonN+build(v,indent2,floatsForced).replace(/^\s+/,''));
					}
					return keyvals.join(',\n') + opad + '}';
				}else{
					const keyvals=sortedKV.map(function(kvs){ kvs[0] = indent+opts.indent+JSON.stringify(kvs[0]); return kvs });
					if (opts.aligned){
						let longest = 0;
						for (let i=keyvals.length;i--;) if (keyvals[i][0].length>longest) longest = keyvals[i][0].length;
						const padding = repeat(' ',longest);
						for (let i=keyvals.length;i--;) keyvals[i][0] = padRight(padding,keyvals[i][0]);
					}
					const indent2 = indent+opts.indent;
					for (let i=keyvals.length;i--;){
						const k=keyvals[i][0], v=keyvals[i][1];
						const oneLine = k+colonN+build(v,'',floatsForced);
						keyvals[i] = (opts.wrap===false || oneLine.length<=opts.wrap || !v || typeof v!="object") ? oneLine : (k+colonN+build(v,indent2,floatsForced).replace(/^\s+/,''));
					}
					return indent+'{\n'+keyvals.join(',\n')+'\n'+(opts.indentLast?indent2:indent)+'}'
				}
			}else{
				return indent+JSON.stringify(o);
			}
		}
	}

	function repeat(str,times){ // http://stackoverflow.com/a/17800645/405017
		let result = '';
		while(true){
			if (times & 1) result += str;
			times >>= 1;
			if (times) str += str;
			else break;
		}
		return result;
	}

	function padRight(pad, str){
		return (str + pad).substring(0, pad.length);
	}
}
neatJSON.version = "0.10";

})(typeof exports === 'undefined' ? this : exports);
