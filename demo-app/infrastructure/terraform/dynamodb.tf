# DynamoDB Tables for Developer Productivity Dashboard
# Terraform Configuration

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Metrics Table
resource "aws_dynamodb_table" "metrics" {
  name           = "DeveloperProductivityMetrics"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "name"
  range_key      = "timestamp"
  stream_enabled = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "name"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  attribute {
    name = "metric_id"
    type = "S"
  }

  attribute {
    name = "source"
    type = "S"
  }

  attribute {
    name = "team_id"
    type = "S"
  }

  global_secondary_index {
    name            = "MetricIdIndex"
    hash_key        = "metric_id"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "SourceIndex"
    hash_key        = "source"
    range_key       = "timestamp"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "TeamIdIndex"
    hash_key        = "team_id"
    range_key       = "timestamp"
    projection_type = "ALL"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Application = "DeveloperProductivityDashboard"
    Environment = var.environment
  }
}

# Raw Events Table
resource "aws_dynamodb_table" "raw_events" {
  name           = "DeveloperProductivityRawEvents"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "event_id"
  stream_enabled = true
  stream_view_type = "NEW_IMAGE"

  attribute {
    name = "event_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  attribute {
    name = "event_type"
    type = "S"
  }

  attribute {
    name = "repo_name"
    type = "S"
  }

  global_secondary_index {
    name            = "TimestampIndex"
    hash_key        = "event_type"
    range_key       = "timestamp"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "RepoIndex"
    hash_key        = "repo_name"
    range_key       = "timestamp"
    projection_type = "ALL"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  tags = {
    Application = "DeveloperProductivityDashboard"
    Environment = var.environment
  }
}

# Sprints Table
resource "aws_dynamodb_table" "sprints" {
  name         = "DeveloperProductivitySprints"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "sprint_id"

  attribute {
    name = "sprint_id"
    type = "S"
  }

  attribute {
    name = "team_id"
    type = "S"
  }

  attribute {
    name = "start_date"
    type = "S"
  }

  global_secondary_index {
    name            = "TeamIdIndex"
    hash_key        = "team_id"
    range_key       = "start_date"
    projection_type = "ALL"
  }

  tags = {
    Application = "DeveloperProductivityDashboard"
    Environment = var.environment
  }
}

# Users Table
resource "aws_dynamodb_table" "users" {
  name         = "DeveloperProductivityUsers"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "user_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "email"
    type = "S"
  }

  attribute {
    name = "team_id"
    type = "S"
  }

  global_secondary_index {
    name            = "EmailIndex"
    hash_key        = "email"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "TeamIdIndex"
    hash_key        = "team_id"
    projection_type = "ALL"
  }

  tags = {
    Application = "DeveloperProductivityDashboard"
    Environment = var.environment
  }
}

# AI Insights Cache Table
resource "aws_dynamodb_table" "ai_insights" {
  name         = "DeveloperProductivityAIInsights"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "insight_id"

  attribute {
    name = "insight_id"
    type = "S"
  }

  attribute {
    name = "team_id"
    type = "S"
  }

  attribute {
    name = "generated_at"
    type = "S"
  }

  attribute {
    name = "category"
    type = "S"
  }

  global_secondary_index {
    name            = "TeamIdIndex"
    hash_key        = "team_id"
    range_key       = "generated_at"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "CategoryIndex"
    hash_key        = "category"
    range_key       = "generated_at"
    projection_type = "ALL"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  tags = {
    Application = "DeveloperProductivityDashboard"
    Environment = var.environment
  }
}

# Variables
variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  default     = "production"
}

# Outputs
output "metrics_table_name" {
  description = "Name of the Metrics DynamoDB table"
  value       = aws_dynamodb_table.metrics.name
}

output "metrics_table_arn" {
  description = "ARN of the Metrics DynamoDB table"
  value       = aws_dynamodb_table.metrics.arn
}

output "raw_events_table_name" {
  description = "Name of the Raw Events DynamoDB table"
  value       = aws_dynamodb_table.raw_events.name
}

output "sprints_table_name" {
  description = "Name of the Sprints DynamoDB table"
  value       = aws_dynamodb_table.sprints.name
}

output "users_table_name" {
  description = "Name of the Users DynamoDB table"
  value       = aws_dynamodb_table.users.name
}

output "ai_insights_table_name" {
  description = "Name of the AI Insights DynamoDB table"
  value       = aws_dynamodb_table.ai_insights.name
}

