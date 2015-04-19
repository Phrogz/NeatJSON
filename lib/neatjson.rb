require 'json'
module JSON
	# Generate the JSON string representation for an object,
	# with a variety of formatting options.
	#
	# @author Gavin Kistner <!@phrogz.net>
	# @param object [Object] the object to serialize
	# @param opts [Hash] the formatting options
	# @option opts [Integer] :wrap       (80)    The maximum line width before wrapping. Use `false` to never wrap, or `true` to always wrap.
	# @option opts [String]  :indent     ("  ")  Whitespace used to indent each level when wrapping (without the :short option).
	# @option opts [Boolean] :short      (false) Keep the output 'short' when wrapping, putting opening brackets on the same line as the first value, and closing brackets on the same line as the last item.
	# @option opts [Boolean] :sorted     (false) Sort the keys for objects to be in alphabetical order.
	# @option opts [Boolean] :aligned    (false) When wrapping objects, align the colons (only per object).
	# @option opts [Integer] :decimals    (null) Decimal precision to use for numbers; omit to keep numberic values precise.
	# @option opts [Integer] :padding        (0) Number of spaces to put inside brackets/braces for both arrays and objects.
	# @option opts [Integer] :array_padding  (0) Number of spaces to put inside brackets for arrays. Overrides `:padding`.
	# @option opts [Integer] :object_padding (0) Number of spaces to put inside braces for objects. Overrides `:padding`.
	# @option opts [Integer] :around_comma   (0) Number of spaces to put before/after commas (for both arrays and objects).
	# @option opts [Integer] :before_comma   (0) Number of spaces to put before commas (for both arrays and objects).
	# @option opts [Integer] :after_comma    (0) Number of spaces to put after commas (for both arrays and objects).
	# @option opts [Integer] :around_colon   (0) Number of spaces to put before/after colons (for objects).
	# @option opts [Integer] :before_colon   (0) Number of spaces to put before colons (for objects).
	# @option opts [Integer] :after_colon    (0) Number of spaces to put after colons (for objects).
	# @return [String] the JSON representation of the object.
	def self.neat_generate(object,opts={})
		opts[:wrap] = 80 unless opts.key?(:wrap)
		opts[:wrap] = -1 if opts[:wrap]==true
		opts[:indent]         ||= "  "
		opts[:array_padding]  ||= opts[:padding]      || 0
		opts[:object_padding] ||= opts[:padding]      || 0
		opts[:after_comma]    ||= opts[:around_comma] || 0
		opts[:before_comma]   ||= opts[:around_comma] || 0
		opts[:before_colon]   ||= opts[:around_colon] || 0
		opts[:after_colon]    ||= opts[:around_colon] || 0
		raise ":indent option must only be whitespace" if opts[:indent]=~/\S/

		apad  = " " * opts[:array_padding]
		opad  = " " * opts[:object_padding]
		comma = "#{' '*opts[:before_comma]},#{' '*opts[:after_comma]}"
		colon = "#{' '*opts[:before_colon]}:#{' '*opts[:after_colon]}"

		build = ->(o,indent) do
			case o
				when String               then "#{indent}#{o.inspect}"
				when Symbol               then "#{indent}#{o.to_s.inspect}"
				when TrueClass,FalseClass then "#{indent}#{o}"
				when NilClass             then "#{indent}null"
				when Numeric
					if opts[:decimals]
						"#{indent}%.#{opts[:decimals]}f" % o
					else
						"#{indent}#{o}"
					end

				when Array
					pieces = o.map{ |v| build[v,''] }
					one_line = "#{indent}[#{apad}#{pieces.join comma}#{apad}]"
					if !opts[:wrap] || (one_line.length <= opts[:wrap])
						one_line
					elsif opts[:short]
						indent2 = "#{indent} #{apad}"
						pieces = o.map{ |v| build[ v,indent2 ] }
						pieces[0].sub! indent2, "#{indent}[#{apad}"
						pieces.last << apad << "]"
						pieces.join ",\n"
					else
						indent2 = "#{indent}#{opts[:indent]}"
						"#{indent}[\n#{o.map{ |v| build[ v, indent2 ] }.join ",\n"}\n#{indent}]"
					end

				when Hash
					keyvals = o.map{ |k,v| [ k.to_s.inspect, build[v,''] ] }
					keyvals = keyvals.sort_by(&:first) if opts[:sorted]
					keyvals = keyvals.map{ |kv| kv.join(colon) }.join(comma)
					one_line = "#{indent}{#{opad}#{keyvals}#{opad}}"
					if !opts[:wrap] || (one_line.length <= opts[:wrap])
						one_line
					else
						if opts[:short]
							keyvals = o.map{ |k,v| ["#{indent} #{opad}#{k.to_s.inspect}",v] }
							keyvals = keyvals.sort_by(&:first) if opts[:sorted]
							keyvals[0][0].sub! "#{indent} ", "#{indent}{"
							if opts[:aligned]
								longest = keyvals.map(&:first).map(&:length).max
								keyvals.each{ |k,v| k.replace( "%-#{longest}s" % k ) }
							end
							keyvals.map! do |k,v|
								indent2 = " "*"#{k}#{colon}".length
								one_line = "#{k}#{colon}#{build[v,'']}"
								if opts[:wrap] && (one_line.length > opts[:wrap]) && (v.is_a?(Array) || v.is_a?(Hash))
									"#{k}#{colon}#{build[v,indent2].lstrip}"
								else
									one_line
								end
							end
							keyvals.join(",\n") << opad << "}"
						else
							keyvals = o.map{ |k,v| ["#{indent}#{opts[:indent]}#{k.to_s.inspect}",v] }
							keyvals = keyvals.sort_by(&:first) if opts[:sorted]
							if opts[:aligned]
								longest = keyvals.map(&:first).map(&:length).max
								keyvals.each{ |k,v| k.replace( "%-#{longest}s" % k ) }
							end
							indent2 = "#{indent}#{opts[:indent]}"
							keyvals.map! do |k,v|
								one_line = "#{k}#{colon}#{build[v,'']}"
								if opts[:wrap] && (one_line.length > opts[:wrap]) && (v.is_a?(Array) || v.is_a?(Hash))
									"#{k}#{colon}#{build[v,indent2].lstrip}"
								else
									one_line
								end
							end
							"#{indent}{\n#{keyvals.join(",\n")}\n#{indent}}"
						end
					end

				else
					"#{indent}#{o.to_json(opts)}"
			end
		end

		build[object,'']
	end
end

