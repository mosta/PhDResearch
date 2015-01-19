#!/usr/bin/env ruby

URLsFile = ARGV[0]
id = 0
File.readlines(URLsFile).each do |url|
  system("python DoWork.py '"+id.to_s+"' '"+url+"'")
  id = id + 1
end
