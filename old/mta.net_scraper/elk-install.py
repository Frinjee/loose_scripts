import os

# Install Elasticsearch
os.system("apt-get update && apt-get install elasticsearch")

# Configure Elasticsearch
with open("/etc/elasticsearch/elasticsearch.yml", "w") as file:
    file.write("cluster.name: kali-elk\n")
    file.write("node.name: kali-elk-node\n")
    file.write("network.host: 0.0.0.0\n")
    file.write("http.port: 9200\n")

# Start Elasticsearch service
os.system("service elasticsearch start")

# Install Logstash
os.system("apt-get install logstash")

# Configure Logstash
with open("/etc/logstash/conf.d/logstash.conf", "w") as file:
    file.write("input { beats { port => 5044 } }\n")
    file.write("filter { grok { match => { \"message\" => \"%{COMMONAPACHELOG}\" } } }\n")
    file.write("output { elasticsearch { hosts => [\"localhost:9200\"] } }\n")

# Start Logstash service
os.system("service logstash start")

# Install Kibana
os.system("apt-get install kibana")

# Configure Kibana
with open("/opt/kibana/config/kibana.yml", "w") as file:
    file.write("server.host: \"0.0.0.0\"\n")
    file.write("elasticsearch.url: \"http://localhost:9200\"\n")

# Start Kibana service
os.system("service kibana start")

# Install Filebeat
os.system("apt-get install filebeat")

# Configure Filebeat
with open("/etc/filebeat/filebeat.yml", "w") as file:
    file.write("filebeat.inputs:\n")
    file.write("- type: log\n")
    file.write("  paths: /var/log/*.log\n")
    file.write("output.logstash:\n")
    file.write("  hosts: [\"localhost:5044\"]\n")

# Start Filebeat service
os.system("service filebeat start")

print("Elk stack has been successfully installed, configured, and set up on Kali Linux.")
