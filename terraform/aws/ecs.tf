resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/ads-platform"
  retention_in_days = 7
}

resource "aws_ecs_cluster" "main" {
  name = "ads-platform-cluster"
}

resource "aws_ecs_task_definition" "app" {
  family                   = "ads-platform-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]

  cpu    = 256
  memory = 512

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn

  # Prevent automatic deregistration of old revisions
  skip_destroy = true

  lifecycle {
    create_before_destroy = true
  }

  container_definitions = jsonencode([
    {
      name  = "ads-platform"
      image = "190934385828.dkr.ecr.eu-west-2.amazonaws.com/ads-platform:latest"

      essential = true

      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs.name
          "awslogs-region"        = "eu-west-2"
          "awslogs-stream-prefix" = "ecs"
        }
      }

      environment = [
        {
          name  = "APP_ENV"
          value = "production"
        },
        {
          name  = "APP_HOST"
          value = "0.0.0.0"
        },
        {
          name  = "APP_PORT"
          value = "8000"
        },
        {
          name  = "DATABASE_TYPE"
          value = "postgresql"
        },
        {
          name  = "DATABASE_URL"
          value = "postgresql://postgres:ChangeThisPassword123!@${aws_db_instance.postgres.address}:5432/adsplatform"
        }
      ]
    }
  ])
}