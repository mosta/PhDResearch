##
# Copyright 2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
##

require_relative 'utils'

class PeriodicActivity
  extend AWS::Flow::Activities

  activity :do_some_work do
    {
      :version => "13.0",
      :default_task_list => $activity_task_list,
      :default_task_schedule_to_start_timeout => 6000,
      :default_task_start_to_close_timeout => 6000,

    }
  end

  def do_some_work(parameter)
    Dir.chdir("WorkUnit/")
    url_file = "/srv/www/phdresearch/urls.txt"
    File.write('/srv/www/phdresearch/log.txt', parameter)
    startID = parameter.to_i
    result = "ya rab"
    id = 0
    File.readlines(url_file).each do |url|
	if id >=startID and id<startID+10
		result = system("python DoWork.py '"+id.to_s+"' '"+url+"'")
	end
	id = id + 1
    end
    result
  end
end

activity_worker = AWS::Flow::ActivityWorker.new($swf.client, $domain, $activity_task_list, PeriodicActivity) { {:use_forking => false} }
activity_worker.start if __FILE__ == $0
