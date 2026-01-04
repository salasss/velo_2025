terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ===== VARIABLES =====
variable "project_id" {
  description = "ID du projet Google Cloud"
  type        = string
}

variable "region" {
  description = "Région Google Cloud"
  type        = string
  default     = "us-central1"
}

# ===== RESSOURCES =====

# Instance VM simple pour lancer les simulations
resource "google_compute_instance" "simulator" {
  name         = "velo-simulator"
  machine_type = "e2-medium"  # Petite machine gratuite (si éligible)
  zone         = "${var.region}-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  # Script pour installer Docker
  metadata_startup_script = <<-EOF
#!/bin/bash
apt-get update
apt-get install -y curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
EOF

  network_interface {
    network = "default"
    access_config {}
  }

  tags = ["http-server"]
}

# ===== OUTPUTS =====
output "instance_ip" {
  description = "Adresse IP de la VM"
  value       = google_compute_instance.simulator.network_interface[0].access_config[0].nat_ip
}

output "ssh_command" {
  description = "Commande pour se connecter en SSH"
  value       = "gcloud compute ssh simulator --zone=${google_compute_instance.simulator.zone} --project=${var.project_id}"
}

