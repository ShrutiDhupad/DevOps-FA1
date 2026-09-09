output "environment" {
  value = var.environment
}

output "frontend_url" {
  value = "http://localhost:${var.frontend_port}"
}

output "backend_container" {
  value = docker_container.backend.name
}

output "frontend_container" {
  value = docker_container.frontend.name
}