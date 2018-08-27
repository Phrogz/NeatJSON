local t = {
		value="1e+23",
		tests={'^1%.0+e%+23$', '^1e%+23$'}
}

local value = t.value
local success = false
for _,testPattern in ipairs(t.tests) do
	-- print('!!!!!!!!', value==valtest.maybe, type(json), string.format('%q',json), type(testPattern), string.format('%q',testPattern), testPattern:match(valtest.maybe))
	if testPattern:match(value) then
		success = true
		break
	end
end
print(success)

print(value:match('^1e%+23$'))