# encoding: UTF-8
require 'date'
Gem::Specification.new do |s|
	s.name          = "neatjson"
	s.version       = "0.4"
	s.date          = Date.today.iso8601
	s.authors       = ["Gavin Kistner"]
	s.email         = "gavin@phrogz.net"
	s.homepage      = "http://github.com/Phrogz/NeatJSON"
	s.summary       = "Pretty, powerful, flexible JSON generation."
	s.description   = "Generate JSON strings from Ruby objects with flexible formatting options. The most important feature is that it can behave like pp, keeping arrays and objects on a single line when they fit."
	s.license       = "MIT license (MIT)"
  s.platform      = Gem::Platform::RUBY
  s.require_paths = ['lib']
  s.files         = Dir.glob("{lib,test,html}/**/*") + ['LICENSE.txt', 'README.md', '.yardopts', __FILE__]
	s.has_rdoc      = 'yard'
end
