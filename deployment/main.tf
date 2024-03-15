terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-west-2" # or your preferred region
}

resource "aws_lightsail_key_pair" "buzz_key" {
  name       = "buzz-key"
  public_key = file("~/.ssh/id_rsa_aws.pub")
}

resource "aws_lightsail_instance" "suggestions_app" {
  name              = "SuggestionsAppInstance"
  availability_zone = "us-west-2a"
  blueprint_id      = "amazon_linux_2"
  bundle_id         = "nano_2_0" # plan
  key_pair_name     = aws_lightsail_key_pair.buzz_key.name

  user_data = <<-EOF
    #!/bin/bash
    sudo yum -y update
    sudo yum -y install python3 python3-pip jq git
    sudo yum install -y docker

    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker $USER

    SSH_KEY=$(aws secretsmanager get-secret-value --secret-id id_rsa_aws --region us-west-2 | jq -r .SecretString)

    # Set up SSH for GitHub
    echo "$SSH_KEY" > /home/ec2-user/.ssh/id_rsa
    chmod 600 /home/ec2-user/.ssh/id_rsa
    chown ec2-user /home/ec2-user/.ssh/id_rsa
    ssh-keyscan github.com >> /home/ec2-user/.ssh/known_hosts
    chown ec2-user /home/ec2-user/.ssh/known_hosts

    # Clone your repository
    cd /home/ec2-user
    git clone git@github.com:sjtindell/suggestions.git suggestions

    cd suggestions
    docker build -t suggestions .
    docker run -d -p 80:80 -e DATA_FILEPATH=/app/data/cities_canada-usa.tsv suggestions

    EOF
}

output "public_ip" {
  value = aws_lightsail_instance.suggestions_app.public_ip_address
}
