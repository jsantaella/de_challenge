#Modulo para reutilizar código de Terraform que crea un GCS bucket
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
#Cargue del archivo principal de python que ejecutará el job de Dataproc
resource "google_storage_bucket_object" "top_most_user_by_date" {
  name   = "top_most_user_by_date.py"
  source = "../pyspark_scripts/code/top_most_user_by_date.py"
  bucket = module.bucket.name
}
#Creación del workflow template que crea el cluster, envía el job y desactiva el cluster una vez finalizado
resource "google_dataproc_workflow_template" "template" {
  name     = "${var.project_id}-dataproc-workflow"
  location = "us-west1"
  placement {
    managed_cluster {
      cluster_name = "${var.project_id}-my-cluster"
      config {
        gce_cluster_config {
          zone = "${var.location}-a"
          tags = ["foo", "bar"]
        }
        master_config {
          num_instances = 1
          machine_type  = "n2-standard-2"
          disk_config {
            boot_disk_type    = "pd-ssd"
            boot_disk_size_gb = 30
          }
        }
        worker_config {
          num_instances = 2
          machine_type  = "n1-standard-2"
          disk_config {
            boot_disk_size_gb = 30
            num_local_ssds    = 2
          }
        }
        software_config {
          image_version = "2.0.35-debian10"
        }
      }
    }
  }
  jobs {
    step_id = "PysparkJob"
    pyspark_job {
      main_python_file_uri = join("/",["gs://${module.bucket.name}", google_storage_bucket_object.top_most_user_by_date.output_name])
    }
  }
}