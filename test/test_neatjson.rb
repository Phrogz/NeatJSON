require '../lib/neatjson'
require './tests'

start = Time.now
pass  = 0
count = 0
TESTS.each do |value_tests|
	val, tests = value_tests[:value], value_tests[:tests]
	tests.each do |test|
		begin
			count += 1
			json = test[:opts] ? JSON.neat_generate(val,test[:opts].dup) : JSON.neat_generate(val)
			mesg = test[:opts] ? "JSON.neat_generate(#{val.inspect},#{test[:opts].inspect})" : "JSON.neat_generate(#{val.inspect})"
			raise "#{mesg}\nEXPECTED:\n#{test[:json]}\nACTUAL:\n#{json}\n\n" unless test[:json]===json
			pass += 1
		rescue StandardError => e
			puts e
		end
	end
end
elapsed = Time.now-start
puts "%d/%d test#{:s if count!=1} passed in %.2fms (%d tests per second)" % [pass, count, elapsed*1000, count/elapsed]
