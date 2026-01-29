interface NeatJSONOptions {
	wrap?:              number | boolean,
	indent?:            string,
	indentLast?:        boolean,
	short?:             boolean,
	sort?:              boolean,
	aligned?:           boolean,
	decimals?:          false | number,
	trimTrailingZeros?: boolean,
	forceFloats?:       boolean,
	forceFloatsIn?:     string[],
	arrayPadding?:      number,
	objectPadding?:     number,
	padding?:           number,
	beforeComma?:       number,
	afterComma?:        number,
	aroundComma?:       number,
	beforeColon1?:      number,
	afterColon1?:       number,
	beforeColonN?:      number,
	afterColonN?:       number,
	beforeColon?:       number,
	afterColon?:        number,
	aroundColon?:       number,
};

/**
 * Converts a JavaScript value to a JSON string.
 * @param value The value to convert to a JSON5 string.
 * @param options An object with keys configuring the desired formatting.
 * @returns The JSON string corresponding to the JavaScript value.
 */
export function neatJSON(
    value: any,
    options: NeatJSONOptions
): string
