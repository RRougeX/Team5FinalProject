#REGION
variable "AWSRegion" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

#VPC
variable "VPCCIDR" {
  description = "CIDR block for VPC"
  type        = string
  default     = "172.16.0.0/16"
}

#SUBNETS
variable "Public1CIDR" {
  description = "CIDR for first public subnet in us-east-1a"
  type        = string
  default     = "172.16.1.0/24"
}

variable "Public2CIDR" {
  description = "CIDR for second public subnet in us-east-1b."
  type        = string
  default     = "172.16.2.0/24"
}

variable "Private1CIDR" {
  description = "CIDR for first private subnet in us-east-1a."
  type        = string
  default     = "172.16.11.0/24"
}

variable "Private2CIDR" {
  description = "CIDR for second private subnet in us-east-1b"
  type        = string
  default     = "172.16.12.0/24"
}

#EC2
variable "KeyName" {
  description = "Key pair"
  type        = string
  default     = "VMsKeyPair"
}

variable "MyIP" {
  description = "My public IP"
  type        = string
  default     = "96.247.194.92/32"
}