variable "environment" {
  description = "Deployment environment"
  type        = string

  validation {
    condition = contains(
      ["qa", "uat", "prod"],
      var.environment
    )

    error_message = "Environment must be qa, uat, or prod."
  }
}

variable "frontend_port" {
  description = "Host port for the frontend"
  type        = number
}