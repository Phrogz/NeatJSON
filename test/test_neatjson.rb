require '../lib/neatjson'
require './tests'

TESTS.each do |value_tests|
	val, tests = value_tests[:value], value_tests[:tests]
	tests.each do |test|
		begin
			json = test[:opts] ? JSON.neat_generate(val,test[:opts].dup) : JSON.neat_generate(val)
			mesg = test[:opts] ? "JSON.neat_generate(#{val.inspect},#{test[:opts].inspect})" : "JSON.neat_generate(#{val.inspect})"
			raise "#{mesg}\nEXPECTED:\n#{test[:json]}\nACTUAL:\n#{json}\n\n" unless test[:json]===json
		rescue StandardError => e
			puts e
		end
	end
end