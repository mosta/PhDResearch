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

require 'aws/decider'
require 'json'
require_relative 'utils'
require_relative 'periodic_workflow'
include AWS::Flow



def setup_domain(domain_name, retention_period)
swf = AWS::SimpleWorkflow.new
domain = swf.domains[domain_name]
unless domain.exists?
swf.domains.create(domain_name, retention_period)
end
domain
end
# get the path to the runner configuration file.
if ARGV.length < 1
puts "Please provide the path to the runner configuration file!"
exit
end
runner_spec = ARGV[0]
# Read the domain info from the same JSON file that the runner will be using.
helloworld_options = JSON.parse(File.read(runner_spec))
domain = helloworld_options["domain"]
domain_name = domain["name"]
# If retention is not given, default it to 1
retention_period = domain["retention_in_days"] || 1
# For this test, use the first workflow encountered.
workflow_info = helloworld_options["workflow_workers"][0]
task_list_name = workflow_info["task_list"]
domain = setup_domain(domain_name, retention_period)



my_workflow_client = workflow_client($swf.client, domain) { {:from_class => "PeriodicWorkflow"} }

puts "starting an execution..."
running_options = PeriodicWorkflowOptions.new(60,true,60,307584)
activity_name ="do_some_work"
prefix_name ="PeriodicActivity"
activity_args=["parameter1"]
$workflow_execution = my_workflow_client.start_execution(running_options, prefix_name, activity_name, *activity_args)
