terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.34.0"
    }
  }
}
provider "google" {
  project = "grand-sweep-326023"
  region  = "us-central1"
  zone    = "us-central1-c"
}