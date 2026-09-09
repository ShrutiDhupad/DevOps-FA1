terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = "npipe:////.//pipe//docker_engine"
}

resource "docker_network" "app_network" {
  name = "${var.environment}_network"
}

resource "docker_image" "backend" {
  name = "devops-backend:${var.environment}"

  build {
    context    = "../docker/backend"
    dockerfile = "Dockerfile"
  }
}

resource "docker_image" "frontend" {
  name = "devops-frontend:${var.environment}"

  build {
    context    = "../docker/frontend"
    dockerfile = "Dockerfile"
  }
}

resource "docker_container" "backend" {
  name  = "${var.environment}_backend"
  image = docker_image.backend.image_id

  env = [
    "ENVIRONMENT=${var.environment}"
  ]

    networks_advanced {
    name    = docker_network.app_network.name
    aliases = ["backend"]
  }
}

resource "docker_container" "frontend" {
  name  = "${var.environment}_frontend"
  image = docker_image.frontend.image_id

  ports {
    internal = 80
    external = var.frontend_port
  }

  networks_advanced {
    name = docker_network.app_network.name
  }

  depends_on = [
    docker_container.backend
  ]
}