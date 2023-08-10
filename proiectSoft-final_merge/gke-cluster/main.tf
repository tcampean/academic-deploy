provider "google" {
  credentials = "/Users/tudor/Documents/GitHub/academic-deploy/proiectSoft-final_merge/gitignore/flask-academic-credentials.json"
  project     = "flask-academic"
  region      = "europe-west1"
}

resource "google_container_cluster" "gke_cluster" {
  name               = "my-gke-cluster"
  location           = "europe-west1-b"
  initial_node_count = 3
}

resource "google_sql_database_instance" "my_db_instance" {
  name             = "my-database-instance"
  database_version = "MYSQL_8_0"
  region           = "europe-west1"

  settings {
    tier = "db-f1-micro"
    backup_configuration {
      enabled = true
    }
  }
}

resource "google_compute_instance" "jenkins_vm" {
  name         = "jenkins-instance"
  machine_type = "n1-standard-1"
  zone         = "europe-west1-b"
  tags         = ["http-server", "https-server"]

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
    }
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    sudo apt-get update
    sudo apt-get install -y default-jre

    wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
    sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'

    sudo apt-get update
    sudo apt-get install -y jenkins
  EOT

  network_interface {
    network = "default"
    access_config {
      // Ephemeral IP
    }
  }
}

resource "google_compute_firewall" "jenkins_firewall" {
  name    = "jenkins-firewall"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8080"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags  = google_compute_instance.jenkins_vm.tags
}