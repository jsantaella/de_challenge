module "bucket" {
  source  = "terraform-google-modules/cloud-storage/google//modules/simple_bucket"
  version = "~> 6.0"

  name       = "${var.project_id}-bucket"
  project_id = var.project_id
  location   = "us"

  lifecycle_rules = [{
    action = {
      type = "Delete"
    }
    condition = {
      age            = 365
      with_state     = "ANY"
      matches_prefix = var.project_id
    }
  }]

  custom_placement_config = {
    data_locations : ["US-EAST4", "US-WEST1"]
  }

  iam_members = [{
    role   = "roles/storage.objectViewer"
    member = "group:test-gcp-ops@test.blueprints.joonix.net"
  }]

  autoclass = true
}

data "archive_file" "function_code" {
  type        = "zip"
  source_dir  = "${path.root}/../pyspark_scripts/code"
  output_path = "${path.root}/function.zip"
}

resource "google_storage_bucket_object" "function_code" {
  name   = "function.zip"
  bucket = module.bucket.name
  source = data.archive_file.function_code.output_path
}