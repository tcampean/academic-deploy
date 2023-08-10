
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

resource "google_compute_network" "vpc_network" {
  name = "vpc-network"
}

resource "google_compute_health_check" "app_engine_health_check" {
  name               = "app-engine-health-check"
  check_interval_sec = 5
  timeout_sec       = 5
  tcp_health_check {
    port = "8080"
  }
}

resource "google_compute_backend_service" "app_engine_backend_service" {
  name = "app-engine-backend-service"
  protocol = "HTTP"
  health_checks = [google_compute_health_check.app_engine_health_check.self_link]
  port_name = "http"
  custom_request_headers = [
    "Host: flask-academic.ew.r.appspot.com"
    ]
}

resource "google_compute_url_map" "app_engine_url_map" {
  name            = "app-engine-url-map"
  default_service = google_compute_backend_service.app_engine_backend_service.self_link
}

resource "google_compute_target_http_proxy" "app_engine_proxy" {
  name        = "app-engine-proxy"
  url_map     = google_compute_url_map.app_engine_url_map.self_link
}

resource "google_compute_global_forwarding_rule" "app_engine_forwarding_rule" {
  name                  = "app-engine-forwarding-rule"
  target                = google_compute_target_http_proxy.app_engine_proxy.self_link
  port_range            = "80"
  ip_protocol           = "TCP"
  load_balancing_scheme = "EXTERNAL"
}

resource "google_compute_subnetwork" "subnet_1" {
  name          = "subnet-1"
  ip_cidr_range = "10.0.1.0/24"
  network       = google_compute_network.vpc_network.self_link
  region        = "europe-west1"
}

resource "google_compute_subnetwork" "subnet_2" {
  name          = "subnet-2"
  ip_cidr_range = "10.0.2.0/24"
  network       = google_compute_network.vpc_network.self_link
  region        = "europe-west1"
}

resource "google_compute_subnetwork" "app_engine_subnet" {
  name          = "app-engine-subnet"
  ip_cidr_range = "10.0.3.0/24"
  network       = google_compute_network.vpc_network.self_link
  region        = "europe-west1"
}
