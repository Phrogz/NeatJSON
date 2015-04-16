require 'minitest/autorun'
require '../lib/neatjson'

class Dummy
	def to_json(*a)
		{a:1}.to_json(*a)
	end
end

class Flexi
	def to_json(*a)
		JSON.neat_generate({a:1},*a)
	end
end

class TestFlexiJSON < Minitest::Unit::TestCase
	def test_booleans
		assert_equal "true",       JSON.neat_generate(true)
		assert_equal "false",      JSON.neat_generate(false)
		assert_equal "null",       JSON.neat_generate(nil)
	end

	def test_numbers
		assert_equal "5",          JSON.neat_generate(5)
		assert_equal "4.2",        JSON.neat_generate(4.2)
		assert_equal "4.20",       JSON.neat_generate(4.2,  decimals:2)
		assert_equal "4.20",       JSON.neat_generate(4.199,decimals:2)
		assert_equal "4.20",       JSON.neat_generate(4.204,decimals:2)

		assert_equal "4",          JSON.neat_generate(4.2, decimals:0)
		assert_equal "5",          JSON.neat_generate(4.9, decimals:0)
		assert_equal "-2",         JSON.neat_generate(-1.9,decimals:0)
		assert_equal "-2",         JSON.neat_generate(-2.4,decimals:0)

		assert_equal "1.0e+23",    JSON.neat_generate(1e23)
		assert_equal "1.0e-09",    JSON.neat_generate(1e-9)
	end

	def test_strings
		assert_equal '"foo"',      JSON.neat_generate('foo')
		assert_equal '"foo"',      JSON.neat_generate(:foo)
		assert_equal '"foo\nbar"', JSON.neat_generate("foo\nbar")
	end

	def test_arrays
		@a1 = [1,2,3,4,[5,6,7,[8,9,10],11,12]]
		assert_equal "[1,2,3,4,[5,6,7,[8,9,10],11,12]]", JSON.neat_generate(@a1)
		assert_equal "[\n  1,\n  2,\n  3,\n  4,\n  [5,6,7,[8,9,10],11,12]\n]", JSON.neat_generate(@a1,wrap:30)
		assert_equal "[\n  1,\n  2,\n  3,\n  4,\n  [\n    5,\n    6,\n    7,\n    [8,9,10],\n    11,\n    12\n  ]\n]", JSON.neat_generate(@a1,wrap:20)
		assert_equal "[\n  1,\n  2,\n  3,\n  4,\n  [\n    5,\n    6,\n    7,\n    [\n      8,\n      9,\n      10\n    ],\n    11,\n    12\n  ]\n]", JSON.neat_generate(@a1,wrap:true)
		assert_equal "[\n\t1,\n\t2,\n\t3,\n\t4,\n\t[\n\t\t5,\n\t\t6,\n\t\t7,\n\t\t[\n\t\t\t8,\n\t\t\t9,\n\t\t\t10\n\t\t],\n\t\t11,\n\t\t12\n\t]\n]", JSON.neat_generate(@a1,wrap:true,indent:"\t")
		assert_equal "[1,2,3,4,[5,6,7,[8,9,10],11,12]]", JSON.neat_generate(@a1,array_padding:0)
		assert_equal "[ 1,2,3,4,[ 5,6,7,[ 8,9,10 ],11,12 ] ]", JSON.neat_generate(@a1,array_padding:1)
		assert_equal "[  1,2,3,4,[  5,6,7,[  8,9,10  ],11,12  ]  ]", JSON.neat_generate(@a1,array_padding:2)
		assert_equal "[1, 2, 3, 4, [5, 6, 7, [8, 9, 10], 11, 12]]", JSON.neat_generate(@a1,after_comma:1)
		assert_equal "[ 1, 2, 3, 4, [ 5, 6, 7, [ 8, 9, 10 ], 11, 12 ] ]", JSON.neat_generate(@a1,after_comma:1,array_padding:1)
		assert_equal "[1,\n 2,\n 3,\n 4,\n [5,\n  6,\n  7,\n  [8,\n   9,\n   10],\n  11,\n  12]]", JSON.neat_generate(@a1,short:true,wrap:true)
		assert_equal "[1,\n 2,\n 3,\n 4,\n [5,\n  6,\n  7,\n  [8,\n   9,\n   10],\n  11,\n  12]]", JSON.neat_generate(@a1,short:true,wrap:true,after_comma:1)
		assert_equal "[ 1,\n  2,\n  3,\n  4,\n  [ 5,\n    6,\n    7,\n    [ 8,\n      9,\n      10 ],\n    11,\n    12 ] ]", JSON.neat_generate(@a1,short:true,wrap:true,array_padding:1)

		@a2 = [1,2,3]
		assert_equal "[1,2,3]",     JSON.neat_generate(@a2)
		assert_equal "[1 ,2 ,3]",   JSON.neat_generate(@a2,before_comma:1)
		assert_equal "[1 , 2 , 3]", JSON.neat_generate(@a2,around_comma:1)
	end

	def test_hashes
		@h1 = {b:1,a:2}
		assert_equal '{"b":1,"a":2}', JSON.neat_generate(@h1)
		assert_equal '{"a":2,"b":1}', JSON.neat_generate(@h1,sorted:true)

		assert_equal '{"a":2, "b":1}',       JSON.neat_generate(@h1,sorted:true,after_comma:1)
		assert_equal '{"a" :2,"b" :1}',      JSON.neat_generate(@h1,sorted:true,before_colon:1)
		assert_equal '{"a": 2,"b": 1}',      JSON.neat_generate(@h1,sorted:true,after_colon:1)
		assert_equal '{"a" : 2,"b" : 1}',    JSON.neat_generate(@h1,sorted:true,before_colon:1,after_colon:1)
		assert_equal '{"a" : 2, "b" : 1}',   JSON.neat_generate(@h1,sorted:true,before_colon:1,after_colon:1,after_comma:1)
		assert_equal '{ "a" : 2, "b" : 1 }', JSON.neat_generate(@h1,sorted:true,before_colon:1,after_colon:1,after_comma:1,padding:1)
		assert_equal '{ "a" : 2, "b" : 1 }', JSON.neat_generate(@h1,sorted:true,around_colon:1,after_comma:1,object_padding:1)
		assert_equal '{"a" : 2, "b" : 1}',   JSON.neat_generate(@h1,sorted:true,before_colon:1,after_colon:1,after_comma:1,array_padding:1)
		assert_equal '{  "a"  :  2, "b"  :  1  }', JSON.neat_generate(@h1,sorted:true,around_colon:2,after_comma:1,padding:2)
		assert_equal '{  "a":2, "b":1  }', JSON.neat_generate(@h1,sorted:true,after_comma:1,padding:2)

		@h2 = {b:1,aaa:2,cc:3}
		assert_equal %Q{{\n  "b":1,\n  "aaa":2,\n  "cc":3\n}},    JSON.neat_generate(@h2,wrap:true)
		assert_equal %Q{{\n  "b"  :1,\n  "aaa":2,\n  "cc" :3\n}}, JSON.neat_generate(@h2,wrap:true,aligned:true)
		assert_equal %Q{{"b":1,"aaa":2,"cc":3}},                  JSON.neat_generate(@h2,aligned:true)
		assert_equal %Q{{\n  "aaa":2,\n  "b"  :1,\n  "cc" :3\n}}, JSON.neat_generate(@h2,wrap:true,aligned:true,sorted:true)

		@h3 = {a:1}
		assert_equal '{"a":1}', JSON.neat_generate(@h3)
		assert_equal "{\n  \"a\":1\n}", JSON.neat_generate(@h3,wrap:true)

		@h4 = { b:17, a:42 }
		assert_equal "{\"a\":42,\n \"b\":17}", JSON.neat_generate(@h4,wrap:10,sorted:true,short:true)
	end

	def test_mixed
		a = [1,{a:2},3]
		assert_equal '[1,{"a":2},3]', JSON.neat_generate(a)
		assert_equal '[ 1,{ "a":2 },3 ]', JSON.neat_generate(a,padding:1)
		assert_equal '[ 1, { "a":2 }, 3 ]', JSON.neat_generate(a,padding:1,after_comma:1)
		assert_equal %Q{[\n  1,\n  {\n    "a":2\n  },\n  3\n]}, JSON.neat_generate(a,wrap:true)
		assert_equal %Q{[\n  1,\n  {"a":2},\n  3\n]}, JSON.neat_generate(a,wrap:10)

		a = [1,{a:2,b:3},4]
		assert_equal "[1,\n {\"a\":2,\n  \"b\":3},\n 4]", JSON.neat_generate(a,wrap:0,short:true)

		h = {a:1,b:[2,3,4],c:3}
		assert_equal '{"a":1,"b":[2,3,4],"c":3}', JSON.neat_generate(h)
		assert_equal %Q{{\n  "a":1,\n  "b":[2,3,4],\n  "c":3\n}}, JSON.neat_generate(h,wrap:10)
		assert_equal %Q{{\n  "a":1,\n  "b":[\n    2,\n    3,\n    4\n  ],\n  "c":3\n}}, JSON.neat_generate(h,wrap:true)

		h = {hooo:42,whee:%w[yaaa oooo booy],zoop:"whoop"}
		assert_equal <<-ENDFORMAT.chomp, JSON.neat_generate(h,wrap:20,short:true)
{"hooo":42,
 "whee":["yaaa",
         "oooo",
         "booy"],
 "zoop":"whoop"}
		ENDFORMAT

		h = { a:[ {x:"foo",y:"jim"}, {x:"bar",y:"jam"} ] }
		assert_equal <<-ENDFORMAT.chomp, JSON.neat_generate(h,wrap:true,short:true)
{"a":[{"x":"foo",
       "y":"jim"},
      {"x":"bar",
       "y":"jam"}]}
		ENDFORMAT
	end

	def test_custom
		assert_equal '{  "a":1}', JSON.neat_generate(Dummy.new)
		assert_equal '{  "a":1}', JSON.neat_generate(Dummy.new,wrap:true)
		assert_equal '{"a":1}',   JSON.neat_generate(Dummy.new,indent:'')
		assert_equal '{"a":1}',   JSON.neat_generate(Flexi.new)
		assert_equal "{\n  \"a\":1\n}", JSON.neat_generate(Flexi.new,wrap:true)
	end
end
